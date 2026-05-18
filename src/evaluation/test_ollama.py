from src.evaluation.table_context import (
    load_table,
    dataframe_to_text
)

from src.evaluation.ollama_evaluator import (
    ask_ollama
)


table_id = "1-1000181-1"

df = load_table(table_id)

table_text = dataframe_to_text(df)

question = (
    "Tell me what the notes are for South Australia"
)

answer = ask_ollama(
    question,
    table_text
)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)