import sqlite3


DB_PATH = "data/raw/wikisql/train.db"


def execute_query(query):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    try:

        cursor.execute(query)

        results = cursor.fetchall()

        return {
            "success": True,
            "results": results
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

    finally:
        conn.close()