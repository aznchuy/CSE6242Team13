import os
import pandas as pd
import combine_csvs
from sklearn import model_selection, linear_model, metrics, preprocessing
from constants import save_directory


def add_next_year_data(df, prediction_year):
    prediction_df = df[df['Year'] == prediction_year - 1].copy()
    prediction_df['Year'] = prediction_year
    unscaled_df = prediction_df.copy()
    return df.append(prediction_df), unscaled_df


def make_prediction(model, df, unscaled_df):
    predictions = model.predict(df)
    pred_series = pd.Series(predictions)
    unscaled_df.reset_index(drop=True, inplace=True)
    unscaled_df['Predicted Cost'] = pred_series * 600

    def force_zero_if_no_prevalence(row):
        if row['Prevalence'] == 0:
            return 0
        else:
            return row['Predicted Cost']
    unscaled_df['Predicted Cost'] = unscaled_df.apply(force_zero_if_no_prevalence, axis=1)
    return unscaled_df


def main():
    combine_csvs.main()

    df = pd.read_csv(os.path.join(save_directory, 'regression_input.csv'))
    prediction_year = df['Year'].max() + 1
    df, unscaled_df = add_next_year_data(df, prediction_year)
    df = pd.get_dummies(df)

    prediction_df = df[df['Year'] == prediction_year]  # want everything to be scaled te same to predict
    df = df[(df['Year'] != prediction_year)
            & (df['Cost'] != 0)
            & (df['Prevalence'] != 0)
            & (df['Children_with_Disease'] != 0)]
    cols = df.columns.values.tolist()
    cols.remove('County')

    scaler = preprocessing.MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df[cols]), columns=cols)
    cols.remove('Cost')

    X = df_scaled[cols].values.tolist()
    y = df_scaled['Cost'].tolist()

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, random_state=0)
    linear_regression = linear_model.LinearRegression()
    linear_regression.fit(X_train, y_train)
    print("MSE: {0}".format(metrics.mean_squared_error(y_test, linear_regression.predict(X_test))))
    print("R^2: {:.2f}\n".format(linear_regression.score(X_test, y_test)))

    coefficients = list(linear_regression.coef_)

    for index in range(0, len(cols)):
        if cols[index] in ['Year', 'Prevalence', 'Children_with_Disease']:
            print('{0}: {1}'.format(cols[index], coefficients[index]))

    final_df = make_prediction(linear_regression, prediction_df[cols], unscaled_df)
    final_df.to_csv(os.path.join(save_directory, 'regression_predictions.csv'), index=False)


if __name__ == '__main__':
    main()
