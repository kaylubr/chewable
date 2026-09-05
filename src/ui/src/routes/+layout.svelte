<script lang="ts">
	import { goto } from '$app/navigation';
	import '@fontsource-variable/fraunces';
	import favicon from '$lib/assets/favicon.svg';
	import { auth } from '$lib/auth/store.svelte';

	let { children } = $props();

	function signOut() {
		auth.clear();
		goto('/');
	}
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<header class="nav">
	<a href="/" class="brand">
		<span class="sprocket" aria-hidden="true"></span>
		Chewables
	</a>
	<nav>
		<a href="/photobooth/frame">Photobooth</a>
		{#if auth.isAuthenticated}
			<a href="/photos">My photos</a>
			<button type="button" class="link" onclick={signOut}>Sign out</button>
		{:else}
			<a href="/login">Sign in</a>
		{/if}
	</nav>
</header>

{@render children()}

<style>
	:global(:focus-visible) {
		outline: 2px solid var(--ember);
		outline-offset: 2px;
	}
	:global(html) {
		--ink: #1c1917;
		--paper: #faf7f2;
		--ember: #b45309;
		--ember-deep: #92400e;
		--warm-gray: #57534e;
		--line: #e7e5e4;
		--wash: #f5f2ec;
	}
	@media (prefers-reduced-motion: reduce) {
		:global(*) {
			animation-duration: 0.01ms !important;
			animation-iteration-count: 1 !important;
			transition-duration: 0.01ms !important;
		}
	}
	.nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.9rem 1.5rem;
		max-width: 72rem;
		margin: 0 auto;
	}
	.brand {
		display: inline-flex;
		align-items: center;
		gap: 0.55rem;
		font-family: 'Fraunces Variable', Georgia, serif;
		font-weight: 750;
		font-size: 1.3rem;
		letter-spacing: -0.01em;
		color: var(--ink);
		text-decoration: none;
	}
	.brand:hover {
		color: var(--ember-deep);
	}
	.sprocket {
		width: 1.1rem;
		height: 1.1rem;
		border-radius: 50%;
		background: radial-gradient(circle, var(--ember) 0 38%, transparent 42%);
		border: 1px solid var(--ember-deep);
		box-shadow: inset 0 0 0 2px var(--paper);
	}
	nav {
		display: flex;
		gap: 1.1rem;
		align-items: center;
	}
	nav a {
		color: var(--ink);
		text-decoration: none;
		font-weight: 500;
		font-size: 0.95rem;
	}
	nav a:hover {
		color: var(--ember-deep);
	}
	.link {
		background: none;
		border: none;
		color: var(--ink);
		font-weight: 500;
		cursor: pointer;
		font-size: 0.95rem;
		font-family: inherit;
	}
	.link:hover {
		color: var(--ember-deep);
	}
</style>
