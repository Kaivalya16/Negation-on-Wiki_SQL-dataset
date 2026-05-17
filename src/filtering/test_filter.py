import json

from src.data_loader.sql_converter import convert_to_sql
from src.negation.sql_negator import negate_sql
from src.filtering.execute_sql import execute_query
from src.filtering.answer_filter import is_valid_result


# Load one example
with open("data/raw/wikisql/train.jsonl", "r", encoding="utf-8") as f:
    example = json.loads(next(f))


# Load tables
tables = {}

with open("data/raw/wikisql/train.tables.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        table = json.loads(line)

        tables[table["id"]] = table


table = tables[example["table_id"]]


# Generate SQL
original_sql = convert_to_sql(example, table)

# Negate SQL
negated_sql = negate_sql(
    original_sql,
    method="operator_flip"
)

# Execute
original_response = execute_query(original_sql)

negated_response = execute_query(negated_sql)


# Print
print("\nORIGINAL RESULTS:")
print(original_response)

print("\nNEGATED RESULTS:")
print(negated_response)


# Filter check
print("\nORIGINAL VALID:")
print(is_valid_result(original_response))

print("\nNEGATED VALID:")
print(is_valid_result(negated_response))