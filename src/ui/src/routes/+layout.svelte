<script lang="ts">
	import { goto } from '$app/navigation';
	import '@fontsource-variable/fraunces';
	import '@fontsource-variable/jetbrains-mono';
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

<header class="topbar">
	<div class="bar-inner">
		<a href="/" class="brand">
			<span class="mark" aria-hidden="true"></span>
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
	</div>
</header>

{@render children()}

<style>
	:global(:focus-visible) {
		outline: 2px solid var(--mustard);
		outline-offset: 2px;
	}
	:global(html) {
		/* Palette */
		--crimson: #c31b1b;
		--crimson-deep: #9e1212;
		--mustard: #f5c400;
		--mustard-deep: #d9ad00;
		--paper: #fafafa;
		--surface: #ffffff;
		--charcoal: #1a1a1a;
		--ink-soft: #444444;
		--ink-faint: #8a8a8a;
		--line: #e5e5e5;
		--line-strong: #c9c9c9;

		/* State */
		--danger: #b3261e;
		--danger-bg: #fce9e7;
		--danger-line: #f0c4c0;
		--success: #1e7d32;
		--focus: var(--mustard);

		/* Dark stage (camera viewport, deep canvases) */
		--stage: #14100c;
		--stage-raise: #221b15;
		--stage-ink: #f5f1ea;
		--stage-ink-soft: #cfc4b8;
		--stage-line: #3a3028;

		/* Type families */
		--font-display: 'Fraunces Variable', Georgia, 'Times New Roman', serif;
		--font-ui: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
		--font-mono: 'JetBrains Mono Variable', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;

		/* Type scale */
		--text-xs: 0.75rem;
		--text-sm: 0.875rem;
		--text-base: 1rem;
		--text-lg: 1.125rem;
		--text-xl: 1.375rem;
		--text-2xl: 1.75rem;
		--text-3xl: 2.25rem;

		/* Compatibility aliases: old role names map onto the new palette so
		   existing surfaces adopt the brand without per-page churn. */
		--ink: var(--charcoal);
		--ember: var(--crimson);
		--ember-deep: var(--crimson-deep);
		--ember-ink: var(--crimson);
		--dev-bg: var(--stage);
		--dev-bg-raise: var(--stage-raise);
		--dev-ink: var(--stage-ink);
		--dev-ink-soft: var(--stage-ink-soft);
		--dev-line: var(--stage-line);

		font-family: var(--font-ui);
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		text-rendering: optimizeLegibility;
	}
	:global(body) {
		font-size: var(--text-base);
		line-height: 1.6;
		color: var(--charcoal);
		background: var(--paper);
	}
	:global(h1, h2, h3) {
		font-family: var(--font-display);
		font-optical-sizing: auto;
		text-wrap: balance;
		color: var(--charcoal);
	}
	:global(p) {
		text-wrap: pretty;
	}
	:global(input, textarea) {
		font: inherit;
	}
	:global(button) {
		font-family: var(--font-mono);
	}
	:global(::selection) {
		background: color-mix(in srgb, var(--mustard) 40%, transparent);
	}
	:global(a) {
		color: var(--crimson);
		text-decoration-thickness: 1px;
		text-underline-offset: 2px;
	}
	:global(a:hover) {
		color: var(--crimson-deep);
	}
	@media (prefers-reduced-motion: reduce) {
		:global(*) {
			animation-duration: 0.01ms !important;
			animation-iteration-count: 1 !important;
			transition-duration: 0.01ms !important;
		}
	}
	/* Crimson top bar */
	.topbar {
		background: var(--crimson);
		color: #fff;
	}
	.bar-inner {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1rem;
		padding: calc(0.7rem + env(safe-area-inset-top)) 1.5rem 0.7rem;
		max-width: 76rem;
		margin: 0 auto;
	}
	.brand {
		display: inline-flex;
		align-items: center;
		gap: 0.55rem;
		font-family: var(--font-display);
		font-weight: 750;
		font-size: 1.35rem;
		letter-spacing: -0.01em;
		color: #fff;
		text-decoration: none;
	}
	.brand:hover {
		color: #fff;
	}
	.mark {
		width: 1rem;
		height: 1rem;
		border-radius: 50%;
		background: var(--mustard);
		border: 2px solid #fff;
		box-shadow: 0 0 0 1px var(--crimson-deep);
		flex: none;
	}
	nav {
		display: flex;
		gap: 1.5rem;
		align-items: center;
	}
	nav a,
	.link {
		font-family: var(--font-mono);
		font-size: 0.78rem;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: #fff;
		text-decoration: none;
		font-weight: 500;
		background: none;
		border: none;
		padding: 0.5rem 0.2rem;
		cursor: pointer;
		border-radius: 0.25rem;
	}
	nav a:hover,
	.link:hover {
		color: var(--mustard);
	}
	@media (max-width: 520px) {
		.bar-inner {
			padding-inline: 1rem;
		}
		.brand {
			font-size: 1.2rem;
		}
		nav {
			gap: 0.9rem;
		}
		nav a,
		.link {
			font-size: 0.7rem;
			letter-spacing: 0.05em;
		}
	}
	@media (pointer: coarse) {
		nav a,
		.link {
			padding-block: 0.65rem;
			min-height: 44px;
			display: inline-flex;
			align-items: center;
		}
	}
</style>
