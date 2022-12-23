import math
import random
from typing import Dict, Tuple, List

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import numpy as np


def check_value_function(
    student_value_function: Dict[str, float], expected_value_function: Dict[str, float]
) -> None:
    if len(student_value_function) != len(expected_value_function):
        # Check that the number of state-value pairs matches
        print(
            f"Incorrect number of state-value pairs, expected {len(expected_value_function)}, got {len(student_value_function)}"
        )
    elif any(
        exp_state not in student_value_function for exp_state in expected_value_function
    ):
        # Check that all the states expected in this value function are present
        print(
            f"Not all expected states in value function. Expected states: {list(expected_value_function)}, got: {list(student_value_function)}"
        )
    elif any(
        not isinstance(value, (float, int)) for value in student_value_function.values()
    ):
        # Check that dictionary values are numbers
        print(
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
        print(
            f"Not all values are correct! The values associated with these keys are incorrect: {incorrect_keys}."
        )
    else:
        print("Congratulations! That's the correct value function :)")


def check_ex_td_learning_1(your_value_function: Dict[str, float]):
    expected_values = {
        "New York": -19.5,
        "London": 0.0,
        "Amsterdam": -12.0,
        "Tel Aviv": -8.0,
        "Cairo": -6.0,
        "Bangkok": -1.5,
        "Hong Kong": 0.0,
    }
    for city, value in expected_values.items():
        print(
            f"For {city}, you predicted: {round(your_value_function.get(city, ''), 1)}, the correct value is {value}\n"
        )
    check_value_function(your_value_function, expected_values)


WALL_POSITIONS = [
    (9, 3),
    (8, 3),
    (7, 3),
    (6, 3),
    (5, 3),
    (4, 3),
    (3, 3),
    (2, 3),
    (7, 6),
    (6, 6),
    (5, 6),
    (4, 6),
    (3, 6),
    (2, 6),
    (1, 6),
    (0, 6),
]


def visualise_parking_value_fn(value_fn: np.ndarray):
    """Visualises the parking value function"""
    value_fn = value_fn.copy()
    nrows, ncols = value_fn.shape
    value_fn[0, 9] = 10
    values = np.linspace(np.min(value_fn), np.max(value_fn), num=9)
    for wall_pos in WALL_POSITIONS:
        value_fn[wall_pos] = None

    im = plt.imshow(
        value_fn,
        extent=(0, nrows, 0, ncols),
        interpolation="nearest",
        cmap=cm.cool,
    )
    # get the colors of the values, according to the
    # colormap used by imshow
    colors = [im.cmap(im.norm(value)) for value in reversed(values)]
    # create a patch (proxy artist) for every color
    patches = [
        mpatches.Patch(color=colors[i], label=f"{np.round(values[-(i + 1)], 1)}")
        for i in range(len(values))
    ]
    # put those patched as legend-handles into the legend
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.title("Value function of Barry's Parking Problem")
    plt.xlabel("x Position")
    plt.ylabel("y Position")
    plt.show()


def check_numpy_array_value_function(
    student_value_function: np.ndarray, expected_value_function: np.ndarray
) -> None:
    if student_value_function.shape != expected_value_function.shape:
        # Check that the shape of arrays match
        print(
            f"Incorrectly shaped array! Expected {expected_value_function.shape}, got {student_value_function.shape}"
        )
    elif np.allisclose(student_value_function, expected_value_function, rel_tol=1e-3):
        # Check values match
        print(
            f"Not all values are correct! Your value array:\n{student_value_function}\n"
            f"The correct value array:\n{expected_value_function}"
        )
    else:
        print(
            f"Congratulations! That's the correct value function :)\n\nYour value function: {student_value_function}"
        )


STATE = Tuple[int, int]


class ParkingEnv:
    """
    Parking Environment for Barry's Parking Predicament.
    """

    ALL_ACTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def __init__(self):
        """Initialise agent start, finish, grid object"""
        self._grid = np.zeros((10, 10))
        self._reward_grid = np.zeros((10, 10))
        self._reward_grid[0, 9] = 10
        self.reset()

    def get_possible_actions(self, state: STATE) -> List[Tuple[int, int]]:
        return [
            a for a in self.ALL_ACTIONS if is_state_valid(transition_function(state, a))
        ]

    def step(self, action: Tuple[int, int]) -> Tuple[STATE, float, bool, Dict]:
        assert action in self.get_possible_actions(self.state)
        self.state = transition_function(self.state, action)
        reward = self._reward_grid[self.state]
        self.total_return += reward
        self.done = self.state == (0, 9)
        return self.state, reward, self.done, {}

    def reset(self) -> Tuple[STATE, float, bool, Dict]:
        self.state = (9, 0)
        self.total_return = 0
        self.done = False
        return self.state, self.total_return, self.done, {}


def is_state_valid(state: STATE) -> bool:
    """Checks if a given state is on the grid."""
    return all(-1 < coord < 10 for coord in state) and state not in WALL_POSITIONS


def transition_function(state: STATE, action: Tuple[int, int]) -> STATE:
    return state[0] + action[0], state[1] + action[1]


def choose_greedy_action(
    possible_actions: List[Tuple[int, int]], value_fn: np.ndarray, current_state: STATE
) -> Tuple[int, int]:
    """
    Choose the greedy action, given the value function, possible actions and current state.

    Args:
         possible_actions: List of possible actions that can be taken from this state
         value_fn: numpy array representing the value function. Can get the value of
                    a state with `value_fn[state]`.
         current_state: tuple representing the current state

    Returns:
        The action to take which maximises the value of the successor state.
    """
    max_value = -np.Inf
    best_actions = []
    for poss_action in possible_actions:
        poss_new_state = transition_function(current_state, poss_action)
        if value_fn[poss_new_state] > max_value:
            best_actions = [poss_action]
            max_value = value_fn[poss_new_state]
        elif math.isclose(value_fn[poss_new_state], max_value, abs_tol=1e-6):
            best_actions.append(poss_action)
    return random.choice(best_actions)


def check_airport_parking(your_value_function: np.ndarray):
    game = ParkingEnv()
    num_steps_taken = 0

    path_taken = np.array([[" "] * 10] * 10)
    for w in WALL_POSITIONS:
        path_taken[w] = "P"
    path_taken[0, 9] = "F"
    path_taken[9, 0] = "S"

    states = []
    state, reward, done, _ = game.reset()
    didnt_reach_end_str = ""
    while not done:
        num_steps_taken += 1
        states.append(state)
        poss_actions = game.get_possible_actions(state)
        action = choose_greedy_action(poss_actions, your_value_function, state)
        state, reward, done, _ = game.step(action)
        symbol = "-" if action in [(0, 1), (0, -1)] else "|"
        path_taken[state] = symbol
        if num_steps_taken > 100:
            didnt_reach_end_str = "You didnt reach the end!"
            break

    if num_steps_taken > 32:
        err_message = "Suboptimal policy!"
        if num_steps_taken >= 100:
            err_message += "You didn't reach the parking spot in 100 steps"
        else:
            err_message += "Too many steps taken... number of steps taken: {num_steps_taken}. Min number: 32"
        err_message += "\n\n" f"Path taken:\n{path_taken}\n" f"States visited: {states}"
        print(err_message)
    elif num_steps_taken == 32:
        print(
            f"Congrats! You found the shortest path for Barry to take!\n\nPath taken:\n{path_taken}"
        )
    else:
        print(
            "This... shouldn't be possible - please seek help as I think you've broken the exercise!"
        )
