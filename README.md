## 🎥 Robotic Camera System (Arduino + Servo + Face Detection)

### 📖 Overview
This project presents a **Robotic Camera System** designed to track and follow human faces in real-time. The system integrates computer vision with embedded control by using a **ResNet-10 Deep Neural Network (DNN)** model for face detection and an **Arduino-controlled servo mechanism** for camera movement.

A webcam captures live video, which is processed using Python and OpenCV. Once a face is detected, its position is translated into control signals that are transmitted to the Arduino via serial communication. The Arduino then adjusts the **pan and tilt servo motors** to keep the subject centered within the frame.

The system operates over a local network, with communication handled through the host machine using an IP-based setup for video processing and control.

---

### ⚙️ Key Features
- Real-time face detection using DNN (ResNet-10 SSD)
- Intelligent pan-tilt camera tracking
- Serial communication between Python and Arduino
- Smooth and responsive servo-based motion control
- Integration of computer vision and embedded systems

---

### 🌐 Network Configuration
- Host Machine IP Address: `192.168.1.100` *(example — replace with your actual IP)*
- Communication via local network for video processing and control interface

---

### 🧠 Technologies Used
- Python (OpenCV, NumPy, PySerial)
- Arduino (Embedded C++)
- Deep Learning (ResNet-10 SSD)
- Serial Communication Protocol

---

### 🎯 Application
This system can be applied in:
- Smart surveillance systems
- Human-computer interaction setups
- Automated video recording
- Robotics and AI-based tracking systems

---
