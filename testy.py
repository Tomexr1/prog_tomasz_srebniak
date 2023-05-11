import json

def get_hs():
    with open('Lista 6/data.json', 'r') as f:
        data = json.load(f)
        names, scores = [], []
        for score in data["scores"]:
            names.append(score["name"])
            scores.append(score["score"])
    return names, scores

print(get_hs())