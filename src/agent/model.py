def run_imputation(df: pd.DataFrame):

    def fill_value(df, c, value):
        if c in df.columns:
            df[c].fillna(value, inplace=True)

    def fill_mode(df, c):
        if c in df.columns:
            df[c].fillna(df[c].mode()[0], inplace=True)

    def fill_mean_per_group(df, c, group_c):
        df[c] = df.groupby(group_c).transform(lambda x: x.fillna(x.mean()))


    fill_value(df, 'floor', 0)
    fill_value(df, 'basement_size', 0)
    fill_value(df, 'lot_size', 0)
    fill_mode(df, 'energy_class')
    fill_mean_per_group(df, 'exp', 'energy_class')
    fill_mean_per_group(df, 'net', 'energy_class')
    return df
