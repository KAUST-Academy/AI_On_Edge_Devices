// xiao_mjpeg_stream - send the camera of the XIAOML Kit as an MJPEG stream
// over HTTP (Day 11 lab, Part D)
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense), FQBN esp32:esp32:XIAO_ESP32S3
// Core:      esp32 by Espressif Systems 3.3.12 (the camera driver esp_camera
//            and the HTTP server esp_http_server are in the core)
// Libraries: none
// Build:     Tools > PSRAM > OPI PSRAM. The frame buffer is in the PSRAM.
//
// Hardware status: not tested on hardware (prepared on 2026-10-03). The
// sketch compiles for the board.
//
// Use: set the Wi-Fi password below, upload, open the Serial Monitor at
// 115200 baud. The sketch prints the address of the stream, for example
// http://192.168.8.163/. Open it in a browser, or read it with
// mjpeg_rate.py and stream_detect.py of the lab. Each 5 seconds the sketch
// prints the frames that it sent and the mean size of a JPEG image.
//
// Credits: this sketch is the sketch Streeming_Video.ino of "XIAO ESP32S3
// Sense" by Marcelo Rovai (github.com/Mjrovai/XIAO-ESP32S3-Sense,
// Apache-2.0), which is based on the ESP32-CAM project of Rui Santos
// (RandomNerdTutorials.com). Its notice: "Permission is hereby granted, free
// of charge, to any person obtaining a copy of this software and associated
// documentation files. The above copyright notice and this permission notice
// shall be included in all copies or substantial portions of the Software."
// Pin numbers: camera_pins.h of the example CameraWebServer of the esp32
// core, model CAMERA_MODEL_XIAO_ESP32S3.
// Changes of this course (each one is in TEST_NOTES.md): the Wi-Fi name of
// the lab, the frame size VGA in place of UXGA, no endless wait for the
// Serial Monitor, the pins in this file, the new names of the two SCCB pins,
// the boundary before each part (the order of the example CameraWebServer),
// and the status line each 5 seconds.

#include <atomic>
#include "esp_camera.h"
#include <WiFi.h>
#include "esp_http_server.h"
#include "soc/soc.h"            // disable brownout problems
#include "soc/rtc_cntl_reg.h"   // disable brownout problems

// The network of the lab (Labs/hardware/HW-09). The instructor gives the
// password. arduino-cli can set both values with build options.
#ifndef WIFI_SSID
#define WIFI_SSID "edgeai-lab"
#endif
#ifndef WIFI_PASSWORD
#define WIFI_PASSWORD "change-me"
#endif

// Frame size and JPEG quality. Part D of the lab changes them.
// FRAMESIZE_QVGA = 320 x 240, FRAMESIZE_VGA = 640 x 480,
// FRAMESIZE_SVGA = 800 x 600. jpeg_quality: 0 to 63, a lower value gives a
// better image and a larger file.
#ifndef FRAME_SIZE
#define FRAME_SIZE FRAMESIZE_VGA
#endif
#ifndef JPEG_QUALITY
#define JPEG_QUALITY 12
#endif

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

#define PART_BOUNDARY "123456789000000000000987654321"
static const char* _STREAM_CONTENT_TYPE = "multipart/x-mixed-replace;boundary=" PART_BOUNDARY;
static const char* _STREAM_BOUNDARY = "\r\n--" PART_BOUNDARY "\r\n";
static const char* _STREAM_PART = "Content-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n";

httpd_handle_t stream_httpd = NULL;

// Counters for the status line. The stream handler (in the task of the HTTP
// server) adds to them, and loop() reads them. A difference of two values of
// 32 bits stays correct when the counter wraps.
std::atomic<uint32_t> framesSent(0);
std::atomic<uint32_t> bytesSent(0);

static esp_err_t stream_handler(httpd_req_t *req) {
  camera_fb_t *fb = NULL;
  esp_err_t res = ESP_OK;
  char part_buf[64];

  res = httpd_resp_set_type(req, _STREAM_CONTENT_TYPE);
  if (res != ESP_OK) {
    return res;
  }

  while (true) {
    fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("Camera capture failed");
      res = ESP_FAIL;
    } else {
      // The boundary comes before each part, as in the example
      // CameraWebServer of the core. FFmpeg and OpenCV cannot open a stream
      // that starts with a part header and no boundary.
      res = httpd_resp_send_chunk(req, _STREAM_BOUNDARY, strlen(_STREAM_BOUNDARY));
      if (res == ESP_OK) {
        size_t hlen = snprintf(part_buf, sizeof(part_buf), _STREAM_PART, fb->len);
        res = httpd_resp_send_chunk(req, part_buf, hlen);
      }
      if (res == ESP_OK) {
        res = httpd_resp_send_chunk(req, (const char *)fb->buf, fb->len);
      }
      if (res == ESP_OK) {
        framesSent.fetch_add(1);
        bytesSent.fetch_add(fb->len);
      }
      esp_camera_fb_return(fb);
      fb = NULL;
    }
    if (res != ESP_OK) {
      break;               // the reader closed the connection
    }
  }
  return res;
}

void startCameraServer() {
  httpd_config_t config = HTTPD_DEFAULT_CONFIG();
  config.server_port = 80;

  httpd_uri_t index_uri = {
    .uri       = "/",
    .method    = HTTP_GET,
    .handler   = stream_handler,
    .user_ctx  = NULL
  };

  if (httpd_start(&stream_httpd, &config) == ESP_OK) {
    httpd_register_uri_handler(stream_httpd, &index_uri);
  }
}

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);  // disable brownout detector

  Serial.begin(115200);
  // Wait for the Serial Monitor, but not for more than 3 seconds.
  const unsigned long start = millis();
  while (!Serial && millis() - start < 3000) {
    delay(10);
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
  config.frame_size = FRAME_SIZE;
  config.pixel_format = PIXFORMAT_JPEG;   // the camera module makes the JPEG
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = JPEG_QUALITY;
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x\n", err);
    return;
  }

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to " WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("Camera Stream Ready! Go to: http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");

  startCameraServer();
}

void loop() {
  static uint32_t lastFrames = 0;
  static uint32_t lastBytes = 0;
  delay(5000);
  const uint32_t nowFrames = framesSent.load();
  const uint32_t nowBytes = bytesSent.load();
  const uint32_t frames = nowFrames - lastFrames;
  const uint32_t bytes = nowBytes - lastBytes;
  lastFrames = nowFrames;
  lastBytes = nowBytes;
  if (frames > 0) {
    Serial.printf("sent %lu frames in 5 s: %.1f frames/s, mean JPEG %lu bytes, RSSI %d dBm\n",
                  (unsigned long)frames, frames / 5.0,
                  (unsigned long)(bytes / frames), WiFi.RSSI());
  } else {
    Serial.printf("no reader. Stream: http://%s/  RSSI %d dBm\n",
                  WiFi.localIP().toString().c_str(), WiFi.RSSI());
  }
}
