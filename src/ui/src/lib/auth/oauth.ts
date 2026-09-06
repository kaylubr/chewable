/**
 * SPA-side helpers for the backend OAuth redirect flow.
 *
 * The backend redirects here after a provider callback:
 *   {OAUTH_REDIRECT_BASE}/auth/callback?next=/photos#token=...&user=...
 * The token and user live in the URL fragment so they never touch server
 * logs or browser history.
 */
import { PUBLIC_API_BASE } from '$env/static/public';
import type { AuthUser } from '$lib/api/client';

export interface OAuthCallback {
	token: string;
	user: AuthUser;
	next: string;
}

/** Build the backend authorize URL the browser is redirected to. */
export function oauthAuthorizeUrl(provider: string, next?: string): string {
	const params = new URLSearchParams();
	if (next) params.set('next', next);
	const qs = params.toString();
	return `${PUBLIC_API_BASE}/api/auth/${provider}/authorize${qs ? `?${qs}` : ''}`;
}

/**
 * Parse the SPA callback URL (fragment token/user, query next).
 * Returns null when the token fragment is absent (e.g. an error landing).
 */
export function parseOAuthCallback(rawUrl: string): OAuthCallback | null {
	const url = new URL(rawUrl);
	const token = url.hash ? new URLSearchParams(url.hash.slice(1)).get('token') : null;
	if (!token) return null;
	const rawUser = url.hash ? new URLSearchParams(url.hash.slice(1)).get('user') : null;
	const user = rawUser ? (JSON.parse(rawUser) as AuthUser) : null;
	if (!user) return null;
	return { token, user, next: validateNext(url.searchParams.get('next')) };
}

function validateNext(next: string | null): string {
	if (next && next.startsWith('/') && !next.startsWith('//')) return next;
	return '/photos';
}
