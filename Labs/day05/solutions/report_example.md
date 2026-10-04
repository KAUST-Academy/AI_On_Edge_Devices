# Day 5 lab report: example

This lab needs Edge Impulse Studio and the kit for almost all numbers.
Nobody ran the lab on hardware. So this example gives the structure of the
answers, the numbers that the kit lab of the source reports, and "measure in
the lab" for each number of your group. The numbers of the source come from
a different dataset and a different firmware.

Group: example

## Part A: keyword spotting

The dataset:

| Class | Clips of the public dataset | Your own clips |
|---|---|---|
| yes | 300 | measure in the lab, about 8 |
| no | 300 | measure in the lab, about 8 |
| unknown | 300 | 0 |
| noise | 300 | 0 |

The features and the model, from Edge Impulse Studio:

| Item | Your result |
|---|---|
| Frames and coefficients of the MFCC block | 49 frames and 13 coefficients for the default parameters: 637 values |
| Feature block: processing time and peak RAM (estimates of the Studio) | The kit lab reports 675 ms and 16 KB for a board with an ESP32 |
| Accuracy in `Model testing` | measure in the lab. The kit lab reports about 87 percent. |
| Class with the lowest accuracy | measure in the lab. The kit lab reports the class `unknown`. |
| Model: inferencing time, peak RAM, and flash use (estimates of the Studio) | measure in the lab |

The post-processing. Say the word `yes` 10 times:

| Version of the sketch | Events for 10 words |
|---|---|
| Before tasks A1 and A2: each window alone | measure in the lab. Expect more than 10: one word fills some windows. |
| After tasks A1 and A2 | measure in the lab. The target is 10. |

The test of `postprocess.h` on the laptop, with the example of the lecture
(15 windows, one cough, one word): the version before the tasks gives 4
events, and the complete version gives 1 event.

The tuning table: measure in the lab.

- An example of a reason: "We select 3 windows and a threshold of 0.7. With
  2 windows we had ... false accepts in 30 s. With 4 windows we missed ...
  words of 20, because a short word does not fill 4 windows."

## Part B: image classification

The training, from Edge Impulse Studio:

| Item | Your result |
|---|---|
| Images in the training set and in the test set | 81 images in the dataset. The Studio puts about 20 percent into the test set. |
| Accuracy in `Model testing` | measure in the lab |
| Model: inferencing time, peak RAM, and flash use (estimates of the Studio) | measure in the lab. The kit lab reports 1160 ms, 233 KB, and 546 KB for its dataset. |

The test on the kit: measure in the lab.

- An example of an answer: "With the vote, the display changes later, and
  it does not change for one wrong frame."

## Part C: measure

| Number | Keyword model | Image model |
|---|---|---|
| Capture time in ms | not necessary | measure in the lab |
| Feature time in ms (DSP) | measure in the lab | measure in the lab |
| Inference time in ms (classification) | measure in the lab | measure in the lab |
| Complete loop in ms | measure in the lab | measure in the lab |
| Inferencing time, estimate of the Studio in ms | measure in the lab | measure in the lab |
| `Sketch uses ... bytes` (flash) | measure in the lab | measure in the lab |
| Free internal heap in bytes | measure in the lab | measure in the lab |
| Peak RAM, estimate of the Studio | measure in the lab | measure in the lab |

The kit lab of the source reports 81 ms for the pre-processing and 205 ms
for the inference of its image model, with a different firmware.

- An example of an answer for the estimates: "The Studio gives its estimate
  for a board with an older processor. Our board is faster."
- The keyword model: the MFCC features need more time than the small model.

## Decision Log

An example. Replace each `...` with your number:

We use a stride of 250 ms, a mean of 3 windows, a threshold of ..., and a
suppression time of 1000 ms for stage 1. With these settings we had ...
false accepts in 30 s of speech and ... missed words of 20. One XIAO ESP32S3
can run the two stages, but not at the same time: the keyword stage needs
... ms for each window of 250 ms, and the image model needs ... ms for one
frame. So the sketch stops the keyword stage for one image. The RAM is no
limit with the PSRAM: the two models need ... KB and ... KB. The trade-off:
during the image, the device does not listen.
