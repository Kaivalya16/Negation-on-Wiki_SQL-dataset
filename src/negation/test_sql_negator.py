from src.negation.sql_negator import negate_sql


query = """
SELECT [Position]
FROM [1-10015132-11]
WHERE [College] = 'Butler CC (KS)';
"""


print("ORIGINAL QUERY:\n")
print(query)


# -----------------------------------
# NOT method
# -----------------------------------

negated_1 = negate_sql(
    query,
    method="not"
)

print("\nNEGATED QUERY (NOT):\n")

print(negated_1)


# -----------------------------------
# Operator flip method
# -----------------------------------

negated_2 = negate_sql(
    query,
    method="operator_flip"
)

print("\nNEGATED QUERY (OPERATOR FLIP):\n")

print(negated_2)