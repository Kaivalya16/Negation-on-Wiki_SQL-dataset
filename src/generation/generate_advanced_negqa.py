import json
from tqdm import tqdm

from src.data_loader.sql_converter import convert_to_sql

from src.negation.sql_negator import negate_sql
from src.negation.question_negator import negate_question

from src.expansion.numerical_expansion import (
    expand_numeric_sql,
    expand_numeric_question
)

from src.expansion.temporal_expansion import (
    expand_temporal_sql,
    expand_temporal_question
)

from src.filtering.execute_sql import execute_query
from src.filtering.answer_filter import is_valid_result


# -----------------------------------
# CONFIG
# -----------------------------------

TRAIN_PATH = "data/raw/wikisql/train.jsonl"

TABLE_PATH = "data/raw/wikisql/train.tables.jsonl"

OUTPUT_PATH = (
    "data/processed/"
    "advanced_negqa_dataset.json"
)

MAX_SAMPLES = 500


# -----------------------------------
# LOAD TABLES
# -----------------------------------

tables = {}

with open(TABLE_PATH,
          "r",
          encoding="utf-8") as f:

    for line in f:

        table = json.loads(line)

        tables[table["id"]] = table


# -----------------------------------
# STORE RESULTS
# -----------------------------------

generated_dataset = []


# -----------------------------------
# PROCESS DATASET
# -----------------------------------

with open(TRAIN_PATH,
          "r",
          encoding="utf-8") as f:

    for idx, line in enumerate(tqdm(f)):

        if idx >= MAX_SAMPLES:
            break

        try:

            example = json.loads(line)

            question = example["question"]

            table = tables[example["table_id"]]

            # -----------------------------------
            # Generate Original SQL
            # -----------------------------------

            original_sql = convert_to_sql(
                example,
                table
            )

            # -----------------------------------
            # Execute Original SQL
            # -----------------------------------

            original_response = execute_query(
                original_sql
            )

            if not is_valid_result(
                original_response
            ):
                continue

            # =================================================
            # 1. BASIC NEGATION
            # =================================================

            try:

                negated_question = negate_question(
                    question
                )

                negated_sql = negate_sql(
                    original_sql,
                    method="operator_flip"
                )

                if negated_sql:

                    negated_response = execute_query(
                        negated_sql
                    )

                    if is_valid_result(
                        negated_response
                    ):

                        sample = {

                            "type":
                                "basic_negation",

                            "original_question":
                                question,

                            "generated_question":
                                negated_question,

                            "original_sql":
                                original_sql,

                            "generated_sql":
                                negated_sql,

                            "original_answers":
                                original_response["results"],

                            "generated_answers":
                                negated_response["results"],

                            "table_id":
                                example["table_id"]
                        }

                        generated_dataset.append(
                            sample
                        )

            except Exception as e:

                print("NEGATION ERROR:", e)

            # =================================================
            # 2. NUMERICAL EXPANSION
            # =================================================

            try:

                numeric_sql = expand_numeric_sql(
                    original_sql
                )

                numeric_question = (
                    expand_numeric_question(
                        question
                    )
                )

                if numeric_sql and numeric_question:

                    numeric_response = execute_query(
                        numeric_sql
                    )

                    if is_valid_result(
                        numeric_response
                    ):

                        sample = {

                            "type":
                                "numerical_expansion",

                            "original_question":
                                question,

                            "generated_question":
                                numeric_question,

                            "original_sql":
                                original_sql,

                            "generated_sql":
                                numeric_sql,

                            "original_answers":
                                original_response["results"],

                            "generated_answers":
                                numeric_response["results"],

                            "table_id":
                                example["table_id"]
                        }

                        generated_dataset.append(
                            sample
                        )

            except Exception as e:

                print("NUMERIC ERROR:", e)

            # =================================================
            # 3. TEMPORAL EXPANSION
            # =================================================

            try:

                temporal_sql = expand_temporal_sql(
                    original_sql
                )

                temporal_question = (
                    expand_temporal_question(
                        question
                    )
                )

                if temporal_sql and temporal_question:

                    temporal_response = execute_query(
                        temporal_sql
                    )

                    if is_valid_result(
                        temporal_response
                    ):

                        sample = {

                            "type":
                                "temporal_expansion",

                            "original_question":
                                question,

                            "generated_question":
                                temporal_question,

                            "original_sql":
                                original_sql,

                            "generated_sql":
                                temporal_sql,

                            "original_answers":
                                original_response["results"],

                            "generated_answers":
                                temporal_response["results"],

                            "table_id":
                                example["table_id"]
                        }

                        generated_dataset.append(
                            sample
                        )

            except Exception as e:

                print("TEMPORAL ERROR:", e)

        except Exception as e:

            print("GENERAL ERROR:", e)


# -----------------------------------
# SAVE FINAL DATASET
# -----------------------------------

with open(OUTPUT_PATH,
          "w",
          encoding="utf-8") as f:

    json.dump(
        generated_dataset,
        f,
        indent=2,
        ensure_ascii=False
    )


# -----------------------------------
# FINAL STATS
# -----------------------------------

print("\nTOTAL GENERATED SAMPLES:")

print(len(generated_dataset))

# Count types
counts = {}

for sample in generated_dataset:

    t = sample["type"]

    counts[t] = counts.get(t, 0) + 1


print("\nSAMPLE TYPE COUNTS:\n")

for k, v in counts.items():

    print(f"{k}: {v}")

print("\nDATASET SAVED TO:")

print(OUTPUT_PATH)