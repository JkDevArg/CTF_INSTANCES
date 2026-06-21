import os
import qrcode
from PIL import Image

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(FLAG)
qr.make(fit=True)

img = qr.make_image(fill_color='black', back_color='white')

os.makedirs('dist', exist_ok=True)
img.save('dist/codigo.png')

print("[+] codigo.png generado correctamente.")
