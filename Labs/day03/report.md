# Day 3 lab report

Group:

Names:

Date:

Dataset: your own recordings of Day 2, the recordings of a different group,
or the fallback dataset.

## Part A: train

Versions:

| Tool | Version |
|---|---|
| Python | |
| `tensorflow` | |
| `keras` | |

| Item | Your result |
|---|---|
| Training windows and test windows | |
| Test sessions | |
| Training accuracy in percent | |
| Test accuracy in percent | |

The confusion matrix of the test set (rows: real class):

| Real class | idle | terrestrial | lift | maritime |
|---|---|---|---|---|
| idle | | | | |
| terrestrial | | | | |
| lift | | | | |
| maritime | | | | |

### Features against the raw window (task 3)

Write the prediction before you run section 6 of the notebook.

| Question | Your prediction | Result |
|---|---|---|
| Parameters of the model with the raw window | | |
| The input with the higher test accuracy | | |
| The reason | | |

The table of section 6:

| Input | Values | Parameters | Test accuracy for each test session | Mean |
|---|---|---|---|---|
| Features | 63 | | | |
| Raw window | 300 | | | |

Your answers:

1. Compare the result with your prediction.
2. Which input needs less flash on the board? Which input needs less RAM?
   Give the numbers.
3. The raw window needs no feature code on the board. Is this a reason to
   select it? Use your accuracy numbers.

## Part B: convert and deploy

| Item | Your result |
|---|---|
| Size of the LiteRT file in bytes | |
| Operator types of the model | |
| Largest difference between Keras and LiteRT | |
| Peak of the activations in bytes (task 5) | |
| The arena size that you try first (task 5) | |
| `Sketch uses ... bytes` of the first build, before tasks B1 to B4 | |
| Result of the self-test on the board | |

The demonstration:

| Motion that you make | Class that the board shows most of the time |
|---|---|
| idle | |
| terrestrial | |
| lift | |
| maritime | |

## Part C: measure

Prediction before the measurement. Is the inference faster, slower, or equal
when the arena is in the PSRAM?

- Your prediction:

| Number | PSRAM disabled, arena in the internal RAM | OPI PSRAM, arena in the PSRAM |
|---|---|---|
| `Sketch uses ... bytes` (flash) | | |
| Model size in bytes | | |
| Flash that the runtime and the inference code add | | not necessary |
| Arena used in bytes | | |
| `features_us`: median and maximum | | |
| `invoke_us`: median and maximum | | |
| `late_samples` after 20 lines | | |

- The message of the Serial Monitor with `kTensorArenaSize = 1024`:
- Your estimate of the arena (task 5) and the measured value. Explain the
  difference in one sentence:

## Part D: compare with Edge Impulse

Write "measured" or "estimate" next to each number of the second column.

| Number | Your sketch with TensorFlow Lite Micro | Library of Edge Impulse |
|---|---|---|
| Test accuracy in percent | | |
| Flash: `Sketch uses ... bytes` | | |
| RAM: arena used, or peak RAM of the Studio | | |
| Time for the features (DSP) | | |
| Time for the inference (classification) | | |
| Kernels | reference kernels | |
| Who wrote the feature code and the inference code | | |

## Decision Log

About 100 words. A product must classify the motion of a package for one
year with a battery. Which path do you select for the firmware: your own
sketch with TensorFlow Lite Micro, or the library of Edge Impulse? State the
decision, give your numbers for the flash, the RAM, and the latency, and name
the trade-off.

## Problems

Write each problem that you had, and how you solved it.
