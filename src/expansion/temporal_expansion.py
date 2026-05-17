import re


def create_year_range(year,
                      window=5):

    """
    Example:
    2010
    ->
    (2005, 2015)
    """

    lower = year - window

    upper = year + window

    return lower, upper


def expand_temporal_sql(query):

    """
    Convert:
    col3 = 2010

    ->
    col3 NOT BETWEEN 2005 AND 2015
    """

    # Detect 4-digit year
    pattern = r"(col\d+)\s*(=|>|<)\s*(\d{4})"

    match = re.search(pattern, query)

    if not match:
        return None

    column = match.group(1)

    year = int(match.group(3))

    # Basic sanity check
    if year < 1000 or year > 2100:
        return None

    lower, upper = create_year_range(year)

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


def expand_temporal_question(question):
    
    years = re.findall(r"\b\d{4}\b", question)

    if not years:
        return None

    year = int(years[0])

    if year < 1000 or year > 2100:
        return None

    lower, upper = create_year_range(year)

    patterns = {

        r"in \d{4}":
            f"not between {lower} and {upper}",

        r"from \d{4}":
            f"not between {lower} and {upper}",

        r"during \d{4}":
            f"not between {lower} and {upper}",

        r"on \d{4}":
            f"not between {lower} and {upper}"
    }

    for pattern, replacement in patterns.items():

        if re.search(pattern,
                     question,
                     re.IGNORECASE):

            expanded_question = re.sub(
                pattern,
                replacement,
                question,
                flags=re.IGNORECASE
            )

            # Improve grammar
            if " did " not in expanded_question.lower():

                expanded_question = (
                    expanded_question
                    .replace(" died ",
                             " did not die ")
                )

            return expanded_question

    return question