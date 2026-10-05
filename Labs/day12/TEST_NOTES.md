# Test notes: Day 12 lab

## 1. Checklist for the instructor

- Date of the test:
- Mosquitto version on the Raspberry Pi (`mosquitto -h`) and on the
  instructor laptop:
- Edge Impulse project and library of the test:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Part A, steps 1 to 3 | The line of `ss`, the packets of `-d` for QoS 2, the time of the last will | |
| 2 | Part B, step 1 | The `mqtt_check.py` table for 30 s, the gap after 10 s with no cable | |
| 3 | Part B, step 2 | Does the sketch compile with the real library? Flash and RAM. Events for 10 "yes" and 10 "no". | |
| 4 | Part C, step 2 | The local times, the delay from the word to the LED, the LED off after 60 s | |
| 5 | Part C, step 3 | Seconds from the removed cable to FAULT | |
| 6 | Part D, steps 2 to 4 | Seconds until `link lost`, queue length each minute, seconds until the queue is 0, the table of `cloud_check.py` | |
| 7 | Part D with three groups at the same time | Does each group see only its own topics on the cloud broker? | |
| 8 | Time the complete lab with one student group, or alone | Minutes for each part | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|
| | | |
