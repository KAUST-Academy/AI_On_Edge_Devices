# Day 10 lab report

Group: ......  Names: ......  Date: ......

Raspberry Pi: `pi-NN`. Ollama version (`ollama --version`): ......

## Part A: run and measure

### First test with `ollama run llama3.2:1b --verbose`

| Counter | Value |
|---|---|
| prompt eval rate | |
| eval rate | |

### Estimate before the measurement

Use Part 1 of the lecture. KV cache in `f16`: bytes = 2 x layers x KV heads
x head size x context x 2. `llama3.2:1b`: 16 layers, 8 KV heads, head size
64. `llama3.2:3b`: 28 layers, 8 KV heads, head size 128.

| Model | File (GB) | KV cache, 2048 tokens (GB) | KV cache, 8192 tokens (GB) | Weights + KV cache, 2048 tokens (GB) |
|---|---|---|---|---|
| `llama3.2:1b` | 1.32 | | | |
| `llama3.2:3b` | 2.02 | | | |

### The method of the measurement

| Part of the method | Your value |
|---|---|
| Requests that the script does not count | |
| Timed requests for each model | |
| Statistic | |
| Context and largest answer | |
| Threads | |
| The window: what the counters of Ollama measure | |

### Benchmark table

Copy the lines of `python measure_slm.py`.

| Model | Threads | Load s | Prompt tokens | Prompt tokens/s (median) | Eval tokens/s (median) | Eval tokens/s (lowest) | Model MB | Temperature C (start -> highest) | Throttled |
|---|---|---|---|---|---|---|---|---|---|
| `llama3.2:1b` | | | | | | | | | |
| `llama3.2:3b` | | | | | | | | | |

### Context and threads

| Measurement | Value |
|---|---|
| `llama3.2:3b`, `--num-ctx 2048`: model MB | |
| `llama3.2:3b`, `--num-ctx 8192`: model MB | |
| Difference in MB, and your estimate of the difference | |
| `llama3.2:1b`, 1 thread: eval tokens/s | |
| `llama3.2:1b`, 2 threads: eval tokens/s | |
| `llama3.2:1b`, 4 threads: eval tokens/s | |

### Questions

1. Compare your eval rates with the published rates of the README. Give
   one reason for a difference.
2. Multiply the file size of each model by its eval rate. Are the two
   products similar? What does this tell you about the limit of the
   generation (Part 1 of the lecture)?
3. Which model is fast enough for a chat that a person reads (8 to 10
   tokens/s)?
4. How much faster are 4 threads than 1 thread? Is the gain 4 times? Why?

## Part B: Python integration

### Structured output (`part_b/structured.py`, 10 commands)

| Model | Mode | Valid | Correct | Median time (s) |
|---|---|---|---|---|
| `llama3.2:1b` | with the schema | | | |
| `llama3.2:1b` | prompt only | | | |
| `llama3.2:3b` | with the schema | | | |
| `llama3.2:3b` | prompt only | | | |

### Function calls (`part_b/tools.py`, 5 requests)

| Model | Calls that ran | Calls that were refused, with the reason |
|---|---|---|
| `llama3.2:1b` | | |
| `llama3.2:3b` | | |

### Questions

1. Which commands gave a valid answer with a wrong value? Why can a schema
   not prevent this?
2. Why did the prompt-only mode fail for one model? Which small change in
   the program would accept these answers? Is this change safe?
3. Your function `check_call` refused a call. What can happen in a real
   house without this check?

## Part C: application

Option that you selected (1 or 2): ......

### Option 1: retrieval-augmented generation

| Model | k | Valid (of 5) | Correct (of 5) | Prompt tokens (mean) | Time for one question (s) |
|---|---|---|---|---|---|
| `llama3.2:1b` | 1 | | | | |
| `llama3.2:1b` | 2 | | | | |
| `llama3.2:1b` | 4 | | | | |
| `llama3.2:3b` | 2 | | | | |

Your three facts, your question, and the answer: ......

### Option 2: image description

| Image | Time (s) | Valid | Caption | Containers of the model | Cups and bottles of COCO |
|---|---|---|---|---|---|
| `000000132329.jpg` | | | | | 4 |
| `000000166277.jpg` | | | | | 3 |
| `000000333772.jpg` | | | | | 1 |
| `000000347335.jpg` | | | | | 2 |
| `000000429598.jpg` | | | | | 1 |

### Questions

1. Option 1: does a larger k give more correct answers? What does it cost
   on the board? Option 2: how many prompt tokens does one image give, and
   what does this mean for the time to the first token?
2. Is the output of your application correct, or only valid? Give one
   example.
3. Estimate the energy of one answer of your application with the heavy
   load range of Day 9 (7 to 10 W).

## Decision Log

Write about 100 words: one decision, your measured numbers with their
method, and one trade-off.

......
