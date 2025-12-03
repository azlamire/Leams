import requests, json

test = requests.get(
    "https://api.rawg.io/api/platforms?key=1c99d4bafb034c21997b152404f2609a"
)

y = json.dumps(test.content.decode("utf-8"), indent=4)
print(y)
testing = open("testing.json", "w")
testing.write(y)
