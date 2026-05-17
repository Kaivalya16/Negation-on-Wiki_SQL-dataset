import sqlite3


DB_PATH = "data/raw/wikisql/train.db"


def execute_query(query):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    try:

        cursor.execute(query)

        results = cursor.fetchall()

        conn.close()

        return results

    except Exception as e:

        conn.close()

        print("SQL ERROR:", e)

        return None