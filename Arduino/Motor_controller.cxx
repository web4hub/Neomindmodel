#include <Servo.h>

Servo leftMotor;
Servo rightMotor;

void setup() {
  leftMotor.attach(9);
  rightMotor.attach(10);
  Serial.begin(115200);
  
  // Initialize motors to stop position on boot
  stopMotors();
}

void loop() {
  if (Serial.available()) {
    String action = Serial.readStringUntil('\n');
    action.trim(); // Remove trailing newline/spaces

    if (action == "FORWARD") {
      moveForward();
    } else if (action == "LEFT") {
      turnLeft();
    } else if (action == "RIGHT") {
      turnRight();
    } else if (action == "STOP") {
      stopMotors();
    }
  }
}

void moveForward() {
  leftMotor.write(180);  
  rightMotor.write(0);   
}

void turnLeft() {
  leftMotor.write(90);   // Stop left motor
  rightMotor.write(0);   // Spin right motor forward
}

void turnRight() {
  leftMotor.write(180);  // Spin left motor forward
  rightMotor.write(90);  // Stop right motor
}

void stopMotors() {
  leftMotor.write(90);   // Neutral / Stop
  rightMotor.write(90);  // Neutral / Stop
}
