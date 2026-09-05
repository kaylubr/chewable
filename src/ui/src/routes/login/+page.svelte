<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { api, ApiError } from '$lib/api/client';
	import { auth } from '$lib/auth/store.svelte';

	let email = $state('');
	let password = $state('');
	let error = $state<string | null>(null);
	let submitting = $state(false);

	function afterLogin() {
		const next = page.url.searchParams.get('next');
		goto(next && next.startsWith('/') ? next : '/photos');
	}

	async function submit() {
		error = null;
		submitting = true;
		try {
			const res = await api.login(email, password);
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

	<form onsubmit={(e) => { e.preventDefault(); void submit(); }}>
		<label>
			Email
			<input type="email" bind:value={email} required autocomplete="email" />
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
	form {
		display: grid;
		gap: 1rem;
		margin-top: 1.5rem;
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
	/* Touch: inputs and the submit need thumb-sized targets. */
	@media (pointer: coarse) {
		input {
			padding-block: 0.8rem;
			font-size: 1rem; /* keeps >=16px on iOS regardless of class */
		}
		.primary {
			min-height: 48px;
		}
	}
</style>
