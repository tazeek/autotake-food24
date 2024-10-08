import pandas as pd

from classes.heifa_composition import *
from convertors.score_convertor import ScoreConvertor
from convertors.daily_calculator import DailyCalculator
from heifa_file_writer import HeifaFileWriter

from classes.User import User

def _column_reorder_recall_file(dataframe):

    # Order: Female, Male, None
    fixed_cols = ["User_ID", "Survey_ID"]
    female_cols = []
    male_cols = []
    neutral_cols = []

    for column in dataframe.columns:

        # We ignore the fixed columns
        if column in fixed_cols:
            continue

        temp_col = column.lower()

        if 'female' in temp_col:
            female_cols.append(column)
            continue

        if 'male' in temp_col:
            male_cols.append(column)
            continue
        
        neutral_cols.append(column)

    ordered_cols = fixed_cols + female_cols + male_cols + neutral_cols

    return dataframe[ordered_cols]

def get_file_google(file_link):
    return 'https://drive.google.com/uc?id=' + file_link.split('/')[-2]

def create_user_objects(intake24_df: pd.DataFrame) -> dict:

    user_dict = {}

    # Go row by row
    def populate_user_information(intake24_row):

        # Fetch the User
        user_id = intake24_row['user_id']
        user_obj = user_dict.get(user_id, User(user_id))

        # Fetch the survey, regardless if it is same or not
        survey_obj = user_obj.get_survey(
            intake24_row['survey_id']
        )

        # Fetch the meal, regardless if it is the same or not
        meal_obj = survey_obj.get_meal(intake24_row['meal_id'])

        # Update the meal object with the new row
        meal_obj.heifa_list = intake24_row['heifa_nutrient_id']

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


def calculate_user_servings(*args) -> dict:

    user_dict, food_composition_dict, recipe_dict = args

    # First, we get all the meals (broken down by the date)
    user_meals = {
        user_id : user_obj.get_meals_information()
        for user_id, user_obj in user_dict.items()
    }

    # Create the calculator object and fetch the missing IDs
    daily_calculator = DailyCalculator(food_composition_dict, recipe_dict)
    missing_ids_list = daily_calculator.missing_nutrition_ids

    # We calculate each serving on a daily basis and return
    return missing_ids_list, {
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

def create_heifa_csv(scores_dict, composition_dict, 
    daily_intake, user_scores, file_name = None):

    writer_obj = HeifaFileWriter(scores_dict, composition_dict)

    column_names, rows_data = writer_obj.create_row_data(
        daily_intake, user_scores
    )

    # Create DF and fill up the None values
    transformed_df = pd.DataFrame(rows_data, columns=column_names)
    transformed_df.fillna(0.00, inplace=True)

    # This is if you want to generate in-line, without the streamlit app
    if file_name is not None:
        transformed_df.to_csv(f'{file_name}.csv', sep=",", index=False)

    # Return after re-order the columns: Female, Male, Neither
    return _column_reorder_recall_file(transformed_df)
