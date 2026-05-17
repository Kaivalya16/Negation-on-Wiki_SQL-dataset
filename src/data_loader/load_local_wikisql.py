import json

TRAIN_PATH = "data/raw/wikisql/train.jsonl"


def load_jsonl(path):

    data = []

    with open(path, "r", encoding="utf-8") as f:

        for line in f:
            data.append(json.loads(line))

    return data


# Load training dataset
train_data = load_jsonl(TRAIN_PATH)

print("Total examples:", len(train_data))

print("\nFirst Example:\n")

print(train_data[0])