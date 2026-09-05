/**
 * Download helpers for the composed photobooth result.
 */

/** Trigger a browser download of a data URL under a given filename. */
export function downloadDataUrl(dataUrl: string, filename: string): void {
	const a = document.createElement('a');
	a.href = dataUrl;
	a.download = filename;
	document.body.appendChild(a);
	a.click();
	a.remove();
}

/** Derive a sensible filename from the frame id. */
export function photoFilename(frameId: string | undefined): string {
	const base = frameId ? frameId.toLowerCase() : 'photo';
	return `chewables-${base}.webp`;
}
