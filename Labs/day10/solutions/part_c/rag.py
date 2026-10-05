#!/usr/bin/env python3
"""Part C of the Day 10 lab, option 1: retrieval-augmented generation.

Runs on: the Raspberry Pi 5 in ~/ollama, or a laptop with Ollama.
Needs:   the packages "ollama" and "pydantic", a running Ollama server, and
         the models nomic-embed-text and llama3.2:1b (or llama3.2:3b).

Use:
    python part_c/rag.py                     the five test questions
    python part_c/rag.py --k 2 --model llama3.2:3b
    python part_c/rag.py --ask "When does the fan stop?"

Steps:
  1. Embed each fact of part_c/facts.txt with nomic-embed-text (once).
  2. Embed the question.
  3. Select the k facts with the highest cosine similarity (Task C1).
  4. Send the question and these facts to the language model. The answer is
     a JSON object with two fields (the class Answer).
The script checks each answer with Pydantic and with the correct answer of
part_c/questions.txt.
"""

import argparse
import math
import os
import pathlib
import re
import sys
import time

import ollama
from pydantic import BaseModel, Field, ValidationError

HERE = pathlib.Path(__file__).resolve().parent
LAB = HERE.parent.parent if HERE.parent.name == "solutions" else HERE.parent
EMBED_MODEL = "nomic-embed-text"


class Answer(BaseModel):
    answer: str = Field(max_length=200)
    fact_number: int


def cosine(u, v):
    """Task C1, step 1: return the cosine similarity of the vectors u and v."""
    dot = sum(a * b for a, b in zip(u, v))
    return dot / (math.sqrt(sum(a * a for a in u)) * math.sqrt(sum(b * b for b in v)))


def top_k(query, vectors, k):
    """Task C1, step 2: return the indexes of the k vectors that are most
    similar to query, the most similar first."""
    scores = [cosine(query, v) for v in vectors]
    return sorted(range(len(vectors)), key=lambda i: scores[i], reverse=True)[:k]


def read_lines(path):
    return [l.strip() for l in pathlib.Path(path).read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]


def embed(texts):
    return ollama.embed(model=EMBED_MODEL, input=texts).embeddings


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", default="llama3.2:1b")
    parser.add_argument("--k", type=int, default=2, help="facts in each prompt (default: 2)")
    parser.add_argument("--ask", help="one question of your own")
    args = parser.parse_args()

    if abs(cosine([1, 0], [1, 0]) - 1) > 1e-9 or abs(cosine([1, 0], [0, 2])) > 1e-9 \
            or top_k([1, 0], [[0, 1], [1, 0.1], [1, 1]], 2) != [1, 2]:
        print("Task C1 is not complete: check cosine and top_k.")
        return 1
    print("Task C1: complete")

    options = {"temperature": 0, "seed": 0, "num_ctx": 2048, "num_predict": 96}
    if os.environ.get("EDGEAI_CPU"):   # the course tested on a computer with a GPU
        options["num_gpu"] = 0
    facts = read_lines(LAB / "part_c" / "facts.txt")
    start = time.monotonic()
    fact_vectors = embed(["search_document: " + f for f in facts])
    print("Embedded %d facts in %.1f s (%d values for each vector)"
          % (len(facts), time.monotonic() - start, len(fact_vectors[0])))

    if args.ask:
        questions = [(args.ask, None)]
    else:
        questions = [tuple(x.strip() for x in l.split("|")) for l in read_lines(LAB / "part_c" / "questions.txt")]
    valid = correct = 0
    for question, expected in questions:
        start = time.monotonic()
        q_vector = embed(["search_query: " + question])[0]
        best = top_k(q_vector, fact_vectors, args.k)
        context = "\n".join("%d. %s" % (i + 1, facts[i]) for i in best)
        prompt = ("Use only these numbered facts to answer the question. Give the answer "
                  "in one short sentence and the number of the fact that you used.\n"
                  "Facts:\n%s\nQuestion: %s" % (context, question))
        reply = ollama.generate(model=args.model, prompt=prompt, format=Answer.model_json_schema(),
                                options=options, keep_alive="10m")
        seconds = time.monotonic() - start
        try:
            a = Answer.model_validate_json(reply.response)
            valid += 1
            text = "%s (fact %d)" % (a.answer, a.fact_number)
            ok = expected is not None and re.search(r"(?<![\w-])%s(?!\w)" % re.escape(expected), a.answer)
            correct += bool(ok)
            mark = "" if expected is None else ("correct" if ok else "WRONG, expected %s" % expected)
        except ValidationError:
            text, mark = "not valid: " + reply.response[:60], ""
        print("Q: %s\n   facts %s, prompt %d tokens, %.1f s\n   A: %s %s"
              % (question, [i + 1 for i in best], reply.prompt_eval_count or 0, seconds, text, mark))
    print()
    print("Model %s, k = %d: valid structured output %d of %d, correct %d of %d"
          % (args.model, args.k, valid, len(questions), correct, len(questions)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
