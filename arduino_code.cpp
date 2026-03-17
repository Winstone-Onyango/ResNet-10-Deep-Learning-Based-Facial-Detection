// Arduino code to receive coordinates and control servos
#include <Servo.h>

Servo panServo;   // Horizontal (X-axis) 
Servo tiltServo;  // Vertical (Y-axis)

int panAngle = 90;   // Start at center
int tiltAngle = 90;

void setup() {
  Serial.begin(9600);
  panServo.attach(9);   // Pan servo on pin 9
  tiltServo.attach(10); // Tilt servo on pin 10
  
  panServo.write(panAngle);
  tiltServo.write(tiltAngle);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    
    // Parse "X:123,Y:-45"
    int xIndex = data.indexOf("X:");
    int yIndex = data.indexOf("Y:");
    
    if (xIndex != -1 && yIndex != -1) {
      int offsetX = data.substring(xIndex + 2, yIndex - 1).toInt();
      int offsetY = data.substring(yIndex + 2).toInt();
      
      // Convert offset to servo angles (adjust these values)
      int panAdjust = map(offsetX, -320, 320, -30, 30);
      int tiltAdjust = map(offsetY, -240, 240, -30, 30);
      
      panAngle = constrain(90 + panAdjust, 0, 180);
      tiltAngle = constrain(90 - tiltAdjust, 0, 180);  // Inverted for tilt
      
      panServo.write(panAngle);
      tiltServo.write(tiltAngle);
    }
  }
}
