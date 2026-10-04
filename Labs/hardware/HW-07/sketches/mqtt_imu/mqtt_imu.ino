// mqtt_imu - send IMU telemetry and results from the XIAOML Kit with MQTT
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense), FQBN esp32:esp32:XIAO_ESP32S3
// Core:      esp32 by Espressif Systems 3.3.12
// Libraries: PubSubClient 2.8 (Nick O'Leary), Seeed Arduino LSM6DS3 2.0.7
// Broker:    Mosquitto on the Raspberry Pi of the group (port 1883)
//
// Hardware status: not tested on hardware (prepared on 2026-10-01).
// The sketch compiles for the board.
//
// Credits: this sketch adapts the programs of Task 2 (telemetry) and Task 3
// (commands) of chapter 3.5 of "XIAO: Big Power, Small Board" by Lei Feng and
// Marcelo Rovai (github.com/Mjrovai/XIAO_Big_Power_Small_Board-ebook,
// GPL-3.0). The IMU code comes from imu_test.ino of "XIAO ESP32S3 Sense" by
// Marcelo Rovai (github.com/Mjrovai/XIAO-ESP32S3-Sense, Apache-2.0).
//
// Changes from the chapter:
//   - Board XIAO ESP32S3, not XIAO ESP32C3.
//   - A local broker with an IP address, not the public broker hivemq.com.
//   - The IMU of the kit, not the DHT20 sensor. JSON payload.
//   - One topic tree for each group: edgeai/<group>/xiao/...
//   - A last will message, a sequence number, and a command for the LED.
//   - The connection code does not block the loop for 5 seconds.
//
// Topics (GROUP_ID is in arduino_secrets.h):
//   edgeai/<group>/xiao/status   "online" or "offline", retained, last will
//   edgeai/<group>/xiao/imu      telemetry, each 1000 ms
//   edgeai/<group>/xiao/result   result of the model, each 1000 ms
//   edgeai/<group>/xiao/cmd      command to the board: "led=1" or "led=0"

#include <WiFi.h>
#include <PubSubClient.h>
#include <LSM6DS3.h>
#include <Wire.h>

#include "arduino_secrets.h"

const char* kSsid = SECRET_SSID;
const char* kPassword = SECRET_PASS;
const char* kBroker = MQTT_BROKER;
const uint16_t kPort = 1883;

const char* kClientId = "xiao-" GROUP_ID;
const char* kTopicStatus = "edgeai/" GROUP_ID "/xiao/status";
const char* kTopicImu = "edgeai/" GROUP_ID "/xiao/imu";
const char* kTopicResult = "edgeai/" GROUP_ID "/xiao/result";
const char* kTopicCmd = "edgeai/" GROUP_ID "/xiao/cmd";

const unsigned long kPublishPeriodMs = 1000;
const unsigned long kRetryPeriodMs = 5000;

// The built-in LED is on GPIO21. LOW turns it on (kit setup chapter).
const int kLedPin = LED_BUILTIN;

WiFiClient espClient;
PubSubClient client(espClient);
LSM6DS3 myIMU(I2C_MODE, 0x6A);

unsigned long lastPublish = 0;
unsigned long lastRetry = 0;
unsigned long sequence = 0;
char payload[160];

void setupWifi() {
  Serial.print("Connecting to ");
  Serial.println(kSsid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(kSsid, kPassword);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("WiFi connected. IP address: ");
  Serial.println(WiFi.localIP());
}

// The broker calls this function for each message on the command topic.
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
  }
  Serial.println();

  if (length == 5 && memcmp(message, "led=1", 5) == 0) {
    digitalWrite(kLedPin, LOW);    // on
  } else if (length == 5 && memcmp(message, "led=0", 5) == 0) {
    digitalWrite(kLedPin, HIGH);   // off
  }
}

// Try one time to connect. Return true when the connection is open.
bool connectBroker() {
  Serial.print("Attempting MQTT connection to ");
  Serial.print(kBroker);
  Serial.print(" ... ");
  // Last will: the broker sends "offline" when the board disappears.
  if (client.connect(kClientId, kTopicStatus, 1, true, "offline")) {
    Serial.println("connected");
    client.publish(kTopicStatus, "online", true);
    client.subscribe(kTopicCmd, 1);
    return true;
  }
  Serial.print("failed, rc=");
  Serial.println(client.state());
  return false;
}

// Send one result of a model. The Day 12 lab calls this function with the
// class and the confidence of the keyword model or of the image model.
void publishResult(const char* label, float score) {
  snprintf(payload, sizeof(payload),
           "{\"seq\":%lu,\"ms\":%lu,\"label\":\"%s\",\"score\":%.2f}",
           sequence, millis(), label, score);
  client.publish(kTopicResult, payload);
}

void setup() {
  Serial.begin(115200);
  const unsigned long start = millis();
  while (!Serial && millis() - start < 3000) {
    delay(10);
  }

  pinMode(kLedPin, OUTPUT);
  digitalWrite(kLedPin, HIGH);     // off

  if (myIMU.begin() != 0) {
    Serial.println("ERROR: IMU initialization failed!");
  }

  setupWifi();
  client.setServer(kBroker, kPort);
  client.setCallback(callback);
  client.setKeepAlive(15);
}

void loop() {
  const unsigned long now = millis();

  if (WiFi.status() != WL_CONNECTED) {
    // The core connects to the Wi-Fi again without help.
    delay(100);
    return;
  }

  if (!client.connected()) {
    if (now - lastRetry >= kRetryPeriodMs || lastRetry == 0) {
      lastRetry = now;
      connectBroker();
    }
    return;
  }
  client.loop();

  if (now - lastPublish >= kPublishPeriodMs) {
    lastPublish = now;

    const float ax = myIMU.readFloatAccelX();
    const float ay = myIMU.readFloatAccelY();
    const float az = myIMU.readFloatAccelZ();
    const float gx = myIMU.readFloatGyroX();
    const float gy = myIMU.readFloatGyroY();
    const float gz = myIMU.readFloatGyroZ();

    snprintf(payload, sizeof(payload),
             "{\"seq\":%lu,\"ms\":%lu,\"ax\":%.3f,\"ay\":%.3f,\"az\":%.3f,"
             "\"gx\":%.2f,\"gy\":%.2f,\"gz\":%.2f}",
             sequence, now, ax, ay, az, gx, gy, gz);
    client.publish(kTopicImu, payload);
    Serial.println(payload);

    // Placeholder for a model: the axis with the largest acceleration.
    // Replace these lines with the result of your classifier.
    const float absX = fabs(ax), absY = fabs(ay), absZ = fabs(az);
    const char* label = "z";
    float largest = absZ;
    if (absX > largest) { label = "x"; largest = absX; }
    if (absY > largest) { label = "y"; largest = absY; }
    const float sum = absX + absY + absZ;
    publishResult(label, sum > 0 ? largest / sum : 0);

    sequence++;
  }
}
