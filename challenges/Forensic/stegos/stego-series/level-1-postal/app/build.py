import os
import base64
from PIL import Image, ImageDraw, PngImagePlugin

FLAG = os.environ.get('FLAG', 'H4L{METADATA_NO_ES_BASURA}')
COMMENT_B64 = base64.b64encode(FLAG.encode()).decode()


def build_cover(width=900, height=600):
    img = Image.new("RGB", (width, height))
    px = img.load()
    for y in range(height):
        for x in range(width):
            r = int(30 + 110 * x / width)
            g = int(70 + 90 * y / height)
            b = int(140 + 80 * (x + y) / (width + height))
            px[x, y] = (r, g, b)
    draw = ImageDraw.Draw(img)
    draw.rectangle((60, 60, width - 60, height - 60), outline=(245, 232, 188), width=6)
    draw.rectangle((100, 100, width - 100, height - 100), fill=(235, 214, 175))
    draw.rectangle((140, 140, width - 140, height - 170), fill=(168, 198, 224))
    draw.ellipse((220, 210, 420, 410), fill=(247, 202, 79))
    draw.rectangle((0, 390, width, height), fill=(212, 162, 106))
    draw.polygon([(520, 150), (700, 330), (340, 330)], fill=(79, 109, 122))
    draw.polygon([(620, 170), (780, 350), (470, 350)], fill=(54, 77, 93))
    return img


os.makedirs('dist', exist_ok=True)
cover = build_cover()
pnginfo = PngImagePlugin.PngInfo()
pnginfo.add_text("Comment", COMMENT_B64)
pnginfo.add_text("Title", "postal")
pnginfo.add_text("Series", "Ecos Ocultos")
cover.save('dist/postal.png', pnginfo=pnginfo)
print(f'[build] postal.png creado, Comment={COMMENT_B64[:20]}...')
