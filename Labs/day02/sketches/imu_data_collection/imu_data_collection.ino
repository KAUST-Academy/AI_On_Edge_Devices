// imu_data_collection.ino - send IMU samples to the serial port at 50 Hz
//
// Day 2 lab, fallback for Part B: use this sketch if MicroPython does not
// work on your kit. The sketch prints the same lines as
// board/imu_stream.py, so host/check_rate.py and host/logger.py work with
// no change.
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense with the expansion board)
// FQBN:      esp32:esp32:XIAO_ESP32S3
// Core:      esp32 by Espressif Systems 3.3.12
// Library:   Seeed Arduino LSM6DS3 2.0.7
// Serial:    115200 baud
//
// Output: one CSV line for each sample.
//   n      sample number, starts at 0
//   t_us   time since the start, in microseconds
//   ax..az acceleration in g
//   gx..gz angular rate in degrees per second

#include <LSM6DS3.h>
#include <Wire.h>

#define FREQUENCY_HZ 50
#define PERIOD_US (1000000UL / FREQUENCY_HZ)

LSM6DS3 myIMU(I2C_MODE, 0x6A);

static uint32_t n = 0;              // sample number
static uint64_t elapsed_us = 0;     // time since the start
static uint32_t last_us = 0;
static uint32_t deadline_us = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  if (myIMU.begin() != 0) {
    Serial.println("# ERROR: IMU initialization failed!");
    while (1) delay(1000);
  }

  Serial.println("n,t_us,ax,ay,az,gx,gy,gz");
  last_us = micros();
  deadline_us = last_us;
}

void loop() {
  uint32_t now = micros();
  if ((int32_t)(now - deadline_us) < 0) {
    return;                          // the deadline is in the future
  }

  // The next deadline does not depend on the time that the read and the
  // print need, so the rate does not drift.
  deadline_us += PERIOD_US;
  if ((int32_t)(now - deadline_us) > 0) {
    deadline_us = now + PERIOD_US;   // the loop is too slow: new time base
  }

  elapsed_us += (uint32_t)(now - last_us);
  last_us = now;

  // Read accelerometer data (in g-force)
  float ax = myIMU.readFloatAccelX();
  float ay = myIMU.readFloatAccelY();
  float az = myIMU.readFloatAccelZ();

  // Read gyroscope data (in degrees per second)
  float gx = myIMU.readFloatGyroX();
  float gy = myIMU.readFloatGyroY();
  float gz = myIMU.readFloatGyroZ();

  Serial.print(n);
  Serial.print(",");
  Serial.print(elapsed_us);
  Serial.print(",");
  Serial.print(ax, 4);
  Serial.print(",");
  Serial.print(ay, 4);
  Serial.print(",");
  Serial.print(az, 4);
  Serial.print(",");
  Serial.print(gx, 2);
  Serial.print(",");
  Serial.print(gy, 2);
  Serial.print(",");
  Serial.println(gz, 2);
  n++;
}
