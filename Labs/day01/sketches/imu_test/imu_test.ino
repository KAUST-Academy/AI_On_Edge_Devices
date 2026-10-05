// imu_test - read the accelerometer and the gyroscope of the XIAOML Kit
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense with the expansion board),
//            FQBN esp32:esp32:XIAO_ESP32S3
// Core:      esp32 by Espressif Systems 3.3.12
// Libraries: Seeed Arduino LSM6DS3 2.0.7
//
// Credits: XIAOML_Kit_code/imu_test/imu_test.ino of the repository
// XIAO-ESP32S3-Sense by Marcelo Rovai
// (github.com/Mjrovai/XIAO-ESP32S3-Sense, Apache-2.0).
// Changes: this comment, and the two lines that print the sensor range.
// The source prints 2 g and 250 dps. The library sets 16 g and 2000 dps
// (LSM6DS3.cpp, default settings), so the sketch prints those values.

#include <LSM6DS3.h>
#include <Wire.h>

// Create IMU object using I2C interface
// LSM6DS3TR-C sensor is located at I2C address 0x6A
LSM6DS3 myIMU(I2C_MODE, 0x6A);

// Variables to store sensor readings
float accelX, accelY, accelZ;  // Accelerometer values (g-force)
float gyroX, gyroY, gyroZ;     // Gyroscope values (degrees per second)

void setup() {
  // Initialize serial communication at 115200 baud rate
  Serial.begin(115200);
  
  // Wait for serial port to connect (useful for debugging)
  while (!Serial) {
    delay(10);
  }
  
  Serial.println("XIAOML Kit IMU Test");
  Serial.println("LSM6DS3TR-C 6-Axis IMU Sensor");
  Serial.println("=============================");
  
  // Initialize the IMU sensor
  if (myIMU.begin() != 0) {
    Serial.println("ERROR: IMU initialization failed!");
    Serial.println("Check connections and I2C address");
    while(1) {
      delay(1000); // Halt execution if IMU fails to initialize
    }
  } else {
    Serial.println("✓ IMU initialized successfully");
    Serial.println();
    
    // Print sensor information
    Serial.println("Sensor Information:");
    Serial.println("- Accelerometer range: ±16 g (default of the library)");
    Serial.println("- Gyroscope range: ±2000 dps (default of the library)");
    Serial.println("- Communication: I2C at address 0x6A");
    Serial.println();
    
    // Print data format explanation
    Serial.println("Data Format:");
    Serial.println("AccelX,AccelY,AccelZ,GyroX,GyroY,GyroZ");
    Serial.println("Units: g-force (m/s²), degrees/second");
    Serial.println();
    
    delay(2000); // Brief pause before starting measurements
  }
}

void loop() {
  // Read accelerometer data (in g-force units)
  accelX = myIMU.readFloatAccelX();
  accelY = myIMU.readFloatAccelY();
  accelZ = myIMU.readFloatAccelZ();
  
  // Read gyroscope data (in degrees per second)
  gyroX = myIMU.readFloatGyroX();
  gyroY = myIMU.readFloatGyroY();
  gyroZ = myIMU.readFloatGyroZ();
  
  // Print readable format to Serial Monitor
  Serial.print("Accelerometer (g): ");
  Serial.print("X="); Serial.print(accelX, 3);
  Serial.print(" Y="); Serial.print(accelY, 3);
  Serial.print(" Z="); Serial.print(accelZ, 3);
  
  Serial.print(" | Gyroscope (°/s): ");
  Serial.print("X="); Serial.print(gyroX, 2);
  Serial.print(" Y="); Serial.print(gyroY, 2);
  Serial.print(" Z="); Serial.print(gyroZ, 2);
  Serial.println();
  
  // Print CSV format for Serial Plotter (uncomment the line below)
  Serial.println(String(accelX) + "," + String(accelY) + "," + String(accelZ) + "," + String(gyroX) + "," + String(gyroY) + "," + String(gyroZ));
  
  // Update rate: 10 Hz (100ms delay)
  delay(100);
}
