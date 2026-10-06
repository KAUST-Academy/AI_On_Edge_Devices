# HW-05: Small language models on the Raspberry Pi 5

Needed by: the Day 10 lab (run and measure, Python integration, application).

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

1. Write the Ollama version in `Labs/VERSIONS.md`.
2. Write the measured numbers in the Day 10 lab `README.md`, next to the
   published numbers.
3. If a model is too slow for the lab time, replace it.
