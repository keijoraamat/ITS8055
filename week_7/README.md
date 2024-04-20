# Sparsity

- [x] Import data from csv files
- [x] Convert the time series to equally-spaced data wit one minute intervalls
- [x] Impute missing data for each time series using the "nearest" interpolant
- [x] For each station, create lag plots with lags of 1, 10, 60 and 720 minutes. Overlay the four lags on each plot, and calculate the coefficient of determination, R^2.
- [x] Compare the R^2 values for each of the lag plots and comment on when they switch from deterministic to non-deterministic.
- [x] Randomly resample the data from three stations using a uniform distribution with sample sizes of 1%, 5%, 10%, 50% and 90%. 
- [x] Choose two stations next to each other, and one further away to see if their location has an influence.
- [x] Plot the three statistical parameters mean, median and standard deviation as a function of the sample percentage for each site.
- [ ] Next, plot the same three statistical parameters, but as ensembles (e.g. the mean of two stations and then all three stations for each time step).
    * [ ] Calculate the statistical params from combined data from two stations.
    * [ ] Plot the params.
    * [ ] Repeat for all stations. Thistime combine the data from all three stations at each time step.

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
