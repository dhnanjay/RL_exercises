from typing import Dict, Tuple, Any


class Env:
    def __init__(self):
        """
        Initialises the object.

        Is called when you call `environment = Env()`.

        It sets everything up in the starting state for the episode to run.
        """
        self.reset()

    def step(self, action: Any) -> Tuple[Any, float, bool, Dict]:
        """
        Given an action to take:
            1. sample the next state and update the state
            2. get the reward from this timestep
            3. determine whether the episode has terminated

        Args:
            action: The action to take. Determined by user code
                that runs the policy

        Returns:
            Tuple of:
                1. state (Any): The updated state after taking the action
                2. reward (float): Reward at this timestep
                3. done (boolean): Whether the episode is over
                4. info (dict): Dictionary of extra information
        """
        raise NotImplementedError()

    def reset(self) -> Tuple[Any, float, bool, Dict]:
        """
        Resets the environment (resetting state, total return & whether
            the episode has terminated) so it can be re-used for another
            episode.

        Returns:
            Same type output as .step(). Tuple of:
                1. state (Any): The state after resetting the environment
                2. reward (None): None at this point, since no reward is
                                                                                                                                                given initially
                3. done (boolean): Always `True`, since the episode has just
                                                                                                                                                been reset
                4. info (dict): Dictionary of any extra information
        """
        raise NotImplementedError()


class FlightPathEnv(Env):
    """
    You need to use this FlightPathEnv class to learn the
        optimal value function.

    Check the example code in the tutorial if this confuses
        you.
    """

    # This defines the possible cities to fly to from each city
    POSS_STATE_ACTION = {
        "New York": ["London", "Amsterdam"],
        "London": ["Cairo", "Tel Aviv"],
        "Amsterdam": ["Tel Aviv", "Cairo"],
        "Tel Aviv": ["Bangkok", "Cairo", "Hong Kong"],
        "Cairo": ["Bangkok"],
        "Bangkok": ["Hong Kong"],
        "Hong Kong": [],
    }

    # The values define the time to fly from the 1st city in the
    #  tuple to the 2nd. E.g. New York -> Amsterdam takes 7.5 hours
    REWARDS = {
        ("New York", "Amsterdam"): -7.5,
        ("New York", "London"): -6,
        ("London", "Cairo"): -8,
        ("London", "Tel Aviv"): -8,
        ("Amsterdam", "Cairo"): -10,
        ("Amsterdam", "Tel Aviv"): -4,
        ("Tel Aviv", "Cairo"): -2,
        ("Tel Aviv", "Bangkok"): -8,
        ("Tel Aviv", "Hong Kong"): -13,
        ("Cairo", "Bangkok"): -4.5,
        ("Bangkok", "Hong Kong"): -1.5,
    }

    def __init__(self):
        """Initialise the environment"""
        self.reset()

    def reset(self) -> Tuple[str, float, bool, Dict]:
        """
        Reset the environment, allowing you to use the same FlightPathMDP object
            for multiple runs of training.
        """
        self.state = "New York"
        self.total_return = 0
        self.done = False
        return self.state, self.total_return, self.done, {}

    def check_new_state_is_valid(self, new_state: str) -> None:
        """
        Check that a state transition is valid based on
            which cities can be flown to from where.
        """
        assert (
            new_state in self.POSS_STATE_ACTION
        ), f"{new_state} is not a valid state to fly to"
        assert (
            new_state in self.POSS_STATE_ACTION[self.state]
        ), f"You can't fly from {self.state} to {new_state}. Options: {self.POSS_STATE_ACTION[self.state]}"

    def step(self, action: str) -> Tuple[str, float, bool, Dict]:
        """
        Given an action to take, update the environment and give the reward.
        """
        # In this case the actions and new states are the same.
        # THIS IS NOT ALWAYS THE CASE.
        new_state = action

        self.check_new_state_is_valid(new_state)

        # Get the reward at this timestep (the time taken to make this flight)
        reward = self.REWARDS[(self.state, new_state)]

        # Add the reward from flight to the total
        self.total_return += reward

        # Update the state to the new state
        self.state = new_state

        # The game is over if you've reached Hong Kong
        self.done = self.state == "Hong Kong"

        return self.state, reward, self.done, {}
