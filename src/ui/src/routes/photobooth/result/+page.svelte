<script lang="ts">
	import { goto } from '$app/navigation';
	import { api, ApiError } from '$lib/api/client';
	import { auth } from '$lib/auth/store.svelte';
	import { downloadDataUrl, photoFilename } from '$lib/photobooth/download';
	import { booth } from '$lib/photobooth/store.svelte';

	const resultUrl = booth.session.resultUrl;
	const frame = booth.frame;

	let saving = $state(false);
	let saveError = $state<string | null>(null);

	function download() {
		if (!resultUrl) return;
		downloadDataUrl(resultUrl, photoFilename(frame?.id));
	}

	function dataUrlToBlob(url: string): Blob {
		const [meta, b64] = url.split(',');
		const mime = /data:(.*?);/.exec(meta)?.[1] ?? 'image/webp';
		const bin = atob(b64);
		const bytes = new Uint8Array(bin.length);
		for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
		return new Blob([bytes], { type: mime });
	}

	async function save() {
		saveError = null;
		if (!auth.isAuthenticated) {
			// Return to this page after signing in so the user can save again.
			const next = encodeURIComponent('/photobooth/result');
			goto(`/login?next=${next}`);
			return;
		}
		if (!resultUrl || !frame || !auth.token) return;
		saving = true;
		try {
			await api.uploadPhoto(auth.token, frame.id, dataUrlToBlob(resultUrl));
			booth.session.state = 'completed';
			goto('/photos?justSaved=1');
		} catch (e) {
			saveError = e instanceof ApiError ? e.message : 'Could not save the photo. Please retry.';
		} finally {
			saving = false;
		}
	}

	function startOver() {
		booth.reset();
		goto('/photobooth/frame');
	}
</script>

<svelte:head>
	<title>Your photo — Chewables</title>
</svelte:head>

<main class="result-page">
	{#if resultUrl}
		<h1>Here's your photo!</h1>
		<img
			class="result"
			src={resultUrl}
			alt={frame ? `Your finished ${frame.name.toLowerCase()} photobooth result` : 'Your finished photobooth result'}
			width="360"
		/>
		<div class="actions">
			<button type="button" class="primary" onclick={download}>Download</button>
			<button type="button" class="secondary" onclick={() => void save()} disabled={saving}>
				{#if saving}
					Saving…
				{:else if auth.isAuthenticated}
					Save to my photos
				{:else}
					Save to account
				{/if}
			</button>
			<button type="button" class="ghost" onclick={startOver}>Take another</button>
		</div>
	{:else}
		<p class="empty">No finished photo in this session.</p>
		<button type="button" class="secondary" onclick={startOver}>Start over</button>
	{/if}

	{#if saveError}<p class="save-error" role="alert">{saveError}</p>{/if}
</main>

<style>
	.result-page {
		max-width: 40rem;
		margin: 0 auto;
		padding: 2rem 1.5rem;
		font-family: var(--font-ui);
		color: var(--ink);
		text-align: center;
	}
	.result-page h1 {
		font-weight: 620;
	}
	.result {
		max-width: min(360px, 100%);
		border-radius: 0.5rem;
		box-shadow: 0 8px 30px oklch(0.28 0.03 55 / 0.22);
		margin: 1.5rem auto;
		display: block;
	}
	.actions {
		display: flex;
		gap: 0.75rem;
		justify-content: center;
		flex-wrap: wrap;
	}
	.primary,
	.secondary,
	.ghost {
		border-radius: 0.5rem;
		padding: 0.7rem 1.4rem;
		font-weight: 600;
		cursor: pointer;
		border: none;
		font-size: var(--text-base);
	}
	.primary {
		background: var(--ember);
		color: white;
	}
	.primary:hover {
		background: var(--ember-deep);
	}
	.secondary {
		background: var(--dev-bg);
		color: var(--dev-ink);
	}
	.secondary:hover {
		background: var(--dev-bg-raise);
	}
	.ghost {
		background: transparent;
		color: var(--ink-soft);
		border: 1px solid var(--line-strong);
	}
	.ghost:hover {
		border-color: var(--ink-faint);
		color: var(--ink);
	}
	.empty {
		color: var(--ink-soft);
	}
	.save-error {
		color: var(--danger);
		background: var(--danger-bg);
		border: 1px solid var(--danger-line);
		padding: 0.6rem 0.75rem;
		border-radius: 0.5rem;
		margin-top: 1rem;
		font-size: var(--text-sm);
	}
</style>
