// memory_report - print the memory budget of the XIAO ESP32S3
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense), FQBN esp32:esp32:XIAO_ESP32S3
// Core:      esp32 by Espressif Systems 3.3.12
// Libraries: none
//
// Hardware status: new code, not tested on hardware (prepared on 2026-10-01).
// The sketch compiles for the board with PSRAM disabled and with OPI PSRAM.
//
// Build the sketch two times:
//   Tools > PSRAM > Disabled     the budget of the internal RAM only
//   Tools > PSRAM > OPI PSRAM    the budget with the 8 MB of external RAM
//
// The functions come from the class EspClass of the Arduino core
// (cores/esp32/Esp.h) and from esp32-hal-psram.h.
//
// Credits: the PSRAM setting comes from the XIAOML Kit setup chapter of
// "Machine Learning Systems" (mlsysbook.ai, CC BY-NC-SA 4.0).

void printRow(const char* name, uint32_t bytes) {
  Serial.printf("%-34s %10lu bytes  %8.1f KB\n", name, (unsigned long)bytes,
                bytes / 1024.0);
}

void printMemoryReport(const char* title) {
  Serial.println();
  Serial.println(title);
  Serial.println("--- Flash ---");
  printRow("Flash chip size", ESP.getFlashChipSize());
  printRow("Sketch size", ESP.getSketchSize());
  printRow("Free space for a sketch", ESP.getFreeSketchSpace());
  Serial.println("--- Internal RAM (heap) ---");
  printRow("Heap size", ESP.getHeapSize());
  printRow("Free heap", ESP.getFreeHeap());
  printRow("Lowest free heap since start", ESP.getMinFreeHeap());
  printRow("Largest block that malloc can give", ESP.getMaxAllocHeap());
  Serial.println("--- External RAM (PSRAM) ---");
  if (psramFound()) {
    printRow("PSRAM size", ESP.getPsramSize());
    printRow("Free PSRAM", ESP.getFreePsram());
    printRow("Largest PSRAM block", ESP.getMaxAllocPsram());
  } else {
    Serial.println("PSRAM is not active (Tools > PSRAM > Disabled).");
  }
}

void setup() {
  Serial.begin(115200);
  // Wait for the Serial Monitor, but not for more than 3 seconds.
  const unsigned long start = millis();
  while (!Serial && millis() - start < 3000) {
    delay(10);
  }

  Serial.printf("Chip: %s, %d core(s), %lu MHz\n", ESP.getChipModel(),
                ESP.getChipCores(), (unsigned long)ESP.getCpuFreqMHz());
  printMemoryReport("Memory report at the start");

  // Experiment: reserve 100 KB, as a model with a 100 KB arena does.
  const size_t kBlock = 100 * 1024;
  void* block = malloc(kBlock);
  if (block == nullptr) {
    Serial.println("\nmalloc(100 KB) failed.");
  } else {
    printMemoryReport("Memory report with 100 KB reserved");
    free(block);
  }
}

void loop() {
  delay(5000);
  printMemoryReport("Memory report (repeats each 5 s)");
}
