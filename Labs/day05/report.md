# Day 5 lab report

Group:

Names:

Date:

Core version of the esp32 boards package:

## Part A: keyword spotting

The dataset:

| Class | Clips of the public dataset | Your own clips |
|---|---|---|
| yes | | |
| no | | |
| unknown | | |
| noise | | |

The features and the model, from Edge Impulse Studio:

| Item | Your result |
|---|---|
| Frames and coefficients of the MFCC block | |
| Feature block: processing time and peak RAM (estimates of the Studio) | |
| Accuracy in `Model testing` | |
| Class with the lowest accuracy | |
| Model: inferencing time, peak RAM, and flash use (estimates of the Studio) | |

The post-processing. Say the word `yes` 10 times:

| Version of the sketch | Events for 10 words |
|---|---|
| Before tasks A1 and A2: each window alone | |
| After tasks A1 and A2 | |

The tuning table. Do at least three rounds:

| Round | `STRIDE_MS` | `SMOOTH_WINDOWS` | `THRESHOLD` | `SUPPRESSION_MS` | False accepts in 30 s of speech | Missed words of 20 | Delay |
|---|---|---|---|---|---|---|---|
| 1 | 250 | 3 | 0.60 | 1000 | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |

- The settings that you select, and the reason:

## Part B: image classification

The training, from Edge Impulse Studio:

| Item | Your result |
|---|---|
| Images in the training set and in the test set | |
| Accuracy in `Model testing` | |
| Model: inferencing time, peak RAM, and flash use (estimates of the Studio) | |

The test on the kit. Write the class of the display:

| Photo or object | `VOTE_FRAMES 3` | `VOTE_FRAMES 1` |
|---|---|---|
| background, photo 1 | | |
| background, photo 2 | | |
| background, photo 3 | | |
| periquito, photo 1 | | |
| periquito, photo 2 | | |
| periquito, photo 3 | | |
| robot, photo 1 | | |
| robot, photo 2 | | |
| robot, photo 3 | | |

- What does the vote of three frames change?

## Part C: measure

Write the median of 10 lines of the Serial Monitor.

| Number | Keyword model | Image model |
|---|---|---|
| Capture time in ms | not necessary | |
| Feature time in ms (DSP) | | |
| Inference time in ms (classification) | | |
| Complete loop in ms | | |
| Inferencing time, estimate of the Studio in ms | | |
| `Sketch uses ... bytes` (flash) | | |
| Free internal heap in bytes | | |
| Peak RAM, estimate of the Studio | | |

- Compare your measured times with the estimates of the Studio. Explain the
  difference in one sentence:
- For which model is the feature time larger than the inference time?

## Decision Log

About 100 words. The two models go into one product, the voice-controlled
camera of the lecture. Which settings do you select for the post-processing
of stage 1? Can one XIAO ESP32S3 run the two stages? State the decision, give
your numbers for the RAM and for the time, and name the trade-off.

## Problems

Write each problem that you had, and how you solved it.
