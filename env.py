from typing import Tuple, List, Dict

import numpy as np

# State type
State = Tuple[int, int]

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


def is_state_valid(state: State) -> bool:
    """Checks if a given state is on the grid."""
    return 0 <= state[0] < 10 and 0 <= state[1] < 10 and state not in WALL_POSITIONS


def transition_function(state: State, action: Tuple[int, int]) -> State:
    return state[0] + action[0], state[1] + action[1]


class ParkingEnv:
    """
    Parking Environment for Barry's Parking Predicament.
    """

    ALL_ACTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def __init__(self):
        self._grid = np.zeros((10, 10))
        self.reset()

    def get_possible_actions(self, state: State) -> List[Tuple[int, int]]:
        return [
            a for a in self.ALL_ACTIONS if is_state_valid(transition_function(state, a))
        ]

    def step(self, action: Tuple[int, int]) -> Tuple[State, float, bool, Dict]:
        assert action in self.get_possible_actions(
            self.state
        ), f"Action {action} from state {self.state} is invalid! Valid actions: {self.get_possible_actions(self.state)}"

        self.state = transition_function(self.state, action)

        reward = 10 if self.state == (0, 9) else 0

        self.done = self.state == (0, 9)

        self.total_return += reward

        return self.state, reward, self.done, {}

    def reset(self) -> Tuple[State, float, bool, Dict]:
        self.state = (9, 0)
        self.total_return = 0
        self.done = False
        return self.state, self.total_return, self.done, {}
