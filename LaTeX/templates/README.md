# Deck skeletons

This folder holds three skeletons for the decks of the course "AI on Edge Devices":

| Skeleton | Use for | Section files |
|---|---|---|
| `Theory_Deck.tex` | the theory deck of one day | `sections/theory/` |
| `Lab_Deck.tex` | the lab deck of one day | `sections/lab/` |
| `Module_Deck.tex` | one backup module | `sections/module/` |

Each skeleton loads `preamble/course.tex` and ends with the credits frame
`sections/credits.tex`. A skeleton does not build in this folder, because its
paths start at `LaTeX/`. Copy it first.

The placeholder text is in capital letters. Replace every capital placeholder
before you hand the deck to the instructor.

Run all commands below from the root of this repository.

## Start the theory deck of a day

```bash
cp LaTeX/templates/Theory_Deck.tex LaTeX/Day01_Theory.tex
cp -r LaTeX/templates/sections/theory LaTeX/sections/day01
sed -i 's/NN/01/g' LaTeX/Day01_Theory.tex LaTeX/sections/day01/*.tex
```

The deck has a cover, a contents frame, a motivation frame, a learning
outcomes frame, three blocks, a recap frame, a further reading frame, and the
credits frame. The three block files hold only comments, so the deck builds
from the first minute. Write one block in each file.

## Start the lab deck of a day

```bash
cp LaTeX/templates/Lab_Deck.tex LaTeX/Day01_Lab.tex
cp -r LaTeX/templates/sections/lab LaTeX/sections/day01_lab
sed -i 's/NN/01/g' LaTeX/Day01_Lab.tex LaTeX/sections/day01_lab/*.tex
```

The deck gives the goal, the plan of the three hours, the hardware and the
wiring, one frame for each part, the check criterion, the Decision Log
question, and the common problems.

## Start a backup module

```bash
mkdir -p LaTeX/sections/modules
cp LaTeX/templates/Module_Deck.tex LaTeX/Module_MC-1.tex
cp -r LaTeX/templates/sections/module LaTeX/sections/modules/MC-1
sed -i 's/MODID/MC-1/g' LaTeX/Module_MC-1.tex LaTeX/sections/modules/MC-1/*.tex
```

`MC-1` is the module ID. A module with theory and lab keeps `lab.tex`. A
module with theory only deletes `lab.tex` and its `\input` line in the main
file.

## Build a deck

```bash
bash build.sh --file Day01_Theory.tex
```

The PDF goes to `Lectures/`. The script prints an error in its last cleaning
step. The PDF is still correct.

## Rules for every deck

- Load only `preamble/course.tex`. Do not load `preamble/packages.tex` or
  `preamble/commands.tex`. Those two files belong to the older CNN recap deck.
- Keep the cover frame unchanged.
- Set `\coursecredits` in the main file. Name only the sources that the deck
  uses. The header of `preamble/course.tex` lists the commands.
- Name the source of each reused figure and each reused text on the same
  frame, with `\source{...}` or `\sourcehere{...}`.
- A frame that holds code needs the option `[fragile]`. A listing cannot stand
  in the argument of a command, so such a frame uses the environment
  `exerciseblock` or `answerblock` in place of `\exerciseframe`.
