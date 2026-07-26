import os
import cv2
import numpy as np
from PIL import Image

def convert_video_to_transparent_gif(video_path, output_gif_path, max_duration_sec=5.0):
    if not os.path.exists(video_path):
        print(f"Error: Video file {video_path} not found!")
        return False

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open {video_path}")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    max_frames = int(fps * max_duration_sec)
    frames_to_process = min(total_frames, max_frames)

    print(f"Processing {video_path}: {frames_to_process} frames (max {max_duration_sec}s)...")

    # Sample up to 24 frames for optimal performance & quality
    num_samples = min(24, frames_to_process)
    sample_indices = np.linspace(0, frames_to_process - 1, num_samples, dtype=int)

    frames = []

    for idx in range(frames_to_process):
        ret, frame = cap.read()
        if not ret:
            break

        if idx not in sample_indices:
            continue

        # BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # White background mask: pixels where R, G, B > 230
        r, g, b = frame_rgb[:, :, 0], frame_rgb[:, :, 1], frame_rgb[:, :, 2]
        white_mask = (r > 230) & (g > 230) & (b > 230)

        # Create RGBA
        height, width, _ = frame_rgb.shape
        rgba = np.dstack((frame_rgb, np.full((height, width), 255, dtype=np.uint8)))
        rgba[white_mask, 3] = 0

        pil_img = Image.fromarray(rgba, "RGBA")

        # Crop tight bounding box around non-transparent pixels
        bbox = pil_img.getbbox()
        if bbox:
            cropped = pil_img.crop(bbox)
        else:
            cropped = pil_img

        # Resize height to 190px (+50% scale up)
        scale = 190.0 / cropped.height
        new_w = max(1, int(cropped.width * scale))
        resized = cropped.resize((new_w, 190), Image.Resampling.LANCZOS)

        # Place on 225x225 transparent canvas
        canvas = Image.new("RGBA", (225, 225), (0, 0, 0, 0))
        canvas.paste(resized, ((225 - new_w) // 2, 225 - 190), resized)

        frames.append(canvas)

    cap.release()

    if not frames:
        print(f"Error: No frames extracted from {video_path}")
        return False

    os.makedirs(os.path.dirname(output_gif_path) or ".", exist_ok=True)

    # Calculate frame duration in ms
    duration = int(1000.0 / (len(frames) / max_duration_sec)) if len(frames) > 0 else 150

    frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        disposal=2
    )
    print(f"Successfully generated {output_gif_path} ({len(frames)} frames)")
    return True

if __name__ == "__main__":
    walk_in_path = "walk_in_video.mp4" if os.path.exists("walk_in_video.mp4") else "walki_in_video.mp4"
    walk_out_path = "walk_out_video.mp4" if os.path.exists("walk_out_video.mp4") else "walki_out_video.mp4"
    
    convert_video_to_transparent_gif(walk_in_path, "assets/walk.gif", max_duration_sec=5.0)
    convert_video_to_transparent_gif(walk_out_path, "assets/exit.gif", max_duration_sec=5.0)
