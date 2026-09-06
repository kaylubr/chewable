<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { api, ApiError } from '$lib/api/client';
	import { auth } from '$lib/auth/store.svelte';
	import { oauthAuthorizeUrl } from '$lib/auth/oauth';
	import OAuthIcon from '$lib/components/OAuthIcon.svelte';

	let username = $state('');
	let password = $state('');
	let error = $state<string | null>(null);
	let submitting = $state(false);

	const oauthError = $derived(page.url.searchParams.get('oauth_error'));

	function afterLogin() {
		const next = page.url.searchParams.get('next');
		goto(next && next.startsWith('/') ? next : '/photos');
	}

	function nextParam(): string {
		const next = page.url.searchParams.get('next');
		return next && next.startsWith('/') ? next : '/photos';
	}

	async function submit() {
		error = null;
		submitting = true;
		try {
			const res = await api.login(username, password);
			auth.setSession(res.access_token, res.user);
			afterLogin();
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'Could not sign in. Please retry.';
		} finally {
			submitting = false;
		}
	}
</script>

<svelte:head>
	<title>Sign in — Chewables</title>
</svelte:head>

<main class="auth-page">
	<h1>Sign in</h1>
	<p class="sub">Sign in only to save photos to your gallery.</p>

	{#if oauthError}
		<p class="error" role="alert">
			Could not sign in with that provider. Please try again or use email.
		</p>
	{/if}

	<div class="social">
		<a class="social-btn" href={oauthAuthorizeUrl('google', nextParam())}>
			<OAuthIcon provider="google" />
			<span>Continue with Google</span>
		</a>
		<a class="social-btn" href={oauthAuthorizeUrl('facebook', nextParam())}>
			<OAuthIcon provider="facebook" />
			<span>Continue with Facebook</span>
		</a>
	</div>

	<div class="divider"><span>or with email</span></div>

	<form onsubmit={(e) => { e.preventDefault(); void submit(); }}>
		<label>
			Username
			<input type="text" bind:value={username} required autocomplete="username" />
		</label>
		<label>
			Password
			<input type="password" bind:value={password} required autocomplete="current-password" />
		</label>

		{#if error}<p class="error" role="alert">{error}</p>{/if}

		<button type="submit" class="primary" disabled={submitting}>
			{submitting ? 'Signing in…' : 'Sign in'}
		</button>
	</form>

	<p class="alt">
		No account? <a href="/register">Create one</a>
	</p>
</main>

<style>
	.auth-page {
		max-width: 24rem;
		margin: 0 auto;
		padding: 3rem 1.5rem;
		font-family: var(--font-ui);
		color: var(--ink);
	}
	.auth-page h1 {
		font-weight: 640;
	}
	.sub {
		color: var(--ink-soft);
		margin-top: -0.5rem;
	}
	.social {
		display: grid;
		gap: 0.6rem;
		margin-top: 1.5rem;
	}
	.social-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.6rem;
		padding: 0.7rem 1rem;
		border: 1px solid var(--line-strong);
		border-radius: 0.5rem;
		background: var(--surface);
		color: var(--ink);
		font-weight: 600;
		text-decoration: none;
	}
	.social-btn:hover {
		border-color: var(--ember);
		color: var(--ember);
	}
	.divider {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin: 1.25rem 0;
		color: var(--ink-faint);
		font-size: var(--text-sm);
	}
	.divider::before,
	.divider::after {
		content: '';
		flex: 1;
		height: 1px;
		background: var(--line);
	}
	form {
		display: grid;
		gap: 1rem;
		margin-top: 0;
	}
	label {
		display: grid;
		gap: 0.35rem;
		font-weight: 600;
		font-size: var(--text-sm);
	}
	input {
		padding: 0.6rem 0.75rem;
		border: 1px solid var(--line-strong);
		border-radius: 0.5rem;
		font-size: var(--text-base);
		font-weight: 400;
		background: var(--surface);
		color: var(--ink);
	}
	input:focus {
		border-color: var(--ember);
	}
	.error {
		color: var(--danger);
		background: var(--danger-bg);
		border: 1px solid var(--danger-line);
		padding: 0.6rem 0.75rem;
		border-radius: 0.5rem;
		font-size: var(--text-sm);
	}
	.primary {
		background: var(--ember);
		color: white;
		border: none;
		border-radius: 0.5rem;
		padding: 0.75rem;
		font-weight: 650;
		font-size: var(--text-base);
		cursor: pointer;
	}
	.primary:hover {
		background: var(--ember-deep);
	}
	.primary:disabled {
		opacity: 0.6;
	}
	.alt {
		margin-top: 1.25rem;
		font-size: 0.95rem;
		color: var(--ink-soft);
	}
	@media (pointer: coarse) {
		input {
			padding-block: 0.8rem;
			font-size: 1rem;
		}
		.primary {
			min-height: 48px;
		}
	}
</style>
