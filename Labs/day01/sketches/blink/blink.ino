// blink - switch the built-in LED of the XIAO ESP32S3 on and off
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense), FQBN esp32:esp32:XIAO_ESP32S3
// Core:      esp32 by Espressif Systems 3.3.12
// Libraries: none
//
// Credits: the code comes from the XIAOML Kit setup chapter of "Machine
// Learning Systems" by Vijay Janapa Reddi and contributors, written by
// Marcelo Rovai (mlsysbook.ai, CC BY-NC-SA 4.0). Changes: this comment and the
// serial messages.

#define LED_PIN 21  // The built-in LED of the XIAO ESP32S3 is on GPIO21.

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
}

// The LED pin works with inverted logic: LOW turns the LED on and HIGH turns
// it off.
void loop() {
  digitalWrite(LED_PIN, LOW);   // on
  Serial.println("LED on");
  delay(1000);
  digitalWrite(LED_PIN, HIGH);  // off
  Serial.println("LED off");
  delay(1000);
}
