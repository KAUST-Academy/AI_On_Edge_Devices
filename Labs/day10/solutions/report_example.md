# Day 10 lab report: example

This example has the parts of the report that need no board: the
estimates, the method, and the counts of valid and correct answers. The
counts come from a run of the scripts (Ollama 0.32.6, CPU only,
temperature 0). The counts depend on the model file and the settings, so
your counts are probably the same or near. A rate, a temperature, and a
time on a Raspberry Pi are values of the board. These cells have the text
"measure in the lab".

## Part A: run and measure

### Estimate before the measurement

| Model | File (GB) | KV cache, 2048 tokens (GB) | KV cache, 8192 tokens (GB) | Weights + KV cache, 2048 tokens (GB) |
|---|---|---|---|---|
| `llama3.2:1b` | 1.32 | 0.067 | 0.268 | 1.39 |
| `llama3.2:3b` | 2.02 | 0.235 | 0.940 | 2.25 |

The calculation for the 3B model: 2 x 28 x 8 x 128 x 2 = 114 688 bytes for
each token. 114 688 x 2048 = 0.235 GB.

### The method of the measurement

| Part of the method | Value |
|---|---|
| Requests that the script does not count | One request that loads the model, one request to warm up |
| Timed requests for each model | 10: the five prompts of `prompts.txt`, two times |
| Statistic | The median of the rates, and the lowest rate |
| Context and largest answer | 2048 tokens, 128 tokens |
| Threads | The choice of Ollama (step 4), then 1, 2, and 4 (step 5) |
| The window: what the counters of Ollama measure | The model only: the prompt evaluation and the generation. Not the HTTP time and not the Python time. |

### Benchmark table

| Model | Threads | Load s | Prompt tokens | Prompt tokens/s (median) | Eval tokens/s (median) | Eval tokens/s (lowest) | Model MB | Temperature C (start -> highest) | Throttled |
|---|---|---|---|---|---|---|---|---|---|
| `llama3.2:1b` | default | measure in the lab | 38.4 | measure in the lab | measure in the lab | measure in the lab | 1450 | measure in the lab | measure in the lab |
| `llama3.2:3b` | default | measure in the lab | 38.4 | measure in the lab | measure in the lab | measure in the lab | 2325 | measure in the lab | measure in the lab |

The prompt tokens and the model memory do not depend on the computer. The
values are from the solution scripts.

### Context and threads

| Measurement | Value |
|---|---|
| `llama3.2:3b`, `--num-ctx 2048`: model MB | 2325 |
| `llama3.2:3b`, `--num-ctx 8192`: model MB | 3119 |
| Difference in MB, and your estimate of the difference | 794 MB measured. Estimate: 114 688 x 6144 = 705 MB. The buffers of the runtime also grow a little. |
| `llama3.2:1b`, 1, 2, and 4 threads: eval tokens/s | measure in the lab |

### Answers

1. Measure in the lab. Reasons for a difference: the context, the length of
   the answer, the temperature of the board, the Ollama version, and the
   prompt.
2. The published values give 1.32 x 8.99 = 11.9 GB/s and 2.02 x 5.3 = 10.7
   GB/s. The two products are similar: the reading of the weights limits
   the generation. Your products are probably similar too.
3. With the published values, only the 1B model is near 8 to 10 tokens/s.
4. Measure in the lab. The gain is smaller than 4 times: the four cores
   share the memory bandwidth (Part 2 of the lecture).

## Part B: Python integration

### Structured output (10 commands)

| Model | Mode | Valid | Correct | Median time (s) |
|---|---|---|---|---|
| `llama3.2:1b` | with the schema | 10 | 8 | measure in the lab |
| `llama3.2:1b` | prompt only | 0 | 0 | measure in the lab |
| `llama3.2:3b` | with the schema | 10 | 10 | measure in the lab |
| `llama3.2:3b` | prompt only | 10 | 10 | measure in the lab |

### Function calls (5 requests)

| Model | Calls that ran | Calls that were refused, with the reason |
|---|---|---|
| `llama3.2:1b` | 3 | 2: the call for the office temperature had a wrong structure (`unknown room None`), and the heater at 300 degrees (`outside 5 to 30`) |
| `llama3.2:3b` | 4 | 1: the heater at 300 degrees |

### Answers

1. The 1B model made "It is too dark in the bedroom" into `lamp off
   bedroom`, and "The office is cold" into `heater off office`. The schema
   allows only valid values, and `off` is a valid value. The schema cannot
   check the meaning.
2. The 1B model put each JSON object into a Markdown code block (three
   back quotes). A program can remove the code block first. This is safe
   only if the program still checks the result with the schema.
3. The heater runs at its highest power, or the controller does an action
   that nobody asked for. The check in the code is the safety rule, not the
   prompt.

## Part C: application

### Option 1: retrieval-augmented generation (k = 2)

| Model | k | Valid (of 5) | Correct (of 5) | Prompt tokens (mean) | Time for one question (s) |
|---|---|---|---|---|---|
| `llama3.2:1b` | 2 | 5 | 4 | 109 | measure in the lab |
| `llama3.2:3b` | 2 | 5 | 5 | 109 | measure in the lab |

The 1B model answered the first question with fact 2 ("below 27 degrees")
and not with fact 1. Retrieval put fact 2 first, and the two facts are
similar. The check of the script looks only for the number: the answer
"Below 42% soil moisture" counts as correct, but the fact says "above". Read
each answer.

### Option 2: image description

| Image | Time (s) | Valid | Caption | Containers of the model | Cups and bottles of COCO |
|---|---|---|---|---|---|
| `000000132329.jpg` | measure in the lab | yes | A refrigerator with two shelves and three water bottles on top. | 3 | 4 |
| `000000166277.jpg` | measure in the lab | yes | A cat drinking from a glass on a table. | 2 | 3 |
| `000000333772.jpg` | measure in the lab | yes | Two cats lounging on a desk in front of an Apple computer. | 0 | 1 |
| `000000347335.jpg` | measure in the lab | yes | A plate with eggs benedict on top of hash browns. | 0 | 2 |
| `000000429598.jpg` | measure in the lab | yes | A kitchen with brick walls and wooden cabinets. | 0 | 1 |

Each image gave 618 prompt tokens. The captions are good. The count is
wrong for all five images: a vision-language model is not a counter. For a
count, use a detector (Day 8).

### Answers

1. Option 1: k = 4 gives a longer prompt. At the published prompt rate of
   19.46 tokens/s, each 100 more tokens cost about 5 s. Option 2: 618
   tokens at 19.46 tokens/s is about 32 s before the first token. This is
   an estimate with the rate of a text model.
2. See the two examples above.
3. Example: 15 s at 7 to 10 W gives 105 to 150 J. Use your measured time.

## Decision Log

An example of the form. Replace each text in brackets with your numbers.

Decision: the greenhouse assistant uses `llama3.2:1b` (`Q8_0`) with
retrieval, k = 2, and a context of 2048 tokens. The rules of the controller
(the window, the irrigation) stay in the controller: they need no language
model.

Numbers: the 1B model generates [median] tokens/s and the prompt of a
question has about 109 tokens: [time] s to the first token, below the limit
of 10 s. The 3B model was correct 5 times out of 5 and the 1B model 4 times,
but the 3B model needs [time] s.

Trade-off: the 1B model is fast enough, but it confused two similar facts.
The program shows the number of the fact with each answer, so that a worker
can check the source.
