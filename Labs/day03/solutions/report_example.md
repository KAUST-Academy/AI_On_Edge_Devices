# Day 3 lab report: example

This example has the parts of the report that need no board. The numbers of
Parts A and B come from the solution notebook with the fallback dataset of
Day 2. The signals of the fallback dataset are simulated. The flash
numbers come from the compiler. The parts that need a board say "measure in
the lab".

Group: example

Dataset: the fallback dataset.

## Part A: train

| Item | Your result |
|---|---|
| Training windows and test windows | 1312 and 656 |
| Test sessions | `s3` |
| Training accuracy in percent | 100.0 |
| Test accuracy in percent | 100.0 |

The confusion matrix of the test set (rows: real class):

| Real class | idle | terrestrial | lift | maritime |
|---|---|---|---|---|
| idle | 164 | 0 | 0 | 0 |
| terrestrial | 0 | 164 | 0 | 0 |
| lift | 0 | 0 | 164 | 0 |
| maritime | 0 | 0 | 0 | 164 |

A result of 100.0 percent comes from the simulated signals. Real recordings
give a lower value.

### Features against the raw window (task 3)

| Question | Your prediction | Result |
|---|---|---|
| Parameters of the model with the raw window | 6274 | 6274 |
| The input with the higher test accuracy | features | features |
| The reason | The features do not change when the window starts later | The raw window fails for one session |

The table of section 6:

| Input | Values | Parameters | Test accuracy for each test session | Mean |
|---|---|---|---|---|
| Features | 63 | 1534 | 100.0, 100.0, and 100.0 percent | 100.0 percent |
| Raw window | 300 | 6274 | 100.0, 54.0, and 100.0 percent | 84.7 percent |

Answers:

1. The prediction was correct. The model with the raw window has 6274
   parameters and fails for the test session `s2`.
2. The features need less flash and less RAM. The weights need
   1534 x 4 = 6136 bytes against 6274 x 4 = 25 096 bytes. The peak of the
   activations is 63 x 4 + 80 = 332 bytes against 300 x 4 + 80 = 1280
   bytes.
3. No. The raw window gives a larger model and a result that depends on the
   session. The feature code costs some flash and some time, and it makes
   the model smaller and more stable.

## Part B: convert and deploy

| Item | Your result |
|---|---|
| Size of the LiteRT file in bytes | 8328 |
| Operator types of the model | FULLY_CONNECTED and SOFTMAX |
| Largest difference between Keras and LiteRT | 1.79e-07 |
| Peak of the activations in bytes (task 5) | 252 + 80 = 332, in the first operator |
| The arena size that you try first (task 5) | 4096 |
| `Sketch uses ... bytes` of the first build, before tasks B1 to B4 | 311 297 (result of the compiler with the core 3.3.12) |
| Result of the self-test on the board | measure in the lab |

The demonstration: measure in the lab.

## Part C: measure

An example of a prediction: the inference is slower with the arena in the
PSRAM, because each access to the PSRAM goes through a serial bus (Part 1 of
the Day 2 lecture).

| Number | PSRAM disabled, arena in the internal RAM | OPI PSRAM, arena in the PSRAM |
|---|---|---|
| `Sketch uses ... bytes` (flash) | 364 005 (result of the compiler) | 369 323 (result of the compiler) |
| Model size in bytes | 8328 | 8328 |
| Flash that the runtime and the inference code add | 364 005 - 311 297 = 52 708 | not necessary |
| Arena used in bytes | measure in the lab | measure in the lab |
| `features_us`: median and maximum | measure in the lab | measure in the lab |
| `invoke_us`: median and maximum | measure in the lab | measure in the lab |
| `late_samples` after 20 lines | measure in the lab | measure in the lab |

- The message of the Serial Monitor with `kTensorArenaSize = 1024`: measure
  in the lab. The library prints a line of the form
  `Failed to resize buffer. Requested: ..., available ..., missing: ...`,
  and the sketch prints `ERROR: AllocateTensors() failed. The arena is too
  small.`
- The estimate and the measured value: the estimate of 332 bytes holds only
  the activations. The arena also holds the data of the interpreter for each
  tensor and each operator, so the measured value is larger.

## Part D: compare with Edge Impulse

Measure in the lab. The column of your sketch takes its numbers from Part C.

## Decision Log

An example. Replace each `...` with your number:

We select our own sketch with TensorFlow Lite Micro. It needs ... bytes of
flash and an arena of ... bytes, against ... bytes of flash and ... bytes of
RAM for the library of Edge Impulse. The features and the inference need
... microseconds, so the processor can sleep for the rest of each 200 ms. We
know each line of the code, and we can change the features. The trade-off:
our library uses reference kernels, so the inference is slower than with the
optimized kernels of Edge Impulse, and we must keep the feature code of the
board equal to the code of the notebook by hand.
