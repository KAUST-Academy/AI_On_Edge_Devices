# MC-3 lab report: example

This is the example of the report of the MC-3 lab. Every number comes from
one run of `solutions/spectral_features.ipynb` on the fallback dataset of
the module. The signals are simulated, and the processor is an x86 with
AVX2. The numbers say nothing about a board. A group with real recordings
gets other numbers, and writes its own.

Group: g07

Names: student one, student two



Laptop (processor):
Versions:

| Tool | Version |
|---|---|
| Python | 3.13.11 |
| `tensorflow` | 2.21.0 |
| `keras` | 3.12.0 |
| `numpy` | 2.5.3 |

Dataset used: the simulated fallback dataset of the folder
`fallback_data/`.

Number of training windows: 1312, from 32 files of the sessions `s1` and
`s2`.

Number of test windows: 656, from 16 files of the session `s3`.

Session of the test set: `s3`, 164 windows for each of the four classes.

## Part A: the time-domain features (task 1)

The three values of the first window:

| RMS | Skewness | Kurtosis |
|---|---|---|
| 0.0038 | -0.3266 | -0.0771 |

The first window is an idle window, so its RMS is small.

The frequency that holds the power of `lift`, in Hz: 1.28 Hz, which is bin
3 of an FFT of length 128.

The frequency that holds the power of `maritime`, in Hz: 0.78 Hz, which is
bin 2.

Mean and standard deviation of the first nine features. The first three are
the RMS, the skewness, and the kurtosis of the axis `x`, and the next six
are power values.

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Mean | 0.10 | 0.02 | -1.04 | 0.35 | 0.20 | 0.24 | 0.04 | 0.01 | 0.01 |
| Standard deviation | 0.08 | 0.20 | 0.70 | 0.62 | 0.23 | 0.52 | 0.09 | 0.02 | 0.01 |

The mean of the third value is below zero because the kurtosis of an idle
window is negative, and the mean is computed over the four classes.

## Part C: the classifier (task 3)

| Item | Your result |
|---|---|
| Number of input values | 201 |
| Number of parameters | 4294 |
| Test accuracy in percent | 98.8 |

## Part D: five inputs for the same task (task 4)

| Input | Values | Parameters | Test accuracy |
|---|---|---|---|
| Raw window | 300 | 6274 | 58.5 |
| Time-domain features | 9 | 454 | 100.0 |
| Spectral features, FFT length of the notebook | 201 | 4294 | 98.8 |
| Spectral features, FFT length 32 | 57 | 1414 | 99.2 |
| Spectral features, FFT length 64 | 105 | 2374 | 100.0 |

Your prediction for task 4, written before the experiment: FFT length 128,
because the four classes move below 2 Hz and only a long FFT gives bins
below 1 Hz.

FFT length that won in your run: 64, with 100.0 percent. The difference
between 64 and 128 is one window of 656, so it is inside the noise of the
test set.

## Questions

1. The time-domain features give the smallest model: 454 parameters against
   6274 for the raw window, so 5820 parameters less, or 93 percent less.
2. The time-domain features also give the best accuracy in this run, 100.0
   percent. The four simulated classes differ in the size of the motion on
   each axis, and the RMS, the skewness, and the kurtosis of the three axes
   already carry that. The 64 power values per axis add nothing on this
   dataset. With real recordings of a pallet the answer can be different:
   the classes of a real pallet have a similar size and differ in their
   frequency content, and then the power values pay.
3. With an FFT length of 64, the bins are `50 / 64 = 0.78` Hz apart. With a
   length of 32 they are 1.56 Hz apart, so the bins cover 0 Hz to 25 Hz but
   each one is 1.56 Hz wide. The motion of `maritime` is 0.5 Hz, so it falls
   in bin 0, which the feature vector drops after the removal of the mean.
   Its power then has no bin at all.

