import json

# {"scores": [{"name": "A", "score": 100}, {"name": "B", "score": 90}, {"name": "C", "score": 80}], "settings": {"music_in_game": "off", "music_in_menu": "off"}}
def set_scores(name, score):
    with open('Lista 6/data.json', 'r') as f:
        data = json.load(f)
    with open('Lista 6/data.json', 'w') as f:
        scores = data["scores"]
        for i in range(3):
            if score > scores[i]["score"]:
                scores.insert(i, {"name": name, "score": score})
                break
        if len(scores) > 3:
            scores.pop()
        data["scores"] = scores
        json.dump(data, f)


set_scores("test", 2)