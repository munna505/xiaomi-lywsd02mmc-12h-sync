# Xiaomi LYWSD02 12-Hour Sync 🕰️

A lightweight macOS background automation to sync the **Xiaomi Temperature and Humidity Monitor Clock (LYWSD02MMC)** and force it into a 12-hour display format using a dynamic timezone offset "dodge."

---

## 📖 The Problem

The **Xiaomi LYWSD02MMC** is a beautiful e-ink clock, but it natively only supports a 24-hour military time format (e.g., it shows `13:00` instead of `01:00`). While Xiaomi’s website claims it has a 12-hour format, there are actually two slightly different versions with the exact same model number. 

One version does **not** support the 12-hour toggle in the Mi Home app. If you own that version, you are usually stuck with 24-hour time.

## 💡 The "Dodge" Logic

This script performs a **Hybrid Sync**. It sends the exact current time from your Mac but intentionally "lies" to the clock about the timezone offset based on the time of day:

* **Morning Block (1:00 AM – 12:59 PM):** Syncs normally using a `+6` offset. The clock shows `10:00`.
* **Afternoon Block (1:00 PM – 12:59 AM):** Syncs using a `-6` offset. The clock calculates `UTC Time + (-6)` and displays `01:00` instead of `13:00`.

---

## 🛠️ Features

* **Deep Scan (60s):** Patiently scans to wake up low-energy (BLE) sensors from their sleep cycle.
* **macOS Native:** Uses `launchd` for 0% idle CPU usage.
* **Locked-Screen Support:** Works while your Mac is locked (as long as the machine is awake).
* **Auto-Catchup:** If your Mac is off during a scheduled trigger, it will sync immediately upon wake-up.

---

## 🚀 Installation (macOS)

### 1. Clone & Setup Environment
```bash
git clone [https://github.com/munna505/xiaomi-lywsd02mmc-12h-sync](https://github.com/munna505/xiaomi-lywsd02mmc-12h-sync)
cd xiaomi-lywsd02-12h-sync
python3 -m venv venv
source venv/bin/activate
pip install bleak
