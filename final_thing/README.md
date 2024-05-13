# Final task

## Task 1 - Plot station loacations

Using the location coordinates (latitude and longitude), plot the locations of the stations as a 2D scatter plot.

> mapser.py -> map.html

Color coded markers by regions (names for regions and sensors taken from file names).

## Task 2 - Fill in missing time-series data

Data should be evaluated in the period from **August 02** to **13th** 2022.
Interpolate missing data using 2 different methods (linear and nearest for example).

Repository.py interpolates and filters out need data.
Asking for data interpolated data using linear method

```python
Repo().get_interpolated_data('linear') 
```

## Task 3 - Data assimilation of time-series data

How often the SPL level exceeds 65 dBA at the region 4 only(eight stations in total)? The data should be reported as a percentage of the day, evening and night periods (e.g. the SPL exceeded 65 dBA 23.6% day, 14.9% evening and 2.4% night).

## Task 4 Embedded hardware SPL recording

serial_reader.py to read data from serial into csv file

## Task 5 Three SPL heatmaps

- Use your spatially interpolated time-averaged sound levels for each of the three time periods (day, evening and night).

- Compare the map results from your two different interpolation (created in Task 2) methods.

## how to create venv and install required components

Activate everytime, create and install depencies once.

```bash
# Create Virtual Environment
python3 -m venv venv

# Activate Virtual Environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
