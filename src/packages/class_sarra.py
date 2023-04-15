import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from statsmodels.graphics.gofplots import ProbPlot

class DataPlotter:
    def __init__(self, df, column):
        self.df = df
        self.column = column

    def plot(self):
        """
        Plots the given column from the given DataFrame
        """
        plt.figure(figsize=(15,5))
        ax = sns.lineplot(data=self.df[self.column])
        ax.set(title=f'{self.column} plot for {self.df.index.name}', xlabel='Date' if 'date' in self.df.index.name.lower() else 'Week', ylabel=self.column)

    def plot_prob(self):
        """
        Plots the probability plot for the given column from the given DataFrame
        """
        qq = ProbPlot(self.df[self.column]).qqplot(line='s')
