import numpy as np
import pandas as pd
import numpy as np
from scipy.fft import fft
from datetime import datetime


class FeatureEngineer:

    def __init__(self, df):
        self.df = df

    def lag_creation(self, lag, time="day"):
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

        return pd.concat([self.df] + new_cols, axis=1)

    def window_rolling(self, window_size, time="day"):
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
            self.df[f'Global_active_power_mean_{window}'] = self.df['Global_active_power'].rolling(
                window).mean()
            self.df[f'Global_active_power_min_{window}'] = self.df['Global_active_power'].rolling(
                window).min()
            self.df[f'Global_active_power_max_{window}'] = self.df['Global_active_power'].rolling(
                window).max()
            self.df[f'Global_active_power_std_{window}'] = self.df['Global_active_power'].rolling(
                window).std()

    def create_time_based_features(self):
        self.df['hour'] = self.df.index.hour
        self.df['is_daytime'] = np.where(
            self.df['hour'].isin(range(7, 20)), 1, 0)
        
    def winter_summer_features(self):
        self.df['winter'] = np.where((self.df.index.month == 12) | (self.df.index.month == 1) | (self.df.index.month == 2), 1, 0)
        self.df['summer'] = np.where((self.df.index.month == 6) | (self.df.index.month == 7) | (self.df.index.month == 8), 1, 0)

    def create_fourier_transform_features(self, num_features=5):
        fft_vals = fft(self.df['Global_active_power'])
        abs_fft_vals = np.abs(fft_vals)
        num_samples = len(self.df)
        freqs = np.arange(num_samples) / num_samples
        top_freqs = freqs[np.argsort(-abs_fft_vals)[:num_features]]

        for i, freq in enumerate(top_freqs, 1):
            self.df[f'Global_active_power_freq_{i}'] = abs_fft_vals[int(
                freq*num_samples)]
