# Compressed sensing

## the tasks

- [*] Recreate the all SPL data sets over the period from 2022.02.20 00:00:00 to 2022.03.04 24:00:00, increasing the rank of the SVD (from rank 1,...,12).
Make sure to first resample the time, so that all stations are synchronized.

- [*] Calculate the RMSE as a function of rank against the resampled data for each station.

- [*] Calculate the ensemble average SPL (mean of all stations at each time step). Subtract the ensemble average from each individual station.

Rerun steps (1) and (2) of this assignment on the datasets after removing the ensemble average from each station.

- [ ] Plot the singular values and the RMSE (dual y-axes) versus the rank (x-axis) for all stations.

Do this for the SPL data before and after removing the ensemble average.

What does this relationship tell you about how much the data can be compressed using SVD?

- [ ] What is the physical interpretation of the U, Σ and V matrices from the SVD of the Tallinn SPL data?

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