# HW-05: Small language models on the Raspberry Pi 5

Hardware status: not tested on hardware (prepared on 2026-10-01)

Needed by: the Day 10 lab (run and measure, Python integration, application).

## Decision

| Topic | Decision |
|---|---|
| Runtime | Ollama |
| Model 1 (small) | `llama3.2:1b`: Llama 3.2, 1.2 billion parameters, Q8_0, 1.32 GB download |
| Model 2 (large) | `llama3.2:3b`: Llama 3.2, 3.2 billion parameters, Q4_K_M, 2.02 GB download |
| Measurement | `measure_slm.py` of this folder, with the five prompts of `prompts.txt` |
| Models for Part C (not fixed) | `nomic-embed-text` for retrieval-augmented generation, `llava-phi3:3.8b` for image description. The Day 10 lab task makes the final selection. |

The tag, the quantization, and the download size come from the Ollama library
(read on 2026-10-01).

## Reason

- Both models are in the kit lab of the book. The author ran them on a
  Raspberry Pi 5 and published the speed. The lab then has reference numbers.
- The two models are from one family. The size is the main difference. A
  student can then explain the speed difference with the size.
- The two models have different quantization levels (Q8_0 and Q4_K_M). This
  gives an example for Block 1 of the Day 10 theory: disk size is parameters
  times bits per weight.
- The guide gives 8 to 10 tokens per second as the limit for a chat that
  feels fluent. The published speed of the small model is near this limit,
  and the large model is below it. The lab shows both sides of the limit.
- Both models fit in 8 GB with a large margin. The rule of the guide is:
  usable model size = (total RAM − operating system and applications) × 0.7.
- Llama 3.2 supports tool calls in Ollama. Part B (structured output and
  function calling) uses the same models.
- Ollama needs one command to install and one command for each model. The
  guide recommends Ollama first on the Raspberry Pi 5, and llama.cpp "for the
  last 10 percent". Module GA-4 covers llama.cpp.

## Published numbers

Use these numbers as the reference. They are not measurements of this course.

**Source 1: lab "Small Language Models" of "Machine Learning Systems"
(Raspberry Pi 5, Ollama, one short prompt).**

| Model | Quantization and size in the source | Prompt eval rate | Eval rate |
|---|---|---|---|
| `llama3.2:1b` | Q8_0, 1.3 GB | 19.46 tokens/s | 8.99 tokens/s |
| `llama3.2:3b` | Q4_0, 2 GB | not stated | 5.3 tokens/s |
| `gemma2:2b` | Q4_0, 1.6 GB | not stated | "around the same performance as Llama 3.2:3B" |
| `phi3.5:3.8b` | Q4_0, 2.2 GB of RAM | not stated | 2.25 tokens/s |
| `llava-phi3:3.8b` (text prompt) | not stated | not stated | 3.93 tokens/s |

The same lab reports for the Raspberry Pi 5:

- All four CPU cores run at almost 100 percent during inference.
- The memory in use is 3.24 GB with a 3.8-billion-parameter model loaded. It
  is about 377 MB after Ollama stops (no desktop).
- One image description with `llava-phi3:3.8b` took almost 4 minutes.

**Source 2: guide "SLMs at the Edge" of "EdgeML with Raspberry Pi", section 5.1
(speed compiled from published Raspberry Pi 5 benchmarks, CPU only, short
context).**

| Model | Quantization | RAM | Generation speed |
|---|---|---|---|
| Llama 3.2 1B | Q4_K_M | about 1 GB | 8 to 20 tokens/s |
| Llama 3.2 3B | Q4_K_M | about 2.2 GB | 2 to 5 tokens/s |

The guide also says: a Raspberry Pi 5 that reduces its clock speed because of
heat loses 20 to 30 percent of its speed. Install the active cooler.

**Difference between the sources.** The Ollama tag `llama3.2:1b` is Q8_0. The
guide gives its numbers for Q4_K_M. The numbers of source 1 fit the tag of
this course.

## Sources

| Item | Source |
|---|---|
| Models, published speed, memory, temperature command | `kits/contents/raspi/llm/llm.qmd` of "Machine Learning Systems" |
| Model table, RAM rule, token speed limit, checklist | `A_Guide_to_Local_Inference/README.md` of "EdgeML with Raspberry Pi", sections 2, 5, 7, and 8 |
| Install command of Ollama | The same guide, section 5.1 |
| Tags, quantization, download sizes | Ollama library, `registry.ollama.ai` (read on 2026-10-01) |

## Files

| File | Content |
|---|---|
| `pull_models.sh` | Downloads the two models. With `extras`: also the two models for Part C. |
| `measure_slm.py` | Measures load time, prompt rate, generation rate, model memory, and CPU temperature |
| `prompts.txt` | Five prompts. The first three come from the kit lab. |

## Steps

### 1. Download the models

`setup_pi.sh` of `HW-04` installs Ollama. Then, on the master card:

```bash
bash pull_models.sh            # 3.3 GB
bash pull_models.sh extras     # 3.2 GB more, for Part C
```

Do this before the copy of the master card. The lab then needs no download.

### 2. Run one model by hand

```bash
ollama run llama3.2:1b --verbose
```

Enter `What is the capital of France?`. Ollama prints the answer and then
the counters: total duration, load duration, prompt eval rate, eval rate.
Enter `/bye` to stop.

### 3. Measure both models

```bash
source ~/ollama/bin/activate
python3 measure_slm.py --csv results.csv
```

The script prints one row for each model:

```
model                load s prompt tok/s   eval tok/s  min tok/s   model MB         temp C
```

- `eval tok/s` is the generation speed. Compare it with 8 tokens per second.
- `model MB` is the memory that Ollama reports for the loaded model.
- `temp C` is the CPU temperature before and after the model.

Options:

- `--num-predict 256` permits longer answers. The temperature then goes up
  more.
- `--num-ctx 2048` sets the context length. Day 10 uses this option to show
  the cost of the KV cache.
- `--models llama3.2:3b` measures one model.

### 4. Watch the system

In a second terminal:

```bash
htop
watch -n 1 vcgencmd measure_temp
```

If `vcgencmd get_throttled` does not print `throttled=0x0`, the Raspberry Pi
reduced its speed or had low voltage. The result is then not valid.

## Estimate before you measure

Day 10 asks the students for an estimate first. The numbers below use only
the parameters and the bits per weight. They are estimates, not measurements.

| Model | Parameters | Bits per weight | Weights = parameters × bits / 8 |
|---|---|---|---|
| `llama3.2:1b` (Q8_0) | 1.24 billion | 8 | about 1.24 GB |
| `llama3.2:3b` (Q4_K_M) | 3.2 billion | about 4.5 to 5 | about 1.8 to 2.0 GB |

The download sizes are 1.32 GB and 2.02 GB. The RAM in use is larger than the
weights: add the KV cache, the runtime, and the operating system.

## Code status

| File | State | Source | Change |
|---|---|---|---|
| `pull_models.sh` | new | Model names from the kit lab | not tested on a Raspberry Pi |
| `measure_slm.py` | new | Metrics of `ollama run --verbose` from the kit lab | Tested on the work computer with Ollama 0.32.6, the library `ollama` 0.6.3, and the model `phi3:mini`: the script runs, skips a model that is not downloaded, and writes the CSV file. Not tested on a Raspberry Pi. |
| `prompts.txt` | new | Prompts 1 to 3 from the kit lab | none |

The work computer has no `vcgencmd`. The temperature then comes from
`/sys/class/thermal/thermal_zone0/temp`. On the Raspberry Pi, the script uses
`vcgencmd measure_temp` first.

## Test steps for the instructor

- Date of the test:
- Ollama version (`ollama --version`):
- Room temperature, and cooler type:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run step 1 | Download time of each model on the lab network. Free space of the card after the download. | |
| 2 | Run step 2 for both models | Prompt eval rate and eval rate. Compare with source 1 (8.99 and 5.3 tokens/s). | |
| 3 | Run step 3 three times | The table of each run. Is the eval rate stable between the runs? | |
| 4 | Read `free -m` with each model loaded and with no model | RAM in use for each state | |
| 5 | Run step 3 with `--num-predict 512` and watch the temperature | Maximum temperature. The output of `vcgencmd get_throttled`. | |
| 6 | Run step 3 with `--num-ctx 2048` and with `--num-ctx 16384` | `model MB` for both context lengths | |
| 7 | In Python, call `ollama.chat` with a `format` schema and with one tool, for both models | Does each model give valid JSON for five prompts? | |
| 8 | Run `ollama run llava-phi3:3.8b` with one image | Time for one image description | |
| 9 | Time the complete Part A with one student group, or alone | Minutes. The plan is 45 minutes. | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## After the test

1. Change the line `Hardware status:` to `tested on hardware (YYYY-MM-DD)`.
2. Write the Ollama version in `Labs/VERSIONS.md`.
3. Write the measured numbers in the Day 10 lab `README.md`, next to the
   published numbers.
4. If a model is too slow for the lab time, replace it. The guide lists other
   models in section 7. Model names change quickly: confirm that the tags
   still exist before each course.

## Credits

The models, the metrics, and the published numbers come from the lab "Small
Language Models" of "Machine Learning Systems" by Vijay Janapa Reddi and
contributors (mlsysbook.ai, CC BY-NC-SA 4.0) and from the guide "SLMs at the
Edge" of "EdgeML with Raspberry Pi" by Marcelo Rovai
(github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0).
