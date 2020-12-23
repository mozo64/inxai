from sklearn.base import TransformerMixin, BaseEstimator
import numpy as np


class NormalNoisePerturber(TransformerMixin, BaseEstimator):
    def __init__(self, loc=0, scale=1, importances = None):
        self.loc = loc
        self.scale = scale
        self.importances = importances
        self.colnames = None

    def set_importances(self, importances):
        self.importances = importances
        print(importances)

    def fit(self, X):
        self.colnames = X.columns
        return self

    def transform(self, X):
        return X.apply(lambda x: x + self.importances * np.random.normal(self.loc, self.scale), axis=1)

    def get_feature_names(self):
        return self.colnames


class CategoricalNoisePerturber(TransformerMixin, BaseEstimator):
    def __init__(self, probability_multiplier=1, importances = None):
        self.probability_multiplier = probability_multiplier
        self.importances = importances

    def set_importances(self, importances):
        self.importances = importances

    def fit(self, X):
        return self

    def transform(self, X):
        for col_idx, column in enumerate(X):
            unique_elements = X[column].unique()
            for row in X[column].iteritems():
                if np.random.random() < self.probability_multiplier * self.importances[col_idx]:
                    X.loc[row[0], column] = np.random.choice(unique_elements)
        return X