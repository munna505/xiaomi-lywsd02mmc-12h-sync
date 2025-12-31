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

if logger.hasHandlers():
    logger.handlers.clear()

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%A, %d-%m-%Y %I:%M:%S %p'))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%I:%M:%S %p'))
logger.addHandler(console_handler)

TIME_CHAR_UUID = "ebe0ccb7-7a0a-4b0c-8a1a-6ff2997da3a6"
DEVICE_NAME = "LYWSD02"
MAX_RETRIES = 3  # Number of times to attempt connection

async def sync():
    device = None
    # 1. SCAN PHASE
    try:
        logging.info(f"Starting deep scan (60s timeout) for {DEVICE_NAME}...")
        device = await BleakScanner.find_device_by_filter(
            lambda d, ad: DEVICE_NAME in (d.name or ""), 
            timeout=60.0
        )
    except Exception as e:
        logging.error(f"Scan failed: {e}")
        return

    if not device:
        logging.error("FAILED: Device not found after 60 seconds.")
        return

    # 2. CONNECT & WRITE PHASE (With Retry Logic)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"Attempt {attempt}/{MAX_RETRIES}: Connecting to {device.address}...")
            
            async with BleakClient(device, timeout=20.0) as client:
                if not client.is_connected:
                    raise Exception("Failed to establish connection handle.")

                logging.info(f"Connected! Syncing time...")
                
                now = time.localtime()
                MY_TZ = 6
                # Logic: PM/Midnight block = -6 | AM block = +6
                tz_offset = -MY_TZ if (now.tm_hour >= 13 or now.tm_hour == 0) else MY_TZ
                
                payload = struct.pack('<ib', int(time.time()), tz_offset)
                
                # Write and wait for response
                await client.write_gatt_char(TIME_CHAR_UUID, payload, response=True)
                
                # Small buffer for hardware to commit write
                await asyncio.sleep(2)
                
                logging.info(f"SUCCESS: Clock synced to {now.tm_hour:02d}:{now.tm_min:02d} (Offset {tz_offset})")
                return # Exit function on success

        except Exception as e:
            logging.warning(f"Attempt {attempt} failed with error: {str(e)}")
            if attempt < MAX_RETRIES:
                wait_time = 5
                logging.info(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                logging.error("CRITICAL ERROR: All connection retries exhausted.")

if __name__ == "__main__":
    asyncio.run(sync())