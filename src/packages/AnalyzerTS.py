import plotly.graph_objs as go
import plotly.express as px
import statsmodels.graphics.tsaplots as tsaplots
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import pandas as pd
import ruptures as rpt


class VizualizationTS:

    def __init__(self, df:pd.DataFrame, target:str):
        self.df = df
        self.target = target
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    def plot_line_series(self, cols):
        """
        Create subplots for each  time series.

        Args:
            self : DataFrame containing the  time series.
            cols: List of column names to plot.

        Returns : 
            Plots representing the evolution of each time series.
        """
        for i, col in enumerate(cols):
            fig = go.Figure()
            fig.add_trace(go.Line(x=self.df.index, y=self.df[col], mode='lines', line_color=self.colors[i]))
            fig.update_layout(title=f"Line Series of {col}",
                              xaxis_title='Date',
                              yaxis_title='Percent Change',
                              template='plotly_white')
            fig.show()

    def plot_acf_pacf(self, cols):
        """
       Graphique des ACF et PACF des différentes séries.

        Args:
            cols (list): Liste des noms des colonnes à utiliser pour l'ACF and PACF .

        Returns:
            ACF et PACF des séries
        """
        for col in cols:
            print(f"ACF and PACF of the series {col}:")
            ts = self.df[col]
            tsaplots.plot_acf(ts, lags=10)
            tsaplots.plot_pacf(ts, lags=10)
            plt.show()

    def plot_target(self):
        """
        Plot the evolution of the default rate using the DataFrame provided during class initialization.

        Args : 
            self : DataFrame containing the default rate time series

        Returns :
            A plot of the default rate evolution.
        """
        fig = px.line(self.df, x=self.df.index, y=self.target)
        fig.update_layout(title_text='Quarterly Default Rate 2010 - 2019')
        fig.show()

    def plot_autocorrelation_target(self):
        """ 
            Autocorrélation de la target
            
         Args : 
             self : DataFrame contenant la série de la target
             
          Returns : 
              ACF de la target """
        fig = tsaplots.plot_acf(self.df[self.target], lags=20)

        plt.xlabel("Lag at k")
        plt.ylabel("Correlation coefficient")
        plt.show()

    def plot_partial_autocorrelation_target(self):
        """ 
        Autocorrélation partielle de la target
        
        Args : 
            self : DataFrame contenant la série de la target
            
        Returns : 
            PACF de la target
                        """
        fig = tsaplots.plot_pacf(self.df[self.target], lags=10)

        plt.xlabel("Lag at k")
        plt.ylabel("Correlation coefficient")
        plt.show()


class StationarityTest:

    def __init__(self, data):
        self.data = data

    def adf_test(self, columns):
        """
        Tests de Dickey Fuller de stationnarité des séries 
        
        Args : 
            self : DataFrame
            columns : séries contenues dans le DataFrame dont on teste la stationnarité
         
         Returns : 
             résultat du test de stationnarité : série stationnaire ou non-stationnaire """
        for col in columns:
            result = sm.tsa.stattools.adfuller(self.data[col])
            print(f'ADF test pour {col}:')
            print(f'ADF statistique: {result[0]}')
            print(f'p-value: {result[1]}')
            print(f'Valeurs critiques: {result[4]}')
            if result[1] < 0.05:
                print("L'hypothèse nulle de non stationnarité a été rejeté, la série est donc stationnaire. ")
            else:
                print(
                    "L'hypothèse nulle de non stationnarité ne peux pas etre rejeté, la série est donc non "
                    "stationnaire.")
            print('')

    def kpss_test(self, columns):
        """
        Tests de KPSS de stationnarité des séries 
        
        Args : 
            self : DataFrame
            columns : séries contenues dans le DataFrame dont on teste la stationnarité
         
         Returns : 
             résultat du test de stationnarité : série stationnaire ou non-stationnaire """
        for col in columns:
            result = sm.tsa.stattools.kpss(self.data[col])
            print(f'KPSS test pour {col}:')
            print(f'KPSS statistique: {result[0]}')
            print(f'p-value: {result[1]}')
            print(f'Lag utilisé: {result[2]}')
            if result[1] < 0.05:
                print("L'hypothèse nulle de non stationnarité a été rejeté, la série est donc stationnaire. ")
            else:
                print(
                    "L'hypothèse nulle de non stationnarité ne peux pas etre rejeté, la série est donc non "
                    "stationnaire.")
            print('')

    def pp_test(self, columns):
        """
        Tests de Phillips Perron de stationnarité des séries 
        
        Args : 
            Self : DataFrame
            columns : séries contenues dans le DataFrame dont on teste la stationnarité
         
        Returns : 
            Résultat du test de stationnarité : série stationnaire ou non-stationnaire """
        for col in columns:
            result = sm.tsa.stattools.adfuller(self.data[col], regression='ct')
            print(f'Phillips-Perron test pour {col}:')
            print(f'ADF statistique: {result[0]}')
            print(f'p-value: {result[1]}')
            print(f'Lag utilisé: {result[2]}')
            if result[1] < 0.05:
                print("L'hypothèse nulle de non stationnarité a été rejeté, la série est donc stationnaire. ")
            else:
                print(
                    "L'hypothèse nulle de non stationnarité ne peux pas etre rejeté, la série est donc non "
                    "stationnaire.")
            print('')
    
    def get_stationary_variables(self):
        results = {}

        for col in self.data.columns:
            adf_test = sm.tsa.stattools.adfuller(self.data[col])
            kpss_test = sm.tsa.stattools.kpss(self.data[col])
            pptest = sm.tsa.stattools.adfuller(self.data[col], regression='ct')

            if adf_test[1] < 0.05 or kpss_test[1] < 0.05 or pptest[1] < 0.05:
                results[col] = True
            else:
                results[col] = False

        return results



class BreakPointsDetection:
    """
    A class to detect breakpoints in a given target variable within a pandas DataFrame
    using the ruptures library and plot the results.
    """

    def __init__(self, df:pd.DataFrame, target:str) -> None:
        """
        Initialize the BreakPointsDetection object.

        :param df: A pandas DataFrame containing the data.
        :param target: The target column name in the DataFrame.
        """
        self.df = df
        self.target = target
    
    def detect_breakpoints_and_visualize(self, n_breaks: int = 6) -> None:
        """
        Detect breakpoints in the target variable and plot the data with the detected breakpoints.

        :param n_breaks: The number of breaks to be detected. Defaults to 6.
        """

        # Detect breakpoints using ruptures library
        y = np.array(self.df[self.target].tolist())
        model = rpt.Dynp(model="l1")
        model.fit(y)
        breaks = model.predict(n_bkps=n_breaks-1)

        breaks_rpt = []
        ts = self.df[self.target]
        for i in breaks:
            breaks_rpt.append(ts.index[i-1])
        breaks_rpt = pd.to_datetime(breaks_rpt)

        # Plot data with detected breakpoints
        plt.plot(ts, label='data')
        plt.title('Default rate')
        print_legend = True
        for i in breaks_rpt:
            if print_legend:
                plt.axvline(i, color='red',linestyle='dashed', label='breaks')
                print_legend = False
            else:
                plt.axvline(i, color='red',linestyle='dashed')
        plt.grid()
        plt.legend()
        plt.show()
