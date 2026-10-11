# MC-5 lab report

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

Number of clips of the dataset:

Training clips:

Test clips:

## Part A: the Mel filter bank (task 1)

The width of the first filter, in bins:

The width of the last filter, in bins:

The peak of the first filter, in bins:

The peak of the last filter, in bins:

## Part B: the cepstral coefficients (task 2)

The mean of the first coefficient:

The mean of the last coefficient:

What the middle panel of the plot shows:

What the bottom panel of the plot shows:

Time to compute the features of all the clips, in seconds:

## Part C: the classifier (task 3)

| Item | Your result |
|---|---|
| Frames after the two convolutions and the two pooling layers | |
| Number of parameters | |
| Test accuracy in percent | |

## Part D: three inputs for the same task (task 4)

| Input | Values per clip | Parameters | Test accuracy |
|---|---|---|---|
| Raw audio | | | |
| Log Mel spectrogram | | | |
| Cepstral coefficients | | | |

Your prediction for task 4, written before the experiment:

The input that won in your run:

## Questions

1. Which input gives the smallest model, and how many parameters does it
   save compared with the raw audio?
2. The first cepstral coefficient is the energy of the whole frame and the
   last one is small. What do the 13 coefficients describe, and why does
   the cosine transform make them comparable?
3. The split of the clips is random, and a clip of one speaker can be in
   the training set and in the test set. What does that do to the test
   accuracy, and what would you change for a product?

## Decision Log

One decision, one number, one trade-off.