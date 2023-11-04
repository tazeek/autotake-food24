import pandas as pd

def _clean_ingredients_file(ingredients_df: pd.DataFrame) -> pd.DataFrame:

    # For ingredients with missing values
    filled_values = {
        'serving_size' : 'N/A',
        'serving_measure': 'N/A',
        'is_beverage': 0
    }

    replaced_columns = list(filled_values.keys())

    # Replace specific columns
    ingredients_df[replaced_columns] = \
        ingredients_df[replaced_columns].fillna(value = filled_values)

    return ingredients_df

def _rename_columns(name_replacer_dict: dict, dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.rename(columns = name_replacer_dict)

def load_intake24(intake24_df = None) -> pd.DataFrame:

    if intake24_df is None:
        intake24_df = pd.read_csv('files/intake24_survey_file.csv')

    # Remove whitespaces in columns
    intake24_df.rename(columns=lambda x: x.strip(), inplace=True)

    # Replace column names
    column_replacer_dict = {
        'Energy, with dietary fibre': 'energy_with_fibre',
        'Meal name': 'meal_name',
        'Survey ID': 'survey_id',
        'User ID': 'user_id',
        'Meal ID': 'meal_id',
        'Nutrient table code': 'heifa_nutrient_id',
        'Portion size (g/ml)': 'portion_size_consumed',
        'Sodium': 'sodium_consumed',
        'Alcohol': 'alcohol_consumed',
        'Total sugars': 'sugar_amount',
        'Satd FA': 'saturated_fat_amount',
        'Monounsaturated fatty acids (g)': 'unsaturated_fat_mono_amount',
        'Polyunsaturated fatty acids (g)': 'unsaturated_fat_poly_amount'
    }

    intake24_df = _rename_columns(column_replacer_dict, intake24_df)

    # Some of the IDs are not present, so we drop them
    print(f"Before dropping function: {len(intake24_df)} rows")
    intake24_df = intake24_df[intake24_df['heifa_nutrient_id'].notna()]
    intake24_df = intake24_df[intake24_df['portion_size_consumed'].notna()]
    print(f"After dropping function: {len(intake24_df)} rows")

    # Filter the columns we only need
    return intake24_df[column_replacer_dict.values()]

def load_latrobe_file(latrobe_df = None) -> pd.DataFrame:

    if latrobe_df is None:
        latrobe_df = pd.read_csv('files/latrobe_cleaned_further.csv')

    # Replace column names
    column_replacer_dict = {
        'Energy, with dietary fibre': 'energy_with_fibre',
        'Survey ID': 'survey_id',
        'User ID': 'user_id',
        'Meal ID': 'meal_id',
        'Nutrient table code': 'heifa_nutrient_id',
        'Sodium ': 'sodium_consumed',
        'Alcohol ': 'alcohol_consumed',
        'Portion size (g/ml)': 'portion_size_consumed',
        'Total sugars': 'sugar_amount',
        'Satd FA': 'saturated_fat_amount',
        'Monounsaturated fatty acids (g)': 'unsaturated_fat_mono_amount',
        'Polyunsaturated fatty acids (g)': 'unsaturated_fat_poly_amount'
    }

    latrobe_df = _rename_columns(column_replacer_dict, latrobe_df)

    # Some of the IDs and portion sizes are not present, so we drop them
    print(f"Before dropping function: {len(latrobe_df)} rows")
    latrobe_df = latrobe_df[latrobe_df['heifa_nutrient_id'].notna()]
    latrobe_df = latrobe_df[latrobe_df['portion_size_consumed'].notna()]
    print(f"After dropping function: {len(latrobe_df)} rows")

    # Filter the columns we only need
    return latrobe_df[column_replacer_dict.values()]

def load_heifa_recipes(heifa_recipes_df = None) -> pd.DataFrame:

    if heifa_recipes_df is None:
        heifa_recipes_df = pd.read_csv('files/heifa_recipes.csv')

    # Replace column names
    column_replacer_dict = {
        'Recipe AUSNUT 8-digit code': 'eight_digit_code',
        'Ingredient Nutrient table code': 'heifa_code',
        'Proportion of ingredients in the recipe': 'proportion',
        'Energy, with dietary fibre (kJ) per 100g': 'energy_fibre_100g',
    }

    heifa_recipes_df = _rename_columns(column_replacer_dict, heifa_recipes_df)

    # Filter the columns we only need
    return heifa_recipes_df[column_replacer_dict.values()]

def load_heifa_ingredients(heifa_food_df = None) -> pd.DataFrame:

    if heifa_food_df is None:
        heifa_food_df = pd.read_csv('files/heifa_food_composition.csv')

    # Replace column names
    column_replacer_dict = {
        'Nutrient table code': 'heifa_code',
        '8 digit code': 'eight_digit_code',
        'HEIFA-2013 Food Group': 'food_group',
        'Energy or grams per Serve \n(HEIFA food groups)': 'serving_size',
        'Serving size unit of measure': 'serving_measure',
        'Non-alcoholic beverage Flag\n(1=Non-alcoholic beverage)': 'is_beverage'
    }

    heifa_food_df = _rename_columns(column_replacer_dict, heifa_food_df)

    # Data cleaning
    heifa_food_df = _clean_ingredients_file(heifa_food_df)

    # Filter the columns we only need
    return heifa_food_df[column_replacer_dict.values()]

def load_heifa_scores(heifa_scores_df = None):

    if heifa_scores_df is None:
        heifa_scores_df = pd.read_csv('files/heifa_scores.csv')

    # Replace column names
    column_replacer_dict = {
        'Food group': 'food_group',
        'Minimum serves per day (Male)': 'minimum_serves_male',
        'Maximum serves per day (Male)': 'maximum_serves_male',
        'Minimum serves per day (Female)': 'minimum_serves_female',
        'Maximum serves per day (Female)': 'maximum_serves_female',
        'HEIFA Score': 'heifa_score',
    }

    heifa_scores_df = _rename_columns(column_replacer_dict, heifa_scores_df)

    # Replace "Fruits" with "Fruit" for consistent mapping
    heifa_scores_df['food_group'].mask(
        heifa_scores_df['food_group'] == 'Fruits', 'Fruit', inplace=True
    )

    # Fill empty cell with INF
    heifa_scores_df.fillna(value=float('inf'), inplace=True)

    return heifa_scores_df