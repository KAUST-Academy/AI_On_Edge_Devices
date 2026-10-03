# Week 1 quiz: Days 1 to 5

**When:** the start of the Day 6 lab. **Time:** 20 minutes.
**Rules:** close the laptop. Use paper, a pen, and a calculator. Work alone.
**Points:** 15 questions, 1 point each. A calculation needs the method and
the result.

All sizes use 1 KB = 1024 bytes, as in the course.

---

## Questions

### Day 1: Edge AI landscape and system constraints

**1.** A machine must stop within 10 ms after a camera sees a hand in the
danger zone. The nearest data centre is 1500 km away. Light in a fibre
travels at about 200 000 km/s.

- (a) Calculate the minimum round-trip time to the data centre.
- (b) Can a model in the cloud meet the budget? Give the reason.

**2.** A convolution layer gets an input of 48 x 48 x 16. It has 32 filters
of 3 x 3, stride 1, padding 1, and a bias for each filter. Calculate:

- (a) the size of the output,
- (b) the number of parameters,
- (c) the number of MACs.

**3.** A model in `int8` has 200 000 parameters. Its peak activation memory
is 300 000 values. The program without the model needs 300 KB of flash.
The device has 1 MB of flash and 256 KB of RAM. Does the model fit? Name
the budget that decides.

### Day 2: Embedded systems, MicroPython, and sensor data collection

**4.** Match each part of the XIAOML Kit to its bus: the IMU, the
microphone, the display, the microSD card.
Buses: I2C, SPI, I2S (PDM). A bus can have more than one part.

**5.** A motor vibration has frequency components up to 120 Hz. Which
sampling rate do you select? Give the reason.

- (a) 100 Hz
- (b) 200 Hz
- (c) 400 Hz
- (d) 4000 Hz

**6.** A team records 10 sessions. It cuts each recording into windows of
2 s with a stride of 0.2 s. It shuffles all windows and takes 20 percent of
them as the test set. The test accuracy is 99 percent. On the board, the
model is much worse.

- (a) Name the error.
- (b) How much of one window does its neighbour window share?
- (c) Give the correct split.

### Day 3: From trained model to microcontroller

**7.** What does the tensor arena of TensorFlow Lite Micro hold?

- (a) The weights of the model
- (b) The activations and the data that the interpreter keeps for each
  tensor and each operator
- (c) The program code
- (d) The training data

**8.** The sketch stops at `AllocateTensors()`. The log says that the model
uses the operator `SOFTMAX`, but the interpreter has no kernel for it. The
sketch uses `MicroMutableOpResolver<1>` with `AddFullyConnected()`. What do
you change?

**9.** A window has 300 input values (2 s at 50 Hz, 3 axes). A feature
block gives 63 features for the same window. The first layer of the model
is a fully connected layer with 20 neurons. Calculate the parameters of
this layer for the raw window and for the features.

### Day 4: Quantization

**10.** The activations of a layer are between r_min = -0.5 and
r_max = 2.0. Use `int8` with an asymmetric range:
S = (r_max - r_min) / 255 and Z = round(-128 - r_min / S).

- (a) Calculate S and Z.
- (b) Quantize r = 0.3 with q = round(r / S) + Z.
- (c) Calculate the value after the dequantization, r' = S (q - Z), and the
  error.

**11.** A team calibrates a full integer model with 100 windows of the
class "idle" only. The other classes have larger signal values. What
happens to the accuracy on the test set? Give the reason.

**12.** A convolution layer has three filters. The largest absolute weights
are 1.0, 0.1, and 0.4. With one symmetric scale for the tensor,
S = 1.0 / 127.

- (a) How many integer levels does filter 2 use?
- (b) What does per-channel quantization change for filter 2?

### Day 5: Audio and vision on microcontrollers

**13.** Audio at 16 kHz. A frame has 20 ms. The FFT has 512 points.

- (a) How many samples does one frame have?
- (b) What is the width of one frequency bin?

**14.** A MobileNet (width 0.35) in `int8` has a peak activation memory of
138 240 bytes at 96 x 96 pixels.

- (a) Estimate the peak at 160 x 160 pixels.
- (b) The XIAO with no PSRAM has 305 848 bytes of free RAM. Does the model
  at 160 x 160 fit? What can you do?

**15.** A keyword spotter starts too often when nobody says the keyword.
You raise the score threshold. What happens to the false accept rate and
to the false reject rate? Name one other method that reduces the false
accepts.

---

## Answers

For the instructor. Each answer names the part of the lecture.

**1.** (a) t = 2 x 1500 km / 200 000 km/s = 0.015 s = **15 ms**.
(b) **No.** The light alone needs 15 ms, more than the budget of 10 ms. The
software adds more time. The model must run at the machine.
(Day 1, Part 1.)

**2.** (a) **48 x 48 x 32** (padding 1 and stride 1 keep the size).
(b) 3 x 3 x 16 x 32 + 32 = **4640** parameters.
(c) 3 x 3 x 16 x 32 x 48 x 48 = 4608 x 2304 = **10 616 832** MACs.
(Day 1, Part 2.)

**3.** **No.** Flash: 200 000 bytes + 300 KB (307 200 bytes) =
507 200 bytes, less than 1 MB (1 048 576 bytes): the flash is enough. RAM:
300 000 bytes are more than 256 KB (262 144 bytes). **The RAM (peak
activation memory) decides.** (Day 1, Parts 2 and 3.)

**4.** IMU: **I2C**. Display: **I2C** (the same bus as the IMU, a different
address). Microphone: **I2S (PDM)**. microSD card: **SPI**.
(Day 2, Part 1.)

**5.** **(c) 400 Hz.** The rule of Nyquist and Shannon needs more than
2 x 120 = 240 Hz. At 100 Hz and 200 Hz the 120 Hz component aliases to a
false lower frequency. 4000 Hz works but gives 10 times more data than
400 Hz and no more information. (Day 2, Part 2.)

**6.** (a) **Data leakage**: windows of the same session are in the
training set and in the test set.
(b) Two neighbour windows share 1.8 s of 2 s: **90 percent**.
(c) **Split by session**: for example 8 sessions for the training and 2
sessions for the test. No session is in both sets. (Day 2, Part 3.)

**7.** **(b).** The arena holds the input, the output, each tensor between
two operators, and the data of the interpreter. The weights stay in the
flash. (Day 3, Part 2.)

**8.** Add the operator to the resolver and increase the number of
operators: `MicroMutableOpResolver<2> resolver;` with
`resolver.AddFullyConnected();` and `resolver.AddSoftmax();`. Each operator
of the model needs a kernel in the resolver. (Day 3, Part 2.)

**9.** Raw window: 300 x 20 + 20 = **6020**. Features: 63 x 20 + 20 =
**1280**. The complete models (20, 10, and 4 neurons) have 6274 and 1534
parameters. The feature block makes the model about 4 times smaller.
(Day 3, Part 3.)

**10.** (a) S = 2.5 / 255 = **0.009804**. Z = round(-128 + 0.5 / 0.009804)
= round(-128 + 51.0) = **-77**.
(b) q = round(0.3 / 0.009804) + Z = round(30.6) - 77 = 31 - 77 = **-46**.
(c) r' = 0.009804 x (-46 + 77) = 0.009804 x 31 = **0.30392**. The error is
**0.0039**, less than S / 2 = 0.0049. (Day 4, Part 1.)

**11.** **The accuracy falls.** The calibration sets the ranges of the
activations from the "idle" data only. The ranges are too small for the
other classes. Their large values are clipped to the largest integer, so
the model loses the information that separates the classes. Use a
calibration set with all classes. (Day 4, Part 2. In the course
experiment, a model fell from 100.0 to 69.2 percent.)

**12.** (a) 0.1 / (1.0 / 127) = 12.7: the integers go from -13 to 13, so
filter 2 uses **27 levels** of 255.
(b) Per-channel quantization gives filter 2 its own scale, 0.1 / 127. Then
filter 2 uses **all 255 levels**, and its rounding error is 10 times
smaller. The zero point stays 0. (Day 4, Part 2.)

**13.** (a) 16 000 x 0.020 = **320 samples**. The FFT adds zeros to get 512
points.
(b) 16 000 / 512 = **31.25 Hz**. (Day 5, Part 1.)

**14.** (a) The peak grows with the number of pixels:
138 240 x (160 / 96)^2 = 138 240 x 25 / 9 = **384 000 bytes**.
(b) **No**: 384 000 bytes are more than 305 848 bytes, and the arena also
needs other tensors. Use the PSRAM (8 MB), or use 96 x 96 pixels.
(Day 5, Part 2.)

**15.** The false accept rate **falls**. The false reject rate **rises**:
the device misses more spoken keywords. Other methods: smooth the scores
over several windows (for example a mean or "3 of 5 windows"), or add
examples of the "unknown" and "noise" classes to the training data.
(Day 5, Parts 1 and 3.)
