from file_loaders import *
from utils import *
from datetime import datetime

import streamlit as st
import pandas as pd

def _dataframe_transformer(function_loader):
    return {
        'intake24': load_intake24,
        'food_compo': load_heifa_ingredients,
        'recipe': load_heifa_recipes,
        'heifa_scores': load_heifa_scores,
    }[function_loader]

@st.cache_data
def convert_df(df):
    return df.to_csv(sep=",", index=False).encode('utf-8')

def get_file_name():

    # Get the current date and time
    datetime_obj = datetime.now()
    
    date = datetime_obj.strftime("%Y_%m_%d")
    time = datetime_obj.strftime("%H-%M")

    return f"HEIFA Scores {date} - {time}.csv"

@st.cache_data(ttl="1d", max_entries=100)
def convert_file_csv(possible_file, function_loader) -> pd.DataFrame:

    if possible_file is None:
        return None
    
    file = pd.read_csv(possible_file)
    transformer_function = _dataframe_transformer(function_loader)
    
    print(f"Loading: {function_loader}\n\n\n")
    return transformer_function(file)

@st.cache_data(ttl="1d", max_entries = 20)
def fetch_heifa_scores(_heifa_scores_dict, _user_daily_intake):
    return calculate_heifa_scores(
        _heifa_scores_dict, _user_daily_intake
    )

@st.cache_data(ttl="1d", max_entries = 20)
def get_user_servings(_user_dict, _food_comp_dict, _recipe_dict):
    return calculate_user_servings(
        _user_dict,
        _food_comp_dict,
        _recipe_dict
    )

st.title('Hello World. Welcome to Autotake24.')

# Upload the Intake24 file
st.header("File upload section")
intake24_file = st.file_uploader(
    "Upload Intake24 file",
    type="csv"
)

# Upload the HEIFA:
# - Recipes
# - Food Composition
# - Scoring file
heifa_recipe_file = st.file_uploader(
    "Upload HEIFA recipe list",
    type="csv"
)

heifa_food_composition_file = st.file_uploader(
    "Upload HEIFA food composition list",
    type="csv"
)

heifa_score_converter = st.file_uploader(
    "Upload HEIFA scoring rules file",
    type="csv"
)

intake_df = convert_file_csv(intake24_file, 'intake24')
recipe_df = convert_file_csv(heifa_recipe_file, 'recipe')
food_comp_df = convert_file_csv(heifa_food_composition_file, 'food_compo')
score_convert_df = convert_file_csv(heifa_score_converter, 'heifa_scores')

user_dict, recipe_dict = None, None
food_composition_dict, heifa_scores_dict = None, None
user_heifa_scores, user_daily_intake = None, None
transformed_df = None

if intake_df is not None:
    user_dict = create_user_objects(intake_df)

if recipe_df is not None:
    recipe_dict = create_recipe_objects(recipe_df)

if food_comp_df is not None:
    food_composition_dict = create_food_objects(food_comp_df)

if score_convert_df is not None:
    heifa_scores_dict = create_scores_objects(score_convert_df)

# Get the serves
if user_dict and recipe_dict and food_composition_dict:

    user_daily_intake = get_user_servings(
        user_dict,
        food_composition_dict,
        recipe_dict
    )

# Get the user intake
if user_daily_intake and heifa_scores_dict:

    user_heifa_scores = fetch_heifa_scores(
        heifa_scores_dict, user_daily_intake
    )

# Get the loaded CSV
if (heifa_scores_dict and food_composition_dict) and \
    (user_daily_intake and user_heifa_scores):

    transformed_df = create_heifa_csv(
        heifa_scores_dict, food_composition_dict, 
        user_daily_intake, user_heifa_scores,
    )

    st.download_button(
        label="Download scoring file",
        data=convert_df(transformed_df),
        file_name=get_file_name(),
        mime='text/csv',
    )

    st.write(transformed_df)
    st.balloons()

