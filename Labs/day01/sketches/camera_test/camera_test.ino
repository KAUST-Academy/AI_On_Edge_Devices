// camera_test - take frames with the camera of the XIAO ESP32S3 Sense and
// print their size, the capture time, and the mean brightness
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense), FQBN esp32:esp32:XIAO_ESP32S3
// Core:      esp32 by Espressif Systems 3.3.12 (the camera driver esp_camera
//            is in the core)
// Libraries: none
// Build:     Tools > PSRAM > OPI PSRAM. The frame buffer is in the PSRAM.
//
// The test needs no Wi-Fi. Cover the lens with your hand: the mean
// brightness must decrease.
//
// Sources of the constants:
//   Pin numbers: camera_pins.h of the example CameraWebServer of the core,
//                model CAMERA_MODEL_XIAO_ESP32S3.
//   Camera settings: CameraWebServer.ino of the same example. The core is
//                by Espressif Systems (github.com/espressif/arduino-esp32,
//                LGPL-2.1).
//
// Credits: the camera test of the XIAOML Kit setup chapter of "Machine
// Learning Systems" (mlsysbook.ai, CC BY-NC-SA 4.0) uses that example. This
// sketch is a smaller test with the same pins and the same driver.

#include "esp_camera.h"

// Pins of the camera connector of the XIAO ESP32S3 Sense.
#define PWDN_GPIO_NUM  -1
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM  10
#define SIOD_GPIO_NUM  40
#define SIOC_GPIO_NUM  39
#define Y9_GPIO_NUM    48
#define Y8_GPIO_NUM    11
#define Y7_GPIO_NUM    12
#define Y6_GPIO_NUM    14
#define Y5_GPIO_NUM    16
#define Y4_GPIO_NUM    18
#define Y3_GPIO_NUM    17
#define Y2_GPIO_NUM    15
#define VSYNC_GPIO_NUM 38
#define HREF_GPIO_NUM  47
#define PCLK_GPIO_NUM  13

void stopWithMessage(const char* message) {
  Serial.println(message);
  while (true) {
    delay(1000);
  }
}

void setup() {
  Serial.begin(115200);
  // Wait for the Serial Monitor, but not for more than 3 seconds.
  const unsigned long start = millis();
  while (!Serial && millis() - start < 3000) {
    delay(10);
  }
  Serial.println("XIAOML Kit camera test");

  if (!psramFound()) {
    stopWithMessage("ERROR: PSRAM is not active. Set Tools > PSRAM > OPI PSRAM.");
  }

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  // One byte for each pixel: 320 x 240 = 76 800 bytes for one frame.
  config.frame_size = FRAMESIZE_QVGA;
  config.pixel_format = PIXFORMAT_GRAYSCALE;
  config.grab_mode = CAMERA_GRAB_LATEST;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 12;
  config.fb_count = 2;

  const esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("ERROR: camera init failed with code 0x%x\n", err);
    stopWithMessage("Check the camera cable and the PSRAM setting.");
  }
  Serial.println("Camera initialized");
  Serial.println("width,height,bytes,capture_ms,mean_brightness");
}

void loop() {
  const unsigned long start = micros();
  camera_fb_t* frame = esp_camera_fb_get();
  const unsigned long capture_us = micros() - start;
  if (frame == nullptr) {
    Serial.println("ERROR: no frame");
    delay(1000);
    return;
  }

  // Mean of all pixel values: 0 is black and 255 is white.
  uint32_t sum = 0;
  for (size_t i = 0; i < frame->len; i++) {
    sum += frame->buf[i];
  }
  const float mean = frame->len > 0 ? (float)sum / frame->len : 0.0f;

  Serial.printf("%u,%u,%u,%.1f,%.1f\n", (unsigned)frame->width,
                (unsigned)frame->height, (unsigned)frame->len,
                capture_us / 1000.0f, mean);

  esp_camera_fb_return(frame);
  delay(1000);
}
