#include <MPU6050_tockn.h>
#include <Wire.h>

MPU6050 mpu6050(Wire);

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu6050.begin();
  
  // Calibration: Keep the sensor flat and still during power-up!
  mpu6050.calcGyroOffsets(true);
}

void loop() {
  mpu6050.update();

  // We send the data in a CSV format: roll,pitch,yaw
  Serial.print(mpu6050.getAngleX());
  Serial.print(",");
  Serial.print(mpu6050.getAngleY());
  Serial.print(",");
  Serial.println(mpu6050.getAngleZ());

  delay(10); // High refresh rate for smooth visualization
}
