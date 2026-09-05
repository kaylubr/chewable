/**
 * Centralized frame configuration.
 *
 * Capture logic only needs `photoCount`; composition reads the full
 * definition (canvas size + photo slots + overlay image). Frame artwork is
 * created externally and dropped into static/frames/, then registered here.
 */
import type { FrameDefinition, FrameId } from "./types";

export const FRAMES: FrameDefinition[] = [
  {
    id: "FILM",
    name: "35mm Film",
    image: "/frames/classic.jpg",
    photoCount: 4,
    width: 1620,
    height: 2880,
    photoSlots: [
      // Measured white windows in the overlay: x 386-1233, y 187-782.
      // Inset ~6px so photos stay cleanly inside each frame opening.
      { x: 392, y: 193, width: 836, height: 584, rotation: 0 },
      { x: 392, y: 829, width: 836, height: 584, rotation: 0 },
      { x: 392, y: 1466, width: 836, height: 584, rotation: 0 },
      { x: 392, y: 2127, width: 836, height: 584, rotation: 0 },
    ],
  },
];

export const FRAME_BY_ID: ReadonlyMap<FrameId, FrameDefinition> = new Map(
  FRAMES.map((frame) => [frame.id, frame]),
);

/** Resolve a frame id to its definition, or undefined if unsupported. */
export function getFrame(id: FrameId): FrameDefinition | undefined {
  return FRAME_BY_ID.get(id);
}
