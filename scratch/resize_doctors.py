import os
from PIL import Image

def resize_image(input_path, output_path, size=(800, 800)):
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Crop to square
            width, height = img.size
            if width > height:
                left = (width - height) / 2
                top = 0
                right = (width + height) / 2
                bottom = height
            else:
                left = 0
                top = (height - width) / 2
                right = width
                bottom = (height + width) / 2
            
            img = img.crop((left, top, right, bottom))
            img = img.resize(size, Image.Resampling.LANCZOS)
            img.save(output_path, "JPEG", quality=90)
            print(f"Resized {input_path} to {output_path}")
    except Exception as e:
        print(f"Error resizing {input_path}: {e}")

mapping = {
    "backups/imagens_originais/dra_tamires.jpeg": "static/imagens/dra_tamires.jpg",
    "backups/imagens_originais/dra_marcela.jpeg": "static/imagens/dra_marcella.jpg",
    "backups/imagens_originais/dr_thiago.jpeg": "static/imagens/dr_thales.jpg",
    "backups/imagens_originais/dra_maria_sabela.JPEG": "static/imagens/dra_isabela.jpg"
}

# Also optimize the background if it exists in the backup
bg_src = "backups/imagens_originais/fundo_new.png"
bg_dst = "static/imagens/fundo_novo_raio.jpg"

if os.path.exists(bg_src):
    try:
        with Image.open(bg_src) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            # Resize to 1920 width, keeping aspect ratio
            w_percent = (1920 / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((1920, h_size), Image.Resampling.LANCZOS)
            img.save(bg_dst, "JPEG", quality=85, optimize=True)
            print(f"Optimized background {bg_src} to {bg_dst}")
    except Exception as e:
        print(f"Error optimizing background: {e}")

for src, dst in mapping.items():
    if os.path.exists(src):
        resize_image(src, dst)
    else:
        print(f"Source file {src} not found")
