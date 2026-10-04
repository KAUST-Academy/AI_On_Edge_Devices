# Day 8 lab report: example

This is an example of a complete report. Part B and the two tables of the
export in Part C have the output of the solution notebook on the work
computer of the course, an x86 computer (2026-10-02). The detections of
Part A come from a run of the two scripts on that computer. Each time of
Part A, the live detection of Part C, and Part D need a Raspberry Pi.
Nobody measured them: the text "measure in the lab" marks each such value.

Group: example

Names: the course team

Date: 2026-10-02

Host name of the Raspberry Pi: measure in the lab

## Part A: pre-trained models

The two models with the image `bus.jpg` on the Raspberry Pi:

| Item | SSD MobileNet V1 | YOLO11n at 640 | YOLO11n at 320 |
|---|---|---|---|
| Shape and type of the input | 1 x 300 x 300 x 3, `uint8` | not in the output | not in the output |
| Load time in ms | measure in the lab | measure in the lab | measure in the lab |
| First run in ms | measure in the lab | measure in the lab | measure in the lab |
| Inference, median in ms | measure in the lab | measure in the lab | measure in the lab |
| Pre-processing and post-processing, median in ms | not in the output | measure in the lab | measure in the lab |
| Number of detections (score 0.5 for SSD, 0.25 for YOLO) | 4 | 5 | 5 |
| Number of persons | 3 | 4 | 4 |

The four outputs of the SSD file:

| Output | Shape | Content |
|---|---|---|
| 0 | 1 x 10 x 4, `float32` | The boxes: `ymin, xmin, ymax, xmax` from 0 to 1 |
| 1 | 1 x 10, `float32` | The class number of each box |
| 2 | 1 x 10, `float32` | The score of each box |
| 3 | 1, `float32` | The number of valid rows |

The detections after Task A1 (image `bus.jpg`). These are the values of the
work computer. The values of the board can differ by a small amount.

| Class | Score | Box x1, y1, x2, y2 in pixels |
|---|---|---|
| person | 0.83 | 51, 387, 221, 899 |
| bus | 0.74 | 19, 254, 786, 757 |
| person | 0.64 | 218, 429, 342, 857 |
| person | 0.61 | 673, 328, 811, 873 |

The IoU threshold of the suppression (YOLO11n at 640, image `bus.jpg`):

| IoU threshold | Number of detections |
|---|---|
| 0.7 (default) | 5 |
| 0.9 | 6 |

The photo of your desk:

| Model | Does it find the bottle? Score | Does it find the cup? Score | Other detections |
|---|---|---|---|
| SSD MobileNet V1 | measure in the lab | | |
| YOLO11n at 640 | measure in the lab | | |

Your answers:

1. The suppression of the SSD model is the last operator of the file
   (`TFLite_Detection_PostProcess`), so the runtime does it, and the file
   gives the final list of 10 rows. For YOLO11n, the suppression runs in the
   Python program of the package, after the inference.
2. measure in the lab. The network has 4 times fewer pixels at 320, so the expected
   factor is about 4 for the inference. The measured factor is usually
   lower, because some costs do not change with the image size.
3. The suppression removes a box only when its IoU with a better box is
   above the threshold. With the threshold 0.9, only boxes that are almost
   the same are removed, so more boxes of the same object stay.

## Part B: custom model

Versions on the laptop:

| Tool | Version |
|---|---|
| Python | 3.10.12 |
| `torch` | 2.13.0 |
| `ultralytics` | 8.4.171 |

The dataset (section 1):

| Split | Images | Labels `bottle` | Labels `cup` | Labels for each image | Median label side |
|---|---|---|---|---|---|
| `train` | 240 | 172 | 185 | 1.49 | 29 percent |
| `valid` | 60 | 41 | 43 | 1.40 | 36 percent |
| `test` | 100 | 71 | 77 | 1.48 | 28 percent |

1. Yes, with a tolerance of some pixels. The boxes of COCO come from the
   outline of each object.
2. An example: a jar or a glass bowl that stands next to a labelled bottle.
   The rules of COCO put it into a different class, or into no class.

Task 1 (section 3):

| Pair | IoU |
|---|---|
| Pair 1 of the lecture | 0.67 |
| Pair 2 of the lecture | 0.33 |
| The second box for pair 1 | 0.82 |

Task 2 (section 4):

| Item | Your result |
|---|---|
| Candidates in the raw output | 8400 |
| Candidates with a score above 0.25 | 47 |
| Detections with the IoU threshold 0.7 | 5 |
| Detections with the IoU threshold 0.9 | 8 |

Task 3 and the baseline (section 5). Write the prediction before you run the
cell: is the recall at 320 pixels lower than at 640 pixels?

Prediction: yes. An object has half the side in pixels at 320, and small
objects are the first objects that a detector misses (Part 3 of the lecture).

| Pre-trained YOLO11n, both classes | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| Image size 320 | 85 | 27 | 63 | 0.76 | 0.57 |
| Image size 640 | 105 | 35 | 43 | 0.75 | 0.71 |

The training (section 6):

| Item | Your result |
|---|---|
| Training time in minutes | 8.7 (4 cores of the work computer) |
| Best epoch | 25 |
| mAP50 on the validation images | 0.656 |
| mAP50-95 on the validation images | 0.491 |

1. The losses go down slowly: the box loss is 0.819 at epoch 20
   and 0.775 at epoch 25. The class loss is 0.918 and 0.840.
2. The mAP50-95 is 0.458 at epoch 20 and 0.491 at epoch
   25. The curve is almost flat, so more epochs give a small gain
   only. More images give more.
3. The 60 images have 84 labels. Some labels that change between a true
   positive and a false negative move the mAP by some hundredths.

Your model on the 100 test images (section 7):

| Class | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| all | 0.678 | 0.468 | 0.545 | 0.380 |
| `bottle` | 0.656 | 0.404 | 0.485 | 0.336 |
| `cup` | 0.699 | 0.532 | 0.604 | 0.425 |

The comparison. Write the prediction before you run the cell: which model
has the higher recall for the two classes?

Prediction: the pre-trained model. It saw many more bottles and cups.

| Model, both classes, score threshold 0.25 | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| Pre-trained at 320 | 85 | 27 | 63 | 0.76 | 0.57 |
| Pre-trained at 640 | 105 | 35 | 43 | 0.75 | 0.71 |
| Your model at 320 | 77 | 66 | 71 | 0.54 | 0.52 |

Your answers:

1. Read the two cases in the figure of your run. A frequent false positive
   is a glass, a jar, or a vase with the class `cup` or `bottle`. A frequent
   false negative is a bottle that a second object hides in part.
2. The validation images selected the best epoch, so their result is too
   good. No step of the training used the test images. The mAP50 is
   0.656 on the validation images and 0.545 on the test images.
3. First case: the product needs a class that the pre-trained model does
   not know, for example the box and the wheel of the kit lab. Second case:
   the images of the product are different from the images of COCO, for
   example a camera above a conveyor. Here the recall is 0.52 for the
   custom model and 0.57 for the pre-trained model at 320 pixels
   (0.71 at 640 pixels): 240 training images are not sufficient to
   pass a model that learned the two classes from a much larger dataset.

## Part C: export and deploy

The export (section 8). Write the prediction before you run the cell: how
large is the `int8` file, as a part of the `float32` file?

Prediction: about one quarter, because a weight needs 1 byte in place of 4
bytes.

| File | Runtime | Precision | Image size | Bytes | Export time in s |
|---|---|---|---|---|---|
| `cupbottle_320_ncnn_model` | NCNN | `float32` | 320 | 10 378 421 | 4 |
| `cupbottle_320.tflite` | LiteRT | `float32` | 320 | 10 553 005 | 16 |
| `cupbottle_320_int8.tflite` | LiteRT | `int8` | 320 | 3 023 254 | 32 |
| `cupbottle_640_ncnn_model` | NCNN | `float32` | 640 | 10 454 023 | 5 |
| `cupbottle_640.tflite` | LiteRT | `float32` | 640 | 10 628 605 | 16 |
| `cupbottle_640_int8.tflite` | LiteRT | `int8` | 640 | 3 041 798 | 53 |

The `int8` file has 29 percent of the size of the `float32` file. The
file also holds the structure of the graph and the scales.

The accuracy of each file on the test images (section 9). Write the two
predictions before you run the cell.

Prediction 1, the loss of `int8` in points of mAP50-95: about 0.09, the
value of the lecture for the complete model.

Prediction 2, the mAP at 640 pixels against the mAP at 320 pixels: lower,
because the model learned from images of 320 pixels.

| File | Precision | Image size | mAP50 | mAP50-95 |
|---|---|---|---|---|
| `cupbottle_320.pt` | PyTorch | 320 | 0.545 | 0.380 |
| `cupbottle_320.tflite` | `float32` | 320 | 0.545 | 0.380 |
| `cupbottle_320_int8.tflite` | `int8` | 320 | 0.520 | 0.339 |
| `cupbottle_640.pt` | PyTorch | 640 | 0.578 | 0.400 |
| `cupbottle_640.tflite` | `float32` | 640 | 0.578 | 0.400 |
| `cupbottle_640_int8.tflite` | `int8` | 640 | 0.543 | 0.320 |

| Loss of `int8` against `float32` | mAP50 | mAP50-95 |
|---|---|---|
| At 320 pixels | 0.025 | 0.041 |
| At 640 pixels | 0.035 | 0.079 |

The LiteRT `float32` file has the same mAP as the PyTorch file. The mAP50-95
at 640 pixels is 0.020 higher than at 320 pixels. With 100 test images, a
difference of 0.02 is not a clear result: the test does not confirm
prediction 2, and it does not show a gain for 640 pixels.

The live detection on the Raspberry Pi:

| Command | Frames in each second | Inference in ms | Objects that the model finds | Objects that it misses, and wrong detections |
|---|---|---|---|---|
| `cupbottle_320_ncnn_model` | measure in the lab | measure in the lab | measure in the lab | measure in the lab |
| `cupbottle_320_int8.tflite` | measure in the lab | measure in the lab | measure in the lab | measure in the lab |
| `cupbottle_320_ncnn_model` with `--conf 0.5` | measure in the lab | measure in the lab | measure in the lab | measure in the lab |

Your answers:

1. measure in the lab
2. measure in the lab
3. A higher score threshold removes the detections with a low score. The
   image has fewer wrong boxes, and the model misses more objects: the
   precision goes up and the recall goes down.

## Part D: measure

Write the prediction before you run `pi/bench_detect.py`.

| Question | Your prediction | Result |
|---|---|---|
| `float32`: which runtime is faster, NCNN or LiteRT? | NCNN: the companion book reports about 80 ms for a custom model at 320 pixels | measure in the lab |
| The gain of the frame rate from 640 to 320 pixels: 4, more than 4, or less than 4? | Less than 4: the capture and the post-processing do not become 4 times faster | measure in the lab |
| LiteRT: is `int8` faster than `float32`? By which factor? | Faster on an Arm processor, by a factor below 2 | measure in the lab |
| Which step is the largest after the inference? | The capture | measure in the lab |

The frame-rate table. Median times in ms of the second run of
`pi/bench_detect.py`, and the mAP50-95 of section 9 of the notebook:

| File | Runtime | Precision | Image size | Capture | Pre-processing | Inference | Post-processing | Frames in each second | mAP50-95 |
|---|---|---|---|---|---|---|---|---|---|
| `cupbottle_320_ncnn_model` | NCNN | `float32` | 320 | measure in the lab | measure in the lab | measure in the lab | measure in the lab | measure in the lab | 0.380 |
| `cupbottle_320.tflite` | LiteRT | `float32` | 320 | measure in the lab | measure in the lab | measure in the lab | measure in the lab | measure in the lab | 0.380 |
| `cupbottle_320_int8.tflite` | LiteRT | `int8` | 320 | measure in the lab | measure in the lab | measure in the lab | measure in the lab | measure in the lab | 0.339 |
| `cupbottle_640_ncnn_model` | NCNN | `float32` | 640 | measure in the lab | measure in the lab | measure in the lab | measure in the lab | measure in the lab | 0.400 |
| `cupbottle_640.tflite` | LiteRT | `float32` | 640 | measure in the lab | measure in the lab | measure in the lab | measure in the lab | measure in the lab | 0.400 |
| `cupbottle_640_int8.tflite` | LiteRT | `int8` | 640 | measure in the lab | measure in the lab | measure in the lab | measure in the lab | measure in the lab | 0.320 |

For the mAP of an NCNN folder, use the value of the LiteRT `float32` file of
the same image size.

| Item | Your result |
|---|---|
| Temperature at the start and at the end | measure in the lab |
| Largest difference of the frame rate between the two runs, in percent | measure in the lab |
| Frame rate of the live application of Part C with `cupbottle_320_ncnn_model` | measure in the lab |

The ratios:

| Ratio of the frame rates | NCNN | LiteRT `float32` | LiteRT `int8` |
|---|---|---|---|
| 320 pixels against 640 pixels | measure in the lab | measure in the lab | measure in the lab |

| Ratio of the frame rates | 320 pixels | 640 pixels |
|---|---|---|
| LiteRT `int8` against LiteRT `float32` | measure in the lab | measure in the lab |
| NCNN against LiteRT `float32` | measure in the lab | measure in the lab |

Your answers:

1. measure in the lab
2. measure in the lab
3. The live application also draws the boxes, makes a JPEG image, and sends
   it to the browser. The benchmark does not do these steps.
4. measure in the lab

## Decision Log

Question: a product with a Raspberry Pi 5 and a camera must count the
bottles and the cups on a table, with 10 frames in each second or more.
Which file do you select: which runtime, which image size, and which
precision?

Decision: measure in the lab. The answer needs the frame-rate table of the board.

Numbers that support the decision: the mAP50-95 on the test images is
0.380 for the `float32` file and 0.339 for the `int8` file at 320 pixels, and
0.400 and 0.320 at 640 pixels. The frame rates: measure in the lab.

Trade-off: the image size of 640 pixels costs about 4 times the inference
time, and it gives no clear gain of accuracy for a model that learned from
images of 320 pixels. The `int8` file is the smallest file, and it loses
0.041 of mAP50-95 at 320 pixels. Select `int8` only if the `float32`
file does not reach 10 frames in each second.
