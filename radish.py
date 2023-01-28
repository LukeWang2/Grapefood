import cohere

co = cohere.Client("syQmRBFrWWq3tpYnYwLz0TZuqIxjhitXqUbmWR5J")
prompt = input("Test").strip()
response = co.generate(prompt=prompt, model="xlarge", temperature=0.6, max_tokens=128)
print(response.generations[0].text)
