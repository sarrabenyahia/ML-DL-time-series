import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from statsmodels.graphics.gofplots import ProbPlot
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import calendar
from ydata_profiling import ProfileReport
from statsmodels.tsa.seasonal import seasonal_decompose


class GeneralPresentator:
    def __init__(self, df):
        self.df = df

    def print_basic_prez(self):
        self.print_column_names()
        self.print_data_types()
        self.print_basic_stats()
        self.print_missing_values()
        # self.print_categorical_uniques()
        self.print_sample_data()

    def print_column_names(self):
        print("Column Names:")
        print(list(self.df.columns))
        print()

    def print_data_types(self):
        print("Data Types:")
        display(self.df.dtypes.to_frame().T)
        print()

    def print_basic_stats(self):
        print("Basic Statistics:")
        display(self.df.describe())
        print()

    def print_missing_values(self):
        missing_values_count = self.df.isna().sum()
        if missing_values_count.sum() > 0:
            print("Missing Values:")
            display(missing_values_count.to_frame().T)
            print()
        else:
            print("No missing values found.\n")

    def print_categorical_uniques(self):
        categorical_features = ["day", "month", "year"]
        for feature in categorical_features:
            unique_values = self.df[feature].unique()
            print(f"Unique values for {feature}:")
            print(unique_values)
            print()

    def print_sample_data(self):
        print("Sample Data:")
        display(self.df.head())
        print()


class DataPlotter:
    """
    A class to analyze basic statistics and generate plots for a given DataFrame.
    """

    def __init__(self, df):
        """
        Initializes the class with the given DataFrame and resamples it.
        """
        self.df = df
        self.granularity_text = ['Hourly', 'Daily', 'Weekly', 'Monthly', 'Quarterly']
        self._resample()

    def _resample(self):
        """
        Resamples the DataFrame into daily, weekly, monthly, and quarterly groups.
        """
        hourly_df = self.df.resample('H').sum()
        daily_df = self.df.resample('D').sum()
        weekly_df = self.df.resample('W').sum()
        monthly_df = self.df.resample('M').sum()
        quarter_df = self.df.resample('3M').sum()

        self.resampled_dfs = [hourly_df, daily_df, weekly_df, monthly_df, quarter_df]

    def _get_granularity_list(self, granularity):
        """
        Returns the list of DataFrames based on the granularity input.
        """
        granularities = {'all': self.resampled_dfs,
                         'H': [self.resampled_dfs[0]],
                         'D': [self.resampled_dfs[1]],
                         'W': [self.resampled_dfs[2]],
                         'M': [self.resampled_dfs[3]],
                         '3M': [self.resampled_dfs[4]]}
        return granularities[granularity]

    def data_profiling(self, granularity='all'):
        """
        Generates a data profiling report for the specified granularity.
        """
        granularity_list = self._get_granularity_list(granularity)

        for df in granularity_list:
            profile = ProfileReport(df, title="Profiling Report")
            profile.to_widgets()

    def plot_time_series(self, column, granularity='all'):
        """
        Plots the time series of the given column for the specified granularity.
        """
        granularity_list = self._get_granularity_list(granularity)

        for index, df in enumerate(granularity_list):
            plt.figure(figsize=(15, 5))
            ax = sns.lineplot(data=df[column])
            if granularity == "all":
                ax.set(title=f'{self.granularity_text[index]} values', ylabel="Watts/hour")
            elif granularity == "H":
                ax.set(title=f'Hourly values', ylabel="Watts/hour")
            elif granularity == "D":
                ax.set(title=f'Daily values', ylabel="Watts/hour")
            elif granularity == "W":
                ax.set(title=f'Weekly values', ylabel="Watts/hour")
            elif granularity == "M":
                ax.set(title=f'Monthly values', ylabel="Watts/hour")
            elif granularity == "3M":
                ax.set(title=f'Quarterly values', ylabel="Watts/hour")

    def plot_prob(self, column, granularity='all'):
        """
        Plots the probability plot for the given column for the specified granularity.
        """
        granularity_list = self._get_granularity_list(granularity)

        for index, df in enumerate(granularity_list):
            ProbPlot(data=df[column]).qqplot(line='s')
            plt.title(f'{self.granularity_text[index]} values')

    def plot_histogram(self, column, granularity='all'):
        """
        Plots the histogram of the given column for the specified granularity.
        """
        granularity_list = self._get_granularity_list(granularity)
        for index, df in enumerate(granularity_list):
            plt.figure(figsize=(15, 5))
            ax = sns.histplot(data=df[column], bins=50,
                              kde=True, stat="density", alpha=0.6)
            mu, sigma = stats.norm.fit(df[column])
            xmin, xmax = plt.xlim()
            x = np.linspace(xmin, xmax, 100)
            p = stats.norm.pdf(x, mu, sigma)
            sns.lineplot(x=x, y=p, color='black')
            if granularity == "all":
                ax.set(title=f'{self.granularity_text[index]} distribution of {column}', xlabel=column, ylabel='Density')
            elif granularity == "D":
                ax.set(title=f'Daily distribution of {column}', xlabel=column, ylabel='Density')
            elif granularity == "W":
                ax.set(title=f'Weekly distribution of {column}', xlabel=column, ylabel='Density')
            elif granularity == "M":
                ax.set(title=f'Monthly distribution of {column}', xlabel=column, ylabel='Density')
            elif granularity == "3M":
                ax.set(title=f'Quarterly distribution of {column}', xlabel=column, ylabel='Density')


class PatternAnalyzer:

    def __init__(self, df):
        """
        Initializes the class with the given DataFrame and resamples it.
        """
        self.df = df
        self._average()

    def _average(self):
        """
        Resamples the DataFrame into daily, weekly, monthly, and yearly groups.
        """
        daily_avg_df = self.df.groupby(self.df.index.day).mean()
        weekly_avg_df = self.df.groupby(self.df.index.week).mean()
        monthly_avg_df = self.df.groupby(self.df.index.month).mean()
        yearly_avg_df = self.df.groupby(self.df.index.year).mean()

        self.averaged_dfs = [daily_avg_df,
                             weekly_avg_df, monthly_avg_df, yearly_avg_df]

    def _get_granularity_list(self, granularity):
        """
        Returns the list of DataFrames based on the granularity input.
        """
        granularities = {'all': self.averaged_dfs,
                         'W': [self.averaged_dfs[0]],
                         'W': [self.averaged_dfs[1]],
                         'M': [self.averaged_dfs[2]],
                         'Y': [self.averaged_dfs[3]]}
        return granularities[granularity]

    def plot_time_series(self, column, granularity='all'):
        """
        Plots the time series of the given column for the specified granularity.
        """
        granularity_text = ['Daily', 'Weekly', 'Monthly', 'Quarterly']
        granularity_list = self._get_granularity_list(granularity)

        for df in granularity_list:
            plt.figure(figsize=(15, 5))
            ax = sns.lineplot(data=df[column])
            if granularity == "all":
                ax.set(title=f'{granularity_text[index]} values for {column}', ylabel="Watts/hour")
            elif granularity == "D":
                ax.set(title=f'Daily values for {column}', ylabel="Watts/hour")
            elif granularity == "W":
                ax.set(title=f'Weekly values for {column}', ylabel="Watts/hour")
            elif granularity == "M":
                ax.set(title=f'Monthly values for {column}', ylabel="Watts/hour")
            elif granularity == "3M":
                ax.set(title=f'Quarterly values for {column}', ylabel="Watts/hour")


    def seasonal_decompositation_additive(self, column, granularity="all"):
        granularity_text = ['Daily', 'Weekly', 'Monthly', 'Quarterly']
        granularity_list = self._get_granularity_list(granularity)

        for index, df in enumerate(granularity_list):
            print(f"{granularity_text[index]} Decomposition of {column}")
            result = seasonal_decompose(
                df[column], model='additive', period=1)
            result.plot()
            plt.show()
            
    def seasonal_decompositation_multiplicative(self, column, granularity="all"):
        granularity_text = ['Daily', 'Weekly', 'Monthly', 'Quarterly']
        granularity_list = self._get_granularity_list(granularity)

        for df in granularity_list:
            print(f"{granularity_text[index]} Decomposition of {column}")
            result = seasonal_decompose(
                df[column], model='multiplicative', period=1)
            result.plot()
            plt.show()


