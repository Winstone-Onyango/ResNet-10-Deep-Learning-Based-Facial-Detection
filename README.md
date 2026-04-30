<div align="center">

# 🎥 Robotic Camera System

### *AI-Powered Face Tracking with Pan-Tilt Servo Control*

[![Arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white)](https://arduino.cc)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![Deep Learning](https://img.shields.io/badge/ResNet--10-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)

</div>

---

## 🚀 How It Works

<table align="center">
  <tr>
    <td width="50%">
      <table>
        <tr><td>📷 <b>1</b></td><td>Webcam captures live video stream</td></tr>
        <tr><td>🧠 <b>2</b></td><td>ResNet-10 DNN detects faces in real-time</td></tr>
        <tr><td>📍 <b>3</b></td><td>Face position offset is calculated from frame center</td></tr>
        <tr><td>🔗 <b>4</b></td><td>Pan/tilt angles sent via <b>Serial Communication</b></td></tr>
        <tr><td>🎮 <b>5</b></td><td>Arduino drives servo motors to track the face</td></tr>
        <tr><td>🔁 <b>6</b></td><td>Loop repeats → <b>Smooth continuous tracking</b></td></tr>
      </table>
    </td>
    <td width="50%" align="center">
      <img src="https://media.giphy.com/media/3o7abB06u9bNzA8LC8/giphy.gif" width="100%">
    </td>
  </tr>
</table>

---

<p align="center">
  <img src="https://media.giphy.com/media/26tn33aiTi1jkl6H6/giphy.gif" width="45%" />
  <img src="https://media.giphy.com/media/xT9IgzoKnwFNmISR8/giphy.gif" width="45%" />
</p>

---

## 🎯 System Flow

```mermaid
graph LR
    A[Webcam] --> B[Face Detection]
    B --> C[Position Calc]
    C --> D[Serial TX]
    D --> E[Arduino]
    E --> F[Servo Motors]
    F --> A
