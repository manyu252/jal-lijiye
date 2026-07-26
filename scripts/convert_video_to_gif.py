import os
import cv2
import numpy as np
from PIL import Image

def process_walk_video():
    video_path = "walk_video.mp4"
    if not os.path.exists(video_path):
        print(f"Error: {video_path} not found!")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Video Info: {width}x{height}, {fps} FPS, {total_frames} total frames.")

    # Read first frame to sample beige wall background color
    ret, frame = cap.read()
    if not ret:
        print("Error reading first frame.")
        cap.release()
        return

    # Sample top-left and top-right corner pixels to estimate background color
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    top_left_bg = hsv_frame[0:30, 0:30]
    avg_bg_hsv = np.mean(top_left_bg, axis=(0, 1))
    print(f"Estimated Background HSV: {avg_bg_hsv}")

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frames = []

    # Sample max 16 evenly spaced frames for a smooth, lightweight GIF
    num_samples = 16
    sample_indices = np.linspace(0, total_frames - 1, num_samples, dtype=int)

    for idx in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        if idx not in sample_indices:
            continue

        # Convert to RGBA
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Color difference mask in HSV / Lab color space
        # Beige background has specific Hue (around 10-30), Low-Medium Saturation (20-100), High Value (>150)
        h_diff = np.abs(frame_hsv[:, :, 0].astype(int) - int(avg_bg_hsv[0]))
        s_diff = np.abs(frame_hsv[:, :, 1].astype(int) - int(avg_bg_hsv[1]))
        v_diff = np.abs(frame_hsv[:, :, 2].astype(int) - int(avg_bg_hsv[2]))

        # Mask background pixels
        bg_mask = (h_diff < 18) & (s_diff < 50) & (v_diff < 50)

        rgba = np.dstack((frame_rgb, np.full((height, width), 255, dtype=np.uint8)))
        rgba[bg_mask, 3] = 0

        # Convert to PIL
        pil_img = Image.fromarray(rgba, "RGBA")

        # Crop to non-transparent bounding box
        bbox = pil_img.getbbox()
        if bbox:
            cropped = pil_img.crop(bbox)
        else:
            cropped = pil_img

        # Resize to standard overlay height (120px)
        scale = 120.0 / cropped.height
        new_w = max(1, int(cropped.width * scale))
        resized = cropped.resize((new_w, 120), Image.Resampling.LANCZOS)

        # Place on 140x140 transparent canvas
        canvas = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
        canvas.paste(resized, ((140 - new_w) // 2, 140 - 120), resized)

        frames.append(canvas)

    cap.release()

    if not frames:
        print("No frames extracted.")
        return

    os.makedirs("assets", exist_ok=True)

    # Save walk.gif
    frames[0].save(
        "assets/walk.gif",
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / 12),
        loop=0,
        disposal=2
    )
    print(f"Successfully generated assets/walk.gif ({len(frames)} frames)")

    # Save exit.gif (flipped left)
    exit_frames = [Image.fromarray(np.fliplr(np.array(f)), "RGBA") for f in frames]
    exit_frames[0].save(
        "assets/exit.gif",
        save_all=True,
        append_images=exit_frames[1:],
        duration=int(1000 / 12),
        loop=0,
        disposal=2
    )
    print(f"Successfully generated assets/exit.gif ({len(exit_frames)} frames)")

if __name__ == "__main__":
    process_walk_video()
