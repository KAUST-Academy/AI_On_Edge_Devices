# Test notes: Day 6 lab

## 1. Checklist for the instructor

Run the solution notebook on one lab laptop before the lab. Record the
result here.

- Date of the test: YYYY-MM-DD
- Laptop (processor, RAM):
- Tool versions: see `Labs/VERSIONS.md`

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run section 0 with no dataset in the home folder | Does the download work in the classroom network? The time. | |
| 2 | Run the complete solution notebook | The run time. The lab plan needs less than 15 minutes. | |
| 3 | Compare the tables with `solutions/compression.ipynb` | Are the accuracy values and the file sizes equal? | |
| 4 | Read the latency column of section 8 | Is `int8` slower or faster than `float32` on this laptop? | |
| 5 | Run the student notebook with no change | Does it print `not complete` for tasks 1, 3, 4, 5, and 7? | |
| 6 | Copy the folder `fashion-mnist` of `.keras/datasets/` to a USB drive | The fallback for a group with no download | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 2. After the test

1. If the notebook needs more than 15 minutes on a lab laptop, decrease the
   number of epochs of runs 3 and 4 in the generator script.
2. If a table of the solution is different on the lab laptop, write the
   difference here. The accuracy can change with a different version of
   TensorFlow.
3. After the hardware test of Day 9, write in the README of this lab which
   format is faster on the Raspberry Pi.
