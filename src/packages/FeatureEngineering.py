import numpy as np
import pandas as pd
import numpy as np
from scipy.fft import fft
from datetime import datetime


class FeatureEngineer:
    def __init__(self, df):
        self.df = df

    def __combine_datetime(self):
        # Combiner les colonnes 'Date' et 'Time' en une seule colonne datetime
        self.df['datetime'] = pd.to_datetime(
            self.df['Date'] + ' ' + self.df['Time'], format='%d/%m/%Y %H:%M:%S')
        # Définir la colonne 'datetime' comme index
        self.df = self.df.set_index('datetime')

    def __convert_numeric(self, cols):
        # Convertir les colonnes souhaitées en valeurs numériques, avec les valeurs non convertibles définies sur NaN.
        self.df = self.df.dropna()
        self.df[cols] = self.df[cols].apply(pd.to_numeric, errors='coerce')

    def __convert_date(self):
        # Convertir la colonne 'Date' en format datetime
        self.df['Date'] = pd.to_datetime(self.df['Date'], dayfirst=True)

    def __convert_time(self):
        # apply the datetime.strptime() method to each element in the column

        self.df['Time'] = self.df['Time'].apply(
            lambda x: datetime.strptime(x, "%H:%M:%S").strftime("%H:%M:%S"))

    def __extract_date_components(self):
        # Extraire les composants jour, mois et année de la colonne 'Date'

        self.df = self.df.assign(day=self.df['Date'].dt.day,
                                 month=self.df['Date'].dt.month,
                                 year=self.df['Date'].dt.year)

    def __downcast(self):
        """
        Downcast in order to save memory
        """
        cols = self.df.dtypes.index.tolist()
        types = self.df.dtypes.values.tolist()
        for i, t in enumerate(types):
            # Integer
            if 'int' in str(t):
                # Check if minimum and maximum are in the limit of int8
                if self.df[cols[i]].min() > np.iinfo(np.int8).min and self.df[cols[i]].max() < np.iinfo(np.int8).max:
                    self.df[cols[i]] = self.df[cols[i]].astype(np.int8)
                # Check if minimum and maximum are in the limit of int16
                elif self.df[cols[i]].min() > np.iinfo(np.int16).min and self.df[cols[i]].max() < np.iinfo(np.int16).max:
                    self.df[cols[i]] = self.df[cols[i]].astype(np.int16)
                # Check if minimum and maximum are in the limit of int32
                elif self.df[cols[i]].min() > np.iinfo(np.int32).min and self.df[cols[i]].max() < np.iinfo(np.int32).max:
                    self.df[cols[i]] = self.df[cols[i]].astype(np.int32)
                # Choose int64
                else:
                    self.df[cols[i]] = self.df[cols[i]].astype(np.int64)
            # Float
            elif 'float' in str(t):
                if self.df[cols[i]].min() > np.finfo(np.float16).min and self.df[cols[i]].max() < np.finfo(np.float16).max:
                    self.df[cols[i]] = self.df[cols[i]].astype(np.float16)
                elif self.df[cols[i]].min() > np.finfo(np.float32).min and self.df[cols[i]].max() < np.finfo(np.float32).max:
                    self.df[cols[i]] = self.df[cols[i]].astype(np.float32)
                else:
                    self.df[cols[i]] = self.df[cols[i]].astype(np.float64)
            # Object
            elif t == object:
                if cols[i] == 'date':
                    self.df[cols[i]] = pd.to_datetime(
                        self.df[cols[i]], format='%Y-%m-%d')
                else:
                    self.df[cols[i]] = self.df[cols[i]].astype('category')
        return self.df

    def process_data(self,numeric_cols):
        self.__combine_datetime()
        self.__convert_numeric(numeric_cols)
        self.__convert_date()
        self.__convert_time()
        self.__extract_date_components()
        self.__downcast()
        # ramener la cible à la bonne unité, nécéssaire avant la réalisation de l'EDA et les analyses descriptives
        self.df['Global_active_power_Wh'] = self.df['Global_active_power']*1000/60
        # création du other_submetering
        self.df['other_submetering'] = self.df['Global_active_power_Wh'] - \
            self.df['Sub_metering_1'] - \
            self.df['Sub_metering_2'] - self.df['Sub_metering_3']
        return self.df

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
        self.df['is_night_time'] = np.where(self.df['hour'].isin(
            range(0, 7)) | self.df['hour'].isin(range(20, 24)), 1, 0)

    def create_fourier_transform_features(self, num_features=5):
        fft_vals = fft(self.df['Global_active_power'])
        abs_fft_vals = np.abs(fft_vals)
        num_samples = len(self.df)
        freqs = np.arange(num_samples) / num_samples
        top_freqs = freqs[np.argsort(-abs_fft_vals)[:num_features]]

        for i, freq in enumerate(top_freqs, 1):
            self.df[f'Global_active_power_freq_{i}'] = abs_fft_vals[int(
                freq*num_samples)]
