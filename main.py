import random

from barry_points import BarryEnv

# Constants in the exercise
n_planes = 100  # number of planes
n_flights = 10000  # number of flights barry takes

env = BarryEnv(n_planes, n_flights)
_, reward, done, _ = env.reset()

observed_barry_points = [[] for _ in range(n_planes)]

# You'll need to use this to decide which plane to pick!
estimated_mean_barry_points = [0 for _ in range(n_planes)]

epsilon = 0.05


while not done:
    # TODO: The bit you write!!
    # ===========================================
    #  Currently choosing the plane randomly
    plane_to_ride = random.choice(range(n_planes))
    if random.random() < epsilon:
        # Random, with probability epsilon!
        chosen_plane_value = random.randint(0, n_planes - 1)
    else:
        # Greedy: pick the one with the best mean
        chosen_plane_value = max(estimated_mean_barry_points)
        # This gets the index of the plane with the best mean
        plane_to_ride = estimated_mean_barry_points.index(chosen_plane_value)
    
    # ===========================================

    # .step() rides the plane & gives the reward
    _, reward, done, _ = env.step(plane_to_ride)

    # This updates the estimates of the mean Barry points
    observed_barry_points[plane_to_ride].append(reward)
    plane_points = observed_barry_points[plane_to_ride]

    estimated_mean_barry_points[plane_to_ride] = sum(plane_points) / len(plane_points)
