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
            merged_df = pd.merge(sensor_df, assimilated_data, on='Time', suffixes=('_sensor', '_assimilated'))
            y_hat = gain * merged_df['dt_sound_level_dB_sensor'] + (1 - gain) * merged_df['dt_sound_level_dB_assimilated'] 

            rmse = calculate_rmse(merged_df['dt_sound_level_dB_assimilated'], y_hat)
            rmse_values[(sensor_name, gain)] = rmse
    return rmse_values
print(model[1].tail())
assimilated_data = assimilate_data(all_data, model, gains)
rmse_values = evaluate_rmse(all_data, assimilated_data, gains) 
print(rmse_values)