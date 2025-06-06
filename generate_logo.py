from moviepy.video.VideoClip import VideoClip
from PIL import Image, ImageEnhance
import numpy as np

image_path = "enhanced_image~2.png"
original_img = Image.open(image_path).convert("RGBA")
resized_img = original_img.resize((512, 512), resample=Image.BICUBIC)

duration = 4
fps = 20
size = resized_img.size

def make_frame(t):
    pulse = 1 + 0.3 * np.sin(2 * np.pi * t * 1.5)
    enhanced_img = ImageEnhance.Brightness(resized_img).enhance(pulse)

    scale = 1 + 0.01 * np.sin(2 * np.pi * t * 2)
    new_size = (int(size[0] * scale), int(size[1] * scale))
    frame = enhanced_img.resize(new_size, resample=Image.BICUBIC)

    background = Image.new("RGBA", size, (0, 0, 0, 255))
    offset = ((size[0] - new_size[0]) // 2, (size[1] - new_size[1]) // 2)
    background.paste(frame, offset, frame)

    alpha = min(1, t / 1.5)
    frame_np = np.array(background).astype(np.float32)
    frame_np *= alpha
    frame_np = np.clip(frame_np, 0, 255).astype(np.uint8)
    return frame_np

animated_clip = VideoClip(make_frame, duration=duration)
animated_clip.fps = fps  # gunakan cara ini jika set_fps tidak tersedia

animated_clip.write_videofile("logo_animated.mp4", codec="libx264", audio=False)
