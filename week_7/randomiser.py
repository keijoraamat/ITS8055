import pandas as pd
import numpy as np

class Randomiser:
    def __init__(self) -> None:
        self.sample_sizes = [0.01, 0.05, 0.1, 0.5, 0.9]

    def randomise(self, data: pd.DataFrame, name) -> list[(str, pd.DataFrame)]:
        resampled_dfs = []

        for i in range(len(self.sample_sizes)):
            n_samples = int(len(data) * self.sample_sizes[i])
            indices = np.random.choice(data.index, size=n_samples, replace=False)
            resampled_dfs[i] = (name, data.loc[indices])

        return resampled_dfs
    