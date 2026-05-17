from src.expansion.numerical_expansion import (
    expand_numeric_sql,
    expand_numeric_question
)


query = """
SELECT col1
FROM table_123
WHERE col2 > 5000;
"""


question = (
    "What cities have population greater than 5000?"
)


print("\nORIGINAL SQL:\n")
print(query)

expanded_sql = expand_numeric_sql(query)

print("\nEXPANDED SQL:\n")
print(expanded_sql)


print("\nORIGINAL QUESTION:\n")
print(question)

expanded_question = expand_numeric_question(
    question
)

print("\nEXPANDED QUESTION:\n")
print(expanded_question)