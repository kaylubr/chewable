<script lang="ts">
</script>

<svelte:head>
	<title>Chewables</title>
	<meta
		name="description"
		content="Chewables is a privacy-conscious photobooth. Pick a frame, take photos with your camera, and download the result — no account needed."
	/>
</svelte:head>

<main class="landing">
	<section class="hero" aria-labelledby="hero-heading">
		<div class="hero-inner">
			<h1 class="marquee" id="hero-heading">
				Expose your strip
			</h1>
			<p class="lede">
				Frame the moments that matter!
			</p>
			<a class="cta" href="/photobooth/frame">
				Start the photobooth
			</a>
		</div>
	</section>

	<section class="process" aria-labelledby="process-heading">
		<div class="process-inner">
			<h2 id="process-heading" class="section-title">Three steps, no darkroom</h2>
			<ol class="steps">
				<li>
					<span class="step-no">01</span>
					<h3>Pick your stock</h3>
					<p>Choose a frame. Each one needs a set number of shots.</p>
				</li>
				<li>
					<span class="step-no">02</span>
					<h3>Take the shots</h3>
					<p>The camera counts you down between each exposure.</p>
				</li>
				<li>
					<span class="step-no">03</span>
					<h3>Keep the strip</h3>
					<p>Download your finished film. Save it to your gallery only if you want.</p>
				</li>
			</ol>
		</div>
	</section>

	<section class="privacy" aria-labelledby="privacy-heading">
		<div class="privacy-inner">
			<h2 id="privacy-heading" class="section-title">What happens to your photos</h2>
			<ul>
				<li>
					<strong>Guests stay off the record.</strong> Your captures and the finished
					strip are composed in your browser. Nothing is uploaded while you shoot.
				</li>
				<li>
					<strong>The booth never makes an account for you.</strong> You can shoot and
					download as a guest, full stop.
				</li>
				<li>
					<strong>Saving is the only upload.</strong> If you choose to keep a photo in
					your gallery, that is the one moment it leaves your device.
				</li>
			</ul>
			<p class="privacy-note">
				Saved photos travel over an encrypted connection and are stored securely, but
				they are not client-side encrypted. We can technically access what you choose
				to save. Guest photos never reach us at all.
			</p>
		</div>
	</section>
</main>

<style>
	.landing {
		font-family: var(--font-ui);
		color: var(--charcoal);
		background: var(--paper);
	}
	.hero {
		position: relative;
		background: var(--crimson);
		color: #fff;
		overflow: hidden;
		padding: 1.5rem 1.5rem 0;
	}
	.hero-inner {
		position: relative;
		z-index: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
		max-width: 72rem;
		margin: 0 auto;
		padding: clamp(4rem, 10vw, 7rem) 1.5rem clamp(4rem, 10vw, 7rem);
		text-align: center;
	}
	.marquee {
		position: relative;
		z-index: 0;
		margin: 0;
		font-family: var(--font-display);
		font-weight: 800;
		font-size: clamp(4.5rem, 16vw, 12rem);
		line-height: 0.95;
		letter-spacing: -0.03em;
		color: #fff;
		text-wrap: balance;
		user-select: none;
		max-width: none;
	}
	.lede {
		font-size: 3rem;
		line-height: 1.6;
		font-weight: bolder;
		color: rgb(255 255 255 / 0.85);
		max-width: 36rem;
		margin: 0;
		text-align: center;
	}
	.cta {
		display: inline-block;
		background: transparent;
		color: var(--mustard);
		font-family: var(--font-mono);
		font-weight: 700;
		font-size: 0.85rem;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		padding: 1.4rem 2rem;
		border-radius: 9999px;
		text-decoration: none;
		border: solid 2px var(--mustard);
		box-shadow: 0 4px 0 var(--crimson-deep);
		margin-top: 1rem;
	}
	.cta:hover {
		background: var(--mustard-deep);
		color: var(--charcoal);
	}
	/* Curved divide: concave flow from red into white */
	.hero::after {
		content: '';
		position: absolute;
		left: 0;
		right: 0;
		bottom: -1px;
		height: 72px;
		background: var(--paper);
		border-radius: 0 0 9999px 9999px / 0 0 72px 72px;
		transform: scaleX(1.6);
		transform-origin: top center;
		z-index: 2;
		pointer-events: none;
	}
	/* === White content sections === */
	.process,
	.privacy {
		background: var(--paper);
	}
	.process-inner,
	.privacy-inner {
		max-width: 72rem;
		margin: 0 auto;
		padding: 4rem 1.5rem;
	}
	.section-title {
		font-weight: 700;
		font-size: clamp(1.9rem, 3.5vw, 2.6rem);
		letter-spacing: -0.01em;
		margin: 0 0 2.5rem;
		color: var(--charcoal);
	}
	.steps {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 2.5rem;
	}
	.step-no {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--crimson);
		letter-spacing: 0.12em;
	}
	.steps h3 {
		font-weight: 700;
		font-size: 1.35rem;
		margin: 0.5rem 0 0.4rem;
		color: var(--charcoal);
	}
	.steps p {
		margin: 0;
		color: var(--ink-soft);
		font-size: 0.98rem;
		line-height: 1.55;
		max-width: 30ch;
	}
	.privacy {
		border-top: 1px solid var(--line);
	}
	.privacy ul {
		margin: 0 0 1.5rem;
		padding: 0;
		list-style: none;
		display: grid;
		gap: 1rem;
	}
	.privacy li {
		padding: 1.1rem 1.3rem;
		background: var(--surface);
		border: 1px solid var(--line);
		border-radius: 0;
		line-height: 1.5;
		color: var(--ink-soft);
		box-shadow: 0 1px 3px rgb(0 0 0 / 0.05);
	}
	.privacy li strong {
		color: var(--charcoal);
	}
	.privacy-note {
		font-size: 0.9rem;
		color: var(--ink-soft);
		border-top: 1px solid var(--line);
		padding-top: 1.25rem;
		margin: 0;
		max-width: 56ch;
		line-height: 1.6;
	}
	@media (max-width: 780px) {
		.marquee {
			font-size: clamp(3.6rem, 18vw, 7rem);
		}
		.steps {
			grid-template-columns: 1fr;
			gap: 2rem;
		}
	}
</style>
