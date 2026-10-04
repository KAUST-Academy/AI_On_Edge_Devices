# Week 2 quiz: Days 6 to 10

**When:** the start of the Day 11 lab. **Time:** 20 minutes.
**Rules:** close the laptop. Use paper, a pen, and a calculator. Work alone.
**Points:** 15 questions, 1 point each. A calculation needs the method and
the result.

In this quiz, 1 GB = 10^9 bytes and 1 GB/s = 10^9 bytes each second, as in
Days 7 and 10.

---

## Questions

### Day 6: Pruning, distillation, and efficient design

**1.** A team sets 90 percent of the weights of a CNN to zero (unstructured
magnitude pruning) and fine-tunes it. The model stays in the dense
`float32` format. What happens to the file size and to the latency on a
normal processor? Give the reason.

**2.** Structured pruning removes half of the filters of two neighbour
convolution layers. Before: a 3 x 3 convolution with 32 input channels and
64 filters, with biases. After: 16 input channels and 32 filters. Calculate
the parameters before and after. By which factor does the layer become
smaller?

**3.** You have a good teacher model, 1000 labelled images, and 60 000
images with no label. Which method gives the small student the best
accuracy?

- (a) Train the student on the 1000 labels only
- (b) Distill on the 1000 labelled images
- (c) Distill on the 60 000 images with the outputs of the teacher
- (d) Prune the teacher to the size of the student with no new training

### Day 7: Hardware acceleration and inference runtimes

**4.** A device has a peak rate of 20 GFLOP/s and a memory bandwidth of
10 GB/s.

- (a) Calculate the ridge point.
- (b) A ReLU in `float32` has an arithmetic intensity of 0.125 FLOP for
  each byte. Is it limited by the memory or by the computation? Calculate
  its highest rate.
- (c) A 3 x 3 convolution with 64 to 64 channels has an intensity of 132.
  Is it limited by the memory or by the computation?

**5.** What does a runtime do when it folds a batch normalization into the
convolution before it? What changes for the output of the model?

**6.** The same MobileNetV2 file runs in LiteRT on one thread: 362.7 ms with
the reference kernels and 11.7 ms with XNNPACK. Name two reasons for the
difference.

### Day 8: Object detection at the edge

**7.** Box A has the corners (0, 0) and (4, 4). Box B has the corners
(2, 2) and (6, 6). Calculate the IoU of the two boxes.

**8.** A detector gives four candidates after the score threshold 0.25:

| Box | Class | Score | Note |
|---|---|---|---|
| 1 | person | 0.90 | |
| 2 | person | 0.60 | IoU with box 1: 0.70 |
| 3 | person | 0.40 | IoU with box 1: 0.10 |
| 4 | dog | 0.80 | IoU with box 1: 0.65 |

The suppression runs for each class with the IoU threshold 0.5. Which
boxes stay? Give the reason for each removed box.

**9.** On the test images, a detector of persons has these counts:

| Score threshold | TP | FP | FN |
|---|---|---|---|
| 0.25 | 80 | 20 | 40 |
| 0.50 | 60 | 5 | 60 |

- (a) Calculate the precision and the recall at each threshold.
- (b) Which threshold do you select for an alarm that must not miss a
  person? Which for a counter that must not count false persons?

### Day 9: Benchmarking and profiling

**10.** Ten latencies in ms: 11, 11, 12, 11, 12, 30, 11, 12, 11, 13.
Calculate the mean, the median, and the p90. Use the nearest-rank rule: the
p-th percentile is the smallest value with at least p percent of the values
at or below it. Which statistic shows the slow run?

**11.** A XIAO runs one inference of 20 ms each second at 217 mW. Between
the inferences, the chip is in light sleep at 0.79 mW. The battery has
1000 mAh at 3.7 V (3700 mWh). Calculate the mean power and the battery life
in days. Use the chip values only.

**12.** Why does a benchmark run warm-up inferences before the timed runs?

- (a) To heat the chip to its working temperature
- (b) The first inferences are slower: the caches are empty, and the
  runtime prepares its memory and its kernels
- (c) To train the model on the device
- (d) To fill the battery

### Day 10: Generative AI at the edge

**13.** A language model has 3 212 749 888 parameters. It uses `Q4_K` with
4.5 bits for each weight. Estimate the file size in GB.

**14.** To generate one token, the processor reads all weights from the
memory one time. A model file has 2.0 GB, and the memory of the board gives
about 12 GB/s. Estimate the highest generation rate in tokens each second.

**15.** An application with `llama3.2:1b` must calculate prices: the product
of two 3-digit numbers. How do you design this part? Give the reason.

---

## Answers

For the instructor. Each answer names the part of the lecture.

**1.** The file size **does not change**, and the latency **does not get
better**. The zeros stay in the dense tensors: the file stores them, and
the kernels multiply them as other values. A gain needs a sparse format and
sparse kernels, or structured pruning. (Day 6, Part 1. In the course
experiment: 99 320 bytes before and after, 76.4 percent at 90 percent
sparsity.)

**2.** Before: 3 x 3 x 32 x 64 + 64 = **18 496**. After:
3 x 3 x 16 x 32 + 32 = **4640**. The layer becomes about **4 times**
smaller (3.99), because both the inputs and the filters are halved.
(Day 6, Part 1.)

**3.** **(c).** The teacher gives a target for each of the 60 000 images, so
the student learns from 60 times more images. In the course experiment:
77.4 percent with the 1000 labels, 78.9 percent with distillation on the
same images, and 85.3 percent with the outputs of the teacher on the 60 000
images. (d) gives a damaged model. (Day 6, Part 2.)

**4.** (a) Ridge point = 20 / 10 = **2 FLOP for each byte**.
(b) 0.125 is below 2: **memory-bound**. Highest rate:
0.125 x 10 = **1.25 GFLOP/s**.
(c) 132 is above 2: **compute-bound**, at most 20 GFLOP/s. (Day 7, Part 1.)

**5.** The runtime calculates new weights and a new bias for the
convolution from the four parameters of the batch normalization (mean,
variance, scale, shift). Then it removes the batch normalization node. The
output **does not change**, except for a very small rounding difference.
The model has fewer nodes and reads less memory. (Day 7, Part 3.)

**6.** Any two: XNNPACK uses the **SIMD** instructions of the processor
(several values in one instruction); it works on **blocks of data that fit
in a cache**; its code is written **for one processor type**. The
reference kernels are simple loops, the same code for each processor, easy
to read and to test. The file and the result are the same. (Day 7,
Part 2.)

**7.** Intersection: the square from (2, 2) to (4, 4), area **4**. Union:
16 + 16 - 4 = **28**. IoU = 4 / 28 = **0.14**. (Day 8, Part 1.)

**8.** **Boxes 1, 3, and 4 stay.** Box 2 is removed: same class as box 1,
lower score, and IoU 0.70 above 0.5. Box 3 stays: its IoU with box 1 is
only 0.10, so it is a second person. Box 4 stays: the suppression compares
only boxes of the same class. (Day 8, Part 1.)

**9.** (a) At 0.25: precision 80 / 100 = **0.80**, recall 80 / 120 =
**0.67**. At 0.50: precision 60 / 65 = **0.92**, recall 60 / 120 =
**0.50**.
(b) The alarm: **0.25**, the higher recall. The counter: **0.50**, the
higher precision. (Day 8, Part 2.)

**10.** Sorted: 11, 11, 11, 11, 11, 12, 12, 12, 13, 30. Mean: 134 / 10 =
**13.4 ms**. Median (p50, the 5th value): **11 ms**. p90 (the 9th value):
**13 ms**. The slow run of 30 ms changes the mean, but not the median or
the p90 of ten runs: only the largest value (p100) shows it. Use more runs
and a high percentile, such as the p99, for the tail. (Day 9, Parts 1 and
2.)

**11.** Duty cycle d = 20 / 1000 = 0.02. Mean power =
0.02 x 217 + 0.98 x 0.79 = 4.34 + 0.774 = **5.114 mW**. Life =
3700 / 5.114 = 723.5 h = **30.1 days**. (Day 9, Part 3.)

**12.** **(b).** In the course experiment, the mean of the first 5
inferences was 13.35 ms, and the median of the inferences 21 to 30 was
10.95 ms. (Day 9, Part 2.)

**13.** 3 212 749 888 x 4.5 / 8 = 1 807 171 812 bytes = **about 1.8 GB**.
The real file of `llama3.2:3b` has 2.02 GB, because some tensors use
`Q6_K` with 6.5625 bits. (Day 10, Part 1.)

**14.** 12 / 2.0 = **about 6 tokens each second**, at most. The
measured rate of `llama3.2:3b` (2.02 GB) on a Raspberry Pi 5 is 5.3 tokens
each second. (Day 10, Part 1.)

**15.** Use a **tool call**: the model gives the name of a function and the
two numbers, and Python calculates the product. The model does not
calculate. In the course test, `llama3.2:1b` gave 0 correct products of 20
in a direct answer, and the correct call with the correct numbers 20 times
of 20. (Day 10, Part 3.)
