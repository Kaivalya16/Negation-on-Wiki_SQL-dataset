import json

from src.data_loader.sql_converter import convert_to_sql
from src.negation.sql_negator import negate_sql
from src.filtering.execute_sql import execute_query


# -----------------------------------
# Load one example
# -----------------------------------

with open("data/raw/wikisql/train.jsonl", "r", encoding="utf-8") as f:

    example = json.loads(next(f))


# -----------------------------------
# Load tables
# -----------------------------------

tables = {}

with open("data/raw/wikisql/train.tables.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        table = json.loads(line)

        tables[table["id"]] = table


table = tables[example["table_id"]]


# -----------------------------------
# Generate original SQL
# -----------------------------------

original_sql = convert_to_sql(example, table)

print("\nQUESTION:")
print(example["question"])

print("\nORIGINAL SQL:")
print(original_sql)


# -----------------------------------
# Execute original SQL
# -----------------------------------

original_results = execute_query(original_sql)

print("\nORIGINAL RESULTS:")
print(original_results)


# -----------------------------------
# Generate negated SQL
# -----------------------------------

negated_sql = negate_sql(
    original_sql,
    method="operator_flip"
)

print("\nNEGATED SQL:")
print(negated_sql)


# -----------------------------------
# Execute negated SQL
# -----------------------------------

negated_results = execute_query(negated_sql)

print("\nNEGATED RESULTS:")
print(negated_results)