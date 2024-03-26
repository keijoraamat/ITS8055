import pandas as pd
import numpy as np

class Randomiser:
    def __init__(self) -> None:
        self.sample_sizes = [0.01, 0.05, 0.1, 0.5, 0.9]

    def randomise(self, data: pd.DataFrame) -> list[pd.DataFrame]:
        resampled_df = []

        for size in self.sample_sizes:
            resampled_df.append([data.sample(frac=size)])

        return  resampled_df
    