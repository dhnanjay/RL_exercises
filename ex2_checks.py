import math
from typing import Dict


def check_value_function(
    student_value_function: Dict[str, float], expected_value_function: Dict[str, float]
) -> None:
    if len(student_value_function) != len(expected_value_function):
        # Check that the number of state-value pairs matches
        raise Exception(
            f"Incorrect number of state-value pairs, expected {len(expected_value_function)}, got {len(student_value_function)}"
        )
    elif any(
        exp_state not in student_value_function for exp_state in expected_value_function
    ):
        # Check that all the states expected in this value function are present
        raise Exception(
            f"Not all expected states in value function. Expected states: {list(expected_value_function)}, got: {list(student_value_function)}"
        )
    elif any(
        not isinstance(value, (float, int)) for value in student_value_function.values()
    ):
        # Check that dictionary values are numbers
        raise Exception(
            f"Not all values in value function dictionary given are numbers. Value function dict given: {student_value_function}"
        )
    elif any(
        not math.isclose(value, expected_value_function[key], rel_tol=1e-3)
        for key, value in student_value_function.items()
    ):
        # Check values match
        incorrect_keys = [
            (key, value, expected_value_function[key])
            for key, value in student_value_function.items()
            if not math.isclose(value, expected_value_function[key], rel_tol=1e-4)
        ]
        raise Exception(
            f"Not all values are correct! The values associated with these keys are incorrect: {incorrect_keys}."
        )
    else:
        print("Congratulations! That's the correct value function :)")


def check_ex_7_2(
    your_value_function_better: Dict[str, float],
    your_value_function_worse: Dict[str, float],
):
    student_value_fns = [your_value_function_better, your_value_function_worse]
    # Swap the order if they've been input wrong!
    if next(iter(your_value_function_better.values())) < next(
        iter(your_value_function_worse.values())
    ):
        student_value_fns.reverse()

    expected_values_better = {
        "Faulty": 2462.311,
        "In Operation": 2537.688,
        "Out of Operation": 2412.311,
    }
    expected_values_worse = {
        "Faulty": 303.3567,
        "In Operation": 400.3232,
        "Out of Operation": 296.3199,
    }

    check_value_function(student_value_fns[0], expected_values_better)
    check_value_function(student_value_fns[1], expected_values_worse)
