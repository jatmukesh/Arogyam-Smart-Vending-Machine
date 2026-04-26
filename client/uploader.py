"""
client/uploader.py
==================
Uploads a prescription image to the laptop OCR server and returns the
parsed medicine list.

Usage (standalone test):
    python client/uploader.py --image path/to/prescription.jpg --server http://192.168.1.10:5000
"""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

DEFAULT_TIMEOUT = 30       # seconds per attempt
MAX_RETRIES = 3
RETRY_DELAY = 2.0          # seconds between retries


@dataclass
class MedicineEntry:
    brand: str
    generic: str
    dosage: Optional[str] = None
    duration_days: Optional[int] = None

    def __str__(self) -> str:
        parts = [f"{self.brand} ({self.generic})"]
        if self.dosage:
            parts.append(self.dosage)
        if self.duration_days:
            parts.append(f"× {self.duration_days} days")
        return " — ".join(parts)


@dataclass
class OCRResult:
    success: bool
    medicines: List[MedicineEntry] = field(default_factory=list)
    raw_ocr_lines: List[str] = field(default_factory=list)
    doctor_id: Optional[int] = None
    processing_time_ms: Optional[int] = None
    error: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "OCRResult":
        medicines = [
            MedicineEntry(
                brand=m.get("brand", ""),
                generic=m.get("generic", ""),
                dosage=m.get("dosage"),
                duration_days=m.get("duration_days"),
            )
            for m in data.get("medicines", [])
        ]
        return OCRResult(
            success=data.get("status") == "success",
            medicines=medicines,
            raw_ocr_lines=data.get("raw_ocr_lines", []),
            doctor_id=data.get("doctor_id"),
            processing_time_ms=data.get("processing_time_ms"),
            error=data.get("error"),
        )


def check_server_health(server_url: str, timeout: float = 5.0) -> bool:
    """Returns True if the server is reachable and pipeline is ready."""
    try:
        resp = requests.get(f"{server_url}/health", timeout=timeout)
        data = resp.json()
        return data.get("status") == "ok"
    except Exception as e:
        print(f"[uploader] Health check failed: {e}")
        return False


def upload_image(image_path: str, server_url: str) -> OCRResult:
    """
    Send the image to the server's /ocr endpoint.
    Retries up to MAX_RETRIES times on network/server errors.
    Returns an OCRResult (success or failure).
    """
    path = Path(image_path)
    if not path.exists():
        return OCRResult(success=False, error=f"Image file not found: {image_path}")

    url = f"{server_url.rstrip('/')}/ocr"
    last_error = "Unknown error"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[uploader] Sending image to {url} (attempt {attempt}/{MAX_RETRIES})…")
            with open(path, "rb") as f:
                files = {"image": (path.name, f, "image/jpeg")}
                resp = requests.post(url, files=files, timeout=DEFAULT_TIMEOUT)

            # Server returned a response (even an error response)
            try:
                data = resp.json()
            except json.JSONDecodeError:
                last_error = f"Server returned non-JSON response (HTTP {resp.status_code})"
                continue

            if resp.status_code == 200:
                result = OCRResult.from_dict(data)
                print(f"[uploader] Success — {len(result.medicines)} medicine(s) found "
                      f"in {result.processing_time_ms}ms")
                return result
            else:
                # 4xx / 5xx — server returned structured error JSON
                last_error = data.get("error", f"HTTP {resp.status_code}")
                print(f"[uploader] Server error: {last_error}")
                # Don't retry 4xx (client errors)
                if 400 <= resp.status_code < 500:
                    return OCRResult(success=False, error=last_error)

        except requests.exceptions.ConnectionError:
            last_error = f"Cannot connect to server at {url}. Is the server running?"
            print(f"[uploader] {last_error}")
        except requests.exceptions.Timeout:
            last_error = f"Request timed out after {DEFAULT_TIMEOUT}s."
            print(f"[uploader] {last_error}")
        except Exception as e:
            last_error = str(e)
            print(f"[uploader] Unexpected error: {e}")

        if attempt < MAX_RETRIES:
            print(f"[uploader] Retrying in {RETRY_DELAY}s…")
            time.sleep(RETRY_DELAY)

    return OCRResult(success=False, error=last_error)


# ---------------------------------------------------------------------------
# Standalone test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Test image upload to OCR server")
    ap.add_argument("--image", required=True, help="Path to prescription image")
    ap.add_argument("--server", default="http://localhost:5000", help="Server base URL")
    args = ap.parse_args()

    print(f"Checking server health at {args.server}…")
    if check_server_health(args.server):
        print("Server is healthy ✓")
    else:
        print("Server not reachable — check the laptop server is running.")

    result = upload_image(args.image, args.server)

    if result.success:
        print(f"\n✅ Detected {len(result.medicines)} medicine(s):")
        for m in result.medicines:
            print(f"  • {m}")
    else:
        print(f"\n❌ OCR failed: {result.error}")
