import { describe, expect, it } from 'vitest';
import { classifyCameraError, type CameraErrorInfo } from './camera';

describe('classifyCameraError', () => {
	it('maps permission denial to a useful message', () => {
		const err = new DOMException('denied', 'NotAllowedError');
		const info: CameraErrorInfo = classifyCameraError(err);
		expect(info.kind).toBe('permission-denied');
		expect(info.message).toMatch(/allow camera access/i);
	});

	it('maps a missing camera to not-found', () => {
		const info = classifyCameraError(new DOMException('none', 'NotFoundError'));
		expect(info.kind).toBe('not-found');
		expect(info.message).toMatch(/no camera/i);
	});

	it('maps an in-use camera to a close-other-app hint', () => {
		const info = classifyCameraError(new DOMException('busy', 'NotReadableError'));
		expect(info.kind).toBe('in-use');
		expect(info.message).toMatch(/already in use/i);
	});

	it('falls back to a generic message for unknown errors', () => {
		const info = classifyCameraError(new Error('weird'));
		expect(info.kind).toBe('unknown');
		expect(info.message).toBeTruthy();
	});

	it('handles non-error values gracefully', () => {
		expect(classifyCameraError(null).kind).toBe('unknown');
		expect(classifyCameraError('boom').kind).toBe('unknown');
	});
});
