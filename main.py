# The time discount factor used
gamma = 0.99

# Get the reward given the current state and action taken
reward_function = {
    ("Faulty", "Repair"): -50,
    ("Faulty", "Fly"): 10,
    ("Out of Operation", "Repair"): -100,
    ("In Operation", "Fly"): 100,
}
# E.g.
# reward = reward_function[(state, action)]

# Get the next state based on action and current state
transition_function = {
    ("Faulty", "Repair"): "In Operation",
    ("Faulty", "Fly"): "Out of Operation",
    ("Out of Operation", "Repair"): "In Operation",
    ("In Operation", "Fly"): "Faulty",
}
# To transition from `state` where you take `action`,
# new_state = transition_function[(state, action)]

# The two possible policies
policy_better = {
    "In Operation": "Fly",
    "Faulty": "Repair",
    "Out of Operation": "Repair",
}
policy_worse = {
    "In Operation": "Fly",
    "Faulty": "Fly",
    "Out of Operation": "Repair",
}
# E.g.
# action = policy[state]

# TODO: Write code to calculate the value functions of these states given the 2 different deterministic policies
value_function_better = { # Don't change variable names
    "In Operation": 0,
    "Faulty": 0,
    "Out of Operation": 0,
}
value_function_worse = { # Don't change variable names
    "In Operation": 0,
    "Faulty": 0,
    "Out of Operation": 0,
}


def better_value_function():
    value_function = value_function_better
    policy = policy_better

    for state in ["In Operation","Faulty","Out of Operation"]:
        currState = state
        for i in range(0, 100):
          action = policy[currState]
          reward = reward_function[(currState, action)]

          value_function[currState] += ((gamma**i) * reward)
          currState = transition_function[(currState, action)]
          # print(currState, value_function)
    return value_function

def worse_value_function():
    value_function = value_function_worse
    policy = policy_worse

    for state in ["In Operation","Faulty","Out of Operation"]:
        currState = state
        for i in range(0, 100):
          action = policy[currState]
          reward = reward_function[(currState, action)]

          value_function[currState] += ((gamma**i) * reward)
          currState = transition_function[(currState, action)]
          # print(currState, value_function)
    return value_function
  
print("Following better policy:",better_value_function())
print("Following worse policy:",worse_value_function())
