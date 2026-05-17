import re


def create_numeric_range(value,
                         percentage=0.2):

    """
    Example:
    5000
    ->
    (4000, 6000)
    """

    lower = int(value * (1 - percentage))

    upper = int(value * (1 + percentage))

    return lower, upper


def expand_numeric_sql(query):

    """
    Convert:
    col2 > 5000

    ->
    col2 NOT BETWEEN 4000 AND 6000
    """

    pattern = r"(col\d+)\s*(=|>|<)\s*(\d+)"

    match = re.search(pattern, query)

    if not match:
        return None

    column = match.group(1)

    number = int(match.group(3))

    lower, upper = create_numeric_range(number)

    replacement = (
        f"{column} NOT BETWEEN "
        f"{lower} AND {upper}"
    )

    expanded_query = re.sub(
        pattern,
        replacement,
        query
    )

    return expanded_query


def expand_numeric_question(question):

    numbers = re.findall(r"\d+", question)

    if not numbers:
        return None

    number = int(numbers[0])

    lower, upper = create_numeric_range(number)

    # Handle common patterns
    patterns = [

        r"greater than \d+",
        r"more than \d+",
        r"less than \d+",
        r"equal to \d+"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            question,
            re.IGNORECASE
        )

        if match:

            replacement = (
                f"not between "
                f"{lower} and {upper}"
            )

            expanded_question = re.sub(
                pattern,
                replacement,
                question,
                flags=re.IGNORECASE
            )

            return expanded_question

    # Fallback
    return question