<script lang="ts">
	const faqs = [
		{
			q: "What happens to my photos while I'm in the booth?",
			a: 'They stay on your device. The preview, the shots, and the finished photo are all composed in your browser. Nothing is uploaded while you shoot.'
		},
		{
			q: "What's the difference between downloading and saving?",
			a: 'Downloading puts the finished photo on your device as a file. Saving uploads it into your gallery here, where it is stored so you can come back to it later. Saving is optional. You can take and download photos without ever saving one.'
		},
		{
			q: 'Do I need an account to use the photobooth?',
			a: 'No. You can choose a frame, take photos, and download the result without one. An account only exists if you want a gallery of saved photos, and creating one is entirely up to you.'
		},
		{
			q: 'Is it free?',
			a: 'Yes. No payment, no trial, nothing to buy.'
		},
		{
			q: 'What do I need to use it?',
			a: 'A phone, tablet, or computer with a camera and a reasonably current browser.'
		}
	];

	let openFaq = $state(-1);
</script>

<svelte:head>
	<title>Chewables</title>
	<meta
		name="description"
		content="Chewables is a privacy-conscious photobooth. Pick a frame, take photos with your camera, and download the result. Accounts are optional for saving photos to a gallery."
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
			<h2 id="process-heading" class="section-title">How it works</h2>
			<ol class="steps">
				<li>
					<span class="step-no">01</span>
					<h3>Choose a frame</h3>
					<p>Each frame needs a set number of photos.</p>
				</li>
				<li>
					<span class="step-no">02</span>
					<h3>Take the photos</h3>
					<p>The camera counts you down between each shot.</p>
				</li>
				<li>
					<span class="step-no">03</span>
					<h3>Download it</h3>
					<p>Your finished photo is composed in your browser. Download it, or save it to your gallery if you want to keep it.</p>
				</li>
			</ol>
		</div>
	</section>

	<section class="faq" id="faq" aria-labelledby="faq-heading">
		<div class="faq-inner">
			<h2 id="faq-heading" class="section-title">FAQs</h2>
			<div class="accordion">
				{#each faqs as faq, i}
					<div class="faq-item" class:open={openFaq === i}>
						<h3>
							<button
								type="button"
								class="faq-question"
								id="faq-button-{i}"
								aria-expanded={openFaq === i}
								aria-controls="faq-panel-{i}"
								onclick={() => (openFaq = openFaq === i ? -1 : i)}
							>
								<span>{faq.q}</span>
								<span class="faq-icon" aria-hidden="true"></span>
							</button>
						</h3>
						<div class="faq-panel" id="faq-panel-{i}" role="region" aria-labelledby="faq-button-{i}">
							<div class="faq-panel-inner">
								<p>{faq.a}</p>
							</div>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<section class="about" id="about" aria-labelledby="about-heading">
		<div class="about-inner">
			<h2 id="about-heading" class="section-title">About</h2>
			<ul class="about-links">
				<li><a href="mailto:kbreyes.dev@gmail.com">Contact us</a></li>
				<li><a href="https://github.com/kaylubr/chewables">GitHub</a></li>
				<li><a href="/report">Report an issue</a></li>
			</ul>
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
		padding: 2rem;
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
	}
	.cta {
		display: inline-block;
		box-sizing: border-box;
		max-width: 100%;
		background: transparent;
		color: var(--mustard);
		font-family: var(--font-ui);
		font-weight: 700;
		font-size: clamp(0.72rem, 0.5vw + 0.65rem, 0.85rem);
		letter-spacing: 0.06em;
		text-transform: uppercase;
		white-space: nowrap;
		padding: clamp(1.15rem, 1vw + 0.9rem, 1.4rem) clamp(1.3rem, 2.5vw + 0.8rem, 2rem);
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
	.faq,
	.about {
		background: var(--paper);
	}
	.process-inner,
	.faq-inner,
	.about-inner {
		max-width: 72rem;
		margin: 0 auto;
		padding: 4rem 1.5rem;
		color: var(--crimson);
	}
	.faq,
	.about {
		border-top: 1px solid var(--line);
		scroll-margin-top: 6.5rem;
	}
	.faq-inner,
	.about-inner {
		max-width: 56rem;
	}
	.section-title {
		font-weight: 700;
		font-size: clamp(1.9rem, 3.5vw, 2.6rem);
		letter-spacing: -0.01em;
		margin: 0 0 2.5rem;
		color: var(--charcoal);
		text-align: center;
	}
	.steps {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 2.5rem;
		text-align: center;
	}
	.step-no {
		font-size: clamp(0.8rem, 1.4vw, 1.2rem);
		color: var(--crimson);
		letter-spacing: 0.12em;
	}
	.steps h3 {
		font-weight: bolder;
		font-size: clamp(1rem, 1.9vw, 1.5rem);
		margin: 0.5rem 0 0.4rem;
		color: var(--charcoal);
	}
	.steps p {
		margin: 0;
		color: var(--ink-soft);
		font-size: clamp(0.82rem, 1.2vw, 1.2rem);
		font-weight: 700;
		line-height: 1.55;
		text-align: center;
	}
	.accordion {
		display: grid;
		gap: 0.75rem;
	}
	.faq-item {
		background: var(--surface);
		border: 1px solid var(--line);
		border-radius: 0.5rem;
	}
	.faq-question {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		padding: 1.1rem 1.3rem;
		background: none;
		border: none;
		font-family: var(--font-ui);
		font-size: 1.05rem;
		font-weight: 700;
		text-align: left;
		color: var(--charcoal);
		cursor: pointer;
		border-radius: 0.5rem;
	}
	.faq-question:hover {
		color: var(--crimson);
	}
	.faq-icon {
		position: relative;
		width: 1rem;
		height: 1rem;
		flex: none;
		color: var(--crimson);
	}
	.faq-icon::before,
	.faq-icon::after {
		content: '';
		position: absolute;
		background: currentColor;
		border-radius: 1px;
		transition: transform 0.2s ease;
	}
	.faq-icon::before {
		left: 0;
		right: 0;
		top: 50%;
		height: 2px;
		transform: translateY(-50%);
	}
	.faq-icon::after {
		top: 0;
		bottom: 0;
		left: 50%;
		width: 2px;
		transform: translateX(-50%);
	}
	.faq-item.open .faq-icon::after {
		transform: translateX(-50%) scaleY(0);
	}
	.faq-panel {
		display: grid;
		grid-template-rows: 0fr;
		transition: grid-template-rows 0.28s ease;
	}
	.faq-item.open .faq-panel {
		grid-template-rows: 1fr;
	}
	.faq-panel-inner {
		overflow: hidden;
	}
	.faq-panel p {
		margin: 0;
		padding: 0 1.3rem 1.2rem;
		color: var(--ink-soft);
		font-size: 0.98rem;
		line-height: 1.6;
		max-width: 60ch;
	}
	.about-links {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 1.25rem 3rem;
	}
	.about-links a {
		font-family: var(--font-ui);
		font-size: clamp(0.72rem, 0.4rem + 0.5vw, 0.9rem);
		letter-spacing: 0.04em;
		text-transform: uppercase;
		font-weight: 600;
		text-decoration: none;
		white-space: nowrap;
	}
	.about-links a:hover {
		text-decoration: underline;
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
