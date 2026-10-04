# Day 8 lab report

Group:

Names:

Date:

Host name of the Raspberry Pi:

## Part A: pre-trained models

The two models with the image `bus.jpg` on the Raspberry Pi:

| Item | SSD MobileNet V1 | YOLO11n at 640 | YOLO11n at 320 |
|---|---|---|---|
| Shape and type of the input | | not in the output | not in the output |
| Load time in ms | | | |
| First run in ms | | | |
| Inference, median in ms | | | |
| Pre-processing and post-processing, median in ms | not in the output | | |
| Number of detections (score 0.5 for SSD, 0.25 for YOLO) | | | |
| Number of persons | | | |

The four outputs of the SSD file:

| Output | Shape | Content |
|---|---|---|
| 0 | | |
| 1 | | |
| 2 | | |
| 3 | | |

The detections after Task A1 (image `bus.jpg`):

| Class | Score | Box x1, y1, x2, y2 in pixels |
|---|---|---|
| | | |
| | | |
| | | |
| | | |

The IoU threshold of the suppression (YOLO11n at 640, image `bus.jpg`):

| IoU threshold | Number of detections |
|---|---|
| 0.7 (default) | |
| 0.9 | |

The photo of your desk:

| Model | Does it find the bottle? Score | Does it find the cup? Score | Other detections |
|---|---|---|---|
| SSD MobileNet V1 | | | |
| YOLO11n at 640 | | | |

Your answers:

1. The SSD file gives 10 rows for each image, and YOLO11n gives 8400
   candidates. Where does the suppression run for each model?
2. The image size goes from 640 to 320 pixels. By which factor does the
   inference time of YOLO11n change? Which factor did you expect?
3. Why does the threshold 0.9 give more detections than the threshold 0.7?

## Part B: custom model

Versions on the laptop:

| Tool | Version |
|---|---|
| Python | |
| `torch` | |
| `ultralytics` | |

The dataset (section 1):

| Split | Images | Labels `bottle` | Labels `cup` | Labels for each image | Median label side |
|---|---|---|---|---|---|
| `train` | | | | | |
| `valid` | | | | | |
| `test` | | | | | |

1. Does each box touch the object on its four sides?
2. Which object looks like a bottle or a cup and has no label? Give the file
   name.

Task 1 (section 3):

| Pair | IoU |
|---|---|
| Pair 1 of the lecture | |
| Pair 2 of the lecture | |
| The second box for pair 1 | |

Task 2 (section 4):

| Item | Your result |
|---|---|
| Candidates in the raw output | |
| Candidates with a score above 0.25 | |
| Detections with the IoU threshold 0.7 | |
| Detections with the IoU threshold 0.9 | |

Task 3 and the baseline (section 5). Write the prediction before you run the
cell: is the recall at 320 pixels lower than at 640 pixels?

Prediction:

| Pre-trained YOLO11n, both classes | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| Image size 320 | | | | | |
| Image size 640 | | | | | |

The training (section 6):

| Item | Your result |
|---|---|
| Training time in minutes | |
| Best epoch | |
| mAP50 on the validation images | |
| mAP50-95 on the validation images | |

1. Do the two losses still go down at the last epoch?
2. Does the mAP still go up at the last epoch? Would more epochs help?
3. How do the 60 validation images explain a curve that is not smooth?

Your model on the 100 test images (section 7):

| Class | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| all | | | | |
| `bottle` | | | | |
| `cup` | | | | |

The comparison. Write the prediction before you run the cell: which model
has the higher recall for the two classes?

Prediction:

| Model, both classes, score threshold 0.25 | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| Pre-trained at 320 | | | | | |
| Pre-trained at 640 | | | | | |
| Your model at 320 | | | | | |

Your answers:

1. Describe one false positive and one false negative of your model in the
   figure. Give the file names.
2. Your model has a lower mAP than the validation images showed. Why is the
   result on the test images the result that you report?
3. Give two cases in which a product needs a custom model, also when a
   pre-trained model has a higher recall on these test images.

## Part C: export and deploy

The export (section 8). Write the prediction before you run the cell: how
large is the `int8` file, as a part of the `float32` file?

Prediction:

| File | Runtime | Precision | Image size | Bytes | Export time in s |
|---|---|---|---|---|---|
| `cupbottle_320_ncnn_model` | NCNN | `float32` | 320 | | |
| `cupbottle_320.tflite` | LiteRT | `float32` | 320 | | |
| `cupbottle_320_int8.tflite` | LiteRT | `int8` | 320 | | |
| `cupbottle_640_ncnn_model` | NCNN | `float32` | 640 | | |
| `cupbottle_640.tflite` | LiteRT | `float32` | 640 | | |
| `cupbottle_640_int8.tflite` | LiteRT | `int8` | 640 | | |

The accuracy of each file on the test images (section 9). Write the two
predictions before you run the cell.

Prediction 1, the loss of `int8` in points of mAP50-95:

Prediction 2, the mAP at 640 pixels against the mAP at 320 pixels:

| File | Precision | Image size | mAP50 | mAP50-95 |
|---|---|---|---|---|
| `cupbottle_320.pt` | PyTorch | 320 | | |
| `cupbottle_320.tflite` | `float32` | 320 | | |
| `cupbottle_320_int8.tflite` | `int8` | 320 | | |
| `cupbottle_640.pt` | PyTorch | 640 | | |
| `cupbottle_640.tflite` | `float32` | 640 | | |
| `cupbottle_640_int8.tflite` | `int8` | 640 | | |

| Loss of `int8` against `float32` | mAP50 | mAP50-95 |
|---|---|---|
| At 320 pixels | | |
| At 640 pixels | | |

The live detection on the Raspberry Pi:

| Command | Frames in each second | Inference in ms | Objects that the model finds | Objects that it misses, and wrong detections |
|---|---|---|---|---|
| `cupbottle_320_ncnn_model` | | | | |
| `cupbottle_320_int8.tflite` | | | | |
| `cupbottle_320_ncnn_model` with `--conf 0.5` | | | | |

Your answers:

1. Your model on the photo of your desk: compare with the pre-trained model
   of Part A.
2. Which change of the scene (distance, background, light, a hand on the
   object) makes the model fail?
3. What does the score threshold 0.5 change in the live image?

## Part D: measure

Write the prediction before you run `pi/bench_detect.py`.

| Question | Your prediction | Result |
|---|---|---|
| `float32`: which runtime is faster, NCNN or LiteRT? | | |
| The gain of the frame rate from 640 to 320 pixels: 4, more than 4, or less than 4? | | |
| LiteRT: is `int8` faster than `float32`? By which factor? | | |
| Which step is the largest after the inference? | | |

The frame-rate table. Median times in ms of the second run of
`pi/bench_detect.py`, and the mAP50-95 of section 9 of the notebook:

| File | Runtime | Precision | Image size | Capture | Pre-processing | Inference | Post-processing | Frames in each second | mAP50-95 |
|---|---|---|---|---|---|---|---|---|---|
| `cupbottle_320_ncnn_model` | NCNN | `float32` | 320 | | | | | | |
| `cupbottle_320.tflite` | LiteRT | `float32` | 320 | | | | | | |
| `cupbottle_320_int8.tflite` | LiteRT | `int8` | 320 | | | | | | |
| `cupbottle_640_ncnn_model` | NCNN | `float32` | 640 | | | | | | |
| `cupbottle_640.tflite` | LiteRT | `float32` | 640 | | | | | | |
| `cupbottle_640_int8.tflite` | LiteRT | `int8` | 640 | | | | | | |

For the mAP of an NCNN folder, use the value of the LiteRT `float32` file of
the same image size.

| Item | Your result |
|---|---|
| Temperature at the start and at the end | |
| Largest difference of the frame rate between the two runs, in percent | |
| Frame rate of the live application of Part C with `cupbottle_320_ncnn_model` | |

The ratios:

| Ratio of the frame rates | NCNN | LiteRT `float32` | LiteRT `int8` |
|---|---|---|---|
| 320 pixels against 640 pixels | | | |

| Ratio of the frame rates | 320 pixels | 640 pixels |
|---|---|---|
| LiteRT `int8` against LiteRT `float32` | | |
| NCNN against LiteRT `float32` | | |

Your answers:

1. Compare the results with your predictions.
2. The lecture measured on an x86 processor: `int8` was slower than
   `float32`, and NCNN was slower than LiteRT. What do you measure on the
   Raspberry Pi?
3. The frame rate of the live application is lower than the frame rate of
   the benchmark for the same file. Which step makes the difference?
4. The exercise of the lecture predicts the frame rate at 320 pixels from
   the times at 640 pixels. Do the same with your times of one runtime, and
   compare with your measurement.

## Decision Log

Question: a product with a Raspberry Pi 5 and a camera must count the
bottles and the cups on a table, with 10 frames in each second or more.
Which file do you select: which runtime, which image size, and which
precision?

Decision:

Numbers that support the decision:

Trade-off:
