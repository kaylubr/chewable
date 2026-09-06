import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { auth } from './store.svelte';

const U1 = { id: 'u1', email: 'a@b.com', username: 'alice' };
const U2 = { id: 'u2', email: 'persist@b.com', username: 'bob' };

describe('auth store', () => {
	beforeEach(() => {
		auth.clear();
		localStorage.clear();
	});

	afterEach(() => {
		vi.restoreAllMocks();
	});

	it('starts unauthenticated', () => {
		expect(auth.isAuthenticated).toBe(false);
		expect(auth.token).toBeNull();
		expect(auth.user).toBeNull();
	});

	it('setSession makes the user authenticated and persists', () => {
		auth.setSession('token-abc', U1);
		expect(auth.isAuthenticated).toBe(true);
		expect(auth.token).toBe('token-abc');
		expect(auth.user?.email).toBe('a@b.com');
		expect(auth.user?.username).toBe('alice');
		expect(localStorage.getItem('chewables.token')).toBe('token-abc');
		expect(localStorage.getItem('chewables.user')).toContain('a@b.com');
	});

	it('clear signs the user out and removes persistence', () => {
		auth.setSession('token-abc', U1);
		auth.clear();
		expect(auth.isAuthenticated).toBe(false);
		expect(auth.token).toBeNull();
		expect(localStorage.getItem('chewables.token')).toBeNull();
	});

	it('persists the session so a reload can restore it', () => {
		auth.setSession('token-xyz', U2);
		const storedToken = localStorage.getItem('chewables.token');
		const storedUser = localStorage.getItem('chewables.user');
		expect(storedToken).toBe('token-xyz');
		expect(JSON.parse(storedUser!)).toEqual(U2);
	});
});
