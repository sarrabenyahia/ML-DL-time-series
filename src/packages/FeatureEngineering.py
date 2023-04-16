import numpy as np
import pandas as pd

def downcast(df):
    """
    Downcast in order to save memory
    """
    cols = df.dtypes.index.tolist()
    types = df.dtypes.values.tolist()
    for i,t in enumerate(types):
        # Integer
        if 'int' in str(t):
            # Check if minimum and maximum are in the limit of int8
            if df[cols[i]].min() > np.iinfo(np.int8).min and df[cols[i]].max() < np.iinfo(np.int8).max:
                df[cols[i]] = df[cols[i]].astype(np.int8)
            # Check if minimum and maximum are in the limit of int16
            elif df[cols[i]].min() > np.iinfo(np.int16).min and df[cols[i]].max() < np.iinfo(np.int16).max:
                df[cols[i]] = df[cols[i]].astype(np.int16)
            # Check if minimum and maximum are in the limit of int32
            elif df[cols[i]].min() > np.iinfo(np.int32).min and df[cols[i]].max() < np.iinfo(np.int32).max:
                df[cols[i]] = df[cols[i]].astype(np.int32)
            # Choose int64
            else:
                df[cols[i]] = df[cols[i]].astype(np.int64)
        # Float
        elif 'float' in str(t):
            if df[cols[i]].min() > np.finfo(np.float16).min and df[cols[i]].max() < np.finfo(np.float16).max:
                df[cols[i]] = df[cols[i]].astype(np.float16)
            elif df[cols[i]].min() > np.finfo(np.float32).min and df[cols[i]].max() < np.finfo(np.float32).max:
                df[cols[i]] = df[cols[i]].astype(np.float32)
            else:
                df[cols[i]] = df[cols[i]].astype(np.float64)
        # Object
        elif t == object:
            if cols[i] == 'date':
                df[cols[i]] = pd.to_datetime(df[cols[i]], format='%Y-%m-%d')
            else:
                df[cols[i]] = df[cols[i]].astype('category')
    return df  

def lag_creation(df, lag, time="day"):
    if isinstance(lag, int):
        lag = [lag]
    if time == "day":
        lag_min = [l*60*24 for l in lag]
    elif time == "hour":
        lag_min = [l*60 for l in lag]
    elif time == "minute":
        lag_min = lag
    else:
        raise ValueError("Invalid time value. Please use 'day', 'hour' or 'minute.")
    
    new_cols = []
    for col in df.columns:
        for index, l in enumerate(lag_min):
            new_col = df[col].shift(l)
            new_col.name = f"{col}_lag{lag[index]}{time[0]}"
            new_cols.append(new_col)

    return pd.concat([df] + new_cols, axis=1)
