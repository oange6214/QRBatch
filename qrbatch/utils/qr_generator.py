import qrcode
from typing import List

class QRCodeGenerator:
    @staticmethod
    def generate_qr_code(data: str, filename: str) -> None:
        qr = qrcode.QRCode(
            version=None, 
            error_correction=qrcode.constants.ERROR_CORRECT_L, 
            box_size=10, 
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)