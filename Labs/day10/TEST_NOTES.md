# Test notes: Day 10 lab

## 1. Checklist for the instructor

- Date of the test:
- Ollama version, and the versions of `ollama` and `pydantic` in
  `~/ollama`:
- Room temperature, and cooler type:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Part A, step 1: `ollama list` and `ollama run llama3.2:1b --verbose` | The four models. The prompt eval rate and the eval rate. | |
| 2 | Part A, step 4: `python solutions/measure_slm.py` | The two lines of the table. The time of the step. | |
| 3 | Part A, step 5: the five commands | Model MB for 2048 and 8192 tokens. The eval rate for 1, 2, and 4 threads. | |
| 4 | Part B: the four runs of `solutions/part_b/structured.py` | Valid and correct for each run. | |
| 5 | Part B: `solutions/part_b/tools.py` for the two models | The refused calls | |
| 6 | Part C, option 1: `solutions/part_c/rag.py` with k = 1, 2, 4 | Valid, correct, prompt tokens, time for one question | |
| 7 | Part C, option 2: `solutions/part_c/describe_image.py` | Time for each image. Valid answers. | |
| 8 | During step 7: `vcgencmd measure_temp` and `vcgencmd get_throttled` | The highest temperature, and the throttle state | |
| 9 | Time the complete lab with one student group, or alone | Minutes for each part | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|
| | | |
