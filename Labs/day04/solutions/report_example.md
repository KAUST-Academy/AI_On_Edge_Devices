# Day 4 lab report: example

This example has the parts of the report that need no board. The numbers of
Parts A, B, and C come from the solution notebook with the fallback dataset
of Day 2. The signals of the fallback dataset are simulated. The flash
numbers come from the compiler. The parts that need a board say "measure in
the lab".

Group: example

Dataset: the fallback dataset.

## Part A: quantize by hand

The input tensor: all acceleration values of the training windows.

| Item | Your result |
|---|---|
| Smallest value and largest value of the tensor | -0.7226 and 1.6729 |
| Scale `S` and zero point `Z` | 0.009394 and -51 |
| Largest error, and the limit `S / 2` | 0.004694, limit 0.004697 |
| Typical error (RMS), and the value `S / sqrt(12)` | 0.002719, value 0.002712 |
| RMS error with 4 bits, against 8 bits | 0.041673: 15.3 times as large |

### The clipping error (task 3)

| Question | Your prediction | Result |
|---|---|---|
| The range with the smallest RMS error, 8 bits | minimum and maximum | percentile 99.9 |
| The range with the smallest RMS error, 4 bits | percentile 99 | percentile 99 |
| The reason | With 4 bits the step is large, so a smaller range helps more | Correct for 4 bits |

Answers:

1. With 8 bits, the range "percentile 99.9" gives the smallest RMS error:
   0.00266 against 0.00272 for "minimum and maximum". The prediction for
   8 bits was wrong. But the gain is 2 percent only, and the largest error
   is 7 times as large: 0.0350 against 0.0047. With 4 bits, the range
   "percentile 99" gives the smallest RMS error: 0.0379 against 0.0417.
2. A tensor with some very large values and many small values, for example
   an activation with no upper limit. The large values make the scale
   large, and all small values get a large rounding error.

## Part B: post-training quantization

| Item | Your result |
|---|---|
| Parameters of the CNN | 852 |
| Windows in the calibration set | 200 |

The table of section 7. The accuracy and the clipped input values are in
percent:

| Model | File in bytes | Accuracy | idle | terrestrial | lift | maritime | Clipped |
|---|---|---|---|---|---|---|---|
| `float32` | 7320 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 0.00 |
| `int8`, all classes | 6008 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 1.03 |

| Item | Your result |
|---|---|
| Largest difference between the float output and the `int8` output | 0.0187 |
| Windows with a different class | 0 of 656 |
| Loss of accuracy in points, and the next step by the rule of the lecture | 0.0 points: use the model |

A result of 100.0 percent comes from the simulated signals. Real recordings
give a lower value.

The file becomes 1312 bytes smaller, not four times smaller. The weights
need 3408 bytes in `float32` and about 852 bytes in `int8`. The other part
of the file is the description of the graph, and it stays.

The model of section 8:

| Question | Your answer |
|---|---|
| Scale and zero point of the input tensor | 0.009344 and -52 |
| Number of scales of the weights of each convolution | 8 and 16: one scale for each filter |
| Zero point of the weights | 0 |
| Type of the biases | `int32` |

### The calibration set (task 6)

| Question | Your prediction | Result |
|---|---|---|
| The calibration class with the lowest accuracy | idle | idle |
| A calibration class with no loss of accuracy | lift | terrestrial and maritime. The class lift loses 0.8 points. |
| The smallest set of all classes with no loss | 20 | 4 |
| The reason | idle has the smallest range, so the other classes are cut | Correct |

Experiment 1. The accuracy and the clipped input values are in percent:

| Calibration set | Accuracy | idle | terrestrial | lift | maritime | Clipped |
|---|---|---|---|---|---|---|
| All classes | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 1.03 |
| Only idle | 84.9 | 100.0 | 73.8 | 100.0 | 65.9 | 21.98 |
| Only terrestrial | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 7.09 |
| Only lift | 99.2 | 100.0 | 97.0 | 100.0 | 100.0 | 7.24 |
| Only maritime | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 4.61 |

Experiment 2:

| Calibration set | Accuracy | Clipped |
|---|---|---|
| 200 windows | 100.0 | 1.03 |
| 20 windows | 100.0 | 1.47 |
| 4 windows | 100.0 | 2.20 |

Answers:

1. The calibration set with the class "idle" only gives the lowest
   accuracy: 84.9 percent in place of 100.0. The second prediction was
   wrong: the class "lift" only gives 99.2 percent.
2. The column "Clipped". It needs no labels.
3. Make a new calibration set that holds the new class, and convert again.
   Then test the `int8` model again on a test set with all classes.

## Part C: quantization-aware training

| Item | Your result |
|---|---|
| Result of the check of task 7 | complete, the gradient is 1 for each value |
| Accuracy with simulated quantization, 8 bits | 100.0 percent |
| Accuracy of the `int8` LiteRT model of Part B | 100.0 percent |

### The number of bits (task 8)

| Question | Your prediction | Result |
|---|---|---|
| Accuracy with weights of 2 bits and no new training | 60 | 49.8 |
| Quantization-aware training repairs the loss at 2 bits | no | yes |
| The reason | A weight with 2 bits has only 3 values: too few for this model | Wrong: the training finds weights with three values |

The table of section 11. The accuracy is in percent:

| Bits of a weight | Values of a weight | No new training | Quantization-aware training |
|---|---|---|---|
| 8 | 255 | 100.0 | 100.0 |
| 4 | 15 | 75.0 | 100.0 |
| 3 | 7 | 100.0 | 100.0 |
| 2 | 3 | 49.8 | 100.0 |

Answers:

1. The second prediction was wrong. With weights of 2 bits and no new
   training, the accuracy is 49.8 percent. Quantization-aware training
   gives 100.0 percent again.
2. No. With 8 bits, post-training quantization loses 0.0 points.

### The layer that loses accuracy

The loss of accuracy in points, with no new training:

| Layer | Parameters | Loss with weights of 4 bits | Loss with weights of 2 bits |
|---|---|---|---|
| Convolution 1 | 128 | 25.0 | 26.2 |
| Convolution 2 | 656 | 0.0 | 25.0 |
| Fully connected | 68 | 0.0 | 27.3 |
| All layers | 852 | 25.0 | 50.2 |
| Sum of the single layers | not necessary | 25.0 | 78.5 |

Answers:

1. With 4 bits, the layer "convolution 1" causes the complete loss, and the
   sum is equal to the loss of the complete model. With 2 bits, each layer
   alone loses 25 to 27 points, and no single layer explains the loss.
2. The layer "convolution 1". Its 120 weights need 120 bytes with 8 bits
   in place of 60 bytes with 4 bits. The cost is 60 bytes.

### The real `int8` model

| Model | File in bytes | Accuracy in percent | Clipped in percent |
|---|---|---|---|
| `float32` | 7320 | 100.0 | 0.00 |
| `int8`, post-training | 6008 | 100.0 | 1.03 |
| `int8`, quantization-aware training | 6008 | 100.0 | 1.03 |

## Part D: on the board

An example of a prediction:

| Number | Your prediction for the `int8` model |
|---|---|
| Flash use of the sketch | Smaller by some KB: the model file is smaller, and the program is the same |
| Arena used | Smaller, but not four times: the data of the interpreter stays |
| Time of `Invoke()` | Equal or slower: the chip has a circuit for float arithmetic, and the kernels are not optimized |

The comparison table:

| Number | `float32` model | `int8` model | Change |
|---|---|---|---|
| LiteRT file in bytes (notebook) | 8328 | 4960 | 3368 bytes smaller, 60 percent of the float file |
| Test accuracy on the laptop in percent (notebook) | 100.0 | 100.0 | none |
| Peak of the activations in bytes (notebook) | 332 | 83 | a quarter |
| `Sketch uses ... bytes` (flash) | 382 785 (result of the compiler) | 379 701 (result of the compiler) | 3084 bytes smaller |
| Arena used in bytes | measure in the lab | measure in the lab | measure in the lab |
| Test set on the board: correct windows of 80 | measure in the lab | measure in the lab | measure in the lab |
| Test set on the board: same class as on the laptop | measure in the lab | measure in the lab | measure in the lab |
| Clipped input values on the board, and on the laptop | not necessary | measure in the lab. The laptop gives 42 of 5040. | not necessary |
| `invoke_us`: median and largest | measure in the lab | measure in the lab | measure in the lab |

Numbers of a test with no board: a 32-bit build of the same library on the
work computer of the course gives an arena of 1232 bytes for the `float32`
model and 1028 bytes for the `int8` model, 80 correct windows of 80 for the
two models, and 42 clipped input values. The values of the board can be
different.

Scale and zero point of the `int8` model:

| Tensor | Scale | Zero point |
|---|---|---|
| Input | 0.030194 | -26 |
| Output | 0.003906 | -128 |

Real motions with the `int8` model: measure in the lab.

## Decision Log

An example. Replace each `...` with your number:

We put the `int8` model on the board. The sketch needs 379 701 bytes of
flash in place of 382 785 bytes, and the arena needs ... bytes in place of
... bytes. The test set gives ... correct windows of 80 for the two models,
so the accuracy does not change: the calibration set holds all four classes,
and only ... of 5040 input values are cut. The time of `Invoke()` is ...
microseconds in place of ... microseconds. The trade-off: the gain is small
for this model with 1534 parameters, and the sketch needs the quantization
code and a calibration set that we must make again for each new class. We
select `int8` because larger models of the product line need it.
