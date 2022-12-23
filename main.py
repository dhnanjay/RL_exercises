from env import FlightPathEnv

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

# Written here to save you time
optimal_policy = {
    "New York": "Amsterdam",
    "London": "Cairo",
    "Amsterdam": "Tel Aviv",
    "Tel Aviv": "Cairo",
    "Cairo": "Bangkok",
    "Bangkok": "Hong Kong",
}
alpha = 0.15  # Update step size

# This is the format that the check function below expects. Dictionary mapping {state: value}
value_fn = {city: 0 for city in POSS_STATE_ACTION}


# TODO: Write code to learn the value function from experience for the optimal policy
env = FlightPathEnv()

# For 1000 episodes
for _ in range(1000):
    # Each iteration is one episode. So we need to call reset() every time
    state, reward, done, _ = env.reset()

    # This while loop runs the episode
    while not done:

        action = optimal_policy[state]

        # Before calling the transition function, keep the prev state for the TD update step
        prev_state = state

        # Transition the env object using the .step() function
        state, reward, done, _ = env.step(action)

        # TD update step
        value_fn[prev_state] += alpha * (
            reward + value_fn[state] - value_fn[prev_state]
        )
