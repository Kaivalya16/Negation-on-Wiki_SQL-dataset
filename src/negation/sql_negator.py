import re


def negate_sql(query, method="not"):

    # Clean query
    query = query.strip()

    # Find WHERE clause
    where_match = re.search(
        r"WHERE (.*);",
        query,
        re.IGNORECASE
    )

    # No WHERE clause
    if not where_match:
        return None

    condition = where_match.group(1)

    # -----------------------------------
    # METHOD 1: NOT (...)
    # -----------------------------------

    if method == "not":

        negated_condition = f"NOT ({condition})"

    # -----------------------------------
    # METHOD 2: Operator Flip
    # -----------------------------------

    elif method == "operator_flip":

        negated_condition = condition

        replacements = {
            " = ": " != ",
            " > ": " <= ",
            " < ": " >= "
        }

        for old, new in replacements.items():

            negated_condition = negated_condition.replace(old, new)

    else:
        raise ValueError("Invalid negation method")

    # Replace WHERE clause
    negated_query = re.sub(
        r"WHERE (.*);",
        f"WHERE {negated_condition};",
        query,
        flags=re.IGNORECASE
    )

    return negated_query