import pandas as pd

def rename_columns(name_replacer_dict: dict, df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns = name_replacer_dict)


def load_intake24() -> pd.DataFrame:

    intake24_df = pd.read_csv('files/intake24_survey_file.csv')

    # Replace column names
    column_replacer_dict = {
    'Energy, with dietary fibre': 'energy_with_fibre',
    'Meal name': 'meal_name',
    'Survey ID': 'survey_id',
    'Intake24 food code': 'food_code',
    'User ID': 'user_id',
    'Meal ID': 'meal_id',
    'Nutrient table code': 'heifa_nutrient_id',
    'Portion size (g/ml)': 'portion_size_consumed'
    }

    intake24_df = rename_columns(column_replacer_dict, intake24_df)

    # Filter the columns we only need
    return intake24_df[column_replacer_dict.values()]