def is_valid_result(response,
                    min_answers=1,
                    max_answers=10):

    # Execution failed
    if not response["success"]:
        return False

    results = response["results"]

    count = len(results)

    # Check range
    return min_answers <= count <= max_answers