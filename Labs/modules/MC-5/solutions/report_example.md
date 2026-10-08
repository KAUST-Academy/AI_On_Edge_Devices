# MC-5 lab report: example

This is the example of the report of the MC-5 lab. Every number comes from
one run of `solutions/mfcc_training.ipynb` on the public dataset of Edge
Impulse, on an x86 processor with AVX2. The accuracies say nothing about a
board. A group that uses another number of clips gets other numbers, and
writes its own.

Group: g07

Names: student one, student two

Date: 2026-10-08

Laptop (processor): Intel Xeon E5-2680 v3

Versions:

| Tool | Version |
|---|---|
| Python | 3.13.11 |
| `tensorflow` | 2.21.0 |
| `keras` | 3.15.1 |
| `numpy` | 2.5.3 |

Number of clips of the dataset: 960, 240 of each of the four classes.

Training clips: 768

Test clips: 192

## Part A: the Mel filter bank (task 1)

The width of the first filter, in bins: 3, which is 94 Hz. The first
filter peaks at bin 2, and the bins are 31.25 Hz apart, so the filter is
narrower than the resolution of the FFT.

The width of the last filter, in bins: 40, which is 1250 Hz.

The peak of the first filter, in bins: 2.

The peak of the last filter, in bins: 236, which is 7375 Hz.

## Part B: the cepstral coefficients (task 2)

The mean of the first coefficient: $-13.071$. It is the mean of the 32
log energies of the frame, and a clip of speech has a power well below 1,
so the logarithm is a large negative number.

The mean of the last coefficient: $0.064$, near zero.

What the middle panel of the plot shows: the energy of each of the 32
filters for the 50 frames. The bright band moves up and down with the
pitch of the voice, and the panels of the word `yes` and of the word `no`
differ in the position of the band.

What the bottom panel of the plot shows: the coefficient 1 to 12 of each
frame. The values change slowly over time, so the picture has horizontal
bands. The cepstrum keeps the envelope of the spectrum and not the fine
structure.

Time to compute the features of all the clips, in seconds: 2.4 s for the
960 clips on the laptop of the report.

## Part C: the classifier (task 3)

| Item | Your result |
|---|---|
| Frames after the two convolutions and the two pooling layers | 11 |
| Number of parameters | 3620 |
| Test accuracy in percent | 77.1 |

The check calculates the same number: the first convolution has
$3 \times 13 \times 16 + 16 = 640$ parameters, the second
$3 \times 16 \times 32 + 32 = 1568$, and the dense layer
$11 \times 32 \times 4 + 4 = 1412$.

## Part D: three inputs for the same task (task 4)

| Input | Values per clip | Parameters | Test accuracy |
|---|---|---|---|
| Raw audio | 16000 | 513380 | 52.6 |
| Log Mel spectrogram | 1600 | 4532 | 72.9 |
| Cepstral coefficients | 650 | 3620 | 77.1 |

Your prediction for task 4, written before the experiment: the cepstral
coefficients, because they have the fewest values and the chapter says that
they are the best choice for speech.

The input that won in your run: the cepstral coefficients, with 77.1
percent against 72.9 percent for the spectrogram and 52.6 percent for the
raw audio.

## Questions

1. The cepstral coefficients give the smallest model: 3620 parameters
   against 513380 for the raw audio, so 509760 parameters less, or 99.3
   percent less. The raw audio needs 16000 inputs, and the flattening layer
   before the dense layer then holds 3998 * 32 = 127936 values.
2. The 13 coefficients describe the shape of the spectrum of the frame.
   The first one is the mean of the 32 log energies, so it holds the energy
   of the frame. The next ones describe the envelope from coarse to fine,
   and the last ones the fine structure. The cosine transform makes them
   comparable because it mixes all the filters: two filters that carry the
   same energy give a small coefficient, and two filters that carry
   different energies give a large one. After the transform the values no
   longer repeat one another, which is what a network needs.
3. The split is random, so a clip of a speaker that is in the training set
   has another clip of the same speaker in the test set. The model then
   recognises the voice of the speaker and not only the word, so the test
   accuracy is too high. For a product I would split by speaker: pick 4 of
   the 6 speakers for the training, and keep the 2 others for the test. The
   file names of the dataset hold the speaker code, so the split needs no
   new file. I expect the accuracy to fall by 5 to 10 points.
