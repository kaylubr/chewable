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
		<div class="hero-copy">
			<p class="eyebrow">Expose · develop · keep</p>
			<h1>
				Four frames.<br />
				One strip.<br />
				Yours.
			</h1>
			<p class="lede">
				A photobooth that runs entirely in your browser. Pick a frame, take a few
				pictures, and the film is yours to download. No account, no upload, no
				waiting.
			</p>
			<a class="cta" href="/photobooth/frame">Start the photobooth</a>
		</div>

		<figure class="strip-figure" aria-label="The 35mm film frame you can fill with your photos">
			<div class="strip-frame">
				<img
					src="/frames/classic.png"
					alt="A 35mm film strip with four empty frames waiting for your photos"
					width="300"
					height="726"
				/>
			</div>
			<figcaption class="rebate">TX 5063 · 4 EXP · DEVELOPED IN-BROWSER</figcaption>
		</figure>
	</section>

	<section class="process" aria-labelledby="process-heading">
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
	:global(body) {
		background: var(--paper);
		color: var(--ink);
	}
	.landing {
		font-family: system-ui, sans-serif;
		color: var(--ink);
	}
	.hero {
		display: grid;
		grid-template-columns: 1.1fr 0.9fr;
		gap: 4rem;
		align-items: center;
		max-width: 72rem;
		margin: 0 auto;
		padding: 4.5rem 1.5rem 5rem;
	}
	.eyebrow {
		font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
		text-transform: uppercase;
		letter-spacing: 0.18em;
		font-size: 0.72rem;
		font-weight: 600;
		color: var(--ember-deep);
		margin: 0 0 1.25rem;
	}
	h1 {
		font-family: 'Fraunces Variable', Georgia, serif;
		font-weight: 560;
		font-size: clamp(2.9rem, 6.5vw, 5.2rem);
		line-height: 0.98;
		letter-spacing: -0.02em;
		margin: 0 0 1.5rem;
	}
	.lede {
		font-size: 1.15rem;
		line-height: 1.6;
		color: var(--warm-gray);
		max-width: 34rem;
		margin: 0 0 2rem;
	}
	.cta {
		display: inline-block;
		background: var(--ember);
		color: #fff;
		font-weight: 650;
		padding: 0.9rem 1.7rem;
		border-radius: 0.5rem;
		text-decoration: none;
		font-size: 1.05rem;
		box-shadow: 0 2px 0 var(--ember-deep);
	}
	.cta:hover {
		background: var(--ember-deep);
	}
	.strip-figure {
		margin: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.75rem;
	}
	.strip-frame {
		filter: drop-shadow(0 24px 40px rgb(28 25 23 / 0.28));
	}
	.strip-frame img {
		display: block;
		border-radius: 0.35rem;
	}
	.rebate {
		font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
		font-size: 0.68rem;
		letter-spacing: 0.14em;
		color: var(--warm-gray);
		text-transform: uppercase;
	}
	.process {
		max-width: 72rem;
		margin: 0 auto;
		padding: 2rem 1.5rem 5rem;
		border-top: 1px solid var(--line);
	}
	.section-title {
		font-family: 'Fraunces Variable', Georgia, serif;
		font-weight: 600;
		font-size: clamp(1.6rem, 3vw, 2.2rem);
		letter-spacing: -0.01em;
		margin: 0 0 2.5rem;
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
		font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
		font-size: 0.75rem;
		color: var(--ember-deep);
		letter-spacing: 0.1em;
	}
	.steps h3 {
		font-family: 'Fraunces Variable', Georgia, serif;
		font-weight: 640;
		font-size: 1.3rem;
		margin: 0.5rem 0 0.4rem;
	}
	.steps p {
		margin: 0;
		color: var(--warm-gray);
		font-size: 0.98rem;
		line-height: 1.55;
		max-width: 30ch;
	}
	.privacy {
		background: #14100c;
		color: #f5f1ea;
		padding: 5rem 1.5rem;
	}
	.privacy-inner {
		max-width: 56rem;
		margin: 0 auto;
	}
	.privacy .section-title {
		color: #f5f1ea;
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
		background: rgb(255 255 255 / 0.04);
		border: 1px solid rgb(255 255 255 / 0.09);
		border-radius: 0.5rem;
		line-height: 1.5;
	}
	.privacy li strong {
		color: #fff;
	}
	.privacy-note {
		font-size: 0.9rem;
		color: #b7aea3;
		border-top: 1px solid rgb(255 255 255 / 0.12);
		padding-top: 1.25rem;
		margin: 0;
		max-width: 52ch;
		line-height: 1.6;
	}
	@media (max-width: 780px) {
		.hero {
			grid-template-columns: 1fr;
			gap: 3rem;
			padding-top: 3rem;
		}
		.steps {
			grid-template-columns: 1fr;
			gap: 2rem;
		}
	}
</style>
