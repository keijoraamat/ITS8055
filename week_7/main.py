from repo.Repository import Repository as Repo
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from sklearn.metrics import r2_score

all_data = Repo().get_all_data()

print(all_data[0])
print(type(all_data[0]))

COLUMN_NAME = 'dt_sound_level_dB'
lags = [1, 10, 60, 720]
colors = ['b', 'g', 'r', 'c']

def plot_4_in_1(all_data, lags):
    data = all_data[1][1][COLUMN_NAME]
    sensor_name = all_data[1][0]
    _, axs = plt.subplots(2, 2, figsize=(15, 15))

    for ax, lag in zip(axs.flat, lags):
        y_true = data.iloc[lag:]
        y_pred = data.iloc[:-lag]
        r2 = r2_score(y_true, y_pred)
        lag_plot(data, lag=lag, ax=ax)
        ax.set_title(f'Lag plot for {COLUMN_NAME} with lag={lag} R2={r2:.2f}')

    plt.tight_layout()
    plt.savefig(f'{sensor_name}_lag_plots.png')


def plot_overlayed(all_data, lags):
    sensor_number = all_data[2][0]
    data = all_data[2][1][COLUMN_NAME]
    _, ax = plt.subplots(figsize=(13, 13))
    for lag, color in zip(lags, colors):
        y_true = data.iloc[lag:]
        y_pred = data.iloc[:-lag]
        r2 = r2_score(y_true, y_pred)
        lag_plot(data, lag=lag, ax=ax, c=color, label=f'lag={lag}, R2={r2:.2f}')

    plt.legend()
    plt.title(f'Sensor nr: {sensor_number}')

    plt.tight_layout()
    plt.savefig(f'{sensor_number}_lag_overlayed.png')

plot_4_in_1(all_data, lags)
plot_overlayed(all_data, lags)
