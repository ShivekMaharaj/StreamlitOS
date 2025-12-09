# 🪟 StreamlitOS - Windows 11 in Python

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url-here.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)

> **A fully functional, stateful Windows 11 Operating System replica built entirely in Python using Streamlit.**

![Screenshot](https://github.com/ShivekMaharaj/StreamlitOS/assets/placeholder.png)
*(Note: Upload a screenshot of your app running to your repo issues or just drag it here to replace this line)*

## 🚀 Live Demo
**[Click here to try StreamlitOS Live](https://your-app-url-here.streamlit.app/)**

---

## 👨‍💻 About The Project

This project pushes the boundaries of what is possible with **Streamlit**. Usually used for data dashboards, I hijacked the component system to build a desktop environment with a working Window Manager, Taskbar, and stateful applications.

It uses a unique combination of **Python** (backend logic/state) and **HTML/CSS/JS Injection** (frontend rendering) to create draggable, resizable, and interactive windows that persist state across re-runs.

### ✨ Features
*   **Desktop Environment:** A draggable, resizable Window Manager system.
*   **Start Menu:** Functional search and pinned apps.
*   **Taskbar:** Dynamic app docking and clock.
*   **State Management:** Apps remember their history and window position.

### 📦 Included Apps
1.  **Terminal:** A stateful command line interface. Supports `cd`, `ls`, `mkdir`, `touch`, `echo`, `neofetch`, `matrix`, and more.
2.  **API Tester:** A robust "Postman-lite" tool to test REST APIs with method selection (GET, POST, etc.) and JSON formatting.
3.  **Calculator:** Fully functional standard calculator.
4.  **Notepad:** Simple text editor.
5.  **Calendar, Clock & Weather:** Utility widgets.

---

## 🛠️ Installation & Local Run

Want to run this on your machine?

```bash
# 1. Clone the repository
git clone https://github.com/ShivekMaharaj/StreamlitOS.git

# 2. Navigate to the directory
cd StreamlitOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the OS
streamlit run main.py
