import json

from sql_converter import convert_to_sql


# Load examples
with open("data/raw/wikisql/train.jsonl", "r", encoding="utf-8") as f:
    example = json.loads(next(f))


# Load tables
tables = {}

with open("data/raw/wikisql/train.tables.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        table = json.loads(line)

        tables[table["id"]] = table


# Get matching table
table = tables[example["table_id"]]

print("QUESTION:")
print(example["question"])

print("\nTABLE HEADERS:")
print(table["header"])

print("\nGENERATED SQL:")

query = convert_to_sql(example, table)

print(query)