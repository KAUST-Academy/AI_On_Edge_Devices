# Day 6 lab report

Group:

Names:

Date:

Laptop (processor):

## Part A: pruning

Versions:

| Tool | Version |
|---|---|
| Python | |
| `tensorflow` | |
| `keras` | |

The baseline:

| Item | Your result |
|---|---|
| Parameters | |
| LiteRT file in bytes | |
| Accuracy in percent | |
| Latency in microseconds | |
| Peak of the activations in bytes | |

### Unstructured pruning (task 2)

Write the prediction before you run the experiment of section 2.

| Question | Your prediction | Result |
|---|---|---|
| Accuracy at a sparsity of 80 percent, before fine-tuning | | |
| Accuracy at a sparsity of 80 percent, after fine-tuning | | |
| LiteRT file at a sparsity of 80 percent: smaller, equal, or larger | | |
| Latency at a sparsity of 80 percent: smaller, equal, or larger | | |

The table of section 2:

| Sparsity | Weights not 0 | Accuracy before | Accuracy after | File | After gzip | Latency |
|---|---|---|---|---|---|---|
| none | | not necessary | | | | |
| 0.50 | | | | | | |
| 0.70 | | | | | | |
| 0.80 | | | | | | |
| 0.90 | | | | | | |

### Structured pruning

The table of section 3:

| Filters | Parameters | Accuracy before | Accuracy after | File | Latency | Peak |
|---|---|---|---|---|---|---|
| 16-32-64 | | not necessary | | | | |
| 12-24-48 | | | | | | |
| 8-16-32 | | | | | | |
| 4-8-16 | | | | | | |

Your answers:

1. Compare the results of section 2 with your prediction.
2. Find one unstructured model and one structured model with almost the same
   accuracy. Compare their file size, their latency, and their peak.
3. Which type of pruning do you use for the XIAO ESP32S3 with TensorFlow Lite
   Micro? Give the reason.

## Part B: knowledge distillation

| Item | Your result |
|---|---|
| The label of the test image of section 5 | |
| The classes with a probability above 0.05 at a temperature of 4 | |
| Mean of the largest probability of the teacher | |
| Result of the check of task 5 | |

### The student (task 6)

Write the prediction before you run the experiment of section 7.

| Question | Your prediction | Result |
|---|---|---|
| Gain of run 2 against run 1, in points | | |
| Gain of run 3 against run 1, in points | | |
| The run with the higher accuracy: run 3 or run 4 | | |
| The reason | | |

| Run | Training data | Target | Accuracy in percent |
|---|---|---|---|
| 1 | 1000 labelled images | the labels | |
| 2 | the same 1000 images | the labels and the soft targets | |
| 3 | 60 000 images with no label | the soft targets only | |
| 4 | 60 000 labelled images | the labels | |

Your answers:

1. Compare the results with your prediction.
2. Run 2 and run 3 use the same teacher. Why is the gain of run 3 much
   larger?
3. Your product collects sensor data in the field, and a label costs one
   minute of a person. What do the results say for your project plan?

## Part C: selection

The table of section 8. The latency is the latency of your laptop:

| Model | Format | Bytes | Accuracy | Latency | Peak |
|---|---|---|---|---|---|
| baseline 16-32-64 | float32 | | | | |
| baseline 16-32-64 | int8 | | | | |
| unstructured 80 percent | float32 | | | | |
| unstructured 80 percent | int8 | | | | |
| pruned 12-24-48 | float32 | | | | |
| pruned 12-24-48 | int8 | | | | |
| pruned 8-16-32 | float32 | | | | |
| pruned 8-16-32 | int8 | | | | |
| pruned 4-8-16 | float32 | | | | |
| pruned 4-8-16 | int8 | | | | |
| student, teacher only | float32 | | | | |
| student, teacher only | int8 | | | | |
| student, all labels | float32 | | | | |
| student, all labels | int8 | | | | |

The plot: add the file `tradeoff.png` to your report.

- The files on the upper left border of the size plot:
- The files on the upper left border of the latency plot:

The selection (task 7):

| Product | Model | Format | Bytes | Accuracy | Latency | Peak | The constraint that decides |
|---|---|---|---|---|---|---|---|
| XIAO ESP32S3 | | int8 | | | | | |
| Raspberry Pi 5 | | | | | | | |

## Decision Log

About 100 words. Which model do you select for the XIAO ESP32S3, and which
model for the Raspberry Pi 5? State the two decisions, give the numbers of
each model, name the constraint that decides for each product, and say what
the product loses with your selection.

## Problems

Write each problem that you had, and how you solved it.
