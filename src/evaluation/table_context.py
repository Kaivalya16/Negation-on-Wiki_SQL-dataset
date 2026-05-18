import sqlite3
import pandas as pd


DB_PATH = "data/raw/wikisql/train.db"


def load_table(table_id,
               limit=10):

    table_name = (
        "table_" +
        table_id.replace("-", "_")
    )

    conn = sqlite3.connect(DB_PATH)

    try:

        query = (
            f"SELECT * FROM {table_name} "
            f"LIMIT {limit}"
        )

        df = pd.read_sql_query(
            query,
            conn
        )

        return df

    except Exception as e:

        print("TABLE LOAD ERROR:", e)

        return None

    finally:
        conn.close()


# -----------------------------------
# Convert dataframe to prompt text
# -----------------------------------

def dataframe_to_text(df):

    if df is None:
        return ""

    return df.to_markdown(index=False)