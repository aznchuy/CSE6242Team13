import os
import pandas as pd
import combine_csvs
from sklearn import model_selection, linear_model, metrics
from constants import save_directory


def set_up_prediction(df, prediction_year):
    prediction_df = df[df['Year'] == prediction_year - 1].copy()
    prediction_df['Year'] = prediction_year
    return prediction_df


def make_prediction(model, df, cols):
    df['Children_with_Disease'] = df['Children_with_Disease'] * 1.007
    predictions = model.predict(df[cols])
    pred_series = pd.Series(predictions)
    df.reset_index(drop=True, inplace=True)
    df['Predicted Cost'] = pred_series

    def force_zero_if_no_prevalence(row):
        if row['Prevalence'] == 0:
            return 0
        else:
            return row['Predicted Cost']
    df['Predicted Cost'] = df.apply(force_zero_if_no_prevalence, axis=1)
    return df


def main():
    combine_csvs.main()

    cols = ['Year', 'Prevalence', 'Children_with_Disease']
    df = pd.read_csv(os.path.join(save_directory, 'regression_input.csv'))
    prediction_year = df['Year'].max() + 1
    prediction_df = set_up_prediction(df, prediction_year)

    df = df[(df['Cost'] != 0)
            & (df['Prevalence'] != 0)
            & (df['Children_with_Disease'] != 0)]

    X = df[cols].values.tolist()
    y = df['Cost'].tolist()

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, random_state=0, test_size=0.33)
    linear_regression = linear_model.LinearRegression()
    linear_regression.fit(X_train, y_train)
    print("MAE: {0}".format(metrics.mean_absolute_error(y_test, linear_regression.predict(X_test))))
    print("R^2: {:.2f}\n".format(linear_regression.score(X_test, y_test)))

    regression_equation = '{0}'.format(linear_regression.intercept_)
    coefficients = list(linear_regression.coef_)
    for index in range(0, len(cols)):
        regression_equation = regression_equation + ' + {0} * {1}'.format(coefficients[index], cols[index])
    print('Regression Equation: {0}'.format(regression_equation))

    final_df = make_prediction(linear_regression, prediction_df, cols)
    final_df.to_csv(os.path.join(save_directory, 'regression_predictions.csv'), index=False)
    final_df['cost_diff'] = final_df['Predicted Cost'] - final_df['Cost']
    percent_diff = final_df['cost_diff'].sum() * 100.0 / final_df['Cost'].sum()
    print('Avg. Percent Difference in Predicted Cost from Previous Year Cost: {0}%\n'.format(round(percent_diff, 1)))

    print('Finished. File wrote to directory: {0}'.format(os.path.join(save_directory, 'regression_predictions.csv')))


if __name__ == '__main__':
    main()
