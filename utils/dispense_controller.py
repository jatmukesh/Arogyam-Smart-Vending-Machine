# utils/dispense_controller.py

import time

try:
    import RPi.GPIO as GPIO
    HARDWARE_AVAILABLE = True
except ImportError:
    HARDWARE_AVAILABLE = False


# ---------------- MOTOR PIN CONFIG ----------------
# Each stepper uses 4 GPIO pins (IN1–IN4 of ULN2003)

STEPPER_PINS = {
    "Crocin":      [17, 18, 27, 22],
    "Cetirizine":  [5, 6, 13, 19],
    "Ondem":       [23, 24, 25, 8],
    "Dompan":      [16, 20, 21, 26],
}


# Map UI names → motor slots
REAL_MOTOR_MEDS = {
    "Crocin 650 mg": "Crocin",
    "Cetirizine 10 mg": "Cetirizine",
    "Ondem": "Ondem",
    "Dompan": "Dompan",
}


# ---------------- INDIVIDUAL SETTINGS ----------------
# Tune these for each medicine

STEPPER_SETTINGS = {
    "Crocin":     {"steps": 400, "delay": 0.002},
    "Cetirizine": {"steps": 350, "delay": 0.002},
    "Ondem":      {"steps": 450, "delay": 0.002},
    "Dompan":     {"steps": 300, "delay": 0.002},
}


# Half-step sequence (smooth rotation)
STEP_SEQUENCE = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1],
]


_gpio_initialized = False


# ---------------- SETUP ----------------

def setup_gpio():
    global _gpio_initialized

    if not HARDWARE_AVAILABLE or _gpio_initialized:
        return

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    for pins in STEPPER_PINS.values():
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

    _gpio_initialized = True


# ---------------- STEPPER CONTROL ----------------

def rotate_stepper(slot_name):
    """
    Rotate one stepper motor based on its configured steps & delay
    """

    if not HARDWARE_AVAILABLE:
        print(f"[SIMULATION] {slot_name} stepper running...")
        return

    setup_gpio()

    pins = STEPPER_PINS[slot_name]
    settings = STEPPER_SETTINGS[slot_name]

    steps = settings["steps"]
    delay = settings["delay"]

    print(f"[INFO] {slot_name} → Steps:{steps}, Delay:{delay}")

    for _ in range(steps):
        for step in STEP_SEQUENCE:
            for i in range(4):
                GPIO.output(pins[i], step[i])
            time.sleep(delay)

    # Turn off coils after movement (important!)
    for pin in pins:
        GPIO.output(pin, 0)

    time.sleep(0.3)


# ---------------- DISPENSE ----------------

def dispense_item(item_name, qty=1):
    slot_name = REAL_MOTOR_MEDS.get(item_name)

    if slot_name:
        for i in range(qty):
            print(f"[DISPENSE] {item_name} → unit {i+1}")
            rotate_stepper(slot_name)

        return f"{item_name}: stepper x{qty}"

    return f"{item_name}: not mapped"


def dispense_cart(cart_items):
    messages = []

    for item in cart_items:
        name = item["name"]
        qty = item.get("qty", 1)

        msg = dispense_item(name, qty)
        messages.append(msg)

    return messages