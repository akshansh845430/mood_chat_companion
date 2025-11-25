from PIL import Image
import os

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "avatars_raw")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")

os.makedirs(OUT_DIR, exist_ok=True)

def make_gif(input_name, output_name, duration=300):
    input_image = os.path.join(RAW_DIR, input_name)
    output_gif = os.path.join(OUT_DIR, output_name)

    img = Image.open(input_image)

    frames = [img, img]

    frames[0].save(
        output_gif,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )

    print(f"GIF saved: {output_gif}")


if __name__ == "__main__":
    make_gif("neutral.jpeg", "avatar_neutral.gif")
    make_gif("happy.jpeg", "avatar_happy.gif")
    make_gif("sad.webp", "avatar_sad.gif")
    make_gif("angry.jpg", "avatar_angry.gif")
