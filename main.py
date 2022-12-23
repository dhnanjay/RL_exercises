import math
import numpy as np
from typing import Tuple, List
import random

from tqdm import tqdm

from ex3_checks import visualise_parking_value_fn, check_airport_parking
from env import State, ParkingEnv, WALL_POSITIONS

### Here we define some useful functions and classes.

# TODO: You should write your code at the end after the next TODO!


def is_state_valid(state: State) -> bool:
    """Checks if a given state is on the grid."""
    return (
        state[0] in range(10) and state[1] in range(10) and state not in WALL_POSITIONS
    )


def transition_function(state: State, action: Tuple[int, int]) -> State:
    return state[0] + action[0], state[1] + action[1]


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
        if value_fn[poss_new_state] > max_value:
            best_actions = [poss_action]
            max_value = value_fn[poss_new_state]
        elif math.isclose(value_fn[poss_new_state], max_value, abs_tol=1e-4):
            best_actions.append(poss_action)
    return random.choice(best_actions)


# How the value function should be represented (as a numpy array) and setting gamma up
value_fn = np.zeros((10, 10))
gamma = 0.95

# Set other hyperparameters. Epsilon here quite high to make the plot prettier ;)
epsilon = 0.5
alpha = 0.3

# TODO: use epsilon greedy & TD-learning to train an RL agent that solves find the optimal value function
#  Tip: use choose_greedy_action()

env = ParkingEnv()

# iterate through 1000 episodes
for _ in tqdm(range(1000)):
    # Reset at the start of each episode
    state, reward, done, info = env.reset()

    while not done:
        # Keep prev_state for use in TD update rule
        prev_state = state

        # Epsilon-greedy policy
        if random.random() < epsilon:
            action = random.choice(env.get_possible_actions(state))
        else:
            action = choose_greedy_action(
                env.get_possible_actions(state), value_fn, state
            )

        # Update the environment given our action
        state, reward, done, info = env.step(action)

        # TD update rule
        value_fn[prev_state] = (1 - alpha) * value_fn[prev_state] + alpha * (
            reward + gamma * value_fn[state]
        )

# Below checks and visualises the value function
if __name__ == "__main__":
    check_airport_parking(value_fn)
    visualise_parking_value_fn(value_fn)
