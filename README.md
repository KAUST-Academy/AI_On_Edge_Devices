# AI on Edge Devices

This repository holds the material of the course "AI on Edge Devices": the
slide decks, the lab files, and the course documents. 

## 1. The course

The course teaches how to run deep learning models on devices with small
memory, low power, and no reliable cloud connection. You optimize models,
you deploy them on a microcontroller and on a Linux single-board computer,
you connect the devices, and you monitor them. The course ends with a team
project that joins all parts into one system that works.

### What you must know before the course

- Deep learning and model development
- Python
- Basic use of the Linux command line
- Earlier contact with computer vision is an advantage

### What you can do at the end of the course

1. Select a deployment paradigm (cloud, edge, mobile, TinyML) from latency,
   memory, power, and privacy constraints.
2. Collect and prepare sensor data from a microcontroller.
3. Convert a trained model and deploy it on a microcontroller with
   TensorFlow Lite Micro.
4. Apply quantization, pruning, and knowledge distillation, and measure the
   effect on accuracy, size, and latency.
5. Run and optimize vision models on a Raspberry Pi with different
   inference runtimes.
6. Benchmark latency, memory, and energy with a correct method.
7. Run a small language model on a Raspberry Pi and use it in an
   application.
8. Connect edge devices with RTSP and MQTT, and make decisions locally
   without the cloud.
9. Monitor a deployed system and design an edge AI system for production.

### The two boards

| Board | Class | Used for |
|---|---|---|
| XIAOML Kit (Seeed XIAO ESP32S3 Sense with an expansion board) | Microcontroller with Wi-Fi, 8 MB PSRAM, camera, microphone, IMU, and display | MicroPython, motion, keyword spotting, vision, MQTT |
| Raspberry Pi 5 (8 GB) with a camera | Linux single-board computer | Inference runtimes, object detection, language models, RTSP, broker, monitoring |

You work in a group of two students. Each group has one XIAOML Kit and one
Raspberry Pi 5.

## 2. Schedule

### One day

| Activity | Duration | Content |
|---|---|---|
| Theory Part 1 | 50 min | Main concept of the day |
| Break | 10 min | |
| Theory Part 2 | 50 min | Methods and tools |
| Break | 10 min | |
| Theory Part 3 | 50 min | Design trade-offs and lab briefing |
| Recap | 10 min | Questions and summary |
| Lab work | 150 min | Work in your group. Each lab has two to four parts: Part A to Part D. |
| Lab check | 30 min | Demonstration to the instructor and Decision Log |

Each theory part has one short exercise of 5 to 10 minutes.

### The 15 days

| Day | Topic | Board | Theory deck | Lab deck | Lab files |
|---|---|---|---|---|---|
| | **Week 1: foundations and TinyML on the XIAOML Kit** | | | | |
| 1 | Edge AI landscape and system constraints | XIAOML Kit | [theory](Lectures/Day01_Theory.pdf) | [lab](Lectures/Day01_Lab.pdf) | [`Labs/day01/`](Labs/day01/README.md) |
| 2 | Embedded systems, MicroPython, and sensor data collection | XIAOML Kit | [theory](Lectures/Day02_Theory.pdf) | [lab](Lectures/Day02_Lab.pdf) | [`Labs/day02/`](Labs/day02/README.md) |
| 3 | From trained model to microcontroller | XIAOML Kit | [theory](Lectures/Day03_Theory.pdf) | [lab](Lectures/Day03_Lab.pdf) | [`Labs/day03/`](Labs/day03/README.md) |
| 4 | Quantization | XIAOML Kit | [theory](Lectures/Day04_Theory.pdf) | [lab](Lectures/Day04_Lab.pdf) | [`Labs/day04/`](Labs/day04/README.md) |
| 5 | Audio and vision on microcontrollers | XIAOML Kit | [theory](Lectures/Day05_Theory.pdf) | [lab](Lectures/Day05_Lab.pdf) | [`Labs/day05/`](Labs/day05/README.md) |
| | **Week 2: optimization and Linux-class edge devices** | | | | |
| 6 | Pruning, distillation, and efficient design | Laptop only | [theory](Lectures/Day06_Theory.pdf) | [lab](Lectures/Day06_Lab.pdf) | [`Labs/day06/`](Labs/day06/README.md) |
| 7 | Hardware acceleration and inference runtimes | Raspberry Pi 5 | [theory](Lectures/Day07_Theory.pdf) | [lab](Lectures/Day07_Lab.pdf) | [`Labs/day07/`](Labs/day07/README.md) |
| 8 | Object detection at the edge | Raspberry Pi 5 | [theory](Lectures/Day08_Theory.pdf) | [lab](Lectures/Day08_Lab.pdf) | [`Labs/day08/`](Labs/day08/README.md) |
| 9 | Benchmarking and profiling | Both boards | [theory](Lectures/Day09_Theory.pdf) | [lab](Lectures/Day09_Lab.pdf) | [`Labs/day09/`](Labs/day09/README.md) |
| 10 | Generative AI at the edge | Raspberry Pi 5 | [theory](Lectures/Day10_Theory.pdf) | [lab](Lectures/Day10_Lab.pdf) | [`Labs/day10/`](Labs/day10/README.md) |
| | **Week 3: connected systems and production** | | | | |
| 11 | Networking fundamentals and RTSP streaming | Both boards | [theory](Lectures/Day11_Theory.pdf) | [lab](Lectures/Day11_Lab.pdf) | [`Labs/day11/`](Labs/day11/README.md) |
| 12 | Local decision-making and MQTT | Both boards | [theory](Lectures/Day12_Theory.pdf) | [lab](Lectures/Day12_Lab.pdf) | [`Labs/day12/`](Labs/day12/README.md) |
| 13 | Monitoring, logging, and visualization | Raspberry Pi 5 | [theory](Lectures/Day13_Theory.pdf) | [lab](Lectures/Day13_Lab.pdf) | [`Labs/day13/`](Labs/day13/README.md) |
| 14 | Production edge AI design and capstone start | Both boards | [theory](Lectures/Day14_Theory.pdf) | [lab](Lectures/Day14_Lab.pdf) | [`Labs/day14/`](Labs/day14/README.md) |
| 15 | Capstone build and demonstrations | Both boards | [theory](Lectures/Day15_Theory.pdf) | [lab](Lectures/Day15_Lab.pdf) | [`Labs/day15/`](Labs/day15/README.md) |

- The labs of Day 6 and Day 11 start with a quiz of 20 minutes: Week 1 and
  Week 2.
- Days 14 and 15 are the capstone: a team project with the two boards.
  [`Docs/capstone.md`](Docs/capstone.md) has the requirements and the
  rubric.

### The backup modules

A backup module is a short unit that you can use instead of part of a day. It
has its own deck and its own lab folder, and each part stands alone. Use a
backup module when your group finishes the core lab early, when the core lab
fails because of the hardware or the network, or when you need more depth on a
topic. The syllabus lists every module:
[`Docs/SYLLABUS.md`](Docs/SYLLABUS.md), Section 6.

| ID | Module | Fits day | Theory deck | Lab deck | Lab files |
|---|---|---|---|---|---|
| TH-3 | ML workflow and life cycle | 1, 14 | [theory](Lectures/modules/Module_TH-3.pdf) | | |

A module with a lab has a lab deck `Module_<ID>_Lab.pdf` in
`Lectures/modules/` and a lab folder `Labs/modules/<ID>/`. The two columns stay
empty for a module of theory only.

Build a module deck with:

```bash
bash build_module.sh --file Module_TH-3.tex
```

The PDF goes to `Lectures/modules/`, so it does not mix with the decks of the
core days.

## 3. Where the material is

| Path | Content |
|---|---|
| `Lectures/` | The slide decks of the core days as PDF files: `DayNN_Theory.pdf` and `DayNN_Lab.pdf` |
| `Lectures/modules/` | The slide decks of the backup modules as PDF files: `Module_<ID>.pdf` |
| `Labs/dayNN/` | The lab of day `NN`: `README.md` (the steps), `report.md` (the report that you hand in), the notebooks, the sketches, the scripts, and `solutions/` |
| [`Labs/SETUP.md`](Labs/SETUP.md) | The setup of your laptop |
| [`Labs/VERSIONS.md`](Labs/VERSIONS.md) | The software versions of the course |
| [`Docs/decision_log.md`](Docs/decision_log.md) | The Decision Log, its rubric, and the lab check |
| [`Docs/capstone.md`](Docs/capstone.md) | The capstone brief |
| [`Docs/reading.md`](Docs/reading.md) | The books and the reading for each day |
| [`Docs/SYLLABUS.md`](Docs/SYLLABUS.md) | The complete syllabus |
| `LaTeX/` | The sources of the slide decks. A module deck is `LaTeX/Module_<ID>.tex` with its sections in `LaTeX/sections/modules/<ID>/` |

## 4. Setup

Do these steps before Day 1.

1. Get the repository:

   ```bash
   git clone https://github.com/KAUST-Academy/AI_On_Edge_Devices.git
   cd AI_On_Edge_Devices
   ```

2. Follow [`Labs/SETUP.md`](Labs/SETUP.md), steps 1 to 6: the Arduino IDE 2
   with the esp32 board core, the Arduino libraries of the kit, the board
   settings, the Python environment, the MicroPython tools, and the Edge
   Impulse CLI. On Linux, do also step 9: the permission for the USB port.
3. Make the Python environment in the root of the repository:

   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r Labs/requirements.txt
   ```

   On Windows, the programs of the environment are in `.venv\Scripts\`.
   On Linux, install the CPU version of PyTorch first. The Day 1 lab
   `README.md` gives the command.
4. Make a free account on `edgeimpulse.com`. Day 2 needs it.
5. Do the checks of step 10 of `Labs/SETUP.md`. The checks that need a
   board wait for Day 1.

Bring these items to each day:

- your laptop with its charger. Windows, macOS, and Linux are possible. The
  laptop needs a microphone for Day 5.
- a USB-C port on the laptop, or an adapter. The kit has a USB-C connector.

The instructor gives the boards, the cables, and the prepared microSD card
of the Raspberry Pi. From Day 7, you connect to the Raspberry Pi of your
group over the lab Wi-Fi `edgeai-lab`, with `ssh edge@pi-NN.local`. `NN` is
the number of your group.

## 5. Rules

### In the lab

- Follow the `README.md` of the lab folder. The lab deck shows the same
  steps in a short form.
- Write a prediction before each measurement. A wrong prediction costs no
  points. A prediction that you wrote after the measurement does.
- Fill `report.md` during the lab. Write measured numbers with their units.
- At the end, show the result to the instructor (the section "Check
  criterion" of the `README.md`), and hand in `report.md` with your
  Decision Log.
- If a part does not work, use the section "If a part does not work" of the
  `README.md`. If you use a file of `solutions/`, write this in the report.
- The instructor asks one question about the Decision Log. Each student of
  the group must be able to answer.

### The Decision Log

A Decision Log is a text of about 100 words. You state one design decision,
you give your measured numbers, and you name the trade-off. Each lab gives
the question. [`Docs/decision_log.md`](Docs/decision_log.md) has the form,
the rubric, and three examples.

### The hardware

- Use a USB-C data cable for the kit. A cable for charging only does not
  work.
- Do not install the heat sinks on the XIAO. They do not fit under the
  expansion board.
- Connect the Wi-Fi antenna of the kit before you use Wi-Fi.
- Do not connect or remove the camera cable of the Raspberry Pi when the
  power is on.
- Shut the Raspberry Pi down with `sudo shutdown -h now` before you remove
  the power.
- Keep the label of your group on each board, card, and cable.

### Assessment

| Component | Weight | Content |
|---|---|---|
| Daily labs | 40% | Demonstration to the instructor and a Decision Log, Days 1 to 13 |
| Quizzes | 20% | Two quizzes of 20 minutes: the start of the Day 6 lab and of the Day 11 lab |
| Capstone | 40% | Proposal, demonstration, and report, Days 14 and 15 |

The instructor confirms the weights on Day 1.

## 6. For the instructor

| File | Content |
|---|---|
| [`Docs/instructor_guide.md`](Docs/instructor_guide.md) | The checklist before the course and the checklist for each day |
| [`Docs/hardware.md`](Docs/hardware.md) | The hardware of one group, of the classroom, and of each backup module |
| [`Labs/hardware/README.md`](Labs/hardware/README.md) | The preparation and the test steps of the boards, the router, and the microSD card |
| `Labs/dayNN/TEST_NOTES.md` | The code status and the test checklist of each lab |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | The build script of the decks and the format of the commit messages |
| [`LaTeX/templates/README.md`](LaTeX/templates/README.md) | The skeletons for a new deck |

## 7. Credits and licence

This course adapts material from these sources:

- *Machine Learning Systems* by Vijay Janapa Reddi and contributors,
  Harvard University (mlsysbook.ai, CC BY-NC-SA 4.0): the textbook, its
  slides, its hardware kit labs, and TinyTorch (MIT).
- *Edge AI Engineering: Raspberry Pi*, *TinyML Made Easy: XIAO ESP32S3*,
  and *XIAO: Big Power, Small Board* by Marcelo Rovai and Lei Feng, with
  the code repositories `Mjrovai/EdgeML-with-Raspberry-Pi` (GPL-3.0) and
  `Mjrovai/XIAO-ESP32S3-Sense` (Apache-2.0).
- The HarvardX TinyML courseware by the TinyMLx team (CC BY-NC-SA 4.0).

Each slide deck ends with a credits frame, and each lab names its sources.
[`ATTRIBUTION.md`](ATTRIBUTION.md) lists each reused figure, table, and
code file with its source and its licence.

The repository has the licence GPL-3.0: see [`LICENSE`](LICENSE). 
