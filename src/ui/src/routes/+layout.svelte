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
		/*
		 * Color roles (OKLCH). Neutrals carry a warm cast toward the brand
		 * hue so surfaces feel related to the film-strip material. The amber
		 * accent is deliberately rare: it marks the exposure moment only.
		 *
		 * Hue 55 is a warm, slightly ochre amber; the dark "developer" tones
		 * live at the same hue with near-zero chroma.
		 */
		--paper: oklch(0.97 0.012 75); /* page canvas, warm off-white */
		--surface: oklch(0.99 0.006 75); /* cards, raised panels */
		--surface-2: oklch(0.955 0.014 75); /* wash, inset fills */
		--ink: oklch(0.28 0.03 55); /* body text */
		--ink-soft: oklch(0.43 0.035 55); /* secondary text */
		--ink-faint: oklch(0.6 0.03 55); /* captions, placeholders */
		--line: oklch(0.9 0.018 75); /* hairline borders */
		--line-strong: oklch(0.83 0.03 70); /* hover/strong borders */

		/* Brand — the exposure accent. Used for the one primary action,
		   selection, focus, and progress. Never spread flat across surfaces. */
		--ember: oklch(0.62 0.15 55); /* primary action, selection */
		--ember-deep: oklch(0.52 0.13 50); /* hover/pressed, rebate text */
		--ember-ink: oklch(0.45 0.12 50); /* amber text on light (AA) */

		/* Dark "developer" surface — completion/relief, privacy section. */
		--dev-bg: oklch(0.2 0.018 60); /* warm near-black */
		--dev-bg-raise: oklch(0.24 0.02 60); /* raised card on dark */
		--dev-ink: oklch(0.92 0.02 75); /* primary text on dark */
		--dev-ink-soft: oklch(0.78 0.025 70); /* secondary text on dark */
		--dev-line: oklch(0.32 0.02 60); /* borders on dark */

		/* States — never the only signal; always paired with shape/label. */
		--danger: oklch(0.55 0.19 30); /* destructive text/icon */
		--danger-bg: oklch(0.95 0.03 30); /* destructive wash */
		--danger-line: oklch(0.88 0.06 30); /* destructive border */
		--success: oklch(0.52 0.12 150);
		--focus: oklch(0.62 0.15 55); /* same as ember, visible ring */

		/* Type families */
		--font-display: 'Fraunces Variable', Georgia, 'Times New Roman', serif;
		--font-ui: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
		--font-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;

		/* Type scale (major-third-ish, tuned for 16px body) */
		--text-xs: 0.75rem;
		--text-sm: 0.875rem;
		--text-base: 1rem;
		--text-lg: 1.125rem;
		--text-xl: 1.375rem;
		--text-2xl: 1.75rem;
		--text-3xl: 2.25rem;

		font-family: var(--font-ui);
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		text-rendering: optimizeLegibility;
	}
	:global(body) {
		font-size: var(--text-base);
		line-height: 1.6;
		color: var(--ink);
		background: var(--paper);
	}
	:global(h1, h2, h3) {
		font-family: var(--font-display);
		font-optical-sizing: auto;
		text-wrap: balance;
		color: var(--ink);
	}
	:global(p) {
		text-wrap: pretty;
	}
	:global(input, textarea) {
		font: inherit;
	}
	:global(button) {
		font-family: var(--font-ui);
	}
	:global(::selection) {
		background: color-mix(in oklch, var(--ember) 22%, transparent);
	}
	:global(a) {
		color: var(--ember-ink);
		text-decoration-thickness: 1px;
		text-underline-offset: 2px;
	}
	:global(a:hover) {
		color: var(--ember-deep);
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
		gap: 1rem;
		padding: calc(0.9rem + env(safe-area-inset-top)) 1.5rem 0.9rem;
		max-width: 72rem;
		margin: 0 auto;
	}
	.brand {
		display: inline-flex;
		align-items: center;
		gap: 0.55rem;
		font-family: var(--font-display);
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
		flex: none;
	}
	nav {
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}
	nav a,
	.link {
		color: var(--ink-soft);
		text-decoration: none;
		font-weight: 500;
		font-size: 0.95rem;
		background: none;
		border: none;
		padding: 0.5rem 0.6rem;
		cursor: pointer;
		font-family: inherit;
		border-radius: 0.375rem;
	}
	nav a:hover,
	.link:hover {
		color: var(--ember-deep);
	}
	/* Narrow screens: keep the nav on one line, tighten the wordmark gap. */
	@media (max-width: 520px) {
		.nav {
			padding-inline: 1rem;
		}
		.brand {
			font-size: 1.15rem;
		}
		nav a,
		.link {
			font-size: 0.9rem;
			padding: 0.5rem 0.4rem;
		}
	}
	/* Touch: generous tap targets on coarse pointers. */
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
