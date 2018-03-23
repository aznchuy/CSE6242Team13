import os
import pandas as pd
from constants import cost_directories, prev_directories, state_codes_dict, save_directory


def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = os.listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]


def fix_county_col(row):
    if row['Type'] == 'cost':
        while len(row['County']) < 3:
            row['County'] = '0' + row['County']
        return state_codes_dict[row['State'].strip().upper()] + row['County']
    return row['County']


def set_up_dfs(directory, filename):
    df = pd.read_csv(directory + '/' + filename)

    if 'cost' in filename:
        df.columns = ['State', 'County', 'Cost', 'Count']
        del df['Count']
        df['Type'] = 'cost'
        df['Disease'] = filename.split('_')[0]
    else:
        df.columns = ['State', 'County', 'Prevalence', 'Children_with_Disease']
        df['Type'] = 'prevalence'
        df['Disease'] = filename.split('Prevalence')[0]

    df['Year'] = directory.split(' - ')[1]
    df['County'] = df['County'].astype(str)
    df['County'] = df.apply(fix_county_col, axis=1)

    del df['Type']
    return df


def combine_all_files(current_directory):
    df_list = []
    for directory in current_directory:
        files = find_csv_filenames(directory)
        for filename in files:
            df_list.append(set_up_dfs(directory, filename))
    return pd.concat(df_list)


def main():
    cost_df = combine_all_files(cost_directories)
    prev_df = combine_all_files(prev_directories)

    join_cols = ['State', 'County', 'Disease', 'Year']
    final_df = cost_df.merge(prev_df, how='left', on=join_cols)
    final_df = final_df.fillna(0).sort_values('Cost', ascending=False)\
        .drop_duplicates(['State', 'County', 'Disease', 'Year'], keep='first')
    final_df.fillna(0).to_csv(os.path.join(save_directory, 'regression_input.csv'), index=False)


if __name__ == '__main__':
    main()
