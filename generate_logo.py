from moviepy.video.VideoClip import VideoClip
from PIL import Image, ImageEnhance
import numpy as np

# === Pengaturan Awal ===
image_path = "enhanced_image~2.png"  # Ganti dengan nama file logomu
original_img = Image.open(image_path).convert("RGBA")
resized_img = original_img.resize((512, 512), resample=Image.BICUBIC)

# Parameter animasi
duration = 4  # detik
fps = 20
size = resized_img.size

# === Fungsi untuk menghasilkan setiap frame animasi ===
def make_frame(t):
    # Kilauan neon
    pulse = 1 + 0.3 * np.sin(2 * np.pi * t * 1.5)
    enhanced_img = ImageEnhance.Brightness(resized_img).enhance(pulse)

    # Gerakan sayap (simulasi scale)
    scale = 1 + 0.01 * np.sin(2 * np.pi * t * 2)
    new_size = (int(size[0] * scale), int(size[1] * scale))
    frame = enhanced_img.resize(new_size, resample=Image.BICUBIC)

    # Tempel ke background hitam
    background = Image.new("RGBA", size, (0, 0, 0, 255))
    offset = ((size[0] - new_size[0]) // 2, (size[1] - new_size[1]) // 2)
    background.paste(frame, offset, frame)

    # Fade-in seluruh gambar
    alpha = min(1, t / 1.5)
    frame_np = np.array(background).astype(np.float32)
    frame_np *= alpha
    frame_np = np.clip(frame_np, 0, 255).astype(np.uint8)

    return frame_np

# === Buat video clip ===
animated_clip = VideoClip(make_frame, duration=duration)
animated_clip.fps = fps  # <- menetapkan FPS langsung

# === Simpan sebagai file MP4 ===
animated_clip.write_videofile("logo_animated.mp4", codec="libx264", audio=False)
