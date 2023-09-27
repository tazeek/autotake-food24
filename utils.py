import pandas as pd

def _rename_columns(name_replacer_dict: dict, df: pd.DataFrame) -> None:
    return df.rename(columns = name_replacer_dict, inplace=True)