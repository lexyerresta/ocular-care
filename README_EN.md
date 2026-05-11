# OculusCare™ - Ocular Protection System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red.svg)
![Contributions welcome](https://img.shields.io/badge/Contributions-welcome-orange.svg)

*(Read this in other languages: **English** | [Bahasa Indonesia](README.md))*

<div align="center">
  <img src="assets/ocular_care.png" alt="OcularCare Dashboard" width="600"/>
</div>

**OculusCare™** is a clinical desktop utility specifically designed to prevent Computer Vision Syndrome (CVS) or Digital Eye Strain. This application operates based on the medically recommended **20-20-20 Protocol** globally recognized by eye care professionals.

## 🩺 Why Do You Need This?
Continuous screen exposure can cause eye muscle fatigue, dry eyes, and tension headaches. The 20-20-20 rule is the most recognized first-line medical intervention:
> *"Every 20 minutes spent looking at a screen, you should look at something 20 feet away for 20 seconds."*

## ✨ Key Features
- **Background Automation:** Runs seamlessly in the background without affecting your computer's performance.
- **Clinical Screen Override:** Automatically takes over your screen every 20 minutes to ensure you genuinely rest your eyes.
- **Smart Timer & Audio Cues:** Accurately counts down 20 seconds and plays an audio notification when the session concludes.
- **One-Click Installer:** Equipped with an Auto-Python Installer system that checks, downloads, and sets up all system requirements on new PCs automatically.

---

## 🚀 Installation Guide (For New PCs)

You can easily distribute this application to various PCs/Laptops in your office or home.

1. Copy the entire application directory to your target PC.
2. Open the folder.
3. Double-click the smart installation file: **`Install_AutoStart.bat`**.
4. The script will process the installation independently:
   - Checks System Requirements (Python Environment).
   - If the system does not meet the requirements, it will **download and install Python in the background** (requires an internet connection). *Note: If a Windows User Account Control (UAC) prompt appears, please click "Yes".*
   - Registers OculusCare™ into the Windows Startup Registry.
5. After the process is complete and a success confirmation appears, press any key to exit. OculusCare™ is now active and will always launch automatically on that computer!

---

## 💻 Daily Usage

- **Automatic Mode:** After the installation above, you don't need to do anything else. Every time the computer turns on, OculusCare™ will be on standby protecting your eyes.
- **Manual Mode:** If you just closed the application and want to restart it without rebooting the PC, simply double-click the **`OcularCareLauncher.bat`** file.

While the application is running, you will see a main control window (Dashboard). We recommend you **Minimize** this window (the minus button in the top right corner) so it doesn't block your workspace. The reminder system will continue to run perfectly in the background.

### Manual Dashboard Controls:
- **Pause Monitoring:** Use this function to temporarily suspend the 20-minute timer. Very useful if you are in the middle of a virtual presentation, playing competitive games, or other critical activities where your screen shouldn't be interrupted.
- **Start Relaxation Session:** If you feel eye strain (stinging/watery eyes) before the timer runs out, click this button to trigger a 20-second recovery session immediately.

---

## 🤝 Let's Contribute (Open Source Community)

This project is 100% Open Source and dedicated to the community. If you are a developer and have ideas to improve this application (e.g., adding custom UI settings, new sounds, or usage statistics), we highly welcome your **Pull Requests (PRs)**!

Please read the [Contributing Guide (CONTRIBUTING.md)](CONTRIBUTING.md) to learn how to submit code, or feel free to open **Issues** if you find bugs or want to discuss new features.

---

## 🗑️ Uninstallation Procedure

If you wish to disable this application so it no longer starts automatically:
1. Open the OculusCare™ installation folder.
2. Double-click the **`Uninstall_AutoStart.bat`** file.
3. The Startup Routine will be successfully removed.
4. You can safely delete the OculusCare™ folder from your computer if it is no longer used.

---

## 💡 Acknowledgments

The core concept and idea of this medical utility were entirely conceived by **Lexy Erresta**. During its development, this project was supported by **Antigravity** (Google DeepMind AI) acting as a pair-programming coding assistant.

---

## 📜 License & Copyright

© 2026 **Lexy Erresta**. All Rights Reserved.
This application is protected by copyright. The project is distributed under the MIT License (see the `LICENSE` file for details).

*Developed with medical awareness in mind. Protect your vision today for a clearer tomorrow.*
