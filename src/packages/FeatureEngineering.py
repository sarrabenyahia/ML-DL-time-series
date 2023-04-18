import numpy as np
import pandas as pd
import numpy as np
import holidays


class FeatureEngineer:

    def __init__(self, df, target):
        self.df = df
        self.target = target

    def create_variables(self, lag, time, window_size):
        self._lag_creation(lag, time)
        self._window_rolling(window_size, time)
        self._day_and_night()
        self._finally_the_weekend()
        self._sinus_hour()
        self._is_ferie()
        self._winter_is_coming()
        self._drop_not_lagged()
        self.df = self.df.dropna()
        return self.df

    def _lag_creation(self, lag, time="day"):
        if isinstance(lag, int):
            lag = [lag]
        if time == "day":
            lag_min = [l*60*24 for l in lag]
        elif time == "hour":
            lag_min = [l*60 for l in lag]
        elif time == "minute":
            lag_min = lag
        else:
            raise ValueError(
                "Invalid time value. Please use 'day', 'hour' or 'minute.")

        new_cols = []
        for col in self.df.columns:
            for index, l in enumerate(lag_min):
                new_col = self.df[col].shift(l)
                new_col.name = f"{col}_lag{lag[index]}{time[0]}"
                new_cols.append(new_col)
        self.df = pd.concat([self.df] + new_cols, axis=1)
 

    def _window_rolling(self, window_size, time="day"):
        if isinstance(window_size, int):
            window_size = [window_size]
            if time == "day":
                window_min = [l*60*24 for l in window_size]
            elif time == "hour":
                window_min = [l*60 for l in window_size]
            elif time == "minute":
                window_min = window_size
            else:
                raise ValueError(
                    "Invalid time value. Please use 'day', 'hour' or 'minute.'")

        for window in window_min:
            self.df[f'{self.target}_mean_{window}'] = self.df[self.target].rolling(
                window).mean()
            self.df[f'{self.target}_min_{window}'] = self.df[self.target].rolling(
                window).min()
            self.df[f'{self.target}_max_{window}'] = self.df[self.target].rolling(
                window).max()
            self.df[f'{self.target}_std_{window}'] = self.df[self.target].rolling(
                window).std()

    def _day_and_night(self):
        self.df['hour'] = self.df.index.hour
        self.df['is_daytime'] = np.where(
            self.df['hour'].isin(range(7, 20)), 1, 0)
        self.df.drop(columns='hour', inplace=True)

    def _sinus_hour(self):
        self.df['hour'] = self.df.index.hour
        self.df['hour_sin'] = np.sin(2 * np.pi * self.df['hour'] / 24)
        self.df.drop(columns='hour', inplace=True)
        
    def _finally_the_weekend(self):
        self.df['is_weekend'] = self.df.index.dayofweek.isin([
            5, 6]).astype(int)

    def _is_ferie(self):
        # Create a new column for whether the date is a public holiday in France
        fr_holidays = holidays.France()
        idx = pd.DatetimeIndex(self.df.index.date)
        self.df['is_ferie'] = idx.isin(fr_holidays).astype(int)

    def _winter_is_coming(self):
        self.df['is_winter'] = np.where((self.df.index.month == 12) | (
            self.df.index.month == 1) | (self.df.index.month == 2), 1, 0)
        self.df['is_summer'] = np.where((self.df.index.month == 6) | (
            self.df.index.month == 7) | (self.df.index.month == 8), 1, 0)

    def _drop_not_lagged(self):
        self.df.drop(columns=["Global_active_power","Global_reactive_power","Voltage",
                      "Global_intensity", "Sub_metering_1", "Sub_metering_2",
                      "Sub_metering_3" , "other_submetering"], inplace=True)
        
        
    
