<script lang="ts">
	// Camera page placeholder — webcam capture arrives in a later stage.
	import { booth } from '$lib/photobooth/store.svelte';
	import { onMount } from 'svelte';

	let message = $state('Loading…');

	onMount(() => {
		message = booth.frame
			? `${booth.frame.name} selected — camera coming next.`
			: 'No frame selected.';
	});
</script>

<svelte:head>
	<title>Camera — Chewables</title>
</svelte:head>

<main class="camera">
	<h1>Camera</h1>
	<p>{message}</p>
	<a href="/photobooth/frame">Choose a different frame</a>
</main>

<style>
	.camera {
		max-width: 44rem;
		margin: 0 auto;
		padding: 4rem 1.5rem;
		font-family: system-ui, sans-serif;
		color: #1c1917;
	}
</style>
