import cohere
from flask import Flask
import numpy as np

app = Flask(__name__)


@app.route("/api")
def test():
    return "foo"


co = cohere.Client("syQmRBFrWWq3tpYnYwLz0TZuqIxjhitXqUbmWR5J")


def textGeneration():
    favRestaurants = input(
        "What restaurants do you like? (input a comma separated list) "
    ).strip()
    favFoods = input("What are your favourite foods? (input a comma separated list) ")
    prompt = f"This is a conversation between someone looking for food recommendations and their friend who will recommend similar food to the ones that the other person already likes. Friend looking for food recommendations: 'I like to eat at {favRestaurants} and my favourite foods are {favFoods} what food do you think I should try? Friend who will recommend food: I thnk you should try these dishes:"

    response = co.generate(
        prompt=prompt, model="xlarge", temperature=0.6, max_tokens=100
    )
    print(response.generations[0].text)


def calculateSimilarity(a, b):
    # compare themes
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def checkSimilary(phrase1, phrase2):
    phrases = [phrase1, phrase2]
    p1, p2 = co.embed(phrases).embeddings
    return calculateSimilarity(p1, p2)
