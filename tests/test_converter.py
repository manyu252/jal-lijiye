import os
import tempfile
import cv2
import numpy as np
from PIL import Image
from scripts.mp4_to_gif import convert_mp4_to_transparent_gif

def test_mp4_to_gif_file_not_found():
    result = convert_mp4_to_transparent_gif("non_existent_video.mp4", "output.gif")
    assert result is False

def test_mp4_to_gif_conversion():
    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = os.path.join(tmpdir, "sample.mp4")
        gif_path = os.path.join(tmpdir, "sample.gif")

        # Create a synthetic 10-frame 100x100 BGR video with white background and a red box character
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(video_path, fourcc, 10.0, (100, 100))
        for i in range(10):
            # White background (255, 255, 255)
            frame = np.full((100, 100, 3), 255, dtype=np.uint8)
            # Red box character in BGR (0, 0, 200) moving right
            frame[30:70, (10 + i * 5):(40 + i * 5)] = [0, 0, 200]
            out.write(frame)
        out.release()

        # Execute conversion
        res = convert_mp4_to_transparent_gif(video_path, gif_path, max_seconds=1.0, target_height=60, canvas_size=100)
        assert res is True
        assert os.path.exists(gif_path)

        # Verify generated GIF
        gif_img = Image.open(gif_path)
        assert gif_img.size == (100, 100)
        
        # Check first frame transparency
        frame0 = gif_img.convert("RGBA")
        # Corner (0,0) should be transparent (alpha = 0)
        assert frame0.getpixel((0, 0))[3] == 0
