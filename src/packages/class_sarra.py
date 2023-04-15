import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from statsmodels.graphics.gofplots import ProbPlot

class DataPlotter:
    def __init__(self, df ):
        self.df = df

    def plotTS(self, column):
        """
        Plots the given column from the given DataFrame
        """
        plt.figure(figsize=(15,5))
        ax = sns.lineplot(data=self.df[column])
        ax.set(title=f'{column} plot for {self.df.index.name}', xlabel='Date' if 'date' in self.df.index.name.lower() else 'Week', ylabel=column)


    def plot_prob(self, column) :
        """
        Plots the probability plot for the given column from the given DataFrame
        """
        qq = ProbPlot(self.df[column]).qqplot(line='s')


    def plot_histogram(self, column):
        """
        Plots a histogram of the given column from the given DataFrame
        """
        plt.figure(figsize=(15,5))
        ax = sns.histplot(data=self.df[column], bins=50, kde=True, stat="density", alpha=0.6)
        mu, sigma = stats.norm.fit(self.df[column])
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.norm.pdf(x, mu, sigma)
        sns.lineplot(x=x, y=p, color='black')
        ax.set(title=f'Distribution of {column}', xlabel=column, ylabel='Density')
        