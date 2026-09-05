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
    image: "/frames/classic.png",
    photoCount: 4,
    width: 564,
    height: 1365,
    photoSlots: [
      // Transparent windows in the overlay (classic.png): x 82-484, y bands
      // 88-371 / 390-672 / 691-974 / 1005-1287. Inset 2px so photo edges
      // sit under the frame's border line.
      { x: 84, y: 90, width: 399, height: 280, rotation: 0 },
      { x: 84, y: 392, width: 399, height: 279, rotation: 0 },
      { x: 84, y: 693, width: 399, height: 280, rotation: 0 },
      { x: 84, y: 1007, width: 399, height: 279, rotation: 0 },
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
