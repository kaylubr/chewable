/**
 * Photobooth capture controller.
 *
 * Drives the timed multi-shot capture: a 5-second countdown precedes each
 * shot, and after the frame's photoCount is reached the session moves to
 * composing. The controller is deliberately injectable — the camera page
 * feeds it a live <video> element, while tests feed it fakes — so the
 * countdown/transition/capture-count logic is exercised without a camera.
 */
import type { FrameDefinition } from '../frames/types';
import type { PhotoCapture } from './session';

export const COUNTDOWN_SECONDS = 5;

export interface CaptureDeps {
	/** Snapshot the current video frame and resolve with a data URL. */
	snap(): Promise<string> | string;
}

export interface CaptureController {
	/** Number of shots captured so far. */
	shots: number;
	/** Seconds remaining in the current countdown. */
	countdown: number;
	/** True while a countdown is ticking. */
	active: boolean;
	/** Start the capture run (idempotent while active). */
	start(): void;
	/** Abort a run in progress. */
	abort(): void;
	/** Whether the run has finished all shots. */
	done: boolean;
	/** Resolves when the run completes (all shots) or aborts. */
	finished: Promise<void>;
}

/**
 * Create a capture controller for a frame.
 * Fires onShot for every captured still.
 */
export function createCaptureController(
	frame: FrameDefinition,
	deps: CaptureDeps,
	onShot: (capture: PhotoCapture) => void,
	onState: (state: 'countdown' | 'capturing' | 'composing' | 'error') => void,
	intervalMs = 1000
): CaptureController {
	let shots = 0;
	let countdown = COUNTDOWN_SECONDS;
	let active = false;
	let done = false;
	let timer: ReturnType<typeof setTimeout> | null = null;
	let resolveFinished: () => void;
	const finished = new Promise<void>((resolve) => {
		resolveFinished = resolve;
	});

	function clearTimer() {
		if (timer) {
			clearInterval(timer);
			timer = null;
		}
	}

	function finish() {
		clearTimer();
		active = false;
		done = true;
		resolveFinished();
	}

	function tick() {
		countdown -= 1;
		if (countdown > 0) {
			onState('countdown');
			return;
		}
		// Countdown reached zero — take the shot.
		clearTimer();
		countdown = COUNTDOWN_SECONDS;
		onState('capturing');
		let dataUrl: string;
		try {
			dataUrl = deps.snap();
		} catch {
			active = false;
			onState('error');
			return;
		}
		const capture: PhotoCapture = { dataUrl, index: shots };
		shots += 1;
		onShot(capture);
		if (shots >= frame.photoCount) {
			onState('composing');
			finish();
			return;
		}
		// Start the next countdown.
		timer = setInterval(tick, intervalMs);
		onState('countdown');
	}

	return {
		get shots() {
			return shots;
		},
		get countdown() {
			return countdown;
		},
		get active() {
			return active;
		},
		get done() {
			return done;
		},
		get finished() {
			return finished;
		},
		start() {
			if (active || done) return;
			active = true;
			countdown = COUNTDOWN_SECONDS;
			onState('countdown');
			timer = setInterval(tick, intervalMs);
		},
		abort() {
			if (!active) return;
			clearTimer();
			active = false;
			done = true;
			resolveFinished();
		}
	};
}
