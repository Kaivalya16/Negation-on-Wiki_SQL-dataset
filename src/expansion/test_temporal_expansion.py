from src.expansion.temporal_expansion import (
    expand_temporal_sql,
    expand_temporal_question
)


query = """
SELECT col1
FROM table_123
WHERE col3 = 2010;
"""


question = (
    "Who died in 2010?"
)


print("\nORIGINAL SQL:\n")
print(query)

expanded_sql = expand_temporal_sql(query)

print("\nEXPANDED SQL:\n")
print(expanded_sql)


print("\nORIGINAL QUESTION:\n")
print(question)

expanded_question = expand_temporal_question(
    question
)

print("\nEXPANDED QUESTION:\n")
print(expanded_question)