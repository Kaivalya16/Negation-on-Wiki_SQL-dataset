def contains_match(prediction,
                   ground_truths):

    prediction = prediction.lower()

    for truth in ground_truths:

        truth = str(truth).lower()

        if truth in prediction:
            return 1

    return 0