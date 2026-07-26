#!/usr/bin/env python3
"""
Simple and straightforward MP4 to transparent GIF converter for Jal Lijiye.
Usage:
    python scripts/mp4_to_gif.py <input.mp4> <output.gif> [max_seconds]
"""

import sys
import os
import cv2
import numpy as np
from PIL import Image

def convert_mp4_to_transparent_gif(video_path: str, gif_path: str, max_seconds: float = 5.0, target_height: int = 190, canvas_size: int = 225) -> bool:
    if not os.path.exists(video_path):
        print(f"Error: {video_path} not found.")
        return False

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open {video_path}.")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    max_frames_to_read = min(total_frames, int(fps * max_seconds))
    actual_duration_sec = max_frames_to_read / fps

    print(f"Converting {video_path} -> {gif_path} ({max_frames_to_read} frames, {actual_duration_sec:.2f}s)...")

    # Sample up to 25-30 frames for lightweight animation
    num_samples = min(25, max_frames_to_read)
    sample_indices = np.linspace(0, max_frames_to_read - 1, num_samples, dtype=int)

    # Estimate background color from top-left 30x30 corner
    ret, first_frame = cap.read()
    if not ret:
        print("Error reading video frame.")
        cap.release()
        return False

    bg_bgr = np.mean(first_frame[0:30, 0:30], axis=(0, 1))
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    frames = []

    for idx in range(max_frames_to_read):
        ret, frame = cap.read()
        if not ret:
            break

        if idx not in sample_indices:
            continue

        h, w = frame.shape[:2]
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Simple background removal by color distance from background color
        diff = np.linalg.norm(frame.astype(float) - bg_bgr, axis=2)
        r, g, b = frame_rgb[:, :, 0], frame_rgb[:, :, 1], frame_rgb[:, :, 2]
        
        # Identify background pixels (matching corner color or light background wall)
        bg_mask = (diff < 40) | ((r > 210) & (g > 210) & (b > 210))

        rgba = np.dstack((frame_rgb, np.full((h, w), 255, dtype=np.uint8)))
        rgba[bg_mask, 3] = 0

        pil_img = Image.fromarray(rgba, "RGBA")

        # Crop tight bounding box
        bbox = pil_img.getbbox()
        cropped = pil_img.crop(bbox) if bbox else pil_img

        # Scale height to target_height on canvas_size x canvas_size transparent canvas
        scale = float(target_height) / cropped.height
        new_w = max(1, int(cropped.width * scale))
        resized = cropped.resize((new_w, target_height), Image.Resampling.LANCZOS)

        canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        canvas.paste(resized, ((canvas_size - new_w) // 2, canvas_size - target_height), resized)

        frames.append(canvas)

    cap.release()

    if not frames:
        print("Error: No frames extracted.")
        return False

    # Calculate exact 1.0x real-time duration per frame
    frame_duration_ms = int((actual_duration_sec / len(frames)) * 1000)

    os.makedirs(os.path.dirname(gif_path) or ".", exist_ok=True)
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration_ms,
        loop=0,
        disposal=2
    )

    print(f"Saved {gif_path} ({len(frames)} frames, {frame_duration_ms}ms/frame).")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/mp4_to_gif.py <input.mp4> <output.gif> [max_seconds]")
        sys.exit(1)

    input_video = sys.argv[1]
    output_gif = sys.argv[2]
    duration_cap = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0

    convert_mp4_to_transparent_gif(input_video, output_gif, max_seconds=duration_cap)
