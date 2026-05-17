import json

TABLE_PATH = "data/raw/wikisql/train.tables.jsonl"


def load_tables(path):

    tables = {}

    with open(path, "r", encoding="utf-8") as f:

        for line in f:

            table = json.loads(line)

            tables[table["id"]] = table

    return tables


tables = load_tables(TABLE_PATH)

print("Total tables:", len(tables))

# Print one table
first_key = list(tables.keys())[0]

print("\nSample Table:\n")

print(tables[first_key])