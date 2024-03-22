import numpy as np
import matplotlib.pyplot as plt

# Set the random seed for reproducibility
np.random.seed(0)

# Length of the random walks
length = 100

# Generate steps for Gaussian random walk
gaussian_steps = np.random.normal(loc=0, scale=1, size=length)
gaussian_walk = np.cumsum(gaussian_steps)

# Generate steps for Uniform random walk
uniform_steps = np.random.uniform(low=-1, high=1, size=length)
uniform_walk = np.cumsum(uniform_steps)

g_walks = []
u_walks = []
for i in range(10):
    gaussian_steps = np.random.normal(loc=0, scale=1, size=length)
    gaussian_steps[0] = 0
    gaussian_walk = np.cumsum(gaussian_steps)

    uniform_steps = np.random.uniform(low=-1, high=1, size=length)
    uniform_steps[0] = 0
    uniform_walk = np.cumsum(uniform_steps)

    u_walks.append(uniform_walk)
    g_walks.append(gaussian_walk)

print(g_walks)
# Plot the random walks
plt.figure(figsize=(10,6))
#plt.plot(g_walks, label='Gaussian')
plt.plot(u_walks)
plt.legend(loc='best')
plt.title('Random Walks')
plt.savefig('crap.png')
