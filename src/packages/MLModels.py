import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

class MoyenneNaive:
    def __init__(self, X, y) -> None:
        self.X = X
        self.y = y

    def predict(self, num_hours):
        last_24_hours_mean = np.mean(self.y[-num_hours:])
        self.y_pred_mean = np.ones(self.X.shape[0]) * last_24_hours_mean
        self.y_pred_seas = self.y[-self.X.shape[0]:]
    
    def metrics(self):
        mse_seas = mean_squared_error(self.y, self.y_pred_seas)
        mse_mean = mean_squared_error(self.y, self.y_pred_mean)
        print(f"MSE benchmark naïf saisonnier = {mse_seas:.2f}")
        print(f"MSE benchmark naïf moyen = {mse_mean:.2f}")