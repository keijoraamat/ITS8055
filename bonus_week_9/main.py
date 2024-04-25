import repo.Repository as Repo
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from scipy.linalg import svd
from sklearn.metrics import mean_squared_error

start = '2022-02-20 00:00:00'
end = '2022-03-05 00:00:00' #pandas cant have 2022-03-04 24:00:00
repo = Repo.Repository()
repo.set_period(start, end)
data = repo.get_filtered_data()
raw_data = repo.get_all_data()

def rank_and_RMSE(data) -> list[tuple[str, list[float], np.ndarray]]:
    sensors_rmse = []
    # Apply SVD and recreate data sets
    for i in range(len(data)):
        U, s, Vt = svd(data[i][1]) # decompose the data matrix into 3 matrices
        m = data[i][1].shape[1]  # Get the number of columns in the original data
        sigma = np.zeros((data[i][1].shape[0], m)) # Create a matrix of zeros with the same shape as the original data
        sigma[:m, :m] = np.diag(s) # Fill the diagonal of the sigma matrix with the singular values

        rmse_values = []
        if len(s) > 1:
            for j in range(1, min(np.min(data[i][1].shape), 13)):
                rank_i_approx = U[:,:j] @ np.diag(s[:j]) @ Vt[:j,:j]
    
                # Calculate RMSE
                mse = mean_squared_error(data[i][1], rank_i_approx)
                rmse = sqrt(mse)
                rmse_values.append(rmse)
        else:
            # Handle the special case where the data is essentially rank-1
            rank_i_approx = U @ np.diag(s) @ Vt
    
            # Calculate RMSE
            mse = mean_squared_error(data[i][1], rank_i_approx)
            rmse = sqrt(mse)
            rmse_values.append(rmse)

        #print(f"rmses: {rmse_values}")
        #print(f"sigma: {sigma}")
        sensors_rmse.append((data[i][0], rmse_values, sigma))
    return sensors_rmse

def plot_vs_datas(rmse_values, singular_values, sensor_name, type=''):
    print(f"plotting")
    print(f"rmse_values: {rmse_values}")
    print(f"singular_values: {singular_values}")
    ranks = range(1, len(singular_values) + 1)

    fig, ax1 = plt.subplots()
    fig.suptitle(f'{sensor_name} {type}')
    color = 'tab:red'
    ax1.set_xlabel('Rank')
    ax1.set_ylabel('Singluar Values', color=color)
    ax1.plot(ranks, singular_values, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('RMSE', color=color)
    ax2.plot(ranks, rmse_values, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    if type == '':
        plt.savefig(f'{sensor_name}_RMSE_vs_Singular_Values.png')
    plt.savefig(f'{sensor_name}_ens_removed_RMSE_vs_Singular_Values.png')


raw_data = rank_and_RMSE(data)

# Calculate the ensemble average SPL (mean of all stations at each time step).
# Subtract the ensemble average from each individual station.
norm_dfs = []
for i in range(len(data)):
    ensemble_avg_spl = data[i][1].mean(axis=1)
    df_normalized = data[i][1].sub(ensemble_avg_spl, axis=0)
    norm_dfs.append((data[i][0], df_normalized))

#Rerun steps (increasing the rank) and (RMSE) of this assignment on the datasets 
# after removing the ensemble average from each station.
removed_ensemble_avg = rank_and_RMSE(norm_dfs)

# Plot the singular values and the RMSE (dual y-axes)
# versus the rank (x-axis) for all stations.
for i in range(len(data)):
    print(f"starting ploting")
    plot_vs_datas(
        removed_ensemble_avg[i][1], 
        removed_ensemble_avg[i][2], 
        removed_ensemble_avg[i][0], 
        'after removing ensemble avg')
    
    # plot_vs_datas(
    #     raw_data[i][1], 
    #     raw_data[i][2], 
    #     raw_data[i][0])