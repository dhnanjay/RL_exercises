from typing import Any, Dict, Tuple
import numpy as np


class BarryEnv:
    def __init__(self, n_planes: int, n_flights: int):
        self.n_planes = n_planes
        self.n_flights = n_flights
        self.reset()

    def reset(self) -> Tuple[Any, float, bool, Dict]:
        """
        Resets the env, use this to try again if you upset Barry!
        """

        self.n_flights_taken = 0
        self.total_points = 0
        self._means = np.arange(10, self.n_planes + 5)
        self._means = np.append(self._means, np.arange(5, 10) * 50)
        np.random.shuffle(self._means)
        return None, 0.0, False, {}

    def step(self, choice: int) -> Tuple[Any, float, bool, Dict]:
        """
        Call this with your choice of plane for Barry's next journey!
        """
        assert (
            not self.done
        ), "You can't step anymore, Barry has completed all his flights! reset the env to try again"
        assert isinstance(
            choice, int
        ), f"You need to pass an integer to step, the number of the plane that Barry should ride"
        assert (
            0 <= choice < self.n_planes
        ), f"Barry cannot ride plane number '{choice}'!. You must give a number between 0 and {BarryEnv.n_planes}"

        reward = self.get_number_of_barry_points(choice)
        self.total_points += reward

        self.n_flights_taken += 1

        if self.done:
            self.check_number_of_points()

        return None, reward, self.done, {}

    def get_number_of_barry_points(self, choice: int) -> int:
        """
        Args:
            choice (int): 0-n_planes, which plane to ride
        Returns:
            number of barry points earned by riding the chosen plane
        """
        return int(np.random.normal(loc=self._means[choice], scale=75, size=None))

    def check_number_of_points(self):
        print("Barry has completed all of his journeys!\n\n")
        if self.total_points / self.n_flights > 350:
            print(
                f"Congratulations, Barry averaged {self.total_points / self.n_flights} points per flight! He's thrilled!"
            )
        else:
            print(
                f"Oh no, you've upset Barry...\n\n"
                f"He wanted to average 350 points per flight\n\n"
                f"You only averaged {round(self.total_points / self.n_flights, 2)} points!"
            )

    @property
    def done(self):
        return self.n_flights_taken == self.n_flights
