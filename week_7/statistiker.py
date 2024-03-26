import pandas as pd

class Statistiker:
    '''
    A class that calculates the mean, median, and mode of a list of numbers.

    '''
    def __init__(self) -> None:
        self.COLUMN_NAME = 'dt_sound_level_dB'
        pass

    def __get_mean(self, data: list[pd.DataFrame]) -> list[pd.DataFrame]:
        result = []
        for d in data:
           result.append(d.mean()[self.COLUMN_NAME])
        return result
    

    def __get_median(self, data: list[pd.DataFrame]) -> list[pd.DataFrame]:
        result = []
        for d in data:
            result.append(d.median()[self.COLUMN_NAME])
        return result
    
    def __get_st_deviation(self, data: list[pd.DataFrame]) -> list[pd.DataFrame]:
        result = []
        for d in data:
            result.append(d.std()[self.COLUMN_NAME])
        return result
    
    def get_stat_params(self, data: list[pd.DataFrame]) -> None:
        '''
        Returns the mean, median, and standard deviation of a list of numbers.
        ---
        Input:
        data: list[pd.DataFrame] -> A list of pandas dataframes.
        ---
        Output:
        {
            'mean': [10.2, 10.3, 10.2, 10.6, 11.0], 
            'median': [10.2, 10.3, 10.2, 10.6, 11.0], 
            'std_dev': [3.2, 2.3, 3.2, 1.6, 1.0]
        }
        '''
        mean = []
        median = []
        st_deviation = []

        for d in data:
            mean.append(self.__get_mean(d))
            median.append(self.__get_median(d))
            st_deviation.append(self.__get_st_deviation(d))

        return {'mean': mean, 'median': median, 'standard deviation': st_deviation}