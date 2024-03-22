# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import random

def uniform_random_walk(n) -> list:
  """
  Simulates a uniform random walk of length n with equal probability of +1 or -1 steps.

  Args:
      n: Length of the random walk.

  Returns:
      A list representing the positions of the random walk.
  """
  steps = np.random.choice([-1, 1], size=n)
  print(steps)
  return steps


def gaussian_random_walk(n) -> list:
  """
  Simulates a gaussian random walk of length n with equal probability of +1 or -1 steps.

  Args:
      n: Length of the random walk.

  Returns:
      A list representing the positions of the random walk.
  """
  steps = np.random.normal(loc=0.0, scale=1.0, size=n)
  print(steps)
  return steps
#   steps = np.random.normal(size=n-1)
#   # Compute the walk by taking the cumulative sum of the steps
#   walk = np.cumsum(steps)
#   # Prepend 0 to the walk
#   walk = np.insert(walk, 0, 0)
#   print(walk)
#   return walk

def logistic_map(n, lmd):
    """
    Simulates a logistic map of length n.

    Args:
        n: Length of the logistic map.
        lmd: Lambda value.

    Returns:
        A list representing the positions of the logistic map.
    """
    results = []
    x = x0
    for _ in range(n):
        x = lmd * x * (1 - x)
        results.append(x)
    return results


def generate_rgb_list(length):
    return [(random.random(), random.random(), random.random()) for _ in range(length)]


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


walk_length = 100
num_walks = 10
lambdas = [0.5, 2.5, 3.5, 4]
x0 = 2 # Initial value of x

# for lmbda in lambdas: 
#     for i in num_walks:
#         results = logistic_map(walk_length, lmbda)


walks = go_walking(num_walks, walk_length)
gaussian_results = analyze_random_walks(walks['gaussian walks'])
uniform_results = analyze_random_walks(walks['uniform walks'])

colors = generate_rgb_list(num_walks)
for i, list in enumerate(walks['gaussian walks']):
    plt.plot(list, color=colors[i], label=f'Gaussian walk {i}')
plt.savefig("gaussian_walks.png")

for i, list in enumerate(walks['uniform walks']):
    plt.plot(list, color=colors[i], label=f'Uniform walk {i}')

plt.savefig("random_walks.png")

#print(gaussian_results['time average'])
#print(uniform_results['ensemble average'])

# Plot both ensemble averages
plt.hist(gaussian_results['ensemble average'], label='Gaussian')
plt.hist(uniform_results['ensemble average'], label='Uniform')

# Add a legend
plt.legend()
# Create figure and axes
fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

# Plot histograms
axs[0].hist(gaussian_results['ensemble average'], bins=10)
axs[1].hist(uniform_results['ensemble average'], bins=10)

# Set titles
axs[0].set_title('Gaussian')
axs[1].set_title('Uniform')


#plt.show()
plt.savefig("plot.png")