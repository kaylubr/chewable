import { afterEach, describe, expect, it, vi } from 'vitest';
import { api, ApiError } from './client';

function jsonResponse(status: number, body: unknown): Response {
	return new Response(JSON.stringify(body), {
		status,
		headers: { 'Content-Type': 'application/json' }
	});
}

describe('api client', () => {
	afterEach(() => {
		vi.unstubAllGlobals();
	});

	it('uploadPhoto sends a bearer token, the frame, and the image as multipart', async () => {
		let captured: { url: string; init: RequestInit } | undefined;
		vi.stubGlobal(
			'fetch',
			vi.fn(async (url: string, init: RequestInit) => {
				captured = { url, init };
				return jsonResponse(201, {
					id: 'p1',
					frame: 'FILM',
					storage_key: 'users/u1/photos/p1.webp',
					created_at: '2026-09-05T00:00:00Z'
				});
			})
		);

		const blob = new Blob(['webp-data'], { type: 'image/webp' });
		const result = await api.uploadPhoto('tok-1', 'FILM', blob);

		expect(result.id).toBe('p1');
		expect(captured!.url).toContain('/api/photos');
		expect(captured!.init.method).toBe('POST');
		const headers = captured!.init.headers as Record<string, string>;
		expect(headers['Authorization']).toBe('Bearer tok-1');
		expect(captured!.init.body).toBeInstanceOf(FormData);
		const form = captured!.init.body as FormData;
		expect(form.get('frame')).toBe('FILM');
		// Browsers normalize appended Blobs to File parts in FormData.
		const filePart = form.get('file');
		expect(filePart).toBeInstanceOf(File);
		expect((filePart as File).type).toBe('image/webp');
		expect((filePart as File).name).toBe('chewables-film.webp');
	});

	it('listPhotos sends the bearer token and returns photos', async () => {
		vi.stubGlobal(
			'fetch',
			vi.fn(async () =>
				jsonResponse(200, [
					{ id: 'p1', frame: 'FILM', storage_key: 'k', created_at: '2026-09-05T00:00:00Z' }
				])
			)
		);
		const photos = await api.listPhotos('tok-1');
		expect(photos).toHaveLength(1);
		const call = vi.mocked(fetch).mock.calls[0];
		const headers = (call[1]!.headers as Record<string, string>);
		expect(headers['Authorization']).toBe('Bearer tok-1');
	});

	it('deletePhoto sends DELETE with the token', async () => {
		vi.stubGlobal('fetch', vi.fn(async () => new Response(null, { status: 204 })));
		await api.deletePhoto('tok-1', 'p1');
		const call = vi.mocked(fetch).mock.calls[0];
		expect(call[0]).toContain('/api/photos/p1');
		expect(call[1]!.method).toBe('DELETE');
	});

	it('maps an API error detail into ApiError with its status', async () => {
		vi.stubGlobal(
			'fetch',
			vi.fn(async () => jsonResponse(401, { detail: 'Incorrect username or password' }))
		);
		await expect(api.login('someuser', 'wrong')).rejects.toMatchObject({
			status: 401,
			message: 'Incorrect username or password'
		});
	});

	it('surfaces non-JSON error bodies with a fallback message', async () => {
		vi.stubGlobal('fetch', vi.fn(async () => new Response('oops', { status: 500 })));
		try {
			await api.listPhotos('tok');
			expect.unreachable('should have thrown');
		} catch (e) {
			expect(e).toBeInstanceOf(ApiError);
		}
	});
});
