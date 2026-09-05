import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { COUNTDOWN_SECONDS, createCaptureController } from './capture';
import { getFrame } from '../frames/frames';

describe('capture controller', () => {
	beforeEach(() => {
		vi.useFakeTimers();
	});

	afterEach(() => {
		vi.useRealTimers();
	});

	function makeFrame(photoCount: number) {
		const film = getFrame('FILM')!;
		return { ...film, photoCount };
	}

	function makeController(photoCount: number, snap: () => string = () => 'data:image/png;base64,x') {
		const frame = makeFrame(photoCount);
		const shots: string[] = [];
		const states: string[] = [];
		const controller = createCaptureController(
			frame,
			{ snap },
			(c) => shots.push(c.dataUrl),
			(s) => states.push(s)
		);
		return { controller, shots, states };
	}

	function advanceSeconds(controller: { start(): void }, seconds: number) {
		controller.start();
		vi.advanceTimersByTime(seconds * 1000);
	}

	it('captures exactly photoCount images with a countdown before each', () => {
		const { controller, shots, states } = makeController(2);
		controller.start();
		expect(states[0]).toBe('countdown');
		// 5s countdown then first capture
		vi.advanceTimersByTime(COUNTDOWN_SECONDS * 1000);
		expect(shots).toHaveLength(1);
		expect(states).toContain('capturing');
		// second countdown then second capture -> composing
		vi.advanceTimersByTime(COUNTDOWN_SECONDS * 1000);
		expect(shots).toHaveLength(2);
		expect(controller.done).toBe(true);
		expect(states[states.length - 1]).toBe('composing');
	});

	it('records each capture index in order', () => {
		const { controller } = makeController(3);
		const indices: number[] = [];
		const frame = makeFrame(3);
		createCaptureController(
			frame,
			{ snap: () => 'x' },
			(c) => indices.push(c.index),
			() => {}
		).start();
		vi.advanceTimersByTime(COUNTDOWN_SECONDS * 1000);
		expect(indices).toEqual([0]);
	});

	it('start is idempotent while active', () => {
		const { controller, shots } = makeController(2);
		controller.start();
		controller.start();
		controller.start();
		vi.advanceTimersByTime(COUNTDOWN_SECONDS * 1000);
		expect(shots).toHaveLength(1);
	});

	it('snap failure surfaces an error and stops', () => {
		const { controller, states } = makeController(1, () => {
			throw new Error('camera died');
		});
		controller.start();
		vi.advanceTimersByTime(COUNTDOWN_SECONDS * 1000);
		expect(states).toContain('error');
		expect(controller.done).toBe(false);
	});

	it('abort stops the run without further shots', () => {
		const { controller, shots } = makeController(3);
		controller.start();
		vi.advanceTimersByTime(2000);
		controller.abort();
		vi.advanceTimersByTime(COUNTDOWN_SECONDS * 1000);
		expect(shots).toHaveLength(0);
		expect(controller.done).toBe(true);
	});
});
