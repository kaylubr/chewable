<script lang="ts">
	import { goto } from '$app/navigation';
	import { api, ApiError } from '$lib/api/client';
	import { auth } from '$lib/auth/store.svelte';
	import { oauthAuthorizeUrl } from '$lib/auth/oauth';
	import OAuthIcon from '$lib/components/OAuthIcon.svelte';

	let email = $state('');
	let username = $state('');
	let password = $state('');
	let confirm = $state('');
	let error = $state<string | null>(null);
	let submitting = $state(false);

	function nextParam(): string {
		const params = new URLSearchParams(location.search);
		const next = params.get('next');
		return next && next.startsWith('/') ? next : '/photos';
	}

	async function submit() {
		error = null;
		if (password !== confirm) {
			error = 'Passwords do not match.';
			return;
		}
		if (password.length < 8) {
			error = 'Password must be at least 8 characters.';
			return;
		}
		submitting = true;
		try {
			const res = await api.register(email, username, password);
			auth.setSession(res.access_token, res.user);
			goto('/photos');
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'Could not create the account. Please retry.';
		} finally {
			submitting = false;
		}
	}
</script>

<svelte:head>
	<title>Create account — Chewables</title>
</svelte:head>

<main class="auth-page">
	<h1>Create an account</h1>
	<p class="sub">Accounts are only for saving photos to your gallery.</p>

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
			<input
				type="text"
				bind:value={username}
				required
				autocomplete="username"
				minlength="3"
				maxlength="32"
				pattern="[a-z0-9_]+"
				title="3-32 characters: lowercase letters, digits, underscores"
			/>
		</label>
		<label>
			Email
			<input type="email" bind:value={email} required autocomplete="email" />
		</label>
		<label>
			Password
			<input type="password" bind:value={password} required autocomplete="new-password" minlength="8" />
		</label>
		<label>
			Confirm password
			<input type="password" bind:value={confirm} required autocomplete="new-password" />
		</label>

		{#if error}<p class="error" role="alert">{error}</p>{/if}

		<button type="submit" class="primary" disabled={submitting}>
			{submitting ? 'Creating…' : 'Create account'}
		</button>
	</form>

	<p class="alt">
		Already have an account? <a href="/login">Sign in</a>
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
