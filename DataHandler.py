import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# Data Handling class for the ISMN networks.
# Get data method returns to dictionary which contains pandas dataframes for several depths.
# Get data returns {depth1 : pd.DataFrame1,depth2:pd.DataFrame2 ... etc}
class DataHandler:
    def __init__(self, direc: str, network: str, station: str):
        self.direc = direc
        self.network = network
        self.station = station
        self.full_path = os.path.join(self.direc, self.network, self.station)

    @staticmethod
    def get_times(date_first: str, date_last: str) -> list:
        fy, fm, fd = date_first.strip("\n").split(" ")[0].split("/")
        ly, lm, ld = date_last.strip("\n").split(" ")[0].split("/")
        start_date = datetime(int(fy), int(fm), int(fd), 0, 0)  # Jan 1, 2021, 00:00
        end_date = datetime(int(ly), int(lm), int(ld), 23, 0)  # Dec 31, 2021, 23:00
        current_date = start_date
        timestamps = []
        time_step = timedelta(hours=1)

        while current_date <= end_date:
            # Format as YY-MM-dd HH:MM
            formatted_date = current_date.strftime("%Y/%m/%d %H:%M")
            timestamps.append(formatted_date)
            current_date += time_step
        return timestamps

    def read_ismn_file(self, file: str, daily_hourly: str = "daily") -> pd.DataFrame:
        # daily_hourly set temporal resolution daily or hourly get save to pandas dataframe
        # Currently only gets quality flag "G"
        import warnings
        warnings.filterwarnings('ignore')

        with open(os.path.join(self.full_path, file)) as f:
            next(f)
            data, date, valid = [], [], []
            for line in f:
                split = line.strip("\n").split(" ")
                y, m, d = split[0].split("/")
                h, mm = split[1].split(":")
                formatted_date = datetime(int(y), int(m), int(d), int(h), int(mm)).strftime("%Y/%m/%d %H:%M")
                date.append(formatted_date)
                data.append(float(split[-3]))
                if split[-2] == "G":
                    valid.append(True)
                else:
                    valid.append(False)

            df2 = pd.DataFrame(index=DataHandler.get_times(date[0], date[-1]))
            df2.loc[date, "data"] = data

            if daily_hourly == "hourly":
                return df2
            elif daily_hourly == "daily":
                df = pd.DataFrame()
                dates = list((pd.date_range(date[0].split(" ")[0], date[-1].split(" ")[0])).strftime('%Y/%m/%d'))
                df2.loc[date, "data"] = data
                df2.loc[date, "valid"] = valid
                if file.split("_")[3] == "p":
                    daily_data = np.nansum(df2.loc[:, "data"].values.reshape(int(len(df2) / 24), 24), axis=1)
                else:
                    daily_data = np.nanmean(df2.loc[:, "data"].values.reshape(int(len(df2) / 24), 24), axis=1)

                df2["valid"] = df2["valid"].fillna(False) 

                logic = np.sum(df2.loc[:, "valid"].values.reshape(int(len(df2) / 24), 24), axis=1)
                daily_data[logic < 8] = np.nan
                df.index = dates
                df["data"] = daily_data
                return df
            else:
                raise ValueError("daily_hourly variable should be hourly or daily always! Check variable")

    def get_data(self, daily_hourly="hourly") -> dict:
        soil_data_dict = {}
        files = os.listdir(self.full_path)
        
        # Filter out CSVs and sort to try and read them in chronological order
        sm_files = sorted(list(filter(lambda x: "csv" not in x, files)))
        
        for file in sm_files:
            splits = file.split("_")
            param = splits[3]
            dict_key = f"{param}_{splits[4]}-{splits[5]}"
            
            # Read the current file
            df_new = self.read_ismn_file(file, daily_hourly)
            
            # Check if this parameter/depth combination already exists
            if dict_key in soil_data_dict:
                # Concatenate the new data to the existing data
                soil_data_dict[dict_key] = pd.concat([soil_data_dict[dict_key], df_new])
            else:
                # First time seeing this combination, create the entry
                soil_data_dict[dict_key] = df_new

        # Optional but highly recommended cleanup step:
        # If files overlap or were read out of order, sort the index and drop duplicate dates
        for key in soil_data_dict.keys():
            # Ensure the index is treated as datetime for proper sorting
            soil_data_dict[key].index = pd.to_datetime(soil_data_dict[key].index)
            
            # Sort chronologically
            soil_data_dict[key] = soil_data_dict[key].sort_index()
            
            # Drop duplicate rows (keeping the first one it finds) in case files had overlapping dates
            soil_data_dict[key] = soil_data_dict[key][~soil_data_dict[key].index.duplicated(keep='first')]

        return soil_data_dict

    def get_coordinates(self) -> dict[str:float, str:float]:  # dict(lat:value,lon:value)
        file = sorted(os.listdir(self.full_path))[0]
        full_path = os.path.join(self.full_path, file)
        with open(full_path) as xx:
            line = next(xx)
            split = list(filter(None, line.split(" ")))
            return {"lat": float(split[3]), "lon": float(split[4])}
