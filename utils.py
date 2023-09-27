import pandas as pd

def rename_columns(name_replacer_dict: dict, df: pd.DataFrame):
    return df.rename(columns = name_replacer_dict)