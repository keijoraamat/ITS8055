import matplotlib.pyplot as plt
import numpy as np

def logistic_map(x0, lmbda, iterations):
    results = []
    x = x0
    for _ in range(iterations):
        x = lmbda * x * (1 - x)
        results.append(x)
    return results

lambdas = [0.5, 2.5, 3.5, 4]
x0 = 0.1  # Initial value of x
iterations = 50  # Number of iterations

for lmbda in lambdas:
    results = logistic_map(x0, lmbda, iterations)
    colorr = 'b'
    if lmbda == 2.5:
        colorr = 'g'
    elif lmbda == 3.5:
        colorr = 'y'
    elif lmbda == 4:
        colorr = 'c'
    plt.hist(results, bins=int(2*lmbda), density=True, alpha=0.7, color=colorr)
    print(f"For 𝜆 = {lmbda}:")
    print(results)

# Calculate logistic map
results = logistic_map(x0, lmbda, iterations)

# Plot histogram

plt.title('Logistic Map Histogram (λ=3.5)')
plt.legend()
plt.xlabel('Values')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# def logistic_map(x, lam):
#     return lam * x * (1 - x)

# def plot_logistic_map(lam_values, x_init, num_iterations):
#     x = np.zeros(num_iterations)
#     for lam in lam_values:
#         x[0] = x_init
#         for i in range(num_iterations-1):
#             x[i+1] = logistic_map(x[i], lam)
#         plt.plot(x, label=f'λ={lam}')
#     plt.legend()
#     plt.show()

# lam_values = [0.5, 2.5, 3.5, 4]
# x_init = 0.5
# num_iterations = 100

# plot_logistic_map(lam_values, x_init, num_iterations)



