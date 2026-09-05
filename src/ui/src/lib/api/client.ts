/**
 * Minimal backend API client.
 *
 * The photobooth guest flow never calls this — it is only used for
 * authentication and saving photos to the user's gallery.
 */
import { PUBLIC_API_BASE } from "$env/static/public";

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const res = await fetch(`${PUBLIC_API_BASE}${path}`, {
    ...init,
    headers: {
      ...(init.body instanceof FormData
        ? {}
        : { "Content-Type": "application/json" }),
      ...init.headers,
    },
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      if (typeof body.detail === "string") detail = body.detail;
    } catch {
      /* keep statusText */
    }
    throw new ApiError(res.status, detail);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export interface AuthUser {
  id: string;
  email: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: AuthUser;
}

export interface SavedPhoto {
  id: string;
  frame: string;
  storage_key: string;
  created_at: string;
}

export const api = {
  register: (email: string, password: string) =>
    request<TokenResponse>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  login: (email: string, password: string) =>
    request<TokenResponse>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  me: (token: string) =>
    request<AuthUser>("/api/auth/me", {
      headers: { Authorization: `Bearer ${token}` },
    }),
  uploadPhoto: (token: string, frame: string, blob: Blob) => {
    const form = new FormData();
    form.append("frame", frame);
    form.append("file", blob, `chewables-${frame.toLowerCase()}.webp`);
    return request<SavedPhoto>("/api/photos", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: form,
    });
  },
  listPhotos: (token: string) =>
    request<SavedPhoto[]>("/api/photos", {
      headers: { Authorization: `Bearer ${token}` },
    }),
  photoUrl: (token: string, id: string) =>
    request<{ url: string }>(`/api/photos/${id}/url`, {
      headers: { Authorization: `Bearer ${token}` },
    }),
  deletePhoto: (token: string, id: string) =>
    request<void>(`/api/photos/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    }),
};
