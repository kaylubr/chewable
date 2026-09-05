/**
 * Shared photobooth store.
 *
 * A single module-level session shared across the /photobooth routes so the
 * selected frame and captures survive navigation from frame -> camera ->
 * result. Lives only in the browser; reloading resets the flow.
 */
import type { FrameId } from '../frames/types';
import { FRAME_BY_ID } from '../frames/frames';
import { initialBooth, type BoothSession } from './session';

class PhotoboothStore {
	session = $state<BoothSession>({ ...initialBooth });

	get frame() {
		return this.session.frameId ? FRAME_BY_ID.get(this.session.frameId) : undefined;
	}

	selectFrame(id: FrameId) {
		this.session.frameId = id;
	}

	reset() {
		this.session = { ...initialBooth };
	}
}

export const booth = new PhotoboothStore();
