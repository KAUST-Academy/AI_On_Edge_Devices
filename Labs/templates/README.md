# Lab skeletons

Start every lab folder from the files here.

| File | Copy to |
|---|---|
| `lab_README.md` | `Labs/dayNN/README.md` or `Labs/modules/<ID>/README.md` |
| `TEST_NOTES.md` | the same folder |
| `lab_notebook.ipynb` | the same folder, with the name of the lab |

## Start the lab of a day

Run the commands from the root of this repository.

```bash
mkdir -p Labs/day01/sketches Labs/day01/solutions
cp Labs/templates/lab_README.md Labs/day01/README.md
cp Labs/templates/TEST_NOTES.md Labs/day01/TEST_NOTES.md
cp Labs/templates/lab_notebook.ipynb Labs/day01/model_budgets.ipynb
sed -i 's/Day NN/Day 01/g' Labs/day01/README.md Labs/day01/TEST_NOTES.md \
  Labs/day01/model_budgets.ipynb
```

Then write the content. The placeholder text is in capital letters. Replace
every capital placeholder.

## Rules

1. Do not write a measured number that nobody measured. Use a number from the
   source and name the source, or write "measure in the lab".
2. Write every changed line and every new file in `TEST_NOTES.md`.
3. The first cell of a notebook gives the credits of the source.
4. Add each new package to `Labs/requirements.txt` and each tool version to
   `Labs/VERSIONS.md`.
5. Add one row for the lab to the index in `Labs/README.md`.
