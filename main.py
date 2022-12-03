from ex1_checks import check_barry_flight_paths

# States are where the senior execs are
states = ["New York", "London", "Amsterdam", "Tel Aviv", "Cairo", "Bangkok"]

# Actions are where to fly to
actions = ["London", "Amsterdam", "Tel Aviv", "Cairo", "Bangkok", "Hong Kong"]

# TODO: The bit you write - fill in the policy as a dictionary of {state: action} for all states
flight_path_policy = {
  "New York":"Amsterdam",
  "London":"Cairo", 
  "Amsterdam":"Tel Aviv",
  "Tel Aviv":"Cairo", 
  "Cairo":"Bangkok",
  "Bangkok":"Hong Kong"
}


# Leave this line! It checks your answer :)
check_barry_flight_paths(flight_path_policy)
