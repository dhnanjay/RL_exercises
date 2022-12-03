from typing import List
import math


def check_returns(returns: List[float]):
    expected_returns = [15.75, 17.5, 19.44, 18.27, 20.3, 20.34, 17.04, 11.15, 12.39, 13.77, 4.19, 4.66, 0.73, 0.81, 0.9, 1.0]
    assert len(returns) == len(expected_returns), \
        f"Incorrect number of returns provided! Expected {len(expected_returns)}, got {len(returns)}"
    assert all(math.isclose(exp_ret, ret, abs_tol=0.01) for exp_ret, ret in zip(expected_returns, returns)), \
        f"Expected following returns: {expected_returns}\n\nReceived: {returns}"
    print("Those are the correct returns for Barry's test run!\n\nHe's happy now, this event will be a roaring success. :)")
