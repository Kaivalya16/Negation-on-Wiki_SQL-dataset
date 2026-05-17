import json

from src.data_loader.sql_converter import convert_to_sql
from src.filtering.execute_sql import execute_query

with open("data/raw/wikisql/train.jsonl", "r", encoding="utf-8") as f:
    example = json.loads(next(f))

tables = {}

with open("data/raw/wikisql/train.tables.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        table = json.loads(line)

        tables[table["id"]] = table


# -----------------------------
# Get matching table
# -----------------------------

table = tables[example["table_id"]]


# -----------------------------
# Generate SQL
# -----------------------------

query = convert_to_sql(example, table)

print("\nQUESTION:")
print(example["question"])

print("\nGENERATED SQL:")
print(query)


# -----------------------------
# Execute query
# -----------------------------

results = execute_query(query)

print("\nRESULTS:")
print(results)