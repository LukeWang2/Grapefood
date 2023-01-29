import cohere, boto3
import numpy as np

AWS_ACCESS_KEY_ID = "AKIA4EX46IN5ZBZ3VRPW"
AWS_SECRET_ACCESS_KEY = "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"
REGION_NAME = "ca-central-1"


db = boto3.resource(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)
table = db.Table("user_interests")

co = cohere.Client("syQmRBFrWWq3tpYnYwLz0TZuqIxjhitXqUbmWR5J")


def registerUser(username, password, contact):
    try:
        table.put_item(
            Item={
                "user": username,
                "pass": password,
                "contact": contact,
                "interests": [],
            },
            ConditionExpression=f"attribute_not_exists(Username)",
        )
    except:
        print("This username taken.")


def storeInterests(username, interests):
    table.update_item(
        Key={"user": username},
        UpdateExpression="SET interests = list_append(interests, :val)",
        ExpressionAttributeValues={":val": [interests]},
    )


def getInterests(username):
    response = table.get_item(Key={"user": username})
    return str(response["Item"]["interests"]).replace("[", "").replace("]", "")


def deleteUser(username):
    table.delete_item(Key={"user": username})


def generateFoodRecommendations(favRestaurants, favFoods):
    prompt = f"""This is a conversation between someone looking for food 
    recommendations and their friend who will recommend similar food to the 
    ones that the other person already likes. Friend looking for food 
    recommendations: 'I like to eat at {favRestaurants} and my favourite foods 
    are {favFoods} what food do you think I should try? Friend who will 
    recommend food: I think you should try these dishes:"""

    response = co.generate(
        prompt=prompt, model="xlarge", temperature=0.6, max_tokens=50
    )
    return response.generations[0].text


def generateRestaurantRecommendations(favRestaurants, favFoods):
    prompt = f"""This is a conversation between someone looking for food 
    recommendations and their friend who will recommend restaurants similar to 
    the ones that the other person already likes. Friend looking for food 
    recommendations: 'I like to eat at {favRestaurants} and my favourite foods 
    are {favFoods} what restaurants do you think I should try? Friend who will 
    recommend a restaurants: I think you should try these restaurants:"""

    response = co.generate(
        prompt=prompt, model="xlarge", temperature=0.6, max_tokens=50
    )
    return response.generations[0].text


def generateRecommendation(type):
    favRestaurants = input(
        "What restaurants do you like? (input a comma separated list) "
    ).strip()
    favFoods = input("What are your favourite foods? (input a comma separated list) ")
    if type == "food":
        return generateFoodRecommendations(favRestaurants, favFoods)
    elif type == "restaurant":
        return generateRestaurantRecommendations(favRestaurants, favFoods)


def calculateSimilarity(a, b):
    # compare themes
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def checkSimilary(phrase1, phrase2):
    phrases = [phrase1, phrase2]
    p1, p2 = co.embed(phrases).embeddings
    return calculateSimilarity(p1, p2)


# find users which have the most similarities and recommend them
def recommendUsers(username):
    response = table.scan()["Items"]
    recommended = []
    for user in response:
        if user["user"] == username:
            pass
        similar = checkSimilary(
            str(user["interests"]).replace("[", "").replace("]", "")
        )
        if similar >= 0.7:
            recommended.append((user["user"], user["contact"]))
    if len(recommended) == 0:
        return "No users have similar enough interests"
    end = ""
    for u, c in recommended:

        end += f"{u} has similar food interests to you and their contact info is {c}\n"
    return end
