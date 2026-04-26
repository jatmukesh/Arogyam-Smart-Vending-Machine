# utils/ocr_inference.py

from typing import Dict, List


# ---------------- PRICE MAP ----------------

PRICE_MAP = {
    "crocin": 20, "paracetamol": 20,
    "ibuprofen": 25, "cetirizine": 15,
    "ondem": 35, "ondansetron": 35,
    "dompan": 30, "domperidone": 30,
    "azithromycin": 40, "dextromethorphan": 60,
    "pantoprazole": 30, "simethicone": 25,
    "ors": 18, "loperamide": 22,
    "lactulose": 80,
}


def get_price(brand: str, generic: str) -> int:
    key = brand.lower().split()[0]
    if key in PRICE_MAP:
        return PRICE_MAP[key]

    key2 = generic.lower().split()[0]
    return PRICE_MAP.get(key2, 30)


# ---------------- MAIN OCR PIPELINE ----------------

def run_ocr_pipeline(server_url: str,
                     no_camera: bool = False,
                     image_path: str = "") -> Dict:
    """
    Full OCR pipeline:
    - Check server
    - Capture image
    - Upload image
    - Process response → cart items

    Returns:
        {
            "success": bool,
            "cart_items": list,
            "error": str
        }
    """

    try:
        from client.camera import capture_image
        from client.uploader import check_server_health, upload_image

        # ---------- SERVER CHECK ----------
        if not check_server_health(server_url, timeout=5.0):
            return {
                "success": False,
                "error": "Server not reachable"
            }

        # ---------- IMAGE ----------
        if no_camera and image_path:
            img_path = image_path
        else:
            img_path = capture_image()

        # ---------- UPLOAD ----------
        result = upload_image(img_path, server_url)

        if not result.success:
            return {
                "success": False,
                "error": result.error or "OCR failed"
            }

        # ---------- CONVERT TO CART ----------
        cart_items = []

        for med in result.medicines:
            price = get_price(med.brand, med.generic)

            cart_items.append({
                "name": med.brand,
                "price": price
            })

        return {
            "success": True,
            "cart_items": cart_items
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }