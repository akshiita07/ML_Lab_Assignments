# Akshita 3796
import pandas as pd
import numpy as np

def normalize_matrix(matrix, weights):
    norm_matrix = matrix / np.sqrt((matrix**2).sum(axis=0))
    weighted_matrix = norm_matrix * weights
    return weighted_matrix

def topsis(data_file, weights, impacts):
    try:
        data = pd.read_csv(data_file)
        fund_names = data.iloc[:, 0]
        matrix = data.iloc[:, 1:].values

        if not np.issubdtype(matrix.dtype, np.number):
            raise ValueError("All criteria columns must contain numeric values.")

        weights = np.array([float(w) for w in weights.split(',')])
        impacts = impacts.split(',')

        if len(weights) != matrix.shape[1] or len(impacts) != matrix.shape[1]:
            raise ValueError("Number of weights and impacts must match the number of criteria.")

        if not all(impact in ['+', '-'] for impact in impacts):
            raise ValueError("Impacts must be either '+' or '-'.")

        weighted_matrix = normalize_matrix(matrix, weights)

        ideal_best = np.max(weighted_matrix, axis=0) * (np.array(impacts) == '+') + \
                     np.min(weighted_matrix, axis=0) * (np.array(impacts) == '-')
        ideal_worst = np.min(weighted_matrix, axis=0) * (np.array(impacts) == '+') + \
                      np.max(weighted_matrix, axis=0) * (np.array(impacts) == '-')

        dist_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
        dist_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))

        topsis_score = dist_worst / (dist_best + dist_worst)
        rank = topsis_score.argsort()[::-1] + 1

        result = data.copy()
        result['Topsis Score'] = topsis_score
        result['Rank'] = rank

        return result

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
