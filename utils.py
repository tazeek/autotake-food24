from heifa_composition import FoodComposition, IngredientInRecipe, RecipeComposition

from Intake import Intake
from Food import Food
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

def _breakdown_recipe_calculation(eight_digit_code, heifa_ing, heifa_rec, portion_size):

    # Get the original list of ingredients

    original_pieces = heifa_rec[eight_digit_code].recipe_pieces

    # Time to break down further
    while True:

        # Some of the ingredients in recipes, can be recipes themselves
        extra_recipes = {
            heifa_id: ingredient_obj for (heifa_id , ingredient_obj) in original_pieces.items() 
            if heifa_ing[heifa_id].is_recipe
        }

        # If nothing found, we break out
        if len(extra_recipes) == 0:
            break

        # Lets break down the extra pieces
        for nutrient_code in extra_recipes.keys():
            
            # Get the eight digit code
            eight_digit_code = heifa_ing[nutrient_code].eight_digit_code
            
            # Update the original list
            original_pieces.update(heifa_rec[eight_digit_code].recipe_pieces)

            # Delete the one from the original list
            del original_pieces[nutrient_code]

        # Repeat until no more

    # Calculate the whole recipe individually
    for heifa_id, piece_obj in original_pieces.items():

        piece_amount = round(portion_size * piece_obj.proroption, 1)
        piece_energy = round((piece_amount * piece_obj.energy_with_fibre) / 100, 1)

        heifa_obj = heifa_ing[heifa_id]
        serving_size = heifa_obj.calculate_serving_size(piece_energy, portion_size)

        print(f"Portion amount for {heifa_id}: {piece_amount:.1f}g")
        print(f"Energy amount for {heifa_id} (based on {piece_amount}g): {piece_energy:.1f}kJ")
        print(f"Serving size for {heifa_id} (based on {piece_amount}g): {serving_size:.1f} serves\n")
    
    return None

def _find_portion_serving(nutrition_list, heifa_ing, heifa_dict):

    print(list(nutrition_list.keys()))

    # One ingredient at a time
    for heifa_id, ingredient_obj in nutrition_list.items():

        # Just in case....
        if heifa_id not in heifa_ing:
            print(f"\nHEIFA ID {heifa_id} not found")
            continue

        portion_size = ingredient_obj.portion_size
        energy_with_fibre = ingredient_obj.energy_with_fibre
        
        print("\n")
        print(f"HEIFA ID: {heifa_id}\n")
        heifa_obj = heifa_ing[heifa_id]

        print(f"Portion size (gram): {portion_size}g")
        print(f"Portion size (energy with fibre): {energy_with_fibre}kJ")
        print(f"Food group: {heifa_obj.food_group}\n")
        
        print(f"HEIFA Serving size: {heifa_obj.serving_size}")
        print(f"HEIFA Serving measure: {heifa_obj.serving_measure}\n")

        # Seperate calculation for recipes
        if heifa_obj.is_recipe:
            _breakdown_recipe_calculation(heifa_obj.eight_digit_code, heifa_ing, heifa_dict, portion_size)
            continue

        # Calculate for non-recipes directly
        serving_size = heifa_obj.calculate_serving_size(energy_with_fibre, portion_size)
        print(f"Serving size: {serving_size} serves \n")

    return None


async def load_intake24() -> pd.DataFrame:

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
        'Proportion of ingredients in the recipe': 'proportion_recipe',
        'Ingredient Food Name': 'ingredient_name',
        'Energy, with dietary fibre (kJ) per 100g': 'energy_with_fibre_100g',
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

def create_user_objects(intake24_df: pd.DataFrame) -> dict:

    user_dict = {}

    # Go row by row
    def populate_user_information(intake24_row):

        # Fetch the User
        user_id = intake24_row['user_id']
        user_obj = user_dict.get(user_id, User(user_id))

        # Fetch the survey, regardless if it is same or not
        survey_obj = user_obj.get_survey(intake24_row['survey_id'])

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

def create_recipe_objects(heifa_recipe_df: pd.DataFrame) -> dict:

    # Store the objects in a dictionary
    # Faster mapping and lookup
    heifa_recipe_dict = {}

    # Turn the ingredient row into an object
    def populate_ingredients_composition(ingredient_row):

        info_dict = {
            'proportion': ingredient_row['proportion_recipe'],
            'ingredient_name': ingredient_row['ingredient_name'],
            'energy_fibre_100g': ingredient_row['energy_with_fibre_100g']
        }

        ingredient_obj = IngredientInRecipe(info_dict)

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


def fetch_user_food_list(user_dict):

    user_meals = {}

    for id, user_obj in user_dict.items():

        user_meals[id] = user_obj.get_meals_information()

    return user_meals

def calculate_portion_serving_heifa(foods_list, heifa_ing_dict, heifa_recipe_dict):

    # Go one by one
    for nutrition_list in foods_list:

        _find_portion_serving(nutrition_list, heifa_ing_dict, heifa_recipe_dict)
        print("=" * 20)
        print("\n\n")

    # Hold for the return type until everything is done properly
    # Discuss with Tracy, Heidi, Samara

    return None