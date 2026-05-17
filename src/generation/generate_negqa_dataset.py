import json
from tqdm import tqdm

from src.data_loader.sql_converter import convert_to_sql
from src.negation.sql_negator import negate_sql
from src.negation.question_negator import negate_question
from src.filtering.execute_sql import execute_query
from src.filtering.answer_filter import is_valid_result


# -----------------------------------
# CONFIG
# -----------------------------------

TRAIN_DATA_PATH = "data/raw/wikisql/train.jsonl"

TABLE_PATH = "data/raw/wikisql/train.tables.jsonl"

OUTPUT_PATH = "data/processed/negqa_dataset.json"


# -----------------------------------
# LOAD TABLES
# -----------------------------------

tables = {}

with open(TABLE_PATH, "r", encoding="utf-8") as f:

    for line in f:

        table = json.loads(line)

        tables[table["id"]] = table


# -----------------------------------
# PROCESS DATASET
# -----------------------------------

generated_data = []

MAX_SAMPLES = 100


with open(TRAIN_DATA_PATH, "r", encoding="utf-8") as f:

    for idx, line in enumerate(tqdm(f)):

        # Limit samples initially
        if idx >= MAX_SAMPLES:
            break

        try:

            example = json.loads(line)

            question = example["question"]

            table = tables[example["table_id"]]

            # -----------------------------------
            # Generate SQL
            # -----------------------------------

            original_sql = convert_to_sql(
                example,
                table
            )

            negated_sql = negate_sql(
                original_sql,
                method="operator_flip"
            )

            # Skip invalid negation
            if negated_sql is None:
                continue

            # -----------------------------------
            # Generate Negated Question
            # -----------------------------------

            negated_question = negate_question(
                question
            )

            # -----------------------------------
            # Execute Queries
            # -----------------------------------

            original_response = execute_query(
                original_sql
            )

            negated_response = execute_query(
                negated_sql
            )

            # -----------------------------------
            # Filter Results
            # -----------------------------------

            original_valid = is_valid_result(
                original_response
            )

            negated_valid = is_valid_result(
                negated_response
            )

            # Keep only meaningful pairs
            if not (original_valid and negated_valid):
                continue

            # -----------------------------------
            # Save Sample
            # -----------------------------------

            sample = {

                "original_question": question,

                "negated_question": negated_question,

                "original_sql": original_sql,

                "negated_sql": negated_sql,

                "original_answers":
                    original_response["results"],

                "negated_answers":
                    negated_response["results"],

                "table_id":
                    example["table_id"]
            }

            generated_data.append(sample)

        except Exception as e:

            print("ERROR:", e)

            continue


# -----------------------------------
# SAVE DATASET
# -----------------------------------

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:

    json.dump(
        generated_data,
        f,
        indent=2,
        ensure_ascii=False
    )


print("\nTOTAL GENERATED SAMPLES:")

print(len(generated_data))

print("\nDATASET SAVED TO:")

print(OUTPUT_PATH)