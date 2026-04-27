from PIL import Image
import os

img_path = '/home/joaonote/elleva.local/imagem_backgraund.png'
out_path = '/home/joaonote/elleva.local/static/imagens/new_background.png'

print(f"Original size: {os.path.getsize(img_path) / 1024 / 1024:.2f} MB")

with Image.open(img_path) as img:
    print(f"Original resolution: {img.size}, Mode: {img.mode}")
    
    # We will resize to max 1920x1080 (HD) keeping aspect ratio
    img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
    
    # Let's save it as optimized JPG instead, as PNGs for background photos are huge.
    # We will save it as 'new_background.jpg'
    
out_jpg = '/home/joaonote/elleva.local/static/imagens/new_background.jpg'
with Image.open(img_path) as img:
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
    img.save(out_jpg, "JPEG", quality=80, optimize=True)

print(f"Optimized JPG size: {os.path.getsize(out_jpg) / 1024:.2f} KB")
