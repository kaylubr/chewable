<script lang="ts">
	import { goto } from '$app/navigation';
	import { FRAMES } from '$lib/frames/frames';
	import type { FrameId } from '$lib/frames/types';
	import { booth } from '$lib/photobooth/store.svelte';

	let selected = $state<FrameId | null>(null);
	let error = $state<string | null>(null);

	function choose(id: FrameId) {
		selected = id;
		error = null;
	}

	function start() {
		if (!selected) {
			error = 'Pick a frame first.';
			return;
		}
		booth.selectFrame(selected);
		booth.session.state = 'requesting-camera';
		goto('/photobooth/camera');
	}
</script>

<svelte:head>
	<title>Choose a frame — Chewables</title>
</svelte:head>

<main class="frame-page">
	<h1>Choose a frame</h1>
	<p class="sub">Your photos will sit inside the frame's openings.</p>

	<div class="grid">
		{#each FRAMES as frame}
			<button
				type="button"
				class="frame-card"
				class:selected={selected === frame.id}
				aria-pressed={selected === frame.id}
				onclick={() => choose(frame.id)}
			>
				<img src={frame.image} alt={`${frame.name} frame preview`} width="220" />
				<span class="name">{frame.name}</span>
				<span class="count">{frame.photoCount} photos</span>
			</button>
		{/each}
	</div>

	{#if error}<p class="error" role="alert">{error}</p>{/if}

	<div class="actions">
		<a href="/photobooth">Back</a>
		<button type="button" class="primary" onclick={start}>Use this frame →</button>
	</div>
</main>

<style>
	.frame-page {
		max-width: 60rem;
		margin: 0 auto;
		padding: 3rem 1.5rem;
		font-family: system-ui, sans-serif;
		color: #1c1917;
	}
	.sub {
		color: #57534e;
		margin-top: -0.5rem;
	}
	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
		gap: 1.25rem;
		margin: 2rem 0;
	}
	.frame-card {
		border: 2px solid #e7e5e4;
		border-radius: 0.75rem;
		background: #fff;
		padding: 1rem;
		cursor: pointer;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		align-items: center;
		transition: border-color 0.15s, box-shadow 0.15s;
	}
	.frame-card:hover {
		border-color: #d6d3d1;
	}
	.frame-card.selected {
		border-color: #b45309;
		box-shadow: 0 0 0 3px rgb(180 83 9 / 0.25);
	}
	.frame-card img {
		border-radius: 0.35rem;
		max-height: 240px;
		object-fit: contain;
	}
	.name {
		font-weight: 600;
	}
	.count {
		font-size: 0.85rem;
		color: #78716c;
	}
	.error {
		color: #b91c1c;
		font-weight: 600;
	}
	.actions {
		display: flex;
		gap: 1rem;
		align-items: center;
	}
	.primary {
		background: #b45309;
		color: #fff;
		border: none;
		border-radius: 0.5rem;
		padding: 0.7rem 1.4rem;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
	}
</style>
