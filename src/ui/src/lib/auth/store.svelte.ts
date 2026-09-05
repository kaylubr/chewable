/**
 * Client-side auth state.
 *
 * Holds the access token + current user. The token is persisted to
 * localStorage so a refresh keeps the user signed in. Logout is purely
 * client-side — no server session exists.
 */
import type { AuthUser } from '../api/client';

const TOKEN_KEY = 'chewables.token';
const USER_KEY = 'chewables.user';

function readStored(): { token: string | null; user: AuthUser | null } {
	if (typeof localStorage === 'undefined') return { token: null, user: null };
	try {
		const token = localStorage.getItem(TOKEN_KEY);
		const rawUser = localStorage.getItem(USER_KEY);
		return { token, user: rawUser ? (JSON.parse(rawUser) as AuthUser) : null };
	} catch {
		return { token: null, user: null };
	}
}

class AuthStore {
	#initial = readStored();

	token = $state<string | null>(this.#initial.token);
	user = $state<AuthUser | null>(this.#initial.user);

	get isAuthenticated() {
		return this.token !== null && this.user !== null;
	}

	setSession(token: string, user: AuthUser) {
		this.token = token;
		this.user = user;
		try {
			localStorage.setItem(TOKEN_KEY, token);
			localStorage.setItem(USER_KEY, JSON.stringify(user));
		} catch {
			/* storage unavailable (private mode) — session lasts for the page */
		}
	}

	clear() {
		this.token = null;
		this.user = null;
		try {
			localStorage.removeItem(TOKEN_KEY);
			localStorage.removeItem(USER_KEY);
		} catch {
			/* ignore */
		}
	}
}

export const auth = new AuthStore();
