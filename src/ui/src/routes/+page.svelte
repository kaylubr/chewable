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
				Make the moment yours.
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
		background: var(--crimson);
		color: #fff;
		padding: 1.5rem 1.5rem 0;
	}
	.hero-inner {
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
		max-width: 72rem;
		margin: 0 auto;
		padding: 4rem 1.5rem 4rem;
		text-align: center;
	}
	.marquee {
		font-family: var(--font-display);
		font-weight: 800;
		font-size: clamp(4.5rem, 16vw, 10rem);
		line-height: 0.95;
		letter-spacing: -0.03em;
		color: var(--mustard);
		text-wrap: balance;
		user-select: none;
		max-width: none;
		margin-bottom: 5rem;
	}
	.lede {
		font-size: clamp(0.9rem, 3.2vw, 2rem);
		text-align: center;
		line-height: 1.6;
		font-weight: bolder;
		color: #fff;
		max-width: 36rem;
		margin: 0 auto;
		text-align: center;
	}
	.cta {
		display: inline-block;
		background: transparent;
		color: var(--mustard);
		font-family: var(--font-ui);
		font-weight: 700;
		font-size: 0.85rem;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		padding: 1.4rem 2rem;
		border-radius: 9999px;
		text-decoration: none;
		border: solid 2px var(--mustard);
		margin-top: 2rem;
	}
	.cta:hover {
		background: var(--mustard-deep);
		color: var(--charcoal);
	}
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
