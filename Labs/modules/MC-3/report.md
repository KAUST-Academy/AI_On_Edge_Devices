# MC-3 lab report

Group:

Names:

Date:

Laptop (processor):

Versions:

| Tool | Version |
|---|---|
| Python | |
| `tensorflow` | |
| `keras` | |
| `numpy` | |

Dataset used: the recordings of the group, or the simulated fallback
dataset of the folder `fallback_data/`.

Number of training windows:

Number of test windows:

Session of the test set:

## Part A: the time-domain features (task 1)

The three values of the first window:

| RMS | Skewness | Kurtosis |
|---|---|---|
| | | |

The frequency that holds the power of `lift`, in Hz:

The frequency that holds the power of `maritime`, in Hz:

Mean and standard deviation of the first nine features (the first three are
the RMS, the skewness, and the kurtosis of the axis `x`):

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Mean | | | | | | | | | |
| Standard deviation | | | | | | | | | |

## Part C: the classifier (task 3)

| Item | Your result |
|---|---|
| Number of input values | |
| Number of parameters | |
| Test accuracy in percent | |

## Part D: five inputs for the same task (task 4)

| Input | Values | Parameters | Test accuracy |
|---|---|---|---|
| Raw window | | | |
| Time-domain features | | | |
| Spectral features, FFT length of the notebook | | | |
| Spectral features, FFT length 32 | | | |
| Spectral features, FFT length 64 | | | |

Your prediction for task 4, written before the experiment:

FFT length that won in your run:

## Questions

1. Which input gives the smallest model, and how many parameters does it
   save compared with the raw window?
2. Which input gives the best test accuracy, and which feature group
   explains the difference?
3. The bins of the FFT are `nfft // 2` values apart by `RATE_HZ / nfft` hertz.
   Write that distance for the FFT length that won, and name the frequency
   of a motion that the bins of a length of 32 cannot show.

## Decision Log

One decision, one number, one trade-off.