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

def _create_objects(function_loader):
    return {
        'intake24': create_user_objects,
        'food_compo': create_food_objects,
        'recipe': create_recipe_objects,
        'heifa_scores': create_scores_objects,
    }[function_loader]

def get_file_name():

    # Get the current date and time
    datetime_obj = datetime.now()
    
    date = datetime_obj.strftime("%Y_%m_%d")
    time = datetime_obj.strftime("%H-%M")

    return f"HEIFA Scores {date} - {time}.csv"

@st.cache_data(ttl="1hr", max_entries=20)
def convert_df(df):
    return df.to_csv(sep=",", index=False).encode('utf-8')

@st.cache_data(ttl="1d", max_entries=100)
def convert_csv_dataframe(possible_file, function_loader) -> pd.DataFrame:

    if possible_file is None:
        return None
    
    file = pd.read_csv(possible_file)

    # Step 1: Load the CSV properly
    cleaner_function = _dataframe_transformer(function_loader)
    cleaned_df = cleaner_function(file)

    # Step 2: Convert from CSV to objects
    transformer_function = _create_objects(function_loader)
    
    return transformer_function(cleaned_df)

@st.cache_data(ttl="1d", max_entries=100)
def convert_dataframe_objects(dataframe, function_loader) -> pd.DataFrame:

    transformer_function = _create_objects(function_loader)
    return transformer_function(dataframe)

@st.cache_data(ttl="1d", max_entries = 20)
def fetch_heifa_scores(file_name, _heifa_scores_dict, _user_daily_intake):
    return calculate_heifa_scores(
        _heifa_scores_dict, _user_daily_intake
    )

@st.cache_data(ttl="1d", max_entries = 20)
def get_user_servings(file_name, _user_dict, _food_comp_dict, _recipe_dict):
    return calculate_user_servings(
        _user_dict,
        _food_comp_dict,
        _recipe_dict
    )

user_dict, recipe_dict = None, None
food_composition_dict, heifa_scores_dict = None, None
user_heifa_scores, user_daily_intake = None, None
transformed_df = None

# Page configurations
st.set_page_config(
    page_title="Autotake24 - Get your scores calculated!",
    page_icon="🍊",
    layout="wide"
)

st.title('Welcome to Autotake24.')
st.header("File upload section")
# Upload:
# - Intake24
# - Recipes
# - Food Composition
# - Scoring file

intake24_file = st.file_uploader(
    "Upload Intake24 file",
    type="csv"
)

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

user_dict = convert_csv_dataframe(intake24_file, 'intake24')
recipe_dict = convert_csv_dataframe(heifa_recipe_file, 'recipe')
food_composition_dict = convert_csv_dataframe(heifa_food_composition_file, 'food_compo')
heifa_scores_dict = convert_csv_dataframe(heifa_score_converter, 'heifa_scores')

# Get the serves
if (user_dict and recipe_dict) and (food_composition_dict and heifa_scores_dict):

    hashed_file = intake24_file.name

    user_daily_intake = get_user_servings(
        hashed_file,
        user_dict,
        food_composition_dict,
        recipe_dict
    )

    # Get the user intake
    user_heifa_scores = fetch_heifa_scores(
        hashed_file,
        heifa_scores_dict, 
        user_daily_intake
    )

    # Get the loaded CSV
    transformed_df = create_heifa_csv(
        heifa_scores_dict, 
        food_composition_dict, 
        user_daily_intake, 
        user_heifa_scores,
    )

    st.download_button(
        label="Download scoring file",
        data=convert_df(transformed_df),
        file_name=get_file_name(),
        mime='text/csv',
    )

    st.write(transformed_df)
    st.balloons()

