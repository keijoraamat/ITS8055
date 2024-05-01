from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from repo.Repository import Repository as Repo


start = '2022-02-20 00:16:00'
end = '2022-03-06 20:20:00'
all_data = Repo().get_filtered_data(start, end)

model = all_data.pop(0)

print(f'Model: {model[0]}')
# for i in range(len(all_data)):
#     data = all_data[i][1]
#     sensor_name = all_data[i][0]
#     print(f'Sensor nr: {sensor_name}')

gains = [0.1, 0.25, 0.5, 0.75]

def assimilate_data(sensor_data, model, gains):
    assimilated_data = {gain: [] for gain in gains}

    for gain in gains:
        model_state = pd.Series(index=model[1].index)
        
        for sensor_name, sensor_df in sensor_data:
            for t in sensor_df.index:
                observation = sensor_df.loc[t, 'dt_sound_level_dB']
                if pd.isna(model_state.loc[t]):
                    model_state.loc[t] = observation
                assimilated_value = gain * observation + (1 - gain) * model_state.loc[t]
                model_state.loc[t] = assimilated_value
            assimilated_data[gain].append((sensor_name, pd.DataFrame({'Time': sensor_df.index, 'dt_sound_level_dB': model_state})))
    return assimilated_data

def calculate_rmse(y, y_hat):
    return np.sqrt(((y - y_hat)**2).mean())

def evaluate_rmse(sensor_data, assimilated_data, gains):
    rmse_values = {}
    for gain in gains:
        for sensor_name, sensor_df in sensor_data:
            assimilated_df = next(df for name, df in assimilated_data[gain] if name == sensor_name)
            # Reset the index of both DataFrames
            merged_df = sensor_df.merge(assimilated_df, left_index=True, right_index=True, suffixes=('_sensor', '_assimilated'))
            y_hat = gain * merged_df['dt_sound_level_dB_sensor'] + (1 - gain) * merged_df['dt_sound_level_dB_assimilated'] 

            rmse = calculate_rmse(merged_df['dt_sound_level_dB_assimilated'], y_hat)
            rmse_values[(sensor_name, gain)] = rmse
    return rmse_values

def calculate_rmse_without_assimilation(sensor_data, model):
    rmse_values = {}
    for sensor_name, sensor_df in sensor_data:
        model_predictions = model[1]['dt_sound_level_dB']
        rmse = calculate_rmse(sensor_df['dt_sound_level_dB'], model_predictions)
        rmse_values[sensor_name] = rmse
    return rmse_values

def plot_rmse(rmse_values_with_assimilation, rmse_values_without_assimilation):
    sensors = rmse_values_with_assimilation.keys()
    gains = [0.1, 0.25, 0.5, 0.75]

    for sensor in sensors:
        print(f"Sensor: {sensor}")
        plt.figure(figsize=(10, 6))

        # Plot RMSE with assimilation for each gain
        for gain in gains:
            print(f"Sensor: {sensor[0]}, gain: {gain}")
            rmse_with_assimilation = rmse_values_with_assimilation[(sensor[0], gain)]
            plt.bar(f'With Assimilation (K={gain})', rmse_with_assimilation)

        # Plot RMSE without assimilation
        print(rmse_values_without_assimilation.keys())
        rmse_without_assimilation = rmse_values_without_assimilation[sensor[0]]
        plt.bar('Without Assimilation', rmse_without_assimilation)

        plt.ylabel('RMSE')
        plt.title(f'RMSE for Sensor {sensor[0]}')
        plt.savefig(f'rmse_{sensor[0]}.png')

def plot_rmse_line(rmse_values_with_assimilation, rmse_values_without_assimilation):
    sensors = rmse_values_with_assimilation.keys()
    gains = [0.1, 0.25, 0.5, 0.75]

    plt.figure(figsize=(10, 6))

    # Plot RMSE with assimilation for each sensor and gain
    for sensor in sensors:
        rmse_with_assimilation = [rmse_values_with_assimilation[(sensor[0], gain)] for gain in gains]
        plt.plot(gains, rmse_with_assimilation, marker='o', label=f'Sensor {sensor[0]}')

    # Plot RMSE without assimilation
    rmse_without_assimilation = [rmse_values_without_assimilation[sensor[0]] for sensor in sensors]
    plt.plot(gains, rmse_without_assimilation, marker='o', label='Without Assimilation', linestyle='--')

    plt.xlabel('Gain')
    plt.ylabel('RMSE')
    plt.title('RMSE with and without Assimilation')
    plt.legend()
    plt.grid(True)
    plt.show()

#print(model[1].tail())
assimilated_data = assimilate_data(all_data, model, gains)
rmse_without_assimilation = calculate_rmse_without_assimilation(all_data, model)
rmse_values = evaluate_rmse(all_data, assimilated_data, gains)
# for sensor_name, gain in rmse_values.keys():
#     print(f"RMSE for sensor {sensor_name} with gain {gain}: {rmse_values[(sensor_name, gain)]}")

for sensor_name, gain in rmse_values.keys():
    rmse_with_assimilation = rmse_values[(sensor_name, gain)]
    rmse_no_assimilation = rmse_without_assimilation[sensor_name]
    print(f"RMSE for sensor: {sensor_name}, gain: {gain}, with assimilation: {rmse_with_assimilation:.2f}, without: {rmse_no_assimilation:.2f}")

#plot_rmse_line(rmse_values, rmse_without_assimilation)

def std_dev_rolling(data):
    window_sizes = [11, 21, 51]
    for sensor in data:
        sensor_df = sensor[1]
        print(f"df length: {len(sensor_df)}")
        for window in window_sizes:
            sensor_df[f'std_dev_{window}'] = sensor_df['dt_sound_level_dB'].rolling(window, center=True).std().fillna(0)

    return data
all_data.insert(0, model)
std_dev_rolling_data = std_dev_rolling(assimilated_data[0.1])

for sensor in std_dev_rolling_data:
    stds =["std_dev_11", "std_dev_21", "std_dev_51"]
    stds_sums = sensor[1][stds].sum()
    print(f"{sensor[0]} \n {stds_sums}")
    #print(sensor[1])

# Create a new figure for plotting
fig, axes = plt.subplots(len(std_dev_rolling_data), 1, figsize=(25, 35))  # Adjust figsize for better visualization

# Iterate through each sensor data and plot on separate subplots
for i, (name, df) in enumerate(std_dev_rolling_data):
    ax = axes[i]
    # Plot sound level and all std_dev columns
    ax.plot(df["Time"], df["dt_sound_level_dB"], label="Sound Level")
    for col in df.columns[1:]:  # Skip the first column (Time)
        ax.plot(df["Time"], df[col], label=col)
    ax.set_title(f"Sensor: {name}")
    ax.set_xlabel("Time")
    ax.legend()

# Adjust layout and display the plot
fig.suptitle("Sound Level Data with Standard Deviations from Different Sensors")
plt.tight_layout()
plt.savefig("std_dev_plot.png")
