# Models of the Day 9 lab

The four files are the reference models for keyword spotting and for image
classification of the benchmark suite MLPerf Tiny.

| File | Bytes | Task | Input | Outputs | Source |
|---|---|---|---|---|---|
| `kws_int8.tflite` | 53 936 | Keyword spotting (DS-CNN) | 49 x 10 x 1, `int8` | 12 classes | `kws_ref_model.tflite`, copy with no change |
| `kws_float32.tflite` | 96 964 | Keyword spotting (DS-CNN) | 49 x 10 x 1, `float32` | 12 classes | made by this course from `kws_ref_model_float32.tflite` |
| `ic_int8.tflite` | 98 496 | Image classification (ResNet, CIFAR-10) | 32 x 32 x 3, `int8` | 10 classes | `pretrainedResnet_quant.tflite`, copy with no change |
| `ic_float32.tflite` | 318 144 | Image classification (ResNet, CIFAR-10) | 32 x 32 x 3, `float32` | 10 classes | `pretrainedResnet.tflite`, copy with no change |

Source: the repository `github.com/mlcommons/tiny` of MLCommons, folders
`benchmark/training/keyword_spotting/trained_models/` and
`benchmark/training/image_classification/trained_models/`, commit `4addd0f`.

Licence: Apache License, Version 2.0. Copyright of the MLPerf Tiny
contributors and MLCommons. You can get a copy of the licence at
`http://www.apache.org/licenses/LICENSE-2.0`. The files are distributed on
an "as is" basis, with no warranties or conditions of any kind.

## The file `kws_float32.tflite`

MLCommons publishes a keyword model with a `float32` input. In that file,
the weights of the five `CONV_2D` operators are stored in `int8`, and the
activations are `float32`. TensorFlow Lite Micro has no kernel for this
mixture. So the course made a file with `float32` weights:

1. Read each `int8` weight tensor of the published file.
2. Calculate the `float32` weights: weight = scale x integer.
3. Build the same network with these weights, and convert it to LiteRT.

The result has the same operators as the published file: 5 `CONV_2D`,
4 `DEPTHWISE_CONV_2D`, `AVERAGE_POOL_2D`, `RESHAPE`, `FULLY_CONNECTED`,
`SOFTMAX`. For 200 random inputs, the new file and the published file give
the same class each time. Nobody measured the accuracy of the new file on
the dataset Speech Commands.

## Inputs

- Keyword spotting: 49 frames with 10 MFCC values each. The `int8` file has
  the input scale 0.5847 and the zero point 83. The `float32` file takes the
  real value: scale x (integer - 83).
- Image classification: one image of 32 x 32 pixels with 3 colours. The
  `int8` file takes the pixel value minus 128. The `float32` file takes the
  pixel value from 0 to 255.

The MLPerf name and logo are trademarks of MLCommons Association. A time
that you measure with these files in this lab is not an MLPerf result.
