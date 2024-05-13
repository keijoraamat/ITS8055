"""Module for the Repository class. Provides data from csv files."""

import os
import sys
import numpy as np
import pandas


class Repository:
    """Provides data from csv files in the data directory."""
    def __init__(self) -> None:
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.i_data_dir = os.path.join(os.path.dirname(__file__), 'interpolated_data')
        self.period_start = '2022-08-02 00:00:00'
        self.period_end = '2022-08-13 23:59:59'
        self.interpolation_method = False

    def set_period(self, start: str, end: str) -> None:
        """Set the period for which to filter the data."""
        self.period_start = start
        self.period_end = end

    def set_interpolation_method(self, method: str) -> None:
        """Set the interpolation method for the data."""
        self.interpolation_method = method

    def get_interpolated_data(self, method: str) -> dict[str, list[pandas.DataFrame]]:
        """Returns all data interpolated using given method"""
        if method is None:
            print("No interpolation method set, exiting")
            sys.exit(0)
        if not os.path.exists(os.path.join(self.i_data_dir, method)):
            print(f"No data found for {method} interpolation method\nStarting interpolating data...")
            self.interpolate_all_data()
        result = {}
        for region in os.listdir(os.path.join(self.i_data_dir, method)):
            result[region] = []
            for filename in os.listdir(os.path.join(self.i_data_dir, method, region)):
                result[region].append(self._get_file_content(filename, region=region, interpol_method=method, data='interpolated'))
        return result

    def get_all_filenames(self, region:str) -> list[str]:
        """Returns a list of all filenames in the region directory"""
        return os.listdir(os.path.join(self.data_dir, region))

    def get_all_regions(self) -> list[str]:
        """Returns a list of all regions in the data directory"""
        return os.listdir(os.path.join(self.data_dir))

    def _get_file_content(self, filename: str, region:str, interpol_method: str, data=None) -> tuple[str, pandas.DataFrame]:
        """Returns the content of a file in the data directory"""
        data_source = self.data_dir
        if data is not None:
            data_source = os.path.join(self.i_data_dir, interpol_method)
        data_frame: pandas.DataFrame = pandas.read_csv(
            filepath_or_buffer=os.path.join(data_source, region, filename),
            index_col='Time',
            parse_dates=['Time'],
            header=0)
        data_frame_resampled: pandas.DataFrame = data_frame.resample(rule='1min').mean()
        filename_cropped: str = filename.split(sep='.')[0].replace("-data",'')
        sensor_name: str = filename_cropped[-4:]
        if self.period_start and self.period_end:
            # Create a complete date range from start to end time
            complete_date_range: pandas.DatetimeIndex = pandas.date_range(start=self.period_start, end=self.period_end, freq='1min')

            # Reindex the dataframe with the complete date range
            data_frame_reindexed: pandas.DataFrame = data_frame_resampled.reindex(labels=complete_date_range)
            data_frame_reindexed.index.name = 'Time'

            # Interpolate the missing values
            if interpol_method == 'linear':
                data_frame_interpolated: pandas.DataFrame = data_frame_reindexed.interpolate(method='linear')
            elif interpol_method == 'nearest':
                data_frame_interpolated: pandas.DataFrame = data_frame_reindexed.interpolate(method='nearest')
            else:
                print("Invalid interpolation method, exiting")
                sys.exit(0)


            data_frame_interpolated = np.ceil(data_frame_interpolated)
            # Forward fill for missing data at the beginning
            data_frame_interpolated.ffill(inplace=True)
            # Backward fill for missing data at the end
            data_frame_interpolated.bfill(inplace=True)

            mask = (data_frame_interpolated.index > self.period_start) & (data_frame_interpolated.index <= self.period_end)
            data_frame_interpolated = data_frame_interpolated.loc[mask]
        else:
            print("no period set, exiting")
            sys.exit(0)
        return (sensor_name, data_frame_interpolated)

    def _save_data(self, data: pandas.DataFrame, file_name: str, path: str) -> None:
        """Saves the data to a csv file"""
        data.to_csv(path_or_buf=os.path.join(path, file_name), index=False, header=True)

    def _interpolate_and_save(self, filename: str, region_name:str, interpol_method: str) -> None:
        """
        Reads raw data, 
        interpolates the missing bits 
        and saves it to a file in separete directory
        """
        content: tuple[str, pandas.DataFrame] = self._get_file_content(filename=filename, region=region_name, interpol_method=interpol_method)
        sensor_name: str = content[0]
        data_frame: pandas.DataFrame = content[1]
        data_frame.reset_index(inplace=True)
        data_frame.rename(columns={'index': 'Time'}, inplace=True)
        if not os.path.exists(os.path.join(self.i_data_dir, interpol_method, region_name)):
            os.makedirs(os.path.join(self.i_data_dir, interpol_method, region_name))
        self._save_data(data=data_frame, file_name=f'{sensor_name}-data.csv', path=os.path.join(
            self.i_data_dir, interpol_method, region_name))

    def interpolate_all_data(self) -> None:
        """Interpolates all data and saves it to a file"""
        for region in self.get_all_regions():
            for filename in self.get_all_filenames(region):
                for method in ['linear', 'nearest']:
                    print(f"Interpolating data for {filename} from {region} using {method} method")
                    self._interpolate_and_save(filename, region, method)
        print("Data interpolation completed")
