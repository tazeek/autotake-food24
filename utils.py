import pandas as pd

from heifa_composition import *
from score_convertor import ScoreConvertor
from daily_calculator import DailyCalculator
from heifa_file_writer import HeifaFileWriter

from User import User

def _clean_ingredients_file(ingredients_df: pd.DataFrame) -> pd.DataFrame:

    # For ingredients without size or measure
    filled_values = {
        'serving_size' : 'N/A',
        'serving_measure': 'N/A'
    }

    return ingredients_df.fillna(value = filled_values)

def _rename_columns(name_replacer_dict: dict, dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.rename(columns = name_replacer_dict)

async def load_intake24() -> pd.DataFrame:

    intake24_df = pd.read_csv('files/intake24_survey_file.csv')

    # Replace column names
    column_replacer_dict = {
        'Start time': 'information_date',
        'Energy, with dietary fibre': 'energy_with_fibre',
        'Meal name': 'meal_name',
        'Survey ID': 'survey_id',
        'User ID': 'user_id',
        'Meal ID': 'meal_id',
        'Nutrient table code': 'heifa_nutrient_id',
        'Portion size (g/ml)': 'portion_size_consumed'
    }

    intake24_df = _rename_columns(column_replacer_dict, intake24_df)

    # Some of the IDs are not present, so we drop them
    print(f"Before dropping function: {len(intake24_df)} rows")
    intake24_df = intake24_df[intake24_df['heifa_nutrient_id'].notna()]
    print(f"After dropping function: {len(intake24_df)} rows")

    # Filter the columns we only need
    return intake24_df[column_replacer_dict.values()]

def load_latrobe_file() -> pd.DataFrame:

    latrobe_df = pd.read_csv('files/latrobe_cleaned_further.csv')

    # Replace column names
    column_replacer_dict = {
        'Start date (AEST)': 'information_date',
        'Energy, with dietary fibre': 'energy_with_fibre',
        'Meal name': 'meal_name',
        'Survey ID': 'survey_id',
        'User ID': 'user_id',
        'Meal ID': 'meal_id',
        'Nutrient table code': 'heifa_nutrient_id',
        'Portion size (g/ml)': 'portion_size_consumed'
    }

    latrobe_df = _rename_columns(column_replacer_dict, latrobe_df)

    # Some of the IDs and portion sizes are not present, so we drop them
    print(f"Before dropping function: {len(latrobe_df)} rows")
    latrobe_df = latrobe_df[latrobe_df['heifa_nutrient_id'].notna()]
    latrobe_df = latrobe_df[latrobe_df['portion_size_consumed'].notna()]
    print(f"After dropping function: {len(latrobe_df)} rows")

    # Filter the columns we only need
    return latrobe_df[column_replacer_dict.values()]


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

def create_scores_objects(heifa_scores_df: pd.DataFrame) -> dict:

    heifa_scores_dict = {}

    def create_scores_object(scores_row):

        # Get the main attributes
        scores_dictionary = {
            'minimum_serves_male': scores_row['minimum_serves_male'],
            'maximum_serves_male': scores_row['maximum_serves_male'],
            'minimum_serves_female': scores_row['minimum_serves_female'],
            'maximum_serves_female': scores_row['maximum_serves_female'],
            'heifa_score': scores_row['heifa_score'],
        }

        food_group_list = heifa_scores_dict.get(scores_row['food_group'], [])
        food_group_list.append(scores_dictionary)
        heifa_scores_dict[scores_row['food_group']] = food_group_list

    heifa_scores_df.apply(create_scores_object, axis=1)
    return heifa_scores_dict


def calculate_user_servings(
        user_dict: dict, food_composition_dict: dict, recipe_dict: dict
    ) -> dict:

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

def calculate_heifa_scores(heifa_scores_dict: dict, user_dict: dict) -> dict:

    score_obj = ScoreConvertor(heifa_scores_dict)
    user_heifa_scores = {}

    for user_id, daily_intake_dict in user_dict.items():

        daily_servings = {
            survey_id: { 
                'total': food_group_dict['total'], 
                'variations': food_group_dict['variations']
            }
            for survey_id, food_group_dict in daily_intake_dict.items()
        }

        # Get the scores
        user_heifa_scores[user_id] = \
            score_obj.transform_servings_score(daily_servings)

    return user_heifa_scores

def create_heifa_csv(scores_dict, composition_dict, daily_intake, user_scores):

    writer_obj = HeifaFileWriter(scores_dict, composition_dict)

    rows_data = writer_obj.create_row_data(daily_intake, user_scores)

    return rows_data
