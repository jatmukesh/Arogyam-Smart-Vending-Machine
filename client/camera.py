"""
client/camera.py
================
✔ Stable preview using picamera2 (NO V4L2 / GStreamer errors)
✔ High-quality capture using picamera2 / libcamera fallback
✔ Compatible with OCRScreen (start_preview, get_frame, stop_preview)
✔ Saves unique timestamp images
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────

CAPTURE_WIDTH = 1920
CAPTURE_HEIGHT = 1080
PREVIEW_WIDTH = 640
PREVIEW_HEIGHT = 480
SETTLE_TIME_SECS = 2.0

BASE_DIR = Path(__file__).resolve().parent.parent
SAVE_DIR = BASE_DIR / "captured_images"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# ── Picamera2 Globals ──────────────────────────────────────────────────

picam2 = None


# ── Utility ────────────────────────────────────────────────────────────

def _generate_file_path() -> str:
    timestamp = int(time.time() * 1000)
    return str(SAVE_DIR / f"prescription_{timestamp}.jpg")


# ── PREVIEW FUNCTIONS (FIXED) ──────────────────────────────────────────

def start_preview():
    global picam2

    try:
        from picamera2 import Picamera2

        picam2 = Picamera2()

        config = picam2.create_preview_configuration(
            main={"size": (PREVIEW_WIDTH, PREVIEW_HEIGHT)}
        )

        picam2.configure(config)
        picam2.start()

        time.sleep(1)  # allow camera to warm up

        print("[camera] Preview started (picamera2)")

    except Exception as e:
        print(f"[camera] Preview start failed: {e}")
        picam2 = None


def get_frame():
    global picam2

    if picam2 is None:
        return None

    try:
        frame = picam2.capture_array()

        if frame is None or frame.size == 0:
            return None

        return frame

    except Exception as e:
        print(f"[camera] Frame error: {e}")
        return None


def stop_preview():
    global picam2

    if picam2:
        try:
            picam2.stop()
            picam2.close()
        except Exception as e:
            print(f"[camera] Stop error: {e}")

        picam2 = None
        print("[camera] Preview stopped")


# ── AUTO CAPTURE (Placeholder for now) ─────────────────────────────────

def auto_capture_ready(frame) -> bool:
    """
    You can upgrade this later:
    - Blur detection
    - Edge detection
    - Stability check
    """
    return False  # keep manual for now


# ── CAPTURE FUNCTION ───────────────────────────────────────────────────

def capture_image(frame=None, manual=False, save_path: str | None = None) -> str:
    """
    Capture image.

    If frame is provided → save directly (fast preview capture)
    Else → use high-quality capture (picamera2/libcamera)
    """

    if save_path is None:
        save_path = _generate_file_path()

    Path(save_path).parent.mkdir(parents=True, exist_ok=True)

    # ✅ CASE 1: Save preview frame directly (FAST + STABLE)
    if frame is not None:
        try:
            import cv2
            cv2.imwrite(save_path, frame)
            print(f"[camera] Saved preview frame → {save_path}")
            return save_path
        except Exception as e:
            print(f"[camera] Frame save failed: {e}")

    # ── Method 1: picamera2 (BEST QUALITY) ─────────────────────────────
    try:
        from picamera2 import Picamera2

        cam = Picamera2()
        config = cam.create_still_configuration(
            main={"size": (CAPTURE_WIDTH, CAPTURE_HEIGHT)}
        )
        cam.configure(config)
        cam.start()

        time.sleep(SETTLE_TIME_SECS)

        cam.capture_file(save_path)

        cam.stop()
        cam.close()

        print(f"[camera] picamera2 capture → {save_path}")
        return save_path

    except ImportError:
        pass
    except Exception as e:
        print(f"[camera] picamera2 failed: {e}")

    # ── Method 2: libcamera fallback ───────────────────────────────────
    try:
        cmd = [
            "libcamera-still",
            "--output", save_path,
            "--width", str(CAPTURE_WIDTH),
            "--height", str(CAPTURE_HEIGHT),
            "--timeout", str(int(SETTLE_TIME_SECS * 1000)),
            "--nopreview",
            "--immediate",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)

        if result.returncode == 0 and Path(save_path).exists():
            print(f"[camera] libcamera capture → {save_path}")
            return save_path

        print(f"[camera] libcamera error: {result.stderr.strip()}")

    except Exception as e:
        print(f"[camera] libcamera failed: {e}")

    # ── Method 3: OpenCV fallback (rarely used on Pi) ──────────────────
    try:
        import cv2

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise RuntimeError("OpenCV: camera not available")

        time.sleep(SETTLE_TIME_SECS)

        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            raise RuntimeError("OpenCV: frame capture failed")

        cv2.imwrite(save_path, frame)

        print(f"[camera] OpenCV fallback → {save_path}")
        return save_path

    except Exception as e:
        print(f"[camera] OpenCV failed: {e}")

    raise RuntimeError("All capture methods failed")


# ── TEST MODE ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    start_preview()

    import cv2

    while True:
        frame = get_frame()

        if frame is not None:
            cv2.imshow("Preview", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    stop_preview()
    cv2.destroyAllWindows()