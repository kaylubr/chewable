/**
 * Canvas composition for the photobooth result.
 *
 * Rendering order per frame: captured photos are drawn into their configured
 * slots (cover-fit so the whole slot is filled), then the frame overlay PNG
 * is drawn on top so the artwork frames the photos.
 *
 * The pure geometry helpers (cover-fit source rectangles) are exported and
 * unit-tested without needing a real canvas.
 */
import type { FrameDefinition, PhotoSlot } from '../frames/types';
import type { PhotoCapture } from './session';

export interface SlotSourceRect {
	/** Source rectangle within the photo, in photo pixels. */
	sx: number;
	sy: number;
	sw: number;
	sh: number;
}

/**
 * Compute the source rectangle that cover-fits a photo into a slot while
 * preserving aspect ratio (like CSS `object-fit: cover`).
 */
export function coverSourceRect(
	photoWidth: number,
	photoHeight: number,
	slot: Pick<PhotoSlot, 'width' | 'height'>
): SlotSourceRect {
	const scale = Math.max(slot.width / photoWidth, slot.height / photoHeight);
	const sw = slot.width / scale;
	const sh = slot.height / scale;
	return {
		sx: (photoWidth - sw) / 2,
		sy: (photoHeight - sh) / 2,
		sw,
		sh
	};
}

export interface ComposeOptions {
	/** Loads an image element from a URL/data URL (injectable for tests). */
	loadImage?: (src: string) => Promise<HTMLImageElement>;
	/** Canvas factory (injectable for tests). */
	createCanvas?: () => HTMLCanvasElement;
	/** Output MIME type and quality. */
	mimeType?: string;
	quality?: number;
}

function defaultLoadImage(src: string): Promise<HTMLImageElement> {
	return new Promise((resolve, reject) => {
		const img = new Image();
		img.onload = () => resolve(img);
		img.onerror = () => reject(new Error(`could not load image: ${src}`));
		img.src = src;
	});
}

/**
 * Compose the final photobooth image: photos into slots, overlay on top.
 * Returns a data URL of the composed result.
 */
export async function composePhoto(
	frame: FrameDefinition,
	captures: PhotoCapture[],
	options: ComposeOptions = {}
): Promise<string> {
	if (captures.length < frame.photoCount) {
		throw new Error(
			`need ${frame.photoCount} captures, got ${captures.length}`
		);
	}
	const loadImage = options.loadImage ?? defaultLoadImage;
	const createCanvas =
		options.createCanvas ??
		(() => {
			const c = document.createElement('canvas');
			c.width = frame.width;
			c.height = frame.height;
			return c;
		});

	const canvas = createCanvas();
	const ctx = canvas.getContext('2d');
	if (!ctx) throw new Error('canvas 2d context unavailable');
	canvas.width = frame.width;
	canvas.height = frame.height;

	const photos = await Promise.all(
		captures.map((c) => loadImage(c.dataUrl))
	);

	// 1. Draw each captured photo into its slot (cover-fit).
	frame.photoSlots.forEach((slot, i) => {
		const photo = photos[i];
		const src = coverSourceRect(photo.naturalWidth, photo.naturalHeight, slot);
		drawPhoto(ctx, slot, src, photo);
	});

	// 2. Draw the frame artwork over the photos.
	const overlay = await loadImage(frame.image);
	ctx.drawImage(overlay, 0, 0, frame.width, frame.height);

	return canvas.toDataURL(options.mimeType ?? 'image/webp', options.quality ?? 0.92);
}

function drawPhoto(
	ctx: CanvasRenderingContext2D,
	slot: PhotoSlot,
	src: SlotSourceRect,
	photo: HTMLImageElement
): void {
	ctx.save();
	if (slot.rotation) {
		const cx = slot.x + slot.width / 2;
		const cy = slot.y + slot.height / 2;
		ctx.translate(cx, cy);
		ctx.rotate((slot.rotation * Math.PI) / 180);
		ctx.translate(-cx, -cy);
	}
	ctx.drawImage(
		photo,
		src.sx,
		src.sy,
		src.sw,
		src.sh,
		slot.x,
		slot.y,
		slot.width,
		slot.height
	);
	ctx.restore();
}
