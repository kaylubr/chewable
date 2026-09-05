<script lang="ts">
	import { goto } from '$app/navigation';
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
	<a href="/" class="brand">Chewables</a>
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
		outline: 2px solid #b45309;
		outline-offset: 2px;
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
		font-family: system-ui, sans-serif;
	}
	.brand {
		font-weight: 800;
		color: #b45309;
		text-decoration: none;
		font-size: 1.15rem;
	}
	nav {
		display: flex;
		gap: 1.1rem;
		align-items: center;
	}
	nav a {
		color: #1c1917;
		text-decoration: none;
		font-weight: 500;
	}
	nav a:hover {
		color: #b45309;
	}
	.link {
		background: none;
		border: none;
		color: #1c1917;
		font-weight: 500;
		cursor: pointer;
		font-size: 1rem;
		font-family: inherit;
	}
	.link:hover {
		color: #b45309;
	}
</style>
