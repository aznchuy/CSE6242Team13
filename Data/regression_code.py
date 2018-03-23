import os
import pandas as pd
import statsmodels.formula.api as sm
import combine_csvs
from constants import save_directory


def make_prediction(model, df):
    predictions = model.predict(df)
    print(predictions[0:5])  # Can do this to predict multiple rows at once --> can just predict all at once? Write Script to upload new files to github and run this first?
    return predictions


def main():
    combine_csvs.main()

    df = pd.read_csv(os.path.join(save_directory, 'regression_input.csv'))
    linar_reg = sm.ols(formula="Cost ~ State + County + Disease + Year + Prevalence + Children_with_Disease",
                       data=df).fit()
    print(linar_reg.params)
    print()
    print(linar_reg.summary())


if __name__ == '__main__':
    main()
