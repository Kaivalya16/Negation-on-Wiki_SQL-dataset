from src.evaluation.table_context import (
    load_table
)


table_id = "1-1000181-1"

df = load_table(table_id)

print(df)