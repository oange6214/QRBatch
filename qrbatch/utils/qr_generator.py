import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from typing import Dict, Any, Optional
from PIL import Image
import io

class QRCodeGenerator:
    DEFAULT_CONFIG = {
        "version": None,
        "error_correction": qrcode.constants.ERROR_CORRECT_L,
        "box_size": 10,
        "border": 4,
        "fill_color": "black",
        "back_color": "white"
    }

    @staticmethod
    def generate_qr_code(data: str, filename: Optional[str] = None, 
                         config: Optional[Dict[str, Any]] = None,
                         style: Optional[str] = None,
                         logo: Optional[str] = None) -> Optional[Image.Image]:
        """
        產生 QR Code 並可選擇性地儲存至檔案。

        :param data: 欲編碼的資料
        :param filename: 儲存 QR Code 影像的檔案名稱（選擇性）
        :param config: QR Code 設定參數（選擇性）
        :param style: QR Code 樣式（使用 'rounded' 來產生圓角模組）
        :param logo: 欲加入 QR Code 中心的標誌圖檔路徑（選擇性）
        :return: 產生的 QR Code 影像物件，若儲存至檔案則回傳 None
        """
        try:
            qr_config = {**QRCodeGenerator.DEFAULT_CONFIG, **(config or {})}
            
            qr = qrcode.QRCode(
                version=qr_config["version"],
                error_correction=qr_config["error_correction"],
                box_size=qr_config["box_size"],
                border=qr_config["border"]
            )
            qr.add_data(data)
            qr.make(fit=True)

            if style == 'rounded':
                img = qr.make_image(fill_color=qr_config["fill_color"], 
                                    back_color=qr_config["back_color"],
                                    image_factory=StyledPilImage, 
                                    module_drawer=RoundedModuleDrawer())
            else:
                img = qr.make_image(fill_color=qr_config["fill_color"], 
                                    back_color=qr_config["back_color"])

            if logo:
                QRCodeGenerator._add_logo(img, logo)

            if filename:
                img.save(filename)
                return None
            return img
        except Exception as e:
            print(f"產生 QR Code 時發生錯誤: {e}")
            return None

    @staticmethod
    def _add_logo(qr_img: Image.Image, logo_path: str, size_percentage: float = 0.2):
        """
        在 QR Code 中心加入標誌。

        :param qr_img: QR Code 影像
        :param logo_path: 標誌圖檔路徑
        :param size_percentage: 標誌大小佔 QR Code 的比例
        """
        try:
            logo = Image.open(logo_path)
            qr_width, qr_height = qr_img.size
            logo_size = int(min(qr_width, qr_height) * size_percentage)
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo, pos, logo)
        except Exception as e:
            print(f"加入標誌時發生錯誤: {e}")

    @staticmethod
    def generate_qr_code_bytes(data: str, config: Optional[Dict[str, Any]] = None, 
                               style: Optional[str] = None, 
                               logo: Optional[str] = None) -> Optional[bytes]:
        """
        產生 QR Code 並回傳位元組資料。

        :param data: 欲編碼的資料
        :param config: QR Code 設定參數（選擇性）
        :param style: QR Code 樣式（使用 'rounded' 來產生圓角模組）
        :param logo: 欲加入 QR Code 中心的標誌圖檔路徑（選擇性）
        :return: QR Code 影像的位元組資料，若產生失敗則回傳 None
        """
        img = QRCodeGenerator.generate_qr_code(data, filename=None, config=config, style=style, logo=logo)
        if img:
            byte_arr = io.BytesIO()
            img.save(byte_arr, format='PNG')
            return byte_arr.getvalue()
        return None

if __name__ == "__main__":
    
    # 基本使用範例
    QRCodeGenerator.generate_qr_code("https://example.com", "basic_qr.png")

    # 使用自訂設定
    custom_config = {
        "box_size": 15,
        "border": 5,
        "fill_color": "blue",
        "back_color": "yellow"
    }
    QRCodeGenerator.generate_qr_code("Custom QR Code", "custom_qr.png", config=custom_config)

    # 使用圓角樣式
    QRCodeGenerator.generate_qr_code("Rounded QR Code", "rounded_qr.png", style='rounded')

    # 加入標誌
    QRCodeGenerator.generate_qr_code("QR with Logo", "logo_qr.png", logo="path_to_logo.png")

    # 產生位元組資料
    qr_bytes = QRCodeGenerator.generate_qr_code_bytes("Bytes QR Code")
    if qr_bytes:
        with open("bytes_qr.png", "wb") as f:
            f.write(qr_bytes)