import os
import pandas

class Repository:
    def __init__(self) -> None:
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.period_start = False
        self.period_end = False

    def set_period(self, start: str, end: str) -> None:
        self.period_start = start
        self.period_end = end

    def get_all_data(self) -> list[str, str]:
        result = []
        for filename in self.get_all_filenames():
            #result.append(self.get_data(filename))
            result.append(self.get_file_content(filename))
        return result
    
    def get_filtered_data(self, start=None, end=None) -> list[str, str]:
        if start != None and end != None:
            #probably want to verify that the start and end are valid dates
            #in the near future ;)
            self.set_period(start, end)
        result = []
        for filename in self.get_all_filenames():
            result.append(self.get_file_content(filename))
        return result
    
    def get_data(self, filename: str) -> str:
        with open(os.path.join(self.data_dir, filename), 'r') as file:
            
            return file.read()
        
    def get_all_filenames(self) -> list[str]:
        return os.listdir(self.data_dir)
    
    def get_file_content(self, filename: str) -> tuple[str, pandas.DataFrame]:
        data_frame = pandas.read_csv(
            os.path.join(self.data_dir, filename), 
            index_col='Time', 
            parse_dates=['Time'],
            header=0)
        data_frame_resampled = data_frame.resample('1min').mean()
        filename_cropped = filename.split('.')[0].strip("-data")
        sensor_name = filename_cropped[-4:]
        data_frame_interpolated = data_frame_resampled.interpolate(method='nearest')
        if self.period_start and self.period_end:
            mask = (data_frame_interpolated.index > self.period_start) & (data_frame_interpolated.index <= self.period_end)
            data_frame_interpolated = data_frame_interpolated.loc[mask]
        return (sensor_name, data_frame_interpolated)
       