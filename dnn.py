import cv2
import numpy as np
import urllib.request
import os
import serial
import time

# URL of the IP camera stream
camera_url = "http://10.2.39.62:8080/video"

# Arduino Serial Configuration
ARDUINO_PORT = "/dev/ttyUSB0"  # Change to your Arduino port (Windows: "COM3", Linux: "/dev/ttyUSB0" or "/dev/ttyACM0")
BAUD_RATE = 9600

# Tracking parameters
DEAD_ZONE = 30  # Pixels - ignore small movements to reduce jitter
SMOOTHING_FACTOR = 0.3  # 0.0 to 1.0 - lower = smoother but slower response

# Model files
model_file = "res10_300x300_ssd_iter_140000.caffemodel"
config_file = "deploy.prototxt"
model_url = "https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel"
config_url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt"

def download_file(url, filename):
    """Download file if it doesn't exist"""
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        try:
            urllib.request.urlretrieve(url, filename)
            print(f"✓ {filename} downloaded successfully!")
        except Exception as e:
            print(f"✗ Error downloading {filename}: {e}")
            return False
    else:
        print(f"✓ {filename} already exists")
    return True

# Download and load model
print("Checking model files...")
if not download_file(config_url, config_file) or not download_file(model_url, model_file):
    exit()

print("\nLoading DNN face detection model...")
try:
    face_net = cv2.dnn.readNetFromCaffe(config_file, model_file)
    print("✓ DNN model loaded successfully!")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    exit()

# Initialize Arduino connection
print(f"\nConnecting to Arduino on {ARDUINO_PORT}...")
try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for Arduino to reset
    print("✓ Arduino connected successfully!")
except Exception as e:
    print(f"✗ Error connecting to Arduino: {e}")
    print("Running in SIMULATION mode (no Arduino commands will be sent)")
    arduino = None

# Initialize video capture
cap = cv2.VideoCapture(camera_url)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

print("Successfully connected to IP camera")
print("Press 'q' to quit\n")

# Tracking variables
frame_count = 0
skip_frames = 2
confidence_threshold = 0.6
resize_width = 640
smoothed_offset_x = 0
smoothed_offset_y = 0

def send_to_arduino(offset_x, offset_y):
    """Send offset coordinates to Arduino"""
    if arduino and arduino.is_open:
        try:
            # Format: "X:123,Y:-45\n"
            command = f"X:{offset_x},Y:{offset_y}\n"
            arduino.write(command.encode())
            print(f"→ Arduino: {command.strip()}")
        except Exception as e:
            print(f"Error sending to Arduino: {e}")
    else:
        print(f"[SIMULATION] Would send - X:{offset_x}, Y:{offset_y}")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to grab frame")
        break
    
    frame_count += 1
    original_h, original_w = frame.shape[:2]
    
    # Calculate frame center
    center_x = original_w // 2
    center_y = original_h // 2
    
    # Draw crosshair at center
    cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), (0, 255, 255), 2)
    cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), (0, 255, 255), 2)
    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 255), -1)
    
    # Skip frames for performance
    if frame_count % skip_frames != 0:
        cv2.imshow('Face Tracking System', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue
    
    # Resize for faster processing
    aspect_ratio = original_h / original_w
    resize_height = int(resize_width * aspect_ratio)
    resized_frame = cv2.resize(frame, (resize_width, resize_height))
    h, w = resized_frame.shape[:2]
    
    # Detect faces
    blob = cv2.dnn.blobFromImage(resized_frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_net.setInput(blob)
    
    try:
        detections = face_net.forward()
    except Exception as e:
        print(f"Error during detection: {e}")
        continue
    
    # Find the largest/most confident face
    best_face = None
    best_confidence = 0
    
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        if confidence > confidence_threshold and confidence > best_confidence:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x2, y2) = box.astype("int")
            
            # Scale back to original size
            scale_x = original_w / w
            scale_y = original_h / h
            
            x = int(max(0, x * scale_x))
            y = int(max(0, y * scale_y))
            x2 = int(min(original_w, x2 * scale_x))
            y2 = int(min(original_h, y2 * scale_y))
            
            best_face = (x, y, x2, y2)
            best_confidence = confidence
    
    # Process the best face
    if best_face:
        x, y, x2, y2 = best_face
        face_width = x2 - x
        face_height = y2 - y
        
        # Calculate face center
        face_center_x = x + face_width // 2
        face_center_y = y + face_height // 2
        
        # Calculate offset from frame center
        offset_x = face_center_x - center_x
        offset_y = face_center_y - center_y
        
        # Apply smoothing to reduce jitter
        smoothed_offset_x = int(smoothed_offset_x * (1 - SMOOTHING_FACTOR) + offset_x * SMOOTHING_FACTOR)
        smoothed_offset_y = int(smoothed_offset_y * (1 - SMOOTHING_FACTOR) + offset_y * SMOOTHING_FACTOR)
        
        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)
        
        # Draw face center point
        cv2.circle(frame, (face_center_x, face_center_y), 8, (255, 0, 0), -1)
        
        # Draw line from center to face
        cv2.line(frame, (center_x, center_y), (face_center_x, face_center_y), (255, 0, 255), 2)
        
        # Display offset values
        cv2.putText(frame, f'Offset X: {smoothed_offset_x}px', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f'Offset Y: {smoothed_offset_y}px', (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f'Confidence: {best_confidence:.1%}', (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Check if outside dead zone
        if abs(smoothed_offset_x) > DEAD_ZONE or abs(smoothed_offset_y) > DEAD_ZONE:
            # Send to Arduino
            send_to_arduino(smoothed_offset_x, smoothed_offset_y)
            cv2.putText(frame, 'TRACKING', (10, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        else:
            cv2.putText(frame, 'CENTERED', (10, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, 'NO FACE DETECTED', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.imshow('Face Tracking System', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
if arduino and arduino.is_open:
    arduino.close()
cap.release()
cv2.destroyAllWindows()
print("\nSystem closed.")
