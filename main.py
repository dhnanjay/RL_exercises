from ex2_checks import check_returns

# Don't delete these!
# They're to be used by your code to calculate the answer
rewards = [0, 0, 3, 0, 2, 5, 7, 0, 0, 10, 0, 4, 0, 0, 0, 1]
gamma = 0.9

# TODO: You write this bit!
def get_returns(rewards, gamma=gamma):
  n=0
  total_returns = 0
  for i in rewards:
    total_returns = total_returns + i*gamma**n
    n=n+1
  return round(total_returns,2)

def get_return_list(rewards=rewards, gamma=gamma):
  total_reward_list=[]
  n=0
  for i in rewards:
    total_reward_list.append(get_returns(rewards[n:], gamma))
    n=n+1
  return total_reward_list
 
returns = get_return_list()

check_returns(returns)