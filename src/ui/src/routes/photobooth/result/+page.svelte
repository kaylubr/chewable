<script lang="ts">
	import { goto } from '$app/navigation';
	import { downloadDataUrl, photoFilename } from '$lib/photobooth/download';
	import { booth } from '$lib/photobooth/store.svelte';

	const resultUrl = booth.session.resultUrl;
	const frame = booth.frame;

	function download() {
		if (!resultUrl) return;
		downloadDataUrl(resultUrl, photoFilename(frame?.id));
	}

	function save() {
		// Auth wiring arrives in a later stage; currently redirect to sign in.
		goto('/login');
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
	<h1>Here's your photo!</h1>

	{#if resultUrl}
		<img class="result" src={resultUrl} alt="The finished 35mm film strip with your four poses" width="360" />
	{:else}
		<p class="empty">No finished photo in this session.</p>
		<button type="button" onclick={startOver}>Start over</button>
	{/if}

	<div class="actions">
		<button type="button" class="primary" onclick={download}>Download</button>
		<button type="button" class="secondary" onclick={save}>Save to account</button>
		<button type="button" class="ghost" onclick={startOver}>Take another</button>
	</div>
</main>

<style>
	.result-page {
		max-width: 40rem;
		margin: 0 auto;
		padding: 2rem 1.5rem;
		font-family: system-ui, sans-serif;
		color: #1c1917;
		text-align: center;
	}
	.result {
		max-width: min(360px, 100%);
		border-radius: 0.5rem;
		box-shadow: 0 8px 30px rgb(0 0 0 / 0.2);
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
	}
	.primary {
		background: #b45309;
		color: white;
	}
	.secondary {
		background: #1c1917;
		color: white;
	}
	.ghost {
		background: transparent;
		color: #44403c;
		border: 1px solid #d6d3d1;
	}
	.empty {
		color: #57534e;
	}
</style>
