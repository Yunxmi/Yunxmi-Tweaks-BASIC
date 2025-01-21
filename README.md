

# 🚀 Yunxmi Tweaks

Welcome to **Yunxmi Tweaks**! 🎉 At just 15 years old, this is one of my biggest projects, and I’m super excited to help you make your phone *faster* and *smoother*! 🚀 Please follow each step carefully to avoid confusion.

---

## 🙌 Acknowledgments

A special thanks to my friend for inspiring the creation of this project! 💡

---

## 🗝️ Symbols Key

- 🔄 = Alternative command

---

## ❗ Important

**Do NOT skip any steps or sections!** Skipping steps could lead to issues or confusion.

---

# 🛠️ Part 1: Installation Guide

### 📱 Step 1: Install Termux or Acode

First, you’ll need to install **Termux** (recommended) or **Acode**. These tools will allow you to run the necessary commands for Yunxmi Tweaks.

---

### 📥 Step 2: Run the Commands in Termux

1. **Install and update Termux packages:**
   ```bash
   pkg install && pkg upgrade -y
   ```

2. **Navigate to your Yunxmi Tweaks folder:**
   ```bash
   cd /storage/emulated/0/YunxmiTweaks 🔄 cd /storage/emulated/0/Download/YunxmiTweaks
   ```
   (Paste the directory into your terminal. Need help? Join the Discord channel for support! 😉)

3. **Install Python 3:**
   ```bash
   pkg install python3
   ```

4. **Install pip (Python package manager):**
   ```bash
   pkg install python-pip
   ```

---

### 🧩 Step 3: Install Yunxmi Tweaks

1. **Grant execute permissions to the installation script:**
   ```bash
   chmod +x install.sh
   ```

2. **Run the installation script:**
   ```bash
   ./install.sh 🔄 bash install.sh
   ```

🎉 Congratulations! You’ve successfully installed all the required modules!

---

# 🔑 Part 2: The Key System

The **Key System** is a feature designed to support this project financially, allowing me to keep it free for everyone while offering extra features in the **premium version**. 💡

---

### ⚙️ Step 4: Complete the Key System

1. Open the **Yunxmi Tweaks** directory:
   ```bash
   cd /storage/emulated/0/YunxmiTweaks
   ```

2. Run the **Key System**:
   ```bash
   python3 boost.py
   ```

3. Complete the **5 checkpoints** (don’t worry, it’s quick and easy!).

---

# 🔧 Additional Commands

If you encounter any issues, try the following commands:

1. **Set up storage permissions for Termux:**
   ```bash
   termux-setup-storage
   ```

2. **Fix missing dependencies:**
   ```bash
   pkg install -y [dependency_name]
   ```

3. **Reinstall Yunxmi Tweaks:**
   ```bash
   ./install.sh or bash install.sh
   ```

4. **Install Android tools:**
   ```bash
   pkg install android-tools
   ```

---

## 💬 Need Help?

If you run into any issues, feel free to reach out through the Discord channel. The community and I are here to help!

---

## Download ADB and Execute It

This step might seem a bit tedious, but you’ll get used to it! First, to download ADB, execute the command below:

```bash
pkg install android-tools
```

Now, follow these steps:

1. **Pair your device with ADB:**
   ```bash
   adb pair <your-ip>:<pair-port>
   ```
   Replace `<your-ip>` and `<pair-port>` with the correct values.

2. **Connect to the device:**
   After pairing, connect to your device using:
   ```bash
   adb connect <your-ip>:<port>
   ```
   Make sure to use the IP and port from the connect step (not the pair section).

3. **Verify the connection:**
   Run:
   ```bash
   adb devices
   ```
   If your device shows up in the list, you're all set to go!
