"""The starting point of the program"""
from Repository import Repository


PERIOD_START = '2022-08-02 00:00:00'
PERIOD_STOP = '2022-08-13 23:59:59'
DAY_START = '07:00:00'
DAY_STOP = '18:59:59'
EVENING_START = '19:00:00'
EVENING_STOP = '22:59:59'
NIGHT_START = '23:00:0'
NIGHT_STOP = '06:59:59'
REGION = 'region_4_ülemiste'

Repo = Repository
Repo().set_period(start=PERIOD_START, end=PERIOD_STOP)

data = Repo().get_interpolated_data('linear')

for tple in data[REGION]:
    df = tple[1]
    sensor = tple[0]
    day_data = (sensor, df.between_time(start_time=DAY_START, end_time=DAY_STOP))
    evening_data = (sensor, df.between_time(EVENING_START, EVENING_STOP))
    night_data = (sensor, df.between_time(NIGHT_START, NIGHT_STOP))

# print(f"Day data: {day_data}")
print(f"Evening data: {evening_data}")
# print(f"Night data: {night_data}")
