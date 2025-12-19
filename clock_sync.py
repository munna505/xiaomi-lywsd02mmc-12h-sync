import asyncio
import time
import struct
import logging
import os
import sys
from bleak import BleakScanner, BleakClient

# --- LOGGING CONFIG (FILE + TERMINAL) ---
log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, "clock_debug.log")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Clear existing handlers to avoid double logs
if logger.hasHandlers():
    logger.handlers.clear()

# 1. File Handler
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%A, %d-%m-%Y %I:%M:%S %p'))
logger.addHandler(file_handler)

# 2. Stream Handler (Terminal)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%I:%M:%S %p'))
logger.addHandler(console_handler)

TIME_CHAR_UUID = "ebe0ccb7-7a0a-4b0c-8a1a-6ff2997da3a6"
DEVICE_NAME = "LYWSD02"

async def sync():
    try:
        # 30-45 seconds is much safer for low-energy (BLE) sleep cycles
        logging.info(f"Starting deep scan (60s timeout) for {DEVICE_NAME}...")
        
        device = await BleakScanner.find_device_by_filter(
            lambda d, ad: DEVICE_NAME in (d.name or ""), 
            timeout=60.0
        )
        
        if not device:
            logging.error("FAILED: Device not found after 45 seconds. The clock is deep sleeping or blocked.")
            return

        logging.info(f"Found {DEVICE_NAME} ({device.address}). Connecting...")
        
        async with BleakClient(device, timeout=20.0) as client:
            now = time.localtime()
            # Your local timezone offset
            MY_TZ = 6
            # Logic: PM/Midnight block = -6 | AM block = +6
            tz_offset = -MY_TZ if (now.tm_hour >= 13 or now.tm_hour == 0) else MY_TZ
            
            payload = struct.pack('<ib', int(time.time()), tz_offset)
            
            # Send and wait for acknowledgment
            await client.write_gatt_char(TIME_CHAR_UUID, payload, response=True)
            
            # Keep alive so the clock hardware can finish writing to its internal memory
            await asyncio.sleep(3)
            
            logging.info(f"SUCCESS: Clock synced to {now.tm_hour:02d}:{now.tm_min:02d} (Offset {tz_offset})")

    except Exception as e:
        logging.error(f"CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    asyncio.run(sync())