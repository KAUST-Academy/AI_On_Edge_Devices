# Day 10 lab: small language models on the Raspberry Pi


**Goal.** Your group measures two small language models on the Raspberry
Pi 5 with the method of Day 9, calls a model from Python with structured
output and function calls, and builds one small application.

**Deliverable.** The file `report.md` with the benchmark table, the results
of the application, and the Decision Log.

**Time.** 150 minutes of work, then 30 minutes for the check by the
instructor.

| Part | Content | Time |
|---|---|---|
| A | Run and measure: two models, tokens per second, RAM, and temperature | 45 min |
| B | Python integration: structured output with a schema, and a function call | 45 min |
| C | Application: select retrieval-augmented generation or image description | 60 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| Raspberry Pi 5 (8 GB) with the active cooler | 1 | With the microSD card of the course. The card has Ollama and the four models of this lab. |
| Power supply for the Raspberry Pi 5 | 1 | 27 W, USB-C |
| Laptop | 1 | In the same network as the Raspberry Pi, with an SSH client |

This lab uses no XIAOML Kit.

## Software

| Tool | Version | Note |
|---|---|---|
| Raspberry Pi OS (64-bit) with the environment `~/ollama` | the card of the course | `Labs/hardware/HW-04/` prepares the card. `~/ollama` has the packages `ollama` and `pydantic`. |
| Ollama | the version of the card (0.32.6 on the work computer of the course) | `Labs/hardware/HW-05/` installs it |
| Models | `llama3.2:1b` (1.32 GB), `llama3.2:3b` (2.02 GB), `nomic-embed-text` (0.27 GB), `llava-phi3:3.8b` (2.93 GB) | `bash pull_models.sh extras` of `Labs/hardware/HW-05/` downloads them before the lab |
| SSH client on the laptop | no version | The commands `ssh` and `scp` |

Run all commands of this lab on the Raspberry Pi, in the folder
`~/edgeai/day10/`, with the environment `~/ollama` active. `NN` is the
number of your group.

## Files

| File | Content |
|---|---|
| `report.md` | The report to hand in. Fill it during the lab. |
| `measure_slm.py` | Part A. Measures the models with the method of Day 9. **Task A1** is in this file. |
| `prompts.txt` | Part A. The five prompts of the measurement |
| `part_b/structured.py` | Part B. Commands to JSON with a schema. **Task B1** is in this file. |
| `part_b/commands.txt` | Part B. Ten commands with the correct answer |
| `part_b/tools.py` | Part B. The model calls two Python functions. **Task B2** is in this file. |
| `part_b/tool_prompts.txt` | Part B. Five requests for the functions |
| `part_c/rag.py` | Part C, option 1. Retrieval-augmented generation. **Task C1** is in this file. |
| `part_c/facts.txt`, `part_c/questions.txt` | Part C, option 1. Twelve facts of a fictional greenhouse controller, and the five test questions |
| `part_c/describe_image.py` | Part C, option 2. Image description with structured output. **Task C2** is in this file. |
| `part_c/images/` | Part C, option 2. Five test images. `part_c/images/README.md` gives the source and the licence of each image. |
| `solutions/` | The complete scripts and an example report |
| `TEST_NOTES.md` | The code status and the test steps for the instructor |

`measure_slm.py` adds its rows to the file `results.csv`. Git ignores this
file.

## Steps

Write each result in `report.md` when you get it.

### Part A: run and measure (45 min)

1. **Copy and check (10 min).** On the laptop, in the folder `Labs/`:

   ```bash
   scp -r day10 edge@pi-NN.local:~/edgeai/
   ssh edge@pi-NN.local
   ```

   On the Raspberry Pi:

   ```bash
   cd ~/edgeai/day10
   source ~/ollama/bin/activate
   ollama list
   ollama run llama3.2:1b --verbose
   ```

   `ollama list` must show the four models of the table "Software". Enter
   `What is the capital of France?`. Ollama prints the answer and then the
   counters. Write the `prompt eval rate` and the `eval rate` in the report.
   Enter `/bye` to stop.

2. **Estimate (5 min).** Fill the estimate table of Part A in the report
   before you measure. Use the formulas of Part 1 of the lecture: the
   weights, and the KV cache for 2048 and 8192 tokens.

3. **Task A1 (5 min).** Open `measure_slm.py`. Complete the function
   `token_rate`: tokens divided by the time in seconds. Ollama gives the
   time in nanoseconds.

4. **Measure the two models (15 min).** Open a second SSH terminal and
   start `watch -n 2 vcgencmd measure_temp`. In the first terminal:

   ```bash
   python measure_slm.py
   ```

   The script prints `Task A1: complete`. Then it measures each model: one
   request to load, one request to warm up, and 10 timed requests (the five
   prompts, two times). Context 2048 tokens, at most 128 tokens for each
   answer. It prints one line for each model with these columns: `model`,
   `threads`, `load s`, `prompt tk`, `prompt tk/s`, `eval tk/s`,
   `min tk/s`, `model MB`, and `temp C`.

   `eval tk/s` is the median generation rate. `model MB` is the memory of
   the loaded model in `ollama ps`. Copy the two lines into the report.

5. **Context and threads (10 min).** Measure the memory of the 3B model for
   two contexts, and the rate of the 1B model for three thread counts:

   ```bash
   python measure_slm.py --memory-only --models llama3.2:3b --num-ctx 2048
   python measure_slm.py --memory-only --models llama3.2:3b --num-ctx 8192
   for t in 1 2 4; do
     python measure_slm.py --models llama3.2:1b --runs 1 --num-predict 32 \
         --num-thread $t
   done
   ```

   Compare the memory with your estimate of step 2.

### Part B: Python integration (45 min)

1. **Task B1 (10 min).** Open `part_b/structured.py`. In the class
   `Command`, replace each `str` with `Literal[...]` and the allowed values
   of the prompt. Pydantic then makes a JSON schema with these values.

2. **Structured output (15 min).** Run the script with the schema and
   without it, for the two models:

   ```bash
   python part_b/structured.py
   python part_b/structured.py --no-schema
   python part_b/structured.py --model llama3.2:3b
   python part_b/structured.py --model llama3.2:3b --no-schema
   ```

   Each run prints one line for each command, and then
   `valid ... of 10, correct ... of 10`. Write the four results in the
   report. Look at each wrong answer.

3. **Task B2 (10 min).** Open `part_b/tools.py`. Complete the function
   `check_call`. It checks a tool call of the model before your code runs
   it: a known function, a known room, and a heater value from 5 to 30
   degrees. The model can send a number as text, for example `"21"`.

4. **Function calls (10 min).** Run the script for the two models:

   ```bash
   python part_b/tools.py
   python part_b/tools.py --model llama3.2:3b
   ```

   For each request, the script prints the call of the model and the result,
   or `REFUSED` with the reason. The request for 300 degrees must give
   `REFUSED`. Write in the report which calls were refused, and why.

### Part C: application (60 min)

Select one option. Each option has five test prompts. The check criterion
needs valid structured output for the five prompts.

**Option 1: retrieval-augmented generation.**

1. **Task C1 (10 min).** Open `part_c/rag.py`. Complete the functions
   `cosine` and `top_k`.
2. **The five test questions (15 min).** Run `python part_c/rag.py`. The
   script embeds the 12 facts once, then answers each question of
   `part_c/questions.txt` with the 2 most similar facts. The last line is
   `valid structured output ... of 5, correct ... of 5`. Run it again with
   `--model llama3.2:3b`.
3. **The number of facts (15 min).** Run the 1B model with `--k 1` and
   `--k 4`. Write the prompt tokens, the time, and the correct answers for
   k = 1, 2, and 4.
4. **Your own facts (10 min).** Add three facts of your own to
   `part_c/facts.txt`, for example about your lab table. Ask a question
   with `--ask "..."`.
5. **Report (10 min).** Answer the questions of Part C in the report.

**Option 2: image description.**

1. **Task C2 (10 min).** Open `part_c/describe_image.py`. In the class
   `Scene`, limit `objects` to 5 items with at most 40 characters each.
2. **The five test images (25 min).** Run `python part_c/describe_image.py`.
   One image can need 1 to 4 minutes on the board (an estimate from the
   published time of the source). The last line is
   `valid structured output ... of 5`. Do the report of Parts A and B
   during the run.
3. **Compare (10 min).** Compare the value `containers` of each image with
   the number of cups and bottles in `part_c/images/README.md`.
4. **Report (15 min).** Answer the questions of Part C in the report.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] `python measure_slm.py` prints `Task A1: complete`.
- [ ] The benchmark table of the report has the two models with measured
      numbers: the median generation rate, the prompt rate, the model
      memory, and the temperature, with the method.
- [ ] `part_b/structured.py` prints `Task B1: complete`, and
      `part_b/tools.py` prints `Task B2: complete` and `REFUSED` for the
      request of 300 degrees.
- [ ] The application of Part C prints `valid structured output 5 of 5`
      for its five test prompts.
- [ ] The Decision Log gives numbers and names one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured
numbers, and name the trade-off.

Question of this lab: a farm wants an offline assistant on a Raspberry Pi 5
in a greenhouse. The workers type questions about the manual of the
greenhouse controller. The first word of the answer must appear in less
than 10 seconds. Which model and which quantization level do you select?
Which context and which k? Which part of the job does not need a language
model?

## Published values

Use these values to compare. They are not measurements of this course.

| Model | Prompt eval rate | Eval rate | Source |
|---|---|---|---|
| `llama3.2:1b` | 19.46 tokens/s | 8.99 tokens/s | Lab "Small Language Models" of "Machine Learning Systems", Raspberry Pi 5 |
| `llama3.2:3b` | not stated | 5.3 tokens/s | The same lab |
| `llava-phi3:3.8b`, one image | not stated | almost 4 minutes for one description | The same lab |

The guide "SLMs at the Edge" gives 8 to 10 tokens/s as the rate for a chat
that a person reads.

## If a part does not work

| Problem | Fallback |
|---|---|
| A task is not complete in time | Use the file of the folder `solutions/`, and write this in the report |
| A model is not on the card | `ollama pull <model>` needs the network and some minutes. Ask the instructor for the card of a second group. |
| The image option is too slow | Run two images only, with `--image part_c/images/000000166277.jpg`, and write this in the report |
| The Raspberry Pi is not available | Run the scripts on a laptop with Ollama. Write the name of the processor in the report. The rates then say nothing about the board. |

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'ollama'` | The environment is not active | `source ~/ollama/bin/activate` |
| `ConnectionError` or `Failed to connect to Ollama` | The Ollama service does not run | `sudo systemctl start ollama` |
| `SKIP llama3.2:3b: not downloaded` | The model is not on the card | See the table above |
| The first request needs many seconds | Ollama loads the model from the card | This is normal. The script does not count this request. |
| The rate falls during a long run | The temperature limits the clock | Check the cooler. Run `vcgencmd get_throttled`, and write the value in the report. |
| The board is very slow, and `free -m` shows swap | The model and the context need too much RAM | Use a smaller context or the 1B model |
| `not valid` for an answer | The answer is longer than the token limit, or a schema has no limits | Check the class of the task. For the image option, the limits of Task C2 are necessary. |
| The answer is valid but wrong | A schema makes the output valid, not correct | Write the case in the report. This is a result. |
| A tool call prints `REFUSED: unknown room None` | The model made a call with a wrong structure | Your guard works. Write the case in the report. |

## Credits

This lab adapts material from these sources:

- The lab "Small Language Models" of "Machine Learning Systems" by Vijay
  Janapa Reddi and contributors (mlsysbook.ai, CC BY-NC-SA 4.0): the models
  `llama3.2:1b`, `llama3.2:3b`, and `llava-phi3:3.8b`, the counters of
  `ollama run --verbose`, the first three prompts of `prompts.txt`, and the
  published rates.
- The guide "SLMs at the Edge" of "EdgeML with Raspberry Pi" by Marcelo
  Rovai (github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0): the rate for
  a chat and the advice for the context and the threads.
- The chapter "SLM: Basic Optimization Techniques" of "Edge AI Engineering:
  Raspberry Pi" by Marcelo Rovai, and the notebooks
  `20-Ollama_Function_Calling_Pydantic.ipynb`,
  `30-Function_Calling_with_images.ipynb`, and `40-RAG-simple-bee.ipynb` of
  "EdgeML with Raspberry Pi" (GPL-3.0): Pydantic with Ollama, the
  tool-calling loop, and the steps of a RAG system.
- The documentation of Ollama (github.com/ollama/ollama, MIT): the API, the
  options, and the timing fields.
- COCO 2017 (cocodataset.org): the five test images and their annotations.
  Each image has the licence CC BY 2.0 of its author on Flickr.
  `part_c/images/README.md` gives the Flickr address of each image.

The scripts, the commands, the tools, the guard, the facts of the
greenhouse controller, and the questions are new work of this course.
