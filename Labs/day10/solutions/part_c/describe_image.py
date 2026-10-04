#!/usr/bin/env python3
"""Part C of the Day 10 lab, option 2: image description with a
vision-language model.

Runs on: the Raspberry Pi 5 in ~/ollama, or a laptop with Ollama.
Needs:   the packages "ollama" and "pydantic", a running Ollama server, and
         the model llava-phi3:3.8b.

Use:
    python part_c/describe_image.py                   the five test images
    python part_c/describe_image.py --image my_photo.jpg

For each image, the model answers with a JSON object (the class Scene,
Task C2): a caption, at most 5 objects, and the number of containers (cups,
glasses, and bottles). The script checks each answer with Pydantic.

Hardware status: not tested on hardware (prepared on 2026-10-03). Tested on
the work computer of the course with Ollama 0.32.6.

Credits: the model and the image prompt follow the lab "Small Language
Models" of "Machine Learning Systems" (mlsysbook.ai, CC BY-NC-SA 4.0) and
the notebook 30-Function_Calling_with_images.ipynb of "EdgeML with
Raspberry Pi" (Marcelo Rovai, GPL-3.0). The five images come from COCO 2017
(part_c/images/README.md gives the source and the licence of each image).
"""

import argparse
import os
import pathlib
import sys
import time
from typing import Annotated

import ollama
from pydantic import BaseModel, Field, ValidationError

HERE = pathlib.Path(__file__).resolve().parent
LAB = HERE.parent.parent if HERE.parent.name == "solutions" else HERE.parent
PROMPT = ("Describe the image. Give a short caption, the list of the main objects, "
          "and the number of cups, glasses, and bottles.")


class Scene(BaseModel):
    """Task C2: the answer for one image.

    caption:    a text
    objects:    a list of at most 5 texts, each with at most 40 characters.
                Without these limits a small model can write until the token
                limit, and the JSON is then not complete.
    containers: an integer
    """
    caption: str
    objects: list[Annotated[str, Field(max_length=40)]] = Field(max_length=5)
    containers: int


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", default="llava-phi3:3.8b")
    parser.add_argument("--image", help="one image of your own")
    args = parser.parse_args()

    schema = Scene.model_json_schema()
    objects = schema.get("properties", {}).get("objects", {})
    if objects.get("maxItems") != 5 or objects.get("items", {}).get("maxLength") != 40 \
            or "containers" not in schema.get("required", []):
        print("Task C2 is not complete: check the three fields of Scene.")
        return 1
    print("Task C2: complete")

    options = {"temperature": 0, "seed": 0, "num_ctx": 2048, "num_predict": 200}
    if os.environ.get("EDGEAI_CPU"):   # the course tested on a computer with a GPU
        options["num_gpu"] = 0
    images = [pathlib.Path(args.image)] if args.image else sorted((LAB / "part_c" / "images").glob("*.jpg"))
    valid = 0
    for path in images:
        start = time.monotonic()
        reply = ollama.generate(model=args.model, prompt=PROMPT, images=[str(path)],
                                format=schema, options=options, keep_alive="10m")
        seconds = time.monotonic() - start
        try:
            s = Scene.model_validate_json(reply.response)
            valid += 1
            text = "%s | objects: %s | containers: %d" % (s.caption, ", ".join(s.objects), s.containers)
        except ValidationError:
            text = "not valid: " + reply.response.strip().replace("\n", " ")[:70]
        print("%s: %.0f s, prompt %d tokens, answer %d tokens\n   %s"
              % (path.name, seconds, reply.prompt_eval_count or 0, reply.eval_count or 0, text))
    print()
    print("Model %s: valid structured output %d of %d" % (args.model, valid, len(images)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
