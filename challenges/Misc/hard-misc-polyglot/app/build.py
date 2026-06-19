import os, io, zipfile
from PIL import Image, ImageDraw

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

# Create PNG image (boring, nothing to see here)
img = Image.new('RGB', (600, 300), color=(15, 15, 25))
draw = ImageDraw.Draw(img)
draw.rectangle([20, 20, 580, 280], outline=(0, 80, 0), width=2)
draw.text((60, 120), "ARTIFACT-7734", fill=(0, 180, 50))
draw.text((60, 160), "Status: CLASSIFIED", fill=(0, 100, 30))
draw.text((60, 200), "Nothing to see here.", fill=(0, 60, 20))

png_buf = io.BytesIO()
img.save(png_buf, format='PNG')
png_data = png_buf.getvalue()

# Create ZIP with flag.txt
zip_buf = io.BytesIO()
with zipfile.ZipFile(zip_buf, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('flag.txt', FLAG + '\n')
    zf.writestr('README.txt', 'You found the hidden archive.\n')
zip_data = zip_buf.getvalue()

os.makedirs('dist', exist_ok=True)
with open('dist/artifact-7734.png', 'wb') as f:
    f.write(png_data)   # valid PNG
    f.write(zip_data)   # valid ZIP appended at end
