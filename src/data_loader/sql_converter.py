AGG_OPS = {
    0: "",
    1: "MAX",
    2: "MIN",
    3: "COUNT",
    4: "SUM",
    5: "AVG"
}

COND_OPS = {
    0: "=",
    1: ">",
    2: "<"
}


def convert_to_sql(example, table):

    sql_data = example["sql"]

    # SELECT column
    sel_index = sql_data["sel"]

    sel_col = table["header"][sel_index]

    # Aggregation
    agg = AGG_OPS[sql_data["agg"]]

    if agg:
        select_clause = f"SELECT {agg}([{sel_col}])"
    else:
        select_clause = f"SELECT [{sel_col}]"

    # FROM
    from_clause = f"FROM [{table['id']}]"

    # WHERE
    conditions = []

    for cond in sql_data["conds"]:

        col_index, op_index, value = cond

        col_name = table["header"][col_index]

        op = COND_OPS[op_index]

        # String handling
        if isinstance(value, str):
            value = value.replace("'", "''")
            value = f"'{value}'"

        condition = f"[{col_name}] {op} {value}"

        conditions.append(condition)

    # Join conditions
    if conditions:
        where_clause = " WHERE " + " AND ".join(conditions)
    else:
        where_clause = ""

    query = f"{select_clause} {from_clause}{where_clause};"

    return query