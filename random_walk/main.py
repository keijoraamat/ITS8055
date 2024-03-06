# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


def uniform_random_walk(n) -> list:
  """
  Simulates a uniform random walk of length n with equal probability of +1 or -1 steps.

  Args:
      n: Length of the random walk.

  Returns:
      A list representing the positions of the random walk.
  """
  steps = np.random.choice([-1, 1], size=n)
  return np.cumsum(steps)


def gaussian_random_walk(n) -> list:
  """
  Simulates a gaussian random walk of length n with equal probability of +1 or -1 steps.

  Args:
      n: Length of the random walk.

  Returns:
      A list representing the positions of the random walk.
  """
  steps = np.random.normal(loc=0.0, scale=1.0, size=n)
  return np.cumsum(steps)



def go_walking(num_walks, walk_length) -> dict:
    """
    Generates gaussianly and uniformly distributed random walks. 
    Args:
        walk_length : int
            length of each walk.
        num_walks : int
            how many walks are walked

    Returns:
        A dictionary containig uniform and gaussian distribution random walks.

    """
    uniform_walks = np.zeros((num_walks, walk_length))
    gaussian_walks = np.zeros((num_walks, walk_length))
    for i in range(num_walks):
        uniform_walks[i] = uniform_random_walk(walk_length)
        gaussian_walks[i] = gaussian_random_walk(walk_length)
        
    return {
        "uniform walks" : uniform_walks,
        "gaussian walks" : gaussian_walks
        }


def analyze_random_walks(random_walk) -> dict:
    """
    Runs random_walk n times, calculates time-average, ensamble average,
    variance, and standard deviation.

    Args:
       random_walk: list of ints
           a list of random walks

    Returns:
        A dictionary containing time-average, ensamble average,
        variance, and standard deviation.
    """


    # Calculate time-average for each walk
    time_avg = [np.mean(walk) for walk in random_walk]

    ensamble_avg = (np.mean(random_walk, axis=0)).tolist()

    variances = [np.var(walk) for walk in random_walk]

    # Calculate standard deviation for each walk
    std_devs = [np.std(walk) for walk in random_walk]

    return {
         "time average": time_avg,
         "ensemble average": ensamble_avg,
         "variances" : variances, 
         "std_devs" : std_devs
     }


walk_length = 1000
num_walks = 10

walks = go_walking(num_walks, walk_length)
gaussian_results = analyze_random_walks(walks['gaussian walks'])
uniform_results = analyze_random_walks(walks['uniform walks'])


print(gaussian_results['time average'])
print(uniform_results['time average'])

plt.plot(gaussian_results['ensemble average'])
plt.show()
