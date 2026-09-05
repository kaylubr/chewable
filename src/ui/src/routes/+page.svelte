<script lang="ts">
	// Landing page for Chewables photobooth.
</script>

<svelte:head>
	<title>Chewables — Photobooth</title>
	<meta
		name="description"
		content="Chewables is a privacy-conscious photobooth. Pick a frame, take photos with your camera, and download the result — no account needed."
	/>
</svelte:head>

<main class="landing">
	<section class="hero">
		<p class="eyebrow">Chewables</p>
		<h1>Snap. Frame it. Keep it.</h1>
		<p class="lede">
			A photobooth that runs entirely in your browser. Choose a frame, take a few
			pictures, and download your finished strip.
		</p>
		<a class="cta" href="/photobooth">Start the photobooth</a>
	</section>

	<section class="privacy" aria-labelledby="privacy-heading">
		<h2 id="privacy-heading">Privacy first</h2>
		<ul>
			<li>
				<strong>No account needed to use the booth.</strong> Guests can pick a
				frame, capture, compose, and download without signing up.
			</li>
			<li>
				<strong>Guest photos stay on your device.</strong> Captured images and the
				finished picture are composed in your browser and are not uploaded while
				you are a guest.
			</li>
			<li>
				<strong>Sign in only to save.</strong> Creating an account is optional and
				only required if you want to keep a photo permanently in your gallery.
			</li>
		</ul>
		<p class="privacy-note">
			Saved photos are transmitted over an encrypted connection and stored securely,
			but they are not client-side encrypted — we can technically access what you
			choose to save.
		</p>
	</section>
</main>

<style>
	.landing {
		max-width: 44rem;
		margin: 0 auto;
		padding: 4rem 1.5rem;
		display: grid;
		gap: 3.5rem;
		font-family: system-ui, sans-serif;
		line-height: 1.6;
		color: #1c1917;
	}

	.eyebrow {
		text-transform: uppercase;
		letter-spacing: 0.12em;
		font-size: 0.8rem;
		font-weight: 700;
		color: #b45309;
		margin: 0 0 0.5rem;
	}

	h1 {
		font-size: clamp(2.2rem, 6vw, 3.5rem);
		line-height: 1.1;
		margin: 0 0 1rem;
	}

	.lede {
		font-size: 1.15rem;
		color: #57534e;
		margin: 0 0 1.75rem;
	}

	.cta {
		display: inline-block;
		background: #b45309;
		color: #fff;
		font-weight: 600;
		padding: 0.85rem 1.6rem;
		border-radius: 0.6rem;
		text-decoration: none;
		font-size: 1.05rem;
	}

	.cta:hover {
		background: #92400e;
	}

	.privacy h2 {
		font-size: 1.5rem;
		margin: 0 0 0.75rem;
	}

	.privacy ul {
		margin: 0;
		padding: 0;
		list-style: none;
		display: grid;
		gap: 1rem;
	}

	.privacy li {
		padding: 0.9rem 1.1rem;
		background: #f5f5f4;
		border-radius: 0.6rem;
	}

	.privacy-note {
		font-size: 0.9rem;
		color: #78716c;
		margin: 1.25rem 0 0;
	}
</style>
