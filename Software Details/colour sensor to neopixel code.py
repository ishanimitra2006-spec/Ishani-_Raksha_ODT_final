from machine import Pin
import time
import neopixel

# ── Pin configuration ────────────────────────────────────────────
S0  = Pin(33, Pin.OUT)
S1  = Pin(5,  Pin.OUT)
S2  = Pin(19, Pin.OUT)
S3  = Pin(32, Pin.OUT)
OUT = Pin(18, Pin.IN)

NEO_PIN = Pin(21, Pin.OUT)
NUM_PIXELS = 16
np = neopixel.NeoPixel(NEO_PIN, NUM_PIXELS)

S0.value(1)
S1.value(0)

# ── Count pulses ─────────────────────────────────────────────────
def read_frequency(duration_ms=150):
    count = 0
    end = time.ticks_add(time.ticks_ms(), duration_ms)
    last = OUT.value()
    while time.ticks_diff(end, time.ticks_ms()) > 0:
        current = OUT.value()
        if last == 1 and current == 0:
            count += 1
        last = current
    return count

# ── Stable averaged reading ───────────────────────────────────────
def stable_read(samples=5):
    r_total = g_total = b_total = 0
    for _ in range(samples):
        S2.value(0); S3.value(0)
        time.sleep_ms(10)
        r_total += read_frequency()

        S2.value(1); S3.value(1)
        time.sleep_ms(10)
        g_total += read_frequency()

        S2.value(0); S3.value(1)
        time.sleep_ms(10)
        b_total += read_frequency()

    return r_total // samples, g_total // samples, b_total // samples

# ── Calibration from YOUR sensor ─────────────────────────────────
R_MIN, R_MAX = 126, 1167
G_MIN, G_MAX = 120, 891
B_MIN, B_MAX = 164, 1120

def map_value(val, in_min, in_max):
    mapped = int((val - in_min) * 255 / (in_max - in_min))
    return max(0, min(255, mapped))

# ── Color name matcher ────────────────────────────────────────────
COLOR_MAP = [
    ("Red",     255,   0,   0),
    ("Green",     0, 255,   0),
    ("Blue",      0,   0, 255),
    ("Yellow",  255, 255,   0),
    ("Orange",  255, 140,   0),
    ("Purple",  148,   0, 211),
    ("Pink",    255, 105, 180),
    ("Cyan",      0, 255, 255),
    ("White",   255, 255, 255),
    ("Black",     0,   0,   0),
    ("Brown",   101,  67,  33),
]

def get_color_name(r, g, b):
    best_match = "Unknown"
    best_distance = float('inf')
    for name, cr, cg, cb in COLOR_MAP:
        distance = ((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2) ** 0.5
        if distance < best_distance:
            best_distance = distance
            best_match = name
    return best_match, int(best_distance)

# ── Set all 16 pixels ─────────────────────────────────────────────
def set_all(r, g, b):
    for i in range(NUM_PIXELS):
        np[i] = (r, g, b)
    np.write()

# ── Default color = brown on startup ─────────────────────────────
set_all(101, 67, 33)
print("Default color: Brown")

# ── Main loop ─────────────────────────────────────────────────────
current_r, current_g, current_b = 101, 67, 33
THRESHOLD = 12

while True:
    r_raw, g_raw, b_raw = stable_read(samples=5)

    r = map_value(r_raw, R_MIN, R_MAX)
    g = map_value(g_raw, G_MIN, G_MAX)
    b = map_value(b_raw, B_MIN, B_MAX)

    if (abs(r - current_r) > THRESHOLD or
        abs(g - current_g) > THRESHOLD or
        abs(b - current_b) > THRESHOLD):

        set_all(r, g, b)
        current_r, current_g, current_b = r, g, b

        name, distance = get_color_name(r, g, b)
        confidence = "High" if distance < 80 else "Medium" if distance < 150 else "Low"

        print("──────────────────────────")
        print("Color     : {}".format(name))
        print("RGB       : ({}, {}, {})".format(r, g, b))
        print("Confidence: {}".format(confidence))

    time.sleep_ms(300)