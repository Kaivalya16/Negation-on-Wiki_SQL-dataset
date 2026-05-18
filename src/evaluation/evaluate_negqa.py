import json

from tqdm import tqdm

from src.evaluation.metrics import (
    contains_match
)

from src.evaluation.table_context import (
    load_table,
    dataframe_to_text
)

from src.evaluation.ollama_evaluator import (
    ask_ollama
)


# -----------------------------------
# CONFIG
# -----------------------------------

DATASET_PATH = (
    "data/processed/"
    "advanced_negqa_dataset.json"
)

TOTAL_SAMPLES = 50


# -----------------------------------
# LOAD DATASET
# -----------------------------------

with open(DATASET_PATH,
          "r",
          encoding="utf-8") as f:

    dataset = json.load(f)


# -----------------------------------
# METRICS
# -----------------------------------

original_correct = 0

negated_correct = 0


# -----------------------------------
# EVALUATION LOOP
# -----------------------------------

for sample in tqdm(dataset[:TOTAL_SAMPLES]):

    table_id = sample["table_id"]

    # =================================
    # LOAD TABLE CONTEXT
    # =================================

    df = load_table(table_id)

    table_text = dataframe_to_text(df)

    # =================================
    # ORIGINAL QUESTION
    # =================================

    original_question = (
        sample["original_question"]
    )

    original_gt = [

        str(x[0])

        for x in sample["original_answers"]
    ]

    original_prediction = ask_ollama(
        original_question,
        table_text
    )

    print("\nORIGINAL QUESTION:")
    print(original_question)

    print("PREDICTION:")
    print(original_prediction)

    print("GROUND TRUTH:")
    print(original_gt)

    if original_prediction:

        original_correct += contains_match(
            original_prediction,
            original_gt
        )

    # =================================
    # NEGATED QUESTION
    # =================================

    negated_question = (
        sample["generated_question"]
    )

    negated_gt = [

        str(x[0])

        for x in sample["generated_answers"]
    ]

    negated_prediction = ask_ollama(
        negated_question,
        table_text
    )

    print("\nNEGATED QUESTION:")
    print(negated_question)

    print("PREDICTION:")
    print(negated_prediction)

    print("GROUND TRUTH:")
    print(negated_gt)

    if negated_prediction:

        negated_correct += contains_match(
            negated_prediction,
            negated_gt
        )

    print("\n" + "="*60)


# -----------------------------------
# FINAL RESULTS
# -----------------------------------

print("\nFINAL RESULTS\n")

print(
    f"Original Accuracy: "
    f"{original_correct/TOTAL_SAMPLES:.2f}"
)

print(
    f"Negated Accuracy: "
    f"{negated_correct/TOTAL_SAMPLES:.2f}"
)