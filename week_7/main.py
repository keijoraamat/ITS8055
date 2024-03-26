from repo.Repository import Repository as Repo
from randomiser import Randomiser
from statistiker import Statistiker
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from sklearn.metrics import r2_score

all_data = Repo().get_all_data()

COLUMN_NAME = 'dt_sound_level_dB'
lags = [1, 10, 60, 720]
colors = ['b', 'r', 'g', 'c']
alphas = [1, 0.7, 0.4, 0.08]
sample_sizes = [0.01, 0.05, 0.1, 0.5, 0.9]

def plot_4_in_1(all_data, i, name='lag_plots'):
    data = all_data[i][1][COLUMN_NAME]
    sensor_name = all_data[i][0]
    _, axs = plt.subplots(2, 2, figsize=(15, 15))

    for ax, lag in zip(axs.flat, lags):
        y_true = data.iloc[lag:]
        y_pred = data.iloc[:-lag]
        r2 = r2_score(y_true, y_pred)
        lag_plot(data, lag=lag, ax=ax)
        ax.set_title(f'Lag plot for {COLUMN_NAME} with lag={lag} R^2={r2:.2f}')

    plt.tight_layout()
    plt.savefig(f'{sensor_name}_{name}.png')


def plot_overlayed(all_data, i, name='lag_overlayed'):
    sensor_number = all_data[i][0]
    data = all_data[i][1][COLUMN_NAME]
    _, ax = plt.subplots(figsize=(13, 13))
    for lag, color, alpha in zip(lags, colors, alphas):
        y_true = data.iloc[lag:]
        y_pred = data.iloc[:-lag]
        r2 = r2_score(y_true, y_pred)
        lag_plot(data, lag=lag, ax=ax, c=color, alpha=alpha, label=f'lag={lag}, R^2={r2:.2f}')

    plt.legend()
    plt.title(f'Sensor nr: {sensor_number}')

    plt.tight_layout()
    plt.savefig(f'{sensor_number}_{name}.png')


def plot_all_overlayed():
    for i in range(len(all_data)):
        plot_overlayed(all_data, i)


def plot_all_4_in_1():
    for i in range(len(all_data)):
        plot_4_in_1(all_data, i)


def plot_stat_params(data) -> None:

    devs = ""
    _, axs = plt.subplots(3, 1, figsize=(7, 20))
    for i, (device, parameters) in enumerate(data.items()):
        axs[0].plot(sample_sizes, parameters['mean'], label=device)
        axs[1].plot(sample_sizes, parameters['median'], label=device)
        axs[2].plot(sample_sizes, parameters['standard deviation'], label=device)
        devs += f"_{device} "

    # Set titles for subplots
    axs[0].set_title('Mean')
    axs[1].set_title('Median')
    axs[2].set_title('Standard Deviation')

    for ax in axs:
        # Set x-label for subplots
        ax.set_xlabel('Sample Size %')
        # Add legends
        ax.legend()
        ax.grid()
        

    plt.tight_layout()
    plt.savefig(f'stat_params_of{devs}.png')
 

# To see which sensor is which
# for i in range(len(all_data)):
#     print(f"Sensor nr {all_data[i][0]} is n:{i}")

concrete_3 = [all_data[9], all_data[3], all_data[10]]

#randed_data - dict{sensor_nr: [randomly sampled DataFrames]}}
randed_data = {}
for data in concrete_3:
    r = Randomiser().randomise(data[1])
    randed_data[data[0]] = r

stats_for_randed_data = {}

for key, value in randed_data.items():
    stats_for_randed_data[key] = Statistiker().get_stat_params(value)

plot_stat_params(stats_for_randed_data)

plot_all_overlayed_plots = False
plot_all_4_in_1s_plots = False
if __name__ == '__main__':
    if plot_all_overlayed_plots:
        plot_all_overlayed()

    if plot_all_4_in_1s_plots:
        plot_all_4_in_1()