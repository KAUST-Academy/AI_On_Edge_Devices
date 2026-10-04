# Instructor guide

This guide is for the instructor of the course "AI on Edge Devices". It
gives one checklist for the time before the course and one checklist for
each day. The checklists come from the preparation notes of the syllabus
(`Docs/SYLLABUS.md`) and from the lab files.


## 1. Where the material is

| Material | Path |
|---|---|
| Theory deck and lab deck of day `NN` | `Lectures/DayNN_Theory.pdf`, `Lectures/DayNN_Lab.pdf` |
| Sources of the decks | `LaTeX/DayNN_Theory.tex`, `LaTeX/DayNN_Lab.tex`, `LaTeX/sections/` |
| Lab of day `NN` | `Labs/dayNN/`: `README.md`, `report.md`, the code, `solutions/`, `TEST_NOTES.md` |
| Hardware preparation | `Labs/hardware/HW-01/` to `Labs/hardware/HW-10/`. Index: `Labs/hardware/README.md`. |
| Setup of a lab computer | `Labs/SETUP.md` |
| Software versions | `Labs/VERSIONS.md` |
| Hardware list | `Docs/hardware.md` |
| Quizzes with answers | `Docs/quiz1.md`, `Docs/quiz2.md` |
| Decision Log, rubric, and lab check sheet | `Docs/decision_log.md` |
| Capstone brief and rubric | `Docs/capstone.md` |
| Reading list for the students | `Docs/reading.md` |
| Syllabus, with the catalogue of the backup modules | `Docs/SYLLABUS.md` |
| Credits of each reused item | `ATTRIBUTION.md` |

To build a deck again after a change, run this command in the root of the
repository. The script always ends with exit code 1. Read its output, not
its exit code.

```bash
bash build.sh --file Day01_Theory.tex
```

## 2. The teaching day

| Activity | Duration | Content |
|---|---|---|
| Theory Part 1 | 50 min | Main concept of the day |
| Break | 10 min | |
| Theory Part 2 | 50 min | Methods and tools |
| Break | 10 min | |
| Theory Part 3 | 50 min | Design trade-offs and lab briefing |
| Recap | 10 min | Questions and summary |
| Lab work | 150 min | Groups of two students. Parts A to D. |
| Lab check | 30 min | Demonstration and Decision Log |

- Each theory part has one exercise frame and one answer frame. Give the
  students 5 to 10 minutes for the exercise before you show the answer.
- In the lab, the students write a prediction before each measurement. Do
  not accept a prediction that a student wrote after the measurement.
- In the lab check, use the sheet of `Docs/decision_log.md`. One lab check
  gives 10 points.
- The labs of Days 6 and 11 start with a quiz of 20 minutes. The lab parts
  of these two days are shorter.
- Day 15 is different: Part 1 of the lecture is the course summary, and the
  time of Parts 2 and 3 (100 minutes) is build time for the capstone.

### The 15 days

| Day | Title | Board | Pages of the theory deck | Pages of the lab deck | Lab parts (min) |
|---|---|---|---|---|---|
| 1 | Edge AI landscape and system constraints | XIAOML Kit | 70 | 19 | A 50, B 45, C 55 |
| 2 | Embedded systems, MicroPython, and sensor data collection | XIAOML Kit | 74 | 22 | A 40, B 50, C 40, D 20 |
| 3 | From trained model to microcontroller | XIAOML Kit | 67 | 18 | A 45, B 50, C 30, D 25 |
| 4 | Quantization | XIAOML Kit | 65 | 20 | A 30, B 50, C 40, D 30 |
| 5 | Audio and vision on microcontrollers | XIAOML Kit | 72 | 18 | A 80, B 55, C 15 |
| 6 | Pruning, distillation, and efficient design | none | 68 | 15 | Quiz 20, A 45, B 45, C 40 |
| 7 | Hardware acceleration and inference runtimes | Raspberry Pi 5 | 69 | 18 | A 35, B 35, C 45, D 35 |
| 8 | Object detection at the edge | Raspberry Pi 5 | 73 | 21 | A 30, B 50, C 40, D 30 |
| 9 | Benchmarking and profiling | both | 76 | 18 | A 20, B 45, C 50, D 35 |
| 10 | Generative AI at the edge | Raspberry Pi 5 | 66 | 17 | A 45, B 45, C 60 |
| 11 | Networking fundamentals and RTSP streaming | both | 69 | 17 | Quiz 20, A 20, B 40, C 45, D 25 |
| 12 | Local decision-making and MQTT | both | 68 | 18 | A 30, B 45, C 40, D 35 |
| 13 | Monitoring, logging, and visualization | Raspberry Pi 5 | 73 | 18 | A 40, B 45, C 40, D 25 |
| 14 | Production edge AI design and capstone start | both | 67 | 18 | A 20, B 50, C 40, D 40 |
| 15 | Capstone build and demonstrations | both | 28 | 14 | A 80, B 70, C 30 |

### Backup modules

The syllabus names the backup modules that fit each day, and its Section 6
describes each module. A backup module has its own deck
(`Lectures/Module_<ID>.pdf`) and its own lab folder (`Labs/modules/<ID>/`).
Check that the files of a module are in the repository before you plan it.

Use a backup module when:

- a group completes the core lab early,
- a core lab fails because of the hardware, the network, or a cloud service,
- the class needs more depth or less depth on a topic,
- the class needs a recap of a machine learning topic (modules `TH-n`).

## 3. Before the course

Do these steps in this order.

### 3.1 Hardware

- [ ] Compare the hardware with `Docs/hardware.md`: the set of each group,
      the items of the classroom, and the spare boards.
- [ ] Label each kit, each Raspberry Pi, and each cable with the group
      number. The files use `gNN` for a group and `pi-NN` for its Raspberry
      Pi, for example `g07` and `pi-07`.
- [ ] Do not install the heat sink on the XIAO. The heat sink does not fit
      under the expansion board.
- [ ] Install the active cooler on each Raspberry Pi 5, and connect the
      camera. Do not connect or remove the camera cable when the power is
      on.

### 3.2 Lab computers and accounts

- [ ] Do steps 1 to 6 of `Labs/SETUP.md` on each lab computer, then step 10
      (the check). On Linux, do also step 9 (the permission for the USB
      port).
- [ ] Connect one XIAO to each type of lab computer and upload the sketch
      `Labs/day01/sketches/blink/`. This tests the USB driver.
- [ ] Ask each student to make a free Edge Impulse account before Day 2.
- [ ] Check the firewall of the lab computers with step 5 of
      `Labs/hardware/HW-09/README.md`.

### 3.3 Router

- [ ] Set the router with the table "Router settings" of
      `Labs/hardware/HW-09/README.md`. The Wi-Fi name is `edgeai-lab`. The
      2.4 GHz band must be on, and the client isolation must be off.
- [ ] Reserve the address `X.10` for the instructor laptop and the address
      `X.(100+NN)` for `pi-NN`.
- [ ] Print the address list. Put one copy on each table.

### 3.4 Master card of the Raspberry Pi

Prepare one master card, then copy it. The order is in
`Labs/hardware/README.md`:

1. `HW-04`: write the card and run `setup_pi.sh`.
2. `HW-05`: download the language models with `bash pull_models.sh extras`
   (four models, 6.5 GB).
3. `HW-06`: install MediaMTX with `install_mediamtx.sh`.
4. `HW-07`: set the Mosquitto broker for the lab network.
5. `HW-08`: install Prometheus and Grafana, only if Day 13 uses them.
6. `HW-04`: run `check_pi.sh`. The last line must be `RESULT: PASS`.
7. `HW-04`: copy the card, and run `set_hostname.sh` one time on each copy.

Write the name `pi-NN` on each card.

### 3.5 Hardware tests

- [ ] Run each `Labs/hardware/HW-nn/README.md`, section "Test steps for the
      instructor", on one kit and on one Raspberry Pi.
- [ ] Run each lab one time with the checklist of its `TEST_NOTES.md`.
      Record the time of each part and the measured numbers.
- [ ] Do the steps "After the test" of each `TEST_NOTES.md`: write the
      measured numbers in `solutions/report_example.md` and in the lab deck,
      and change the line `Hardware status:` of the `README.md`.
- [ ] Write the final tool versions in `Labs/VERSIONS.md`. Use the same
      versions for the complete course.

### 3.6 Fallback files

Put these files in a shared folder or on a USB drive. The lab `README.md`
of each day tells the students when to use them.

| Day | File or folder | Where it comes from |
|---|---|---|
| 5 | `keywords2.zip` (139 MB) | The download script of the Day 5 lab |
| 5 | The two Arduino library ZIP files of Edge Impulse: keyword model and image model | Your hardware test of the Day 5 lab |
| 6 | The folder `fashion-mnist` | The folder `.keras/datasets/` of your home folder, after one run of the notebook |
| 7 | `mnv2.tflite`, `mnv2_static.onnx`, `mnv2_dynamic.onnx`, `mnv2_unfused.onnx` | Your run of `Labs/day07/solutions/export_inspect.ipynb`. You can also put them on the master card in `~/edgeai/day07/models/`. |
| 8 | `cupbottle.pt`, the two NCNN folders, the four LiteRT files, the folder `data/`, `yolo11n.pt` | Your run of `Labs/day08/solutions/custom_detector.ipynb` |
| 9 | The model files of Days 7 and 8 | The two rows above |
| 10 | One spare card with the four language models | The master card |

### 3.7 Other preparation

- [ ] Prepare the keyword spotting demonstration of Day 1 on one kit (see
      Day 1 below).
- [ ] Print the two quizzes without the section "Answers".
- [ ] Print the lab check sheet of `Docs/decision_log.md`: one sheet for
      each group and each day.
- [ ] Select the backup modules that you plan to use, and check their
      hardware in `Docs/hardware.md`.

## 4. Checklist for each day

Each day has the same items. "Before" is the preparation. "Lab" gives the
points to watch during the lab. "Fallback" is the short form of the section
"If a part does not work" of the lab `README.md`.

### Day 1: Edge AI landscape and system constraints

Before:

- [ ] The software is on the lab computers, and the USB driver works.
- [ ] Each kit and each cable has the label of its group.
- [ ] One kit runs the keyword spotting demonstration for Part 3 of the
      lecture: a sketch with an Edge Impulse library (classes YES, NO,
      NOISE, UNKNOWN) that shows the result on the display. The kit chapter
      "Keyword Spotting (KWS)" of *Machine Learning Systems* gives the
      steps. Build the sketch with the option "OPI PSRAM".
- [ ] Explain the daily format, the Decision Log, and the points of a lab
      check (`Docs/decision_log.md`). Say how the students hand in
      `report.md`.

Lab:

- Parts B and C need the toolchain of Part A. Help first the groups with a
  toolchain problem.
- The camera test needs the build option "OPI PSRAM".
- Part C needs no board. A group with a kit that does not work can do it.

Backup modules: MC-1, MC-10, SIM-1, NB-1.

Recap modules: TH-2, TH-3, TH-4, TH-7, TH-9, TH-13, TH-14, TH-20, TH-23,
TH-24, TH-33.

### Day 2: Embedded systems, MicroPython, and sensor data collection

Before:

- [ ] Test the MicroPython firmware and the IMU driver of
      `Labs/hardware/HW-01/` on one kit. The sources give Arduino code
      only: the driver is new.
- [ ] Download the firmware file with `Labs/hardware/HW-01/get_firmware.sh`
      and put it in the shared folder.
- [ ] Each student has an Edge Impulse account.

Lab:

- MicroPython replaces the Arduino firmware. The last step of the lab puts
  the Arduino firmware back. Check this step for each group: Day 3 needs it.
- The groups keep their dataset in `Labs/day02/data/`. Days 3 and 4 use it.
- Check the split in the lab check: no session is in the training set and
  also in the test set.

Fallback:

- MicroPython does not start: the Arduino sketch
  `sketches/imu_data_collection/` sends the same lines.
- No board: `host/sim_board.py` sends simulated signals.
- No dataset at the end: `host/make_fallback_dataset.py` makes a simulated
  dataset. After your hardware test, replace it with your real dataset.

Backup modules: MC-1, MC-2, NB-10, NB-12.

Recap modules: TH-6, TH-10, TH-26.

### Day 3: From trained model to microcontroller

Before:

- [ ] Test the library Chirale_TensorFlowLite 2.0.0 on one kit
      (`Labs/hardware/HW-02/`). The lab uses this library for TensorFlow
      Lite Micro.
- [ ] Test the build of an Edge Impulse library with the esp32 core
      3.3.12. The kit chapter names the core 2.0.17 for this library.
- [ ] Each kit runs the Arduino firmware again.

Lab:

- The student sketch `sketches/motion_classifier/` has the sensor code. The
  students write the inference part (Tasks B1 and B2).
- The first build of the library needs some minutes.
- Part C repeats the measurement with PSRAM and with no PSRAM.

Fallback:

- No dataset of Day 2: the group copies the folder `data/` of a different
  group, or the notebook uses the simulated dataset.
- The inference code is not complete: the sketch of `solutions/`.
- Edge Impulse Studio is not available: the group completes only the column
  of its own sketch.

Backup modules: MC-3, MC-4, MC-10, NB-2, NB-3, NB-4.

Recap modules: TH-10, TH-11, TH-12, TH-15, TH-16, TH-17, TH-18, TH-26,
TH-35.

### Day 4: Quantization

Before:

- [ ] No trained model is necessary. The notebook trains the float baseline
      in the lab (a step of 5 minutes).
- [ ] Each group has the dataset of Day 2 on its laptop.

Lab:

- Only Part D needs the kit. Part D has 30 minutes for two builds.
- The Decision Log must explain the change of the accuracy, or why the
  accuracy does not change.

Fallback:

- A task is not complete: the functions of `solutions/quantization.ipynb`.
- The notebook did not write the four files: the files of
  `sketches/motion_quant/`.
- No kit: Parts A, B, and C, with "no board" in the table of Part D.

Backup modules: SIM-2, PI-2 (after Day 7), NB-8.

Recap modules: TH-14, TH-16, TH-21, TH-32.

### Day 5: Audio and vision on microcontrollers

Before:

- [ ] This day has two applications. The image dataset is in the lab folder
      (`image_dataset/`, 81 photos). The students do not collect images.
- [ ] The room is noisy when many groups record. Plan the recording in
      turns, or use a second room.
- [ ] Put `keywords2.zip` and the two library ZIP files in the shared
      folder.
- [ ] If you have the real objects of the image dataset, bring them. If
      not, the students test with the photos of `test_images/` on a screen.

Lab:

- Part A has 80 minutes and Part B has 55 minutes. Say the time at the end
  of Part A.
- If the class needs more time, move Part B to the start of Day 6. Day 6
  uses no board.
- The check of the keyword model: no event in 30 seconds of normal speech.

Fallback:

- The Studio is not available, or the training is slow: the library ZIP
  file of the shared folder.
- The library does not build with the core 3.3.12: the core 2.0.17.
- Tasks A1 and A2 are not complete: `solutions/sketches/kws_stream/postprocess.h`.

Backup modules: MC-5, MC-6, MC-7, MC-8, MC-2, NB-5, NB-6, NB-7, MC-11.

Recap modules: TH-11, TH-19, TH-22, TH-23, TH-25, TH-26.

### Day 6: Pruning, distillation, and efficient design

Before:

- [ ] Print the Week 1 quiz (`Docs/quiz1.md`) without the answers. The quiz
      takes the first 20 minutes of the lab.
- [ ] The trained baseline model is in the lab folder
      (`models/baseline.keras`). Run the solution notebook one time on a lab
      laptop and record the run time.
- [ ] Put the folder `fashion-mnist` in the shared folder.

Lab:

- This day uses no board. A group can use spare time to complete a hardware
  lab of Week 1.
- The two budgets of the notebook are example budgets. Each model of this
  lab fits the two real boards. `Labs/day06/TEST_NOTES.md` has more points
  for the instructor.

Fallback:

- A task is not complete: the function of `solutions/compression.ipynb`.
- The experiments are slow: two groups on one laptop, or the tables of the
  solution notebook.

Backup modules: GA-9, SIM-2.

Recap modules: TH-6, TH-8, TH-15, TH-17, TH-19, TH-20, TH-24, TH-36.

### Day 7: Hardware acceleration and inference runtimes

Before:

- [ ] All microSD cards are copies of the master card, and each card has a
      different host name `pi-NN`.
- [ ] Test SSH on the lab router from one lab computer:
      `ssh edge@pi-NN.local`. Have the address list ready for the groups
      where the name does not work.
- [ ] Give the password of the user `edge` to the students.
- [ ] Put the four exported model files in the shared folder.

Lab:

- Part A has the first start of the Raspberry Pi. Check that each board has
  its cooler and its camera before the power is on.
- The students copy the lab folder to the board with `scp`.

Fallback:

- The camera gives no photo: Part B with the cat photo only.
- The environment for the notebook does not install: the solution notebook
  and the exported files.

Backup modules: PI-1, PI-2, PI-5, SIM-3, SIM-4, PI-10.

Recap modules: TH-7, TH-21, TH-33, TH-34, TH-35.

### Day 8: Object detection at the edge

Before:

- [ ] Bring one bottle and one cup for each group. Each object of the
      classroom is good: a water bottle, a paper cup, a mug.
- [ ] Put the fallback files of Day 8 in the shared folder: `cupbottle.pt`,
      the exported files, and the folder `data/`.
- [ ] The lab makes its dataset from COCO images with `get_dataset.py`. The
      README gives a second dataset, "box and wheel", which needs a
      Roboflow account.

Lab:

- The training of Part B runs in the background for about 9 minutes on 4
  cores. The students start it first and then do the other steps.
- Each group shows the live image with a box for the bottle and a box for
  the cup.

Fallback:

- The training is not complete: `cupbottle.pt`.
- The export to LiteRT stops: the two NCNN folders, and the four LiteRT
  files of the shared folder.
- The laptop has Windows with no WSL: Colab, or two groups on one laptop.

Backup modules: PI-3, PI-4, PI-8, MC-6, PI-9.

Recap modules: TH-11, TH-18, TH-22, TH-25.

### Day 9: Benchmarking and profiling

Before:

- [ ] A USB power meter gives real energy numbers. Without the meter, the
      students estimate the energy from the data sheet values and from the
      published values of the README.
- [ ] Each Raspberry Pi has the model files of Days 7 and 8.

Lab:

- Part A is the protocol. Check that each group writes the method and the
  predictions before it measures.
- The first build of the kit sketch needs some minutes. The students do the
  next step during the build.
- "Does not fit" is also a result for a model with no memory for its arena.

Fallback:

- A task is not complete: the file of `solutions/`.
- No Raspberry Pi: `pi/bench.py --suite tiny` on the laptop.

Backup modules: PI-6, MC-9, SY-3, SIM-5, NB-8, NB-11.

Recap modules: TH-33, TH-34, TH-37.

### Day 10: Generative AI at the edge

Before:

- [ ] Each card has the four models: `ollama list` shows `llama3.2:1b`,
      `llama3.2:3b`, `nomic-embed-text`, and `llava-phi3:3.8b`. The files
      are large (6.5 GB). Do not download them during the lab.
- [ ] Model names change quickly. Check on the pilot that the four names
      still exist in the Ollama library.
- [ ] Each Raspberry Pi has the active cooler.

Lab:

- The image option of Part C is slow. A group with little time uses two
  images only.
- The check of Part C: valid structured output for five test prompts.

Fallback:

- A model is not on the card: the spare card.
- No Raspberry Pi: a laptop with Ollama. The rates then say nothing about
  the board.

Backup modules: GA-1, GA-2, GA-3, GA-4, GA-5, GA-6, GA-7, GA-8, GA-9, GA-10,
GA-11, GA-12.

Recap modules: TH-5, TH-27, TH-28, TH-29, TH-30, TH-31.

### Day 11: Networking fundamentals and RTSP streaming

Before:

- [ ] Print the Week 2 quiz (`Docs/quiz2.md`) without the answers. The quiz
      takes the first 20 minutes of the lab.
- [ ] Use the dedicated router. A campus network can block the traffic
      between devices.
- [ ] MediaMTX is on each card. If not:
      `bash Labs/hardware/HW-06/install_mediamtx.sh` on the Raspberry Pi.
- [ ] The firewall of the lab computers lets the stream pass.
- [ ] Test the camera sketch of the XIAO on one kit. The source chapter is
      for the XIAO ESP32C3, and the sketch was changed for the ESP32S3.

Lab:

- The XIAO needs the 2.4 GHz band of the router.
- If a wired switch is available, connect each Raspberry Pi with a cable.
  The students write in the report which connection they used.

Fallback:

- The camera of the Raspberry Pi does not work: the test image of step 8 of
  `Labs/hardware/HW-06/README.md`.
- The laptop has no Day 8 environment: the detector runs on the Raspberry
  Pi.

Backup modules: SY-1, MC-8, SY-11.

Recap modules: none.

### Day 12: Local decision-making and MQTT

Before:

- [ ] The instructor laptop has the reserved address `X.10` and runs a
      Mosquitto broker with the settings of
      `Labs/hardware/HW-07/mosquitto_lab.conf`. This broker is the "cloud"
      of Part D.
- [ ] Each group uses its own topic prefix: `edgeai/gNN/`.
- [ ] Test the two MQTT programs of the XIAO on one kit. The source chapter
      is for the XIAO ESP32C3 and a public broker. The code was changed for
      the ESP32S3 and the local broker.
- [ ] The Day 5 library of each group is on its laptop. Part B needs it for
      the keyword events.

Lab:

- Subscribe to `edgeai/#` on the instructor laptop. You then see the
  decisions of all groups.
- Part D cuts the link to the cloud broker. Each group cuts its own link
  with `pi/link.sh`.
- The check of Part D: `cloud_check.py` prints
  `RESULT: PASS - no lost message` after the link returns.

Fallback:

- The Day 5 library is not on the laptop: the sketch
  `Labs/hardware/HW-07/sketches/mqtt_imu/`, or events by hand with
  `mosquitto_pub`.
- The instructor broker does not answer: the Raspberry Pi of a second group
  is the cloud.
- `pi/link.sh` reports an error: stop the cloud broker for 3 minutes.

Backup modules: SY-2, PI-7, GA-8, NB-9, SY-12.

Recap modules: none.

### Day 13: Monitoring, logging, and visualization

Before:

- [ ] The lab uses the Python dashboard of the lab folder. Grafana with
      Prometheus is a second option: `Labs/hardware/HW-08/` has the files.
      Select one tool after your test, and install it on the master card.
- [ ] Bring for each group: a cup, a bottle, one object that the model does
      not know (a phone, a box, or a book), and a desk lamp if the light of
      the room cannot change.

Lab:

- The two drift events are a dim light and an unknown object. The alert
  must fire during the dim light event and clear after it.
- The report has an incident report and a Decision Log.

Fallback:

- The light cannot change: the option `--dim-after` of
  `pi/monitor_detect.py` simulates the event.
- The camera does not work: image files with `--source`.
- The Day 8 model is not on the card: the pre-trained model `yolo11n.pt`.

Backup modules: SY-9, SY-3, SIM-6, SIM-8, SY-10.

Recap modules: TH-8.

### Day 14: Production edge AI design and capstone start

Before:

- [ ] Read `Docs/capstone.md`. It has four example projects for a team with
      no idea.
- [ ] Print `Labs/day14/review_sheet.md`: one copy for each team. A review
      takes about 8 minutes.
- [ ] Volume II of the textbook is a preview. Check the frames of Part 1
      that name Volume II against the current text of the book.
- [ ] Make the demonstration schedule of Day 15 with
      `Labs/day15/schedule.py` and publish it at the end of the day.

Lab:

- A team is two lab groups: three or four students, two kits, and two
  Raspberry Pi boards.
- A proposal is approved when it meets the five requirements and has a
  first test for its riskiest assumption.
- Give the order of the reviews at the start of Part C.

Backup modules: SY-4, SY-5, SY-6, SY-7, SY-8, SY-10.

Recap modules: TH-3, TH-36, TH-37.

### Day 15: Capstone build and demonstrations

Before:

- [ ] The demonstration schedule is published. Part B holds 7 teams with 10
      minutes each. With more teams, use two rooms or shorter slots, or
      start some demonstrations in Part A.
- [ ] Keep the spare boards ready.
- [ ] The cloud broker runs on the instructor laptop. Requirement 3 needs a
      cut of this link during the demonstration.
- [ ] Print the rubric of `Docs/capstone.md`, Section 3: one copy for each
      team.

Lab:

- Visit each team during the build time of the lecture (100 minutes).
- Grade the demonstration and the report with the rubric.
- Part C: each team hands in `report.md`, and each student fills
  `Labs/day15/feedback.md`.

Backup modules: each module of Section 6 of the syllabus can be a part of a
capstone.

Recap modules: none.

## 5. Open decisions

The material uses one option for each of these points. Decide before the
course if you keep it.

| Point | Option that the material uses | Other option |
|---|---|---|
| Dashboard tool of Day 13 | The Python dashboard | Grafana with Prometheus (`Labs/hardware/HW-08/`, option A) |
| Dataset of Day 8, Part B | Cups and bottles from COCO images | "Box and wheel" from Roboflow, with an account for each group |
| Models of Day 9, Part B | The four reference models of MLPerf Tiny | The Edge Impulse models of the students from Day 5 |
| Quiz answers | The answers are in `Docs/quiz1.md` and `Docs/quiz2.md` of this public repository | Move the answers to a private place, or write new questions each year |
| Points of a lab check | 10 points: 4 for the check criteria, 6 for the Decision Log | Your own split |
| Weights of the grade | Daily labs 40, quizzes 20, capstone 40 percent | The rules of KAUST Academy |


