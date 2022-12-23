import math
import random
from typing import Tuple, List

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import numpy as np

from env import WALL_POSITIONS, ParkingEnv, State, transition_function

gamma = 0.95


def visualise_parking_value_fn(value_fn: np.ndarray):
    """Visualises the parking value function"""
    value_fn = value_fn.copy()
    nrows, ncols = value_fn.shape
    values = np.linspace(np.min(value_fn), np.max(value_fn), num=9)
    for wall_pos in WALL_POSITIONS:
        value_fn[wall_pos] = None
    value_fn = np.flipud(value_fn)
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
    plt.title("Your value function")
    plt.xlabel("x Position")
    plt.ylabel("y Position")
    plt.gca().invert_yaxis()
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


def reward_function(successor_state: State) -> float:
    return 10 if successor_state == (0, 9) else 0


def choose_greedy_action(
    possible_actions: List[Tuple[int, int]], value_fn: np.ndarray, current_state: State
) -> Tuple[int, int]:
    """
    Choose the greedy action, given the value function,
     possible actions and current state.

    The 'greedy action' is the action that will lead to the
     highest value state according to your current value
     function.

    Args:
         possible_actions: List of possible actions that
                            can be taken from this state

         value_fn: numpy array representing the value function.
                    Can get the value of a state with
                    `value_fn[state]`.

         current_state: tuple representing the current state

    Returns:
        The action to take which maximises the value of the
         successor state.
    """
    max_value = -np.Inf
    best_actions = []
    for poss_action in possible_actions:
        poss_new_state = transition_function(current_state, poss_action)
        action_value = (
            reward_function(poss_new_state) + gamma * value_fn[poss_new_state]
        )
        if action_value > max_value:
            best_actions = [poss_action]
            max_value = action_value
        elif math.isclose(action_value, max_value, abs_tol=1e-6):
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
    while not done:
        num_steps_taken += 1
        states.append(state)
        poss_actions = game.get_possible_actions(state)
        action = choose_greedy_action(poss_actions, your_value_function, state)
        state, reward, done, _ = game.step(action)
        symbol = "-" if action in [(0, 1), (0, -1)] else "|"
        path_taken[state] = symbol
        if num_steps_taken > 100:
            break

    if num_steps_taken > 32:
        err_message = "Suboptimal policy!"
        if num_steps_taken >= 100:
            err_message += "You didn't reach the parking spot in 100 steps"
        else:
            err_message += "Too many steps taken... number of steps taken: {num_steps_taken}. Min number: 32"
        err_message += "\n\n" f"Path taken:\n{path_taken}\n" f"States visited:"
        print(err_message)
        for step in states:
            print(step)
    elif num_steps_taken == 32:
        print(
            f"Congrats! You found the shortest path for Barry to take!\n\nPath taken:\n{path_taken}"
        )
    else:
        print(
            "This... shouldn't be possible - please seek help as I think you've broken the exercise!"
        )
