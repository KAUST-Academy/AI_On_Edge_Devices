# Test notes: Day 10 lab

This file has two parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `measure_slm.py`, `solutions/measure_slm.py` | new | `Labs/hardware/HW-05/measure_slm.py` of this course | New: the method of Day 9 (a load request and a warm-up request that the script does not count, 10 timed requests, the median), the options `--num-ctx`, `--num-thread`, `--runs`, and `--memory-only`, and the highest temperature during the run. The student version has no body in the function `token_rate` (Task A1). |
| `part_b/structured.py`, `solutions/part_b/structured.py` | new | Pydantic with Ollama: notebook `20-Ollama_Function_Calling_Pydantic.ipynb` of "EdgeML with Raspberry Pi" | The student version has `str` for the three fields of `Command` (Task B1) |
| `part_b/tools.py`, `solutions/part_b/tools.py` | new | The tool-calling loop of the chapter "SLM: Basic Optimization Techniques" | The tools and the guard are new. The student version has no rule in `check_call` (Task B2). The sensor values are simulated. |
| `part_c/rag.py`, `solutions/part_c/rag.py` | new | The steps of the notebook `40-RAG-simple-bee.ipynb` | No vector database: the script keeps the 12 vectors in a list. The student version has no body in `cosine` and `top_k` (Task C1). |
| `part_c/describe_image.py`, `solutions/part_c/describe_image.py` | new | The model and the image prompt of the lab "Small Language Models" | The schema with the limits is new. The student version has no limits in `Scene` (Task C2). |
| `prompts.txt` | copied | `Labs/hardware/HW-05/prompts.txt` | The first comment line |
| `part_b/commands.txt`, `part_b/tool_prompts.txt`, `part_c/facts.txt`, `part_c/questions.txt` | new | none | none |
| `part_c/images/*.jpg` | copied with no change | COCO 2017 validation set, licence CC BY 2.0 | none |

### Test on the work computer of the course (2026-10-03)

Ollama 0.32.6, the Python packages `ollama` 0.6.3 and `pydantic` 2.13.5,
Python 3.10, an x86 processor with 24 cores. Each run used `EDGEAI_CPU=1`,
so the models ran on the CPU. The times say nothing about a Raspberry Pi.

| Script | Model | Result |
|---|---|---|
| `solutions/measure_slm.py --num-thread 4` | both | `Task A1: complete`. 10 timed requests for each model. Model memory 1450 MB (1B) and 2325 MB (3B). 38.4 prompt tokens on average. |
| `solutions/measure_slm.py --memory-only --models llama3.2:3b` | 3B | 2325 MB with `--num-ctx 2048`, 3119 MB with `--num-ctx 8192` |
| `solutions/part_b/structured.py` | 1B | valid 10 of 10, correct 8 of 10 |
| `solutions/part_b/structured.py --no-schema` | 1B | valid 0 of 10: each answer is in a Markdown code block |
| `solutions/part_b/structured.py` | 3B | valid 10 of 10, correct 10 of 10 (also with `--no-schema`) |
| `solutions/part_b/tools.py` | 1B | 3 calls ran. 2 calls refused: a call with a wrong structure, and 300 degrees. |
| `solutions/part_b/tools.py` | 3B | 4 calls ran. 1 call refused: 300 degrees. |
| `solutions/part_c/rag.py` | 1B | valid structured output 5 of 5, correct 4 of 5 |
| `solutions/part_c/rag.py` | 3B | valid structured output 5 of 5, correct 5 of 5 |
| `solutions/part_c/describe_image.py` | `llava-phi3:3.8b` | valid structured output 5 of 5. 618 prompt tokens for each image. |
| The five student scripts | none | Each one prints its message "Task ... is not complete" and stops |

Without the limits of Task C2, the models wrote until the token limit for
some images: `llava-phi3:3.8b` for 1 of 5 images (a very long object text),
and `moondream` for 1 of 2 images (a repeated list item). The JSON was then
not valid. With the limits, the five answers were valid. `moondream`
gave very short captions ("coffee", "glass"). The lab uses
`llava-phi3:3.8b`, the model of `Labs/hardware/HW-05/`.

Points that only a Raspberry Pi 5 can confirm:

- All rates, load times, and temperatures, and the output of
  `vcgencmd get_throttled`.
- The time of one image with `llava-phi3:3.8b`. The source published
  "almost 4 minutes" for one long description. The README gives 1 to 4
  minutes for each image as an estimate.
- The time of each part, mainly step 4 of Part A and option 2 of Part C.
- The memory of the four models on the card, and the free memory with the
  3B model and a context of 8192 tokens.
- The default thread count of Ollama on the board.

## 2. Checklist for the instructor

- Date of the test:
- Ollama version, and the versions of `ollama` and `pydantic` in
  `~/ollama`:
- Room temperature, and cooler type:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Part A, step 1: `ollama list` and `ollama run llama3.2:1b --verbose` | The four models. The prompt eval rate and the eval rate. | |
| 2 | Part A, step 4: `python solutions/measure_slm.py` | The two lines of the table. The time of the step. | |
| 3 | Part A, step 5: the five commands | Model MB for 2048 and 8192 tokens. The eval rate for 1, 2, and 4 threads. | |
| 4 | Part B: the four runs of `solutions/part_b/structured.py` | Valid and correct for each run. Compare with Part 1 of this file. | |
| 5 | Part B: `solutions/part_b/tools.py` for the two models | The refused calls | |
| 6 | Part C, option 1: `solutions/part_c/rag.py` with k = 1, 2, 4 | Valid, correct, prompt tokens, time for one question | |
| 7 | Part C, option 2: `solutions/part_c/describe_image.py` | Time for each image. Valid answers. | |
| 8 | During step 7: `vcgencmd measure_temp` and `vcgencmd get_throttled` | The highest temperature, and the throttle state | |
| 9 | Time the complete lab with one student group, or alone | Minutes for each part | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|
| | | |
