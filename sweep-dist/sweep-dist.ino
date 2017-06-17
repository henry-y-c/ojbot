#include <Wire.h>
#include <LIDARLite.h>
#include <Servo.h>

LIDARLite lidar;
Servo tilt;
Servo pan;

const int PAN_PORT = 9;
const int PAN_MIN = 0;
const int PAN_MAX = 180;
const int PAN_INC = 2;

const int TILT_PORT = 10;
const int TILT_MIN = 5;
const int TILT_MAX = 100;
const int TILT_INC = 2;

const int INIT_DELAY = 1000;
const int SWEEP_DELAY = 15;

int panAngle = PAN_MIN;
int tiltAngle = TILT_MIN;
bool isForwardPan = true;

void setup() {
  Serial.begin(115200);
  
  pan.attach(PAN_PORT);
  pan.write(panAngle);
  
  tilt.attach(TILT_PORT);
  tilt.write(tiltAngle);

  lidar.begin(0, true);
  lidar.configure(0);
  
  delay(INIT_DELAY);
}

void loop() {
  double distance = lidar.distance();
  Serial.println(String(panAngle) + "," + String(tiltAngle) + "," + String(distance));
  moveServo();
}

void moveServo() {
  if (tiltAngle > TILT_MAX) {
    return;
  }
  
  if (isForwardPan) {
    panAngle += PAN_INC;
    if (panAngle >= PAN_MAX) {
      panAngle = PAN_MAX;
      isForwardPan = false;
      tiltAngle += TILT_INC;
    }
  } else {
    panAngle -= PAN_INC;
    if (panAngle <= PAN_MIN) {
      panAngle = PAN_MIN;
      isForwardPan = true;
      tiltAngle += TILT_INC;
    }
  }
  
  pan.write(panAngle);
  tilt.write(tiltAngle);
  delay(SWEEP_DELAY);
}
