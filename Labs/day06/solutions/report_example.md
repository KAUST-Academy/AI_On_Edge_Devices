# Day 6 lab report: example

Group: example

## Part A: pruning

The baseline:

| Item | Your result |
|---|---|
| Parameters | 23 946 |
| LiteRT file in bytes | 99 320 |
| Accuracy in percent | 89.1 |
| Latency in microseconds | 73 |
| Peak of the activations in bytes | 62 720 |

### Unstructured pruning (task 2)

| Question | Your prediction | Result |
|---|---|---|
| Accuracy at a sparsity of 80 percent, before fine-tuning | 40 | 23.4 |
| Accuracy at a sparsity of 80 percent, after fine-tuning | 86 | 85.7 |
| LiteRT file at a sparsity of 80 percent: smaller, equal, or larger | equal | equal |
| Latency at a sparsity of 80 percent: smaller, equal, or larger | equal | equal: the differences are noise |

The table of section 2:

| Sparsity | Weights not 0 | Accuracy before | Accuracy after | File | After gzip | Latency |
|---|---|---|---|---|---|---|
| none | 23 824 | not necessary | 89.1 | 99 320 | 90 877 | 73 |
| 0.50 | 11 912 | 79.9 | 90.0 | 99 320 | 54 423 | 66 |
| 0.70 | 7147 | 50.9 | 88.8 | 99 320 | 36 775 | 66 |
| 0.80 | 4764 | 23.4 | 85.7 | 99 320 | 27 498 | 66 |
| 0.90 | 2383 | 10.0 | 76.4 | 99 320 | 17 796 | 66 |

### Structured pruning

The table of section 3:

| Filters | Parameters | Accuracy before | Accuracy after | File | Latency | Peak |
|---|---|---|---|---|---|---|
| 16-32-64 | 23 946 | not necessary | 89.1 | 99 320 | 82 | 62 720 |
| 12-24-48 | 13 642 | 68.9 | 88.8 | 58 104 | 60 | 47 040 |
| 8-16-32 | 6218 | 18.6 | 85.6 | 28 408 | 26 | 31 360 |
| 4-8-16 | 1674 | 10.7 | 76.2 | 10 232 | 20 | 15 680 |

Answers:

1. The prediction for the accuracy before the fine-tuning was too high: the
   accuracy falls to 23.4 percent. The fine-tuning brings it back to 85.7
   percent. The file stays at 99 320 bytes, and the latency does not become
   smaller.
2. The unstructured model with a sparsity of 80 percent has 85.7 percent.
   The structured model with 8, 16, and 32 filters has 85.6 percent. The
   structured model has a file of 28 408 bytes in place of 99 320 bytes,
   less than half of the latency, and half of the peak: 31 360 bytes in
   place of 62 720 bytes.
3. Structured pruning. The kernels of TensorFlow Lite Micro are dense
   kernels, and the model file is read in place from the flash. Only a
   smaller dense model saves flash, RAM, and time.

## Part B: knowledge distillation

| Item | Your result |
|---|---|
| The label of the test image of section 5 | Shirt |
| The classes with a probability above 0.05 at a temperature of 4 | Shirt, T-shirt, Coat, Pullover, and Dress |
| Mean of the largest probability of the teacher | 0.921 |
| Result of the check of task 5 | complete: 0.0000 and 2.2599 |

### The student (task 6)

| Question | Your prediction | Result |
|---|---|---|
| Gain of run 2 against run 1, in points | 3 | +2.3 |
| Gain of run 3 against run 1, in points | 6 | +8.7 |
| The run with the higher accuracy: run 3 or run 4 | run 4 | run 4 |
| The reason | The labels are correct, and the teacher makes errors | Run 4 is 2.0 points above run 3 |

| Run | Training data | Target | Accuracy in percent |
|---|---|---|---|
| 1 | 1000 labelled images | the labels | 76.5 |
| 2 | the same 1000 images | the labels and the soft targets | 78.8 |
| 3 | 60 000 images with no label | the soft targets only | 85.1 |
| 4 | 60 000 labelled images | the labels | 87.1 |

Answers:

1. The gain of run 2 is 2.3 points, near the prediction. The gain of run 3
   is 8.7 points, more than the prediction. Run 4 is the best, as
   predicted.
2. Run 2 has soft targets for 1000 images. Run 3 has soft targets for
   60 000 images. The teacher gives a target for each image that has no
   label.
3. Label a small part of the data with care, and train the best possible
   teacher. Then let the teacher give targets for the raw data. The student
   of run 3 needs no label and is 2.0 points below the student with
   60 000 labels.

## Part C: selection

The table of section 8. The latency is the latency of a laptop CPU:

| Model | Format | Bytes | Accuracy | Latency | Peak |
|---|---|---|---|---|---|
| baseline 16-32-64 | float32 | 99 320 | 89.1 | 71 | 62 720 |
| baseline 16-32-64 | int8 | 31 280 | 89.1 | 118 | 15 680 |
| unstructured 80 percent | float32 | 99 320 | 85.7 | 73 | 62 720 |
| unstructured 80 percent | int8 | 31 280 | 85.7 | 118 | 15 680 |
| pruned 12-24-48 | float32 | 58 104 | 88.8 | 60 | 47 040 |
| pruned 12-24-48 | int8 | 20 216 | 88.8 | 87 | 11 760 |
| pruned 8-16-32 | float32 | 28 408 | 85.6 | 32 | 31 360 |
| pruned 8-16-32 | int8 | 12 040 | 85.9 | 45 | 7840 |
| pruned 4-8-16 | float32 | 10 232 | 76.2 | 19 | 15 680 |
| pruned 4-8-16 | int8 | 6736 | 76.4 | 35 | 3920 |
| student, teacher only | float32 | 28 408 | 85.1 | 29 | 31 360 |
| student, teacher only | int8 | 12 040 | 85.3 | 50 | 7840 |
| student, all labels | float32 | 28 408 | 87.1 | 28 | 31 360 |
| student, all labels | int8 | 12 040 | 87.3 | 45 | 7840 |

The plot: the file `tradeoff.png` of the solution run has 7 models and 14
points.

- The files on the upper left border of the size plot: the `int8` files of
  the models pruned 4-8-16, student with all labels, pruned 12-24-48, and
  the baseline.
- The files on the upper left border of the latency plot: the `float32`
  files of the models pruned 4-8-16, student with all labels, pruned
  12-24-48, and the baseline.

The selection (task 7):

| Product | Model | Format | Bytes | Accuracy | Latency | Peak | The constraint that decides |
|---|---|---|---|---|---|---|---|
| XIAO ESP32S3 | student, all labels | int8 | 12 040 | 87.3 | 45 | 7840 | RAM |
| Raspberry Pi 5 | pruned 12-24-48 | float32 | 58 104 | 88.8 | 60 | 47 040 | accuracy |

## Decision Log

XIAO ESP32S3: we select the student with all labels in `int8`. It has
12 040 bytes and a peak of 7840 bytes, so it meets the two budgets. The RAM
decides: the models with more filters have a peak of 11 760 bytes or more.
Three models have this architecture. The student with all labels has the
highest accuracy of the three: 87.3 percent.

Raspberry Pi 5: we select the model that is pruned to 12, 24, and 48
filters, in `float32`. Only two models reach 88.5 percent: the baseline and
this model. The accuracy decides. The pruned model is a little faster than
the baseline, and its file is 41 percent smaller.

The trade-off: the model for the XIAO loses about 2 points against the
baseline. It needs 12 040 bytes of flash in place of 31 280 bytes, and half
of the RAM of the `int8` baseline.
