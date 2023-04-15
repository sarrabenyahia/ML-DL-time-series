import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from statsmodels.graphics.gofplots import ProbPlot
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


#! TODO : Class for Stationnarity test 


class GeneralPresentator:
    def __init__(self, df):
        self.df = df

    def print_basic_prez(self):
        self.print_column_names()
        self.print_data_types()
        self.print_basic_stats()
        self.print_missing_values()
        self.print_categorical_uniques()
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
    def __init__(self, df):
        self.df = df

    def plotTS(self, column):
        """
        Plots the given column from the given DataFrame
        """
        plt.figure(figsize=(15, 5))
        ax = sns.lineplot(data=self.df[column])
        ax.set(title=f'{column} plot for {self.df.index.name}',
               xlabel='Date' if 'date' in self.df.index.name.lower() else 'Week', ylabel=column)

    def plot_prob(self, column):
        """
        Plots the probability plot for the given column from the given DataFrame
        """
        qq = ProbPlot(self.df[column]).qqplot(line='s')

    def plot_histogram(self, column):
        """
        Plots a histogram of the given column from the given DataFrame
        """
        plt.figure(figsize=(15, 5))
        ax = sns.histplot(
            data=self.df[column], bins=50, kde=True, stat="density", alpha=0.6)
        mu, sigma = stats.norm.fit(self.df[column])
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.norm.pdf(x, mu, sigma)
        sns.lineplot(x=x, y=p, color='black')
        ax.set(title=f'Distribution of {column}',
               xlabel=column, ylabel='Density')




class DataExplorer:
    def __init__(self, df):
        self.df = df

    def print_correlation_matrix(self):
        """
        Prints the correlation matrix of the numerical columns in the DataFrame
        """
        corr_matrix = self.df.select_dtypes(include=[np.number]).corr()
        print("Correlation Matrix:")
        display(corr_matrix)
        print()

    def plot_correlation_heatmap(self):
        """
        Plots a heatmap of the correlation matrix of the numerical columns in the DataFrame
        """
        corr_matrix = self.df.select_dtypes(include=[np.number]).corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        plt.title("Correlation Heatmap")
        plt.show()
        
    def plot_acf_pacf(self, column):
        """
        Plots the autocorrelation and partial autocorrelation of the given column from the given DataFrame

        Parameters:
        column (str): The name of the column to plot
        """
        plt.figure(figsize=(15, 5))
        plot_acf(self.df[column], lags=30, alpha=0.05)
        plt.title(
            f"Autocorrelation and Partial Autocorrelation of {column} by Lag")
        plt.xlabel("Lag")

        plt.figure(figsize=(15, 5))
        plot_pacf(self.df[column], lags=30, alpha=0.05)
        plt.title(
            f"Autocorrelation and Partial Autocorrelation of {column} by Lag")
        plt.xlabel("Lag")