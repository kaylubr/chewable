import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { auth } from './store.svelte';

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
		auth.setSession('token-abc', { id: 'u1', email: 'a@b.com' });
		expect(auth.isAuthenticated).toBe(true);
		expect(auth.token).toBe('token-abc');
		expect(auth.user?.email).toBe('a@b.com');
		expect(localStorage.getItem('chewables.token')).toBe('token-abc');
		expect(localStorage.getItem('chewables.user')).toContain('a@b.com');
	});

	it('clear signs the user out and removes persistence', () => {
		auth.setSession('token-abc', { id: 'u1', email: 'a@b.com' });
		auth.clear();
		expect(auth.isAuthenticated).toBe(false);
		expect(auth.token).toBeNull();
		expect(localStorage.getItem('chewables.token')).toBeNull();
	});

	it('persists the session so a reload can restore it', () => {
		auth.setSession('token-xyz', { id: 'u2', email: 'persist@b.com' });
		const storedToken = localStorage.getItem('chewables.token');
		const storedUser = localStorage.getItem('chewables.user');
		expect(storedToken).toBe('token-xyz');
		expect(JSON.parse(storedUser!)).toEqual({ id: 'u2', email: 'persist@b.com' });
	});
});
