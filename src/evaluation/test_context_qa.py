from src.evaluation.table_context import (
    load_table,
    dataframe_to_text
)

from src.evaluation.gemini_evaluator import (
    ask_gemini
)


# Example table
table_id = "1-1000181-1"

# Load dataframe
df = load_table(table_id)

# Convert to text
table_text = dataframe_to_text(df)

print("\nTABLE:\n")
print(table_text)


# Ask question
question = (
    "Tell me what the notes are for South Australia"
)

answer = ask_gemini(
    question,
    table_text
)

print("\nQUESTION:\n")
print(question)

print("\nANSWER:\n")
print(answer)