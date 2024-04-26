# Week 10: Data assimiliation

## Tasks

- [ ] Select any one of the 12 stations from the Week 6 assignment course Moodle. This dataset will be your “model”. You can also create a model using regression, neural networks or any other method if you wish.

What is important in this first step, is that you create one independent time series which is considered to be the “model” in your assimilation.

- [ ] Assimilate the data from the remaining 11 noise monitoring stations, if you have used one station as the model from step 1). If you have made your own model, please assimilate all 12 stations and evaluate using the following criteria:

Calculate the Root Mean Squared Error (RMSE), using the station data as the reference value (y^i
) and the assimilated value as the estimator (yi
),  after assimilating using a gain, K of 0.1, 0.25, 0.5, and 0.75.

RMSE(y,y^)=∑N−1i=0(yi−y^i)2N−−−−−−−−−√

- [ ] Compare the RMSE values with those from the model to station RMSE without any assimilation. What effect did assimilation have on the RMSE?

- [ ] Calculate the standard deviations using a sliding window size of 11, 21 and 51. The window should have an equal number of entries "before and after" each value. 

For example, for the window size of 11, the standard deviation will be calculated based on the previous 5 values, the current value and the next 5 values. (Hint: the value of the mean, μ
 is based on the 11 values for that window, and is changing as the window slides across the data.)

σ=1n−1Σ(x−μ)2−−−−−−−−−−−√

- [ ] Which standard deviations were the lowest, which were the highest, and why do you think this is so?

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
