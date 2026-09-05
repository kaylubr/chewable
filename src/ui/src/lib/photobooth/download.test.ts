import { afterEach, describe, expect, it, vi } from 'vitest';
import { downloadDataUrl, photoFilename } from './download';

describe('download helpers', () => {
	afterEach(() => {
		vi.restoreAllMocks();
	});

	it('creates an anchor with the data URL and clicks it', () => {
		const click = vi.fn();
		const remove = vi.fn();
		const anchor = { click, remove, href: '', download: '' };
		vi.spyOn(document, 'createElement').mockReturnValue(anchor as unknown as HTMLAnchorElement);
		vi.spyOn(document.body, 'appendChild').mockImplementation(() => anchor as never);

		downloadDataUrl('data:image/webp;base64,abc', 'chewables-film.webp');

		expect(anchor.href).toBe('data:image/webp;base64,abc');
		expect(anchor.download).toBe('chewables-film.webp');
		expect(click).toHaveBeenCalledOnce();
		expect(remove).toHaveBeenCalledOnce();
	});

	it('derives filenames from the frame id, lowercased', () => {
		expect(photoFilename('FILM')).toBe('chewables-film.webp');
		expect(photoFilename(undefined)).toBe('chewables-photo.webp');
	});
});
