# Labs

This folder holds the lab files of the course "AI on Edge Devices".

## Layout

| Path | Content |
|---|---|
| `Labs/dayNN/` | The lab of core day `NN`: `README.md`, notebooks, `sketches/`, `solutions/`, `TEST_NOTES.md` |
| `Labs/modules/<ID>/` | The lab of backup module `<ID>` |
| `Labs/hardware/HW-nn/` | Preparation and test steps for one hardware decision. Index: `Labs/hardware/README.md`. |
| `Labs/templates/` | Skeletons for a lab folder |
| `Labs/SETUP.md` | Setup guide for the lab computers |
| `Labs/VERSIONS.md` | The tool versions and the board names of the course |
| `Labs/requirements.txt` | The Python packages of the labs |

## Index of the labs

Each lab adds one row here.

| Day or module | Title | Board | Folder | Hardware status |
|---|---|---|---|---|
| Day 1 | Toolchain, sensor tests, and model budgets | XIAOML Kit | `day01/` | not tested on hardware. The sketches compile. The notebook runs on a laptop. |
| Day 2 | MicroPython, sensor input, and a motion dataset | XIAOML Kit | `day02/` | not tested on hardware. The laptop programs and the notebook run with a simulated board. The fallback sketch compiles. |
| Day 3 | From a trained model to the microcontroller | XIAOML Kit | `day03/` | not tested on hardware. The notebook runs on a laptop. The sketches compile. A host build of the runtime confirms the model and the feature code. |
| Day 4 | Quantization | XIAOML Kit | `day04/` | not tested on hardware. The notebook runs on a laptop. The sketch compiles for the two models. A host build of the runtime runs the sketch file and confirms the two models and the quantization code. |
| Day 5 | Audio and vision on the microcontroller | XIAOML Kit | `day05/` | not tested on hardware. The two sketches need the library of an Edge Impulse project. They compile with a replacement for that library. The post-processing code and the download script run on a laptop. |
| Day 6 | Pruning, distillation, and model selection | none | `day06/` | no board is necessary. The notebook runs on a laptop. |
| Day 7 | Inference runtimes on the Raspberry Pi | Raspberry Pi 5 | `day07/` | not tested on hardware. The notebook runs on a laptop. The three scripts for the board ran on an x86 computer, the camera script with a replacement for the camera package. |
| Day 8 | Object detection on the Raspberry Pi | Raspberry Pi 5 with the camera | `day08/` | not tested on hardware. The notebook and the training script run on a laptop. The scripts for the board ran on an x86 computer with image files, the camera path with a replacement for the camera package. |
| Day 9 | One benchmark report for two boards | XIAOML Kit, Raspberry Pi 5 | `day09/` | not tested on hardware. The sketch compiles, and a 32-bit build on an x86 computer ran its four models with the outputs of LiteRT. The two scripts for the board ran on an x86 computer. No power and no throttle state was available there. |
| Day 10 | Small language models on the Raspberry Pi | Raspberry Pi 5 | `day10/` | not tested on hardware. The five scripts ran on an x86 computer with Ollama 0.32.6, on the CPU. |

## Rules for every lab folder

1. The folder has a `README.md` and a `TEST_NOTES.md`. Start both from `Labs/templates/`.
2. The `README.md` has the line `Hardware status:` near the top. No board was
   connected when the material was prepared.
3. The student version marks the places for the student work. The folder
   `solutions/` holds the complete version.
4. The first cell of a notebook and the first comment of a sketch give the
   credits of the source.
5. Data stays in the folder, or a script downloads it. No file is larger than
   20 MB.
6. Each sketch names its board, its libraries, and its library versions in the
   first comment.
