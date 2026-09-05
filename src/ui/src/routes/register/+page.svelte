<script lang="ts">
	import { goto } from '$app/navigation';
	import { api, ApiError } from '$lib/api/client';
	import { auth } from '$lib/auth/store.svelte';

	let email = $state('');
	let password = $state('');
	let confirm = $state('');
	let error = $state<string | null>(null);
	let submitting = $state(false);

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
			const res = await api.register(email, password);
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

	<form onsubmit={(e) => { e.preventDefault(); void submit(); }}>
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
		font-family: system-ui, sans-serif;
		color: #1c1917;
	}
	.sub {
		color: #57534e;
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
	}
	input {
		padding: 0.6rem 0.75rem;
		border: 1px solid #d6d3d1;
		border-radius: 0.5rem;
		font-size: 1rem;
	}
	.error {
		color: #991b1b;
		background: #fef2f2;
		border: 1px solid #fecaca;
		padding: 0.6rem 0.75rem;
		border-radius: 0.5rem;
	}
	.primary {
		background: #b45309;
		color: white;
		border: none;
		border-radius: 0.5rem;
		padding: 0.75rem;
		font-weight: 700;
		font-size: 1rem;
		cursor: pointer;
	}
	.primary:disabled {
		opacity: 0.6;
	}
	.alt {
		margin-top: 1.25rem;
		font-size: 0.95rem;
	}
</style>
