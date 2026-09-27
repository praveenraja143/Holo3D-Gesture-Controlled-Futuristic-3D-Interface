# 🌌 Holo3D — Gesture-Controlled Futuristic 3D Holographic Interface

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-orange.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-green.svg)](https://mediapipe.dev/)
[![Author](https://img.shields.io/badge/Author-Praveen%20Raja-cyan.svg)](https://github.com/praveenraja143)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Holo3D** is a next-generation real-time augmented computer vision interface inspired by Iron Man's JARVIS holographic workstation. Using your webcam and MediaPipe hand tracking, you can interact with virtual 3D objects in free air with natural hand gestures — **and dynamically search or generate ANY object or image from the web into a live 3D hologram!**

---

## ⚡ What Makes Holo3D Special?

- 🔍 **Dynamic Hologram Search & AI Projection**:
  - Don't settle for a single object. Press **`S`** to type **any object** (e.g., *Iron Man, Planet Earth, Ferrari, Cyberpunk Katana, Dragon, T-Rex*).
  - Automatically fetches, removes background, applies holographic alpha-transparency, and projects it into 3D space with genuine perspective warping and depth layers!
- 🖐️ **Touchless 3D Gesture Manipulation**:
  - **Pinch & Drag**: Move the hologram freely in 3D space.
  - **Open Palm**: Rotate on all 3 axes (Pitch, Yaw, Roll) by tilting and moving your hand.
  - **Two Hands**: Dynamic zoom in / zoom out by adjusting distance between your hands.
  - **Fist**: Cloak / stealth-hide the hologram instantly.
- 📐 **Procedural 3D Hologram Library Built-in**:
  - `[1]` **Cyber Supercar**: High-polygon procedural vehicle wireframe with glass canopy, intakes, and aerodynamic diffusers.
  - `[2]` **Planet Earth Globe**: Rotating 3D sphere with latitude and longitude coordinate lines and glowing equator.
  - `[3]` **Iron Man Arc Reactor**: Multi-tier rotating energy coils, core power triangle, and reactor glow.
  - `[4]` **Sci-Fi Drone Fighter**: Aerodynamic fuselage, quad rotor arms, and thrusters.
  - `[5]` **4D Tesseract Hypercube**: Dual-nested inner and outer cubes with 4D cross-connecting struts.
  - `[6]` **Custom Image Hologram**: Your dynamically searched web/AI hologram!
- 🔮 **Cinematic Sci-Fi Aesthetics**:
  - Hologram scanlines & edge glow shaders.
  - 3D bounding wireframe box with glowing cybernetic corner brackets.
  - Rotating concentric arc-reactor projector rings at the base.
  - Ambient glowing particle field.
  - Futuristic glassmorphism telemetry HUD with real-time FPS, coordinates, scale, and gesture tracking.

---

## 🎮 Controls & Gestures

### 🖐️ Hand Gestures

| Gesture | Action | Description |
|---|---|---|
| **🤏 Pinch & Drag** | Move Object | Pinch thumb and index finger to grab and position the hologram in free air. |
| **✋ Open Palm** | 3D Rotation | Move hand horizontally/vertically or tilt wrist to rotate the hologram in 3D (Pitch, Yaw, Roll). |
| **👐 Two Hands** | Dynamic Zoom | Bring two hands into view and spread or close them to scale the hologram seamlessly. |
| **✊ Closed Fist** | Stealth Cloak | Make a fist to instantly hide the hologram; open hand to reveal it again. |

### ⌨️ Keyboard Shortcuts

| Key | Function |
|---|---|
| **`S`** or **`SPACE`** | **Open Hologram Search Bar** (Type any query, e.g., *Iron Man, Earth, Ferrari*) |
| **`1`** | Load **3D Cyber Supercar** |
| **`2`** | Load **3D Planet Earth Globe** |
| **`3`** | Load **3D Iron Man Arc Reactor** |
| **`4`** | Load **3D Sci-Fi Drone Fighter** |
| **`5`** | Load **3D 4D Tesseract Hypercube** |
| **`6`** | Switch back to **Custom Searched Hologram** |
| **`+` / `-`** | Manual Zoom In / Zoom Out |
| **`R`** | Reset Transform (Position, Rotation & Scale to Default) |
| **`V`** | Toggle Hologram Visibility (Show / Hide) |
| **`Q`** | Quit Application |

---

## 🏗️ Architecture & Pipeline

```text
                     ┌────────────────────────┐
                     │   📷 WEBCAM VIDEO FEED │
                     └───────────┬────────────┘
                                 │
                     ┌───────────▼────────────┐
                     │  MediaPipe Hand Tracking│
                     │   (21 3D Landmarks)    │
                     └───────────┬────────────┘
                                 │
                     ┌───────────▼────────────┐
                     │   Gesture Controller   │
                     │  Pinch / Palm / Zoom   │
                     └───────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
┌───────▼────────┐      ┌────────▼────────┐      ┌────────▼────────┐
│  Procedural    │      │ Dynamic Image   │      │ 3D Perspective  │
│  3D Meshes     │      │ Search Engine   │      │ Projection      │
│ (Car/Globe/Arc)│      │(Web/AI Cutouts) │      │(Matrix Rotation)│
└───────┬────────┘      └────────┬────────┘      └────────┬────────┘
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 │
                     ┌───────────▼────────────┐
                     │ Holographic AR Renderer│
                     │ Glow, Scanlines, Rings │
                     └───────────┬────────────┘
                                 │
                     ┌───────────▼────────────┐
                     │   Futuristic HUD UI    │
                     └────────────────────────┘
```

---

## 🚀 Quick Start Installation

### 1. Clone the Repository
```bash
git clone https://github.com/praveenraja143/Holo3D-Gesture-Controlled-Futuristic-3D-Interface.git
cd Holo3D-Gesture-Controlled-Futuristic-3D-Interface
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python main.py
```

---

## 👨‍💻 Author

**Praveen Raja**  
- GitHub: [@praveenraja143](https://github.com/praveenraja143)

---

## 📜 License

This project is licensed under the MIT License.
