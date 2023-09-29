from heifa_composition import FoodComposition

import pandas as pd

def _clean_ingredients_file(ingredients_df: pd.DataFrame) -> pd.DataFrame:

    # For ingredients without size or measure
    filled_values = {
        'serving_size' : 'N/A',
        'serving_measure': 'N/A'
    }

    return ingredients_df.fillna(value = filled_values)

def _rename_columns(name_replacer_dict: dict, df: pd.DataFrame) -> pd.DataFrame:
    
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

    intake24_df = _rename_columns(column_replacer_dict, intake24_df)

    # Filter the columns we only need
    return intake24_df[column_replacer_dict.values()]

def load_heifa_recipes() -> pd.DataFrame:

    heifa_recipes_df = pd.read_csv('files/heifa_recipes.csv')

    # Replace column names
    column_replacer_dict = {
        'Recipe AUSNUT 8-digit code': 'eight_digit_code',
        'Ingredient Nutrient table code': 'heifa_code',
        'Recipe Food Name': 'recipe_name',
        'Proportion of ingredients in the recipe': 'proportion_recipe',
        'Ingredient Food Name': 'ingredient_name',
        'Energy, with dietary fibre (kJ) per 100g': 'energy_with_fibre_100g',
    }

    heifa_recipes_df = _rename_columns(column_replacer_dict, heifa_recipes_df)

    # Filter the columns we only need
    return heifa_recipes_df[column_replacer_dict.values()]

def load_heifa_ingredients() -> pd.DataFrame:

    heifa_food_df = pd.read_csv('files/heifa_food_composition.csv')

    # Replace column names
    column_replacer_dict = {
        'Nutrient table code': 'heifa_code',
        '8 digit code': 'eight_digit_code',
        'HEIFA Food Groups': 'food_group',
        'Energy or grams per Serve \n(HEIFA food groups)': 'serving_size',
        'Serving size unit of measure': 'serving_measure',
    }

    heifa_food_df = _rename_columns(column_replacer_dict, heifa_food_df)

    # Data cleaning
    heifa_food_df = _clean_ingredients_file(heifa_food_df)

    # Filter the columns we only need
    return heifa_food_df[column_replacer_dict.values()]

def create_food_objects(heifa_food_df) -> dict:

    # Store the objects in a dictionary
    # Faster mapping and lookup
    heifa_food_dict = {}

    def populate_food_composition(food_row):

        heifa_code = food_row['heifa_code']
        
        info_dict = {
            'heifa_code': heifa_code,
            'eight_digit_code': food_row['eight_digit_code'],
            'food_group': food_row['food_group'],
            'serving_size': food_row['serving_size'],
            'serving_measure': food_row['serving_measure']
        }

        heifa_food_dict[heifa_code] = FoodComposition(info_dict)

    heifa_food_df.apply(populate_food_composition, axis = 1)

    return heifa_food_dict

def create_recipe_objects(heifa_recipe_df) -> dict:

    # Store the objects in a dictionary
    # Faster mapping and lookup
    heifa_recipe_dict = {}

    # Turn the ingredient row into an object

    # Check if the recipe is in the dictionary
    # Default: Create new recipe
    
    # Store the ingredient inside the recipe object


    return heifa_recipe_dict
    ...