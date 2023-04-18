import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def filter_correlated_variables(df, target, corr_measure="pearson", min_corr=0, max_corr=1, max_var_corr=0.7):
    # Calculate correlations with the target variable
    corr_matrix = df.corr(corr_measure)
    target_corrs = corr_matrix[target].abs()

    # Filter variables based on min and max correlation with the target variable
    filtered_vars = target_corrs[(target_corrs >= min_corr) & (target_corrs <= max_corr)].index
    if target in filtered_vars:
        filtered_vars = filtered_vars.drop(target)

    # Check correlations between filtered variables
    filtered_vars_corr = df[filtered_vars].corr(corr_measure).abs()
    
    # Find highly correlated pairs of variables and discard the one with lower correlation to the target variable
    dropped_vars = set()
    for i in range(len(filtered_vars_corr)):
        for j in range(i + 1, len(filtered_vars_corr)):
            if filtered_vars_corr.iloc[i, j] > max_var_corr:
                var_i = filtered_vars[i]
                var_j = filtered_vars[j]

                if var_i in dropped_vars or var_j in dropped_vars:
                    continue

                if target_corrs[var_i] >= target_corrs[var_j]:
                    dropped_vars.add(var_j)
                else:
                    dropped_vars.add(var_i)

    # Plot correlations with the target variable
    selected_vars = list(set(filtered_vars) - dropped_vars)
    target_corrs = target_corrs[selected_vars]
    target_corrs.sort_values(ascending=False, inplace=True)
    
    plt.figure(figsize=(10, 5))
    sns.barplot(x=target_corrs.index, y=target_corrs)
    plt.xlabel('Features')
    plt.ylabel(f'{corr_measure.capitalize()} correlation')
    plt.title(f'{corr_measure.capitalize()} correlation between {target} and selected features')
    plt.xticks(rotation=90)
    plt.show()

    # Return filtered variables
    return selected_vars

