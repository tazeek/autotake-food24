from heifa_composition import FoodComposition, IngredientInRecipe, RecipeComposition

from daily_calculator import DailyCalculator
from User import User

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

async def load_intake24() -> pd.DataFrame:

    intake24_df = pd.read_csv('files/intake24_survey_file.csv')

    # Replace column names
    column_replacer_dict = {
        'Start time': 'information_date',
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

    # Column conversion
    intake24_df['information_date'] = pd.to_datetime(intake24_df['information_date']).dt.strftime('%Y-%m-%d')

    # Some of the IDs are not present, so we drop them
    print(f"Before dropping function: {len(intake24_df)} rows")
    intake24_df = intake24_df[intake24_df['heifa_nutrient_id'].notna()]
    print(f"After dropping function: {len(intake24_df)} rows")

    # Filter the columns we only need
    return intake24_df[column_replacer_dict.values()]

async def load_heifa_recipes() -> pd.DataFrame:

    heifa_recipes_df = pd.read_csv('files/heifa_recipes.csv')

    # Replace column names
    column_replacer_dict = {
        'Recipe AUSNUT 8-digit code': 'eight_digit_code',
        'Ingredient Nutrient table code': 'heifa_code',
        'Recipe Food Name': 'recipe_name',
        'Proportion of ingredients in the recipe': 'proportion',
        'Ingredient Food Name': 'ingredient_name',
        'Energy, with dietary fibre (kJ) per 100g': 'energy_fibre_100g',
    }

    heifa_recipes_df = _rename_columns(column_replacer_dict, heifa_recipes_df)

    # Filter the columns we only need
    return heifa_recipes_df[column_replacer_dict.values()]

async def load_heifa_ingredients() -> pd.DataFrame:

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

async def load_heifa_scores():

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

def create_user_objects(intake24_df: pd.DataFrame) -> dict:

    user_dict = {}

    # Go row by row
    def populate_user_information(intake24_row):

        # Fetch the User
        user_id = intake24_row['user_id']
        user_obj = user_dict.get(user_id, User(user_id))

        # Fetch the survey, regardless if it is same or not
        survey_obj = user_obj.get_survey(
            intake24_row['survey_id'], intake24_row['information_date']
        )

        # Fetch the meal, regardless if it is the same or not
        meal_obj = survey_obj.get_meal(intake24_row['meal_id'])

        # Update the meal object with the new row
        meal_obj.heifa_list = intake24_row['heifa_nutrient_id']
        meal_obj.meal_name = intake24_row['meal_name']

        meal_obj.nutrition = intake24_row

        # Just in case: for new user objects
        user_dict[user_id] = user_obj
    
    intake24_df.apply(populate_user_information, axis = 1)

    return user_dict

def create_food_objects(heifa_food_df: pd.DataFrame) -> dict:

    # Store the objects in a dictionary
    # Faster mapping and lookup
    heifa_food_dict = {}

    def populate_food_composition(food_row):

        heifa_food_dict[food_row['heifa_code']] = FoodComposition(food_row)

    heifa_food_df.apply(populate_food_composition, axis = 1)

    return heifa_food_dict

def create_recipe_objects(heifa_recipe_df: pd.DataFrame) -> dict:

    # Store the objects in a dictionary
    # Faster mapping and lookup
    heifa_recipe_dict = {}

    # Turn the ingredient row into an object
    def populate_ingredients_composition(ingredient_row):

        ingredient_obj = IngredientInRecipe(ingredient_row)

        # Check if the recipe is in the dictionary
        # Default: Create new recipe if not in dictionary
        recipe_id = ingredient_row['eight_digit_code']
        recipe_obj = heifa_recipe_dict.get(recipe_id, RecipeComposition(ingredient_row))

        # Store the ingredient inside the recipe object
        recipe_obj.recipe_pieces = { ingredient_row['heifa_code']: ingredient_obj }

        # Just in case: for new recipe objects
        heifa_recipe_dict[recipe_id] = recipe_obj

    heifa_recipe_df.apply(populate_ingredients_composition, axis = 1)

    return heifa_recipe_dict


def calculate_user_servings(user_dict, food_composition_dict, recipe_dict):

    # First, we get all the meals (broken down by the date)
    user_meals = {
        user_id : user_obj.get_meals_information()
        for user_id, user_obj in user_dict.items()
    }

    daily_calculator = DailyCalculator(food_composition_dict, recipe_dict)

    # We calculate each serving on a daily basis and return
    return {
        user_id: daily_calculator.calculate_daily_servings(meal_date_dict)
        for user_id, meal_date_dict in user_meals.items()
    }