# PushToUptimeKuma - Home Assistant Integration

[![Version](https://img.shields.io/github/v/release/UnoSite/PushToUptimeKuma?label=version&style=for-the-badge&labelColor=333333&color=cad401)](https://github.com/UnoSite/PushToUptimeKuma/releases/latest)
[![Last Commit](https://img.shields.io/github/last-commit/UnoSite/PushToUptimeKuma?style=for-the-badge&labelColor=333333&color=cad401)](https://github.com/UnoSite/PushToUptimeKuma/commits/main/)
[![License](https://img.shields.io/github/license/UnoSite/PushToUptimeKuma?style=for-the-badge&labelColor=333333&color=cad401)](https://github.com/UnoSite/PushToUptimeKuma/blob/main/LICENSE.md)
[![Code Size](https://img.shields.io/github/languages/code-size/UnoSite/PushToUptimeKuma?style=for-the-badge&labelColor=333333&color=cad401)](#)
[![Stars](https://img.shields.io/github/stars/UnoSite/PushToUptimeKuma?style=for-the-badge&labelColor=333333&color=cad401)](#)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/UnoSite/PushToUptimeKuma/total?style=for-the-badge&labelColor=333333&color=cad401)](#)

![Logo](https://github.com/UnoSite/PushToUptimeKuma/blob/main/logo.png)

[![Sponsor Github](https://img.shields.io/badge/Sponsor-Github-000?style=for-the-badge&logo=githubsponsors&labelColor=333333&color=cad401&logoColor=EA4AAA)](https://github.com/sponsors/UnoSite)\
[![Sponsor Buy Me a Coffee](https://img.shields.io/badge/Sponsor-Buy%20me%20a%20coffee-000?style=for-the-badge&logo=buymeacoffee&labelColor=333333&color=cad401&logoColor=FFDD00)](https://buymeacoffee.com/UnoSite)\
[![Sponsor PayPal.Me](https://img.shields.io/badge/Sponsor-paypal.me-000?style=for-the-badge&logo=paypal&labelColor=333333&color=cad401&logoColor=002991)](https://paypal.me/UnoSite)

---

# 📌 Overview

Home Assistant integration for sending periodic push requests to [Uptime Kuma](https://github.com/louislam/uptime-kuma), with sensors for last call and interval.

---

## 🚀 Features

- Setup via Home Assistant UI (Config Flow)  
- Supports multiple instances (one device per push URL)  
- Choose interval from **20 seconds up to 24 hours**  
- Each device provides sensors for:  
  - **Last called** – timestamp of the last successful push  
  - **Call interval** – interval in seconds + human-readable format  

---

## 📥 Installation

### **1. Manual Installation**
1. **Download the latest release** from the [GitHub releases](https://github.com/UnoSite/PushToUptimeKuma/releases).
2. **Copy the `push_to_uptime_kuma` folder** into your Home Assistant `custom_components` directory.
3. **Restart Home Assistant.**
4. **Add the integration:**
   - Navigate to **Settings > Devices & Services > Integrations**.
   - Click **Add Integration** and search for **Push To Uptime Kuma**.
  
### **2. HACS Installation (Recommended)**
1. Add this repository as a **custom repository** in [HACS](https://hacs.xyz/).
2. Search for **Push To Uptime Kuma** in HACS and install the integration.
3. Restart Home Assistant.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=UnoSite&repository=PushToUptimeKuma&category=Integration)

---

## ⚙️ Configuration

1. Go to **Settings > Devices & Services > Add Integration**.  
2. Search for **Push To Uptime Kuma**.  
3. Enter your **Uptime Kuma push URL**.  
4. Select the **interval** (20s – 24h).  
5. Save – a device will be created automatically with sensors.  

---

## 📡 Sensors

| Entity ID                                    | Name          | Description                                  |
|----------------------------------------------|---------------|----------------------------------------------|
| `sensor.<domain>_last_called`                | Last called   | Timestamp of the last successful push        |
| `sensor.<domain>_call_interval`              | Call interval | Interval in seconds (+ human-readable attr.) |

- All entities are grouped under a single device, named after the **domain** of your Uptime Kuma URL (e.g. `status.unosite.dk`).  

---

## 🔧 Reconfiguration

You can reconfigure the integration at any time:  
- Open **Settings > Devices & Services > Push To Uptime Kuma**  
- Click **Options** to change the interval without removing the integration.  

---

## 📋 Example Dashboard Card (Lovelace)

```yaml
type: entities
title: Uptime Kuma Monitor
entities:
  - entity: sensor.status_unosite_dk_last_called
  - entity: sensor.status_unosite_dk_call_interval
```

---

## ⁉️ Issues & Support

If you encounter any issues or have feature requests, please open an issue on GitHub:

[![ Badge](https://img.shields.io/badge/Report-issues-E00000?style=for-the-badge)](https://github.com/UnoSite/PushToUptimeKuma/issues)  

---

## 📜 License

This integration is licensed under the MIT License.
