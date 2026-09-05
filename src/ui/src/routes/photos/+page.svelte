<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { api, ApiError, type SavedPhoto } from '$lib/api/client';
	import { auth } from '$lib/auth/store.svelte';

	type DisplayPhoto = SavedPhoto & { displayUrl?: string };

	let photos = $state<DisplayPhoto[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);
	let deleting = $state<string | null>(null);

	async function load() {
		error = null;
		const token = auth.token;
		if (!auth.isAuthenticated || !token) return;
		loading = true;
		try {
			const data = await api.listPhotos(token);
			photos = await Promise.all(
				data.map(async (p) => {
					try {
						const { url } = await api.photoUrl(token, p.id);
						return { ...p, displayUrl: url };
					} catch {
						return { ...p, displayUrl: undefined };
					}
				})
			);
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'Could not load your photos.';
		} finally {
			loading = false;
		}
	}

	async function remove(id: string) {
		const token = auth.token;
		if (!token) return;
		deleting = id;
		try {
			await api.deletePhoto(token, id);
			photos = photos.filter((p) => p.id !== id);
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'Could not delete the photo.';
		} finally {
			deleting = null;
		}
	}

	const justSaved = $derived(page.url.searchParams.get('justSaved') === '1');

	onMount(() => {
		void load();
	});
</script>

<svelte:head>
	<title>My photos — Chewables</title>
</svelte:head>

<main class="gallery">
	<h1>My photos</h1>

	{#if !auth.isAuthenticated}
		<p class="empty">
			<a href="/login">Sign in</a> to see the photos you've saved.
		</p>
	{:else if loading}
		<p class="empty">Loading…</p>
	{:else if error}
		<p class="error" role="alert">{error}</p>
		<button type="button" class="secondary" onclick={load}>Retry</button>
	{:else if photos.length === 0}
		<p class="empty">
			{justSaved ? 'Saved! ' : ''}No saved photos yet. Take one in the{' '}
			<a href="/photobooth/frame">photobooth</a>.
		</p>
	{:else}
		<div class="grid">
			{#each photos as photo (photo.id)}
				<figure class="card">
					{#if photo.displayUrl}
						<img src={photo.displayUrl} alt="Saved photobooth result" />
					{:else}
						<div class="placeholder">unavailable</div>
					{/if}
					<figcaption>
						<span>
							{photo.frame} · {new Date(photo.created_at).toLocaleDateString()}
						</span>
						<button
							type="button"
							class="delete"
							onclick={() => void remove(photo.id)}
							disabled={deleting === photo.id}
						>
							{deleting === photo.id ? 'Deleting…' : 'Delete'}
						</button>
					</figcaption>
				</figure>
			{/each}
		</div>
	{/if}
</main>

<style>
	.gallery {
		max-width: 72rem;
		margin: 0 auto;
		padding: 2rem 1.5rem;
		font-family: system-ui, sans-serif;
		color: #1c1917;
	}
	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
		gap: 1.5rem;
		margin-top: 1.5rem;
	}
	.card {
		margin: 0;
		background: white;
		border-radius: 0.75rem;
		overflow: hidden;
		box-shadow: 0 2px 10px rgb(0 0 0 / 0.08);
	}
	.card img {
		width: 100%;
		aspect-ratio: 9 / 16;
		object-fit: cover;
		display: block;
	}
	.placeholder {
		aspect-ratio: 9 / 16;
		display: grid;
		place-items: center;
		color: #a8a29e;
		background: #f5f5f4;
	}
	.card figcaption {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.6rem 0.85rem;
		font-size: 0.85rem;
		color: #57534e;
	}
	.delete {
		background: none;
		border: 1px solid #fecaca;
		color: #991b1b;
		border-radius: 0.4rem;
		padding: 0.25rem 0.6rem;
		cursor: pointer;
		font-size: 0.8rem;
	}
	.empty {
		color: #57534e;
		margin-top: 2rem;
	}
	.error {
		color: #991b1b;
	}
	.secondary {
		background: #1c1917;
		color: white;
		border: none;
		border-radius: 0.5rem;
		padding: 0.6rem 1.2rem;
		cursor: pointer;
		margin-top: 1rem;
	}
</style>
