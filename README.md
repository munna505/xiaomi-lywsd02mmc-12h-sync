# Xiaomi LYWSD02MMC 12-Hour Sync 🕰️

A lightweight macOS background automation to sync the **Xiaomi Temperature and Humidity Monitor Clock (LYWSD02MMC)** and force it into a 12-hour display format using a dynamic timezone offset "dodge."

---

## 📖 The Problem

The **Xiaomi LYWSD02MMC** is a beautiful e-ink clock, but it natively only supports a 24-hour military time format (e.g., it shows `13:00` instead of `01:00`). While Xiaomi's website claims it has a 12-hour format, there are actually two slightly different versions with the exact same model number.

One version does **not** support the 12-hour toggle in the Mi Home app. If you own that version, you are usually stuck with 24-hour time.

## 💡 The "Dodge" Logic

This script performs a **Hybrid Sync**. It sends the exact current time from your Mac but intentionally "lies" to the clock about the timezone offset based on the time of day:

* **Morning Block (1:00 AM – 12:59 PM):** Syncs normally using a `+6` offset. The clock shows `10:00`.
* **Afternoon Block (1:00 PM – 12:59 AM):** Syncs using a `-6` offset. The clock calculates `UTC Time + (-6)` and displays `01:00` instead of `13:00`.

**[You can set your own timezone in MY_TZ variable in clock_sync.py]**

---

## 🛠️ Features

* **Deep Scan (60s):** Patiently scans to wake up low-energy (BLE) sensors from their sleep cycle.
* **macOS Native:** Uses `launchd` for 0% idle CPU usage.
* **Locked-Screen Support:** Works while your Mac is locked (as long as the machine is awake).
* **Auto-Catchup:** If your Mac is off during a scheduled trigger, it will sync immediately upon wake-up.

---

## 🚀 Installation (macOS)

1. **Clone & Setup Environment**
   ```bash
   git clone https://github.com/munna505/xiaomi-lywsd02mmc-12h-sync
   cd xiaomi-lywsd02-12h-sync
   python3 -m venv venv
   source venv/bin/activate
   pip install bleak
   ```

2. **Configure the Automation**
   - Open `com.munna.clock_sync.plist`.
   - Replace the placeholder paths with the absolute path to your project folder (e.g., `/Users/YOUR_NAME/projects/...`).
   - Move the file to your LaunchAgents folder:
     ```bash
     cp com.munna.clock_sync.plist ~/Library/LaunchAgents/
     ```

3. **Load & Fast Test**
   - You don't need to wait until 1:00 PM to see the magic. Load the service and trigger it manually to test:
     ```bash
     # Load the service
     launchctl load ~/Library/LaunchAgents/com.munna.clock_sync.plist

     # Test instantly (Forces a sync right now)
     launchctl kickstart -k gui/$(id -u)/com.munna.clock_sync
     ```

## 📊 Monitoring & Logs

The script maintains a detailed history in your project folder:

- **Python Log:** `tail -f clock_debug.log` (Success/fail timestamps and connection info).
- **System Errors:** `cat system_errors.log` (Troubleshooting if Python fails to start).

## 🐧 Windows & Linux Support

The core `clock_sync.py` is cross-platform.

- **Windows:** Use Task Scheduler to run `python.exe` with the script path as an argument. Ensure "Run only when user is logged on" is checked to allow the script access to the Bluetooth radio.
- **Linux:** Use a systemd timer. Ensure your user is in the bluetooth group (`sudo usermod -aG bluetooth $USER`).

## 👤 Author

Munna

GitHub: [@munna505](https://github.com/munna505)

Feel free to star this repo if it helped you fix your clock!
