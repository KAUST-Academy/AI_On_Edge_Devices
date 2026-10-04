# Day 4 lab report

Group:

Names:

Date:

Dataset: your own recordings of Day 2, the recordings of a different group,
or the fallback dataset.

## Part A: quantize by hand

Versions:

| Tool | Version |
|---|---|
| Python | |
| `tensorflow` | |
| `keras` | |

The input tensor: all acceleration values of the training windows.

| Item | Your result |
|---|---|
| Smallest value and largest value of the tensor | |
| Scale `S` and zero point `Z` | |
| Largest error, and the limit `S / 2` | |
| Typical error (RMS), and the value `S / sqrt(12)` | |
| RMS error with 4 bits, against 8 bits | |

### The clipping error (task 3)

Write the prediction before you run the experiment of section 4.

| Question | Your prediction | Result |
|---|---|---|
| The range with the smallest RMS error, 8 bits | | |
| The range with the smallest RMS error, 4 bits | | |
| The reason | | |

Your answers:

1. Compare the result with your prediction.
2. The converter of LiteRT uses the minimum and the maximum. For which
   tensor of a model is this a risk?

## Part B: post-training quantization

| Item | Your result |
|---|---|
| Parameters of the CNN | |
| Windows in the calibration set | |

The table of section 7. The accuracy and the clipped input values are in
percent:

| Model | File in bytes | Accuracy | idle | terrestrial | lift | maritime | Clipped |
|---|---|---|---|---|---|---|---|
| `float32` | | | | | | | |
| `int8`, all classes | | | | | | | |

| Item | Your result |
|---|---|
| Largest difference between the float output and the `int8` output | |
| Windows with a different class | |
| Loss of accuracy in points, and the next step by the rule of the lecture | |

The model of section 8:

| Question | Your answer |
|---|---|
| Scale and zero point of the input tensor | |
| Number of scales of the weights of each convolution | |
| Zero point of the weights | |
| Type of the biases | |

### The calibration set (task 6)

Write the prediction before you run the experiment of section 9.

| Question | Your prediction | Result |
|---|---|---|
| The calibration class with the lowest accuracy | | |
| A calibration class with no loss of accuracy | | |
| The smallest set of all classes with no loss | | |
| The reason | | |

Experiment 1. The accuracy and the clipped input values are in percent:

| Calibration set | Accuracy | idle | terrestrial | lift | maritime | Clipped |
|---|---|---|---|---|---|---|
| All classes | | | | | | |
| Only idle | | | | | | |
| Only terrestrial | | | | | | |
| Only lift | | | | | | |
| Only maritime | | | | | | |

Experiment 2:

| Calibration set | Accuracy | Clipped |
|---|---|---|
| 200 windows | | |
| 20 windows | | |
| 4 windows | | |

Your answers:

1. Compare the result with your prediction.
2. Which column of the table shows the problem when you have no labels for
   the test inputs?
3. Your product gets a new motion class next year. Which two steps do you
   repeat for the `int8` model?

## Part C: quantization-aware training

| Item | Your result |
|---|---|
| Result of the check of task 7 | |
| Accuracy with simulated quantization, 8 bits | |
| Accuracy of the `int8` LiteRT model of Part B | |

### The number of bits (task 8)

Write the prediction before you run the experiment of section 11.

| Question | Your prediction | Result |
|---|---|---|
| Accuracy with weights of 2 bits and no new training | | |
| Quantization-aware training repairs the loss at 2 bits | | |
| The reason | | |

The table of section 11. The accuracy is in percent:

| Bits of a weight | Values of a weight | No new training | Quantization-aware training |
|---|---|---|---|
| 8 | 255 | | |
| 4 | 15 | | |
| 3 | 7 | | |
| 2 | 3 | | |

Your answers:

1. Compare the result with your prediction.
2. The board of this course runs `int8` kernels only. Is quantization-aware
   training necessary for this model? Give your numbers.

### The layer that loses accuracy

The loss of accuracy in points, with no new training:

| Layer | Parameters | Loss with weights of 4 bits | Loss with weights of 2 bits |
|---|---|---|---|
| Convolution 1 | | | |
| Convolution 2 | | | |
| Fully connected | | | |
| All layers | | | |
| Sum of the single layers | not necessary | | |

Your answers:

1. For each table: which layer causes the loss? Is the sum of the single
   losses near the loss of the complete model?
2. All weights must have 4 bits, and one layer can keep 8 bits. Which
   layer do you select? Give the cost in bytes.

### The real `int8` model

| Model | File in bytes | Accuracy in percent | Clipped in percent |
|---|---|---|---|
| `float32` | | | |
| `int8`, post-training | | | |
| `int8`, quantization-aware training | | | |

## Part D: on the board

Prediction before the measurement. Write for each number: smaller, larger,
or equal, and a factor.

| Number | Your prediction for the `int8` model |
|---|---|
| Flash use of the sketch | |
| Arena used | |
| Time of `Invoke()` | |

The comparison table:

| Number | `float32` model | `int8` model | Change |
|---|---|---|---|
| LiteRT file in bytes (notebook) | | | |
| Test accuracy on the laptop in percent (notebook) | | | |
| Peak of the activations in bytes (notebook) | | | |
| `Sketch uses ... bytes` (flash) | | | |
| Arena used in bytes | | | |
| Test set on the board: correct windows of 80 | | | |
| Test set on the board: same class as on the laptop | | | |
| Clipped input values on the board, and on the laptop | not necessary | | not necessary |
| `invoke_us`: median and largest | | | |

Scale and zero point of the `int8` model:

| Tensor | Scale | Zero point |
|---|---|---|
| Input | | |
| Output | | |

Real motions with the `int8` model:

| Motion that you make | Class that the board shows most of the time |
|---|---|
| idle | |
| terrestrial | |
| lift | |
| maritime | |

Compare your predictions with the measured numbers. Explain each difference
in one sentence:

## Decision Log

About 100 words. The motion classifier of Day 3 goes into a product with the
XIAO ESP32S3. Which model do you put on the board: the `float32` model or
the `int8` model? State the decision, give your numbers for the flash, the
arena, the latency, and the accuracy, and name the trade-off. Explain the
change of the accuracy, or explain why the accuracy does not change.

## Problems

Write each problem that you had, and how you solved it.
