import cohere
from flask import Flask
import numpy as np

app = Flask(__name__)


@app.route("/api")
def test():
    return "foo"


co = cohere.Client("syQmRBFrWWq3tpYnYwLz0TZuqIxjhitXqUbmWR5J")


def textGeneration():
    prompt = input("Test ").strip()
    response = co.generate(
        prompt=prompt, model="xlarge", temperature=0.6, max_tokens=128
    )
    print(response.generations[0].text)


def checkSimilary(phrase1, phrase2):
    phrases = [phrase1, phrase2]
    p1, p2 = co.embed(phrases).embeddings
    return calculate_similarity(p1, p2)


def calculate_similarity(a, b):
    # compare thems
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
