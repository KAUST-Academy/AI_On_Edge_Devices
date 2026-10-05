# Test notes: Day 1 lab

## 1. Checklist for the instructor

Run the lab on the real hardware. Record the result here.

- Date of the test: YYYY-MM-DD
- Tool versions: see `Labs/VERSIONS.md`
- Board: XIAOML Kit, esp32 core version:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Part A on a lab computer with no tools installed | The time for the install. The versions. | |
| 2 | Upload `blink` | Does the LED blink? The two lines of the build output. | |
| 3 | Upload `imu_test` | Z value with the kit flat. Do the values change when you move the kit? | |
| 4 | Upload `oled_test` | Is the text readable and in the correct orientation? | |
| 5 | Upload `mic_test`, open the Serial Plotter | Does the line follow your voice? | |
| 6 | Upload `camera_test` with OPI PSRAM | The printed line. The capture time. Does the mean brightness decrease when you cover the lens? | |
| 7 | `CameraWebServer` with the lab Wi-Fi | Does the browser show the image? The time that the students need for the two changes. | |
| 8 | `WiFiScan` | Number of networks. Does the lab network appear? | |
| 9 | `memory_report` with the two PSRAM settings | Heap size, free heap, largest block, PSRAM size, free PSRAM | |
| 10 | Put the two measured budgets in task 3 of the solution notebook and run it | Does a result of the table change? | |
| 11 | Start bootloader mode with the steps of the README | Do the steps work? | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 2. After the test

1. Write the measured numbers in the lab `README.md`, in
   `solutions/report_example.md`, and in the lab deck.
2. Put the two measured RAM budgets in `solutions/model_budgets.ipynb` and
   run the notebook again.
3. Write the fixed tool versions in `Labs/VERSIONS.md`.
