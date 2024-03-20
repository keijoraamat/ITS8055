import os
import pandas

class Repository:
    def __init__(self) -> None:
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def get_all_data(self) -> list[str, str]:
        result = []
        for filename in self.get_all_filenames():
            #result.append(self.get_data(filename))
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
        return (sensor_name, data_frame_resampled.interpolate(method='nearest'))
       