from file_loaders import *
from utils import *
from datetime import datetime

import streamlit as st
import pandas as pd

def _dataframe_transformer(function_loader):
    return {
        'intake24': [load_intake24, create_user_objects],
        'food_compo': [load_heifa_ingredients, create_food_objects],
        'recipe': [load_heifa_recipes, create_recipe_objects],
        'heifa_scores': [load_heifa_scores, create_scores_objects],
    }[function_loader]

def _get_file_name():

    # Get the current date and time
    datetime_obj = datetime.now()
    
    date = datetime_obj.strftime("%Y_%m_%d")
    time = datetime_obj.strftime("%H-%M")

    return f"HEIFA Scores {date} - {time}.csv"

@st.cache_data(ttl="1hr", max_entries=20)
def _convert_df(df):
    return df.to_csv(sep=",", index=False).encode('utf-8')

@st.cache_data(ttl="1d", max_entries=100)
def _convert_csv_dataframe(possible_file, function_loader) -> pd.DataFrame:

    if possible_file is None:
        return None
    
    file = pd.read_csv(possible_file)

    # Step 1: Load the CSV properly (Cleaner)
    # Step 2: Convert from CSV to objects (Transformer)
    cleaner_function, transformer_function = \
        _dataframe_transformer(function_loader)
    
    cleaned_df = cleaner_function(file)

    #transformer_function = _create_objects(function_loader)
    
    return transformer_function(cleaned_df)

@st.cache_data(ttl="1hr", max_entries = 30)
def get_csv_heifa_scores(*args):

    intake24_file, heifa_recipe_file, heifa_food_file, heifa_score_file = args

    # 1. Load the files
    user_dict = _convert_csv_dataframe(intake24_file, 'intake24')
    recipe_dict = _convert_csv_dataframe(heifa_recipe_file, 'recipe')
    food_composition_dict = _convert_csv_dataframe(heifa_food_file, 'food_compo')
    heifa_scores_dict = _convert_csv_dataframe(heifa_score_file, 'heifa_scores')

    # 2. Get the user servings
    missing_ids_list, user_daily_intake = calculate_user_servings(
        user_dict,
        food_composition_dict,
        recipe_dict
    )

    # 3. Convert to HEIFA scores
    user_heifa_scores = calculate_heifa_scores(
        heifa_scores_dict, user_daily_intake
    )

    # 4. Return the created CSV file
    return missing_ids_list, create_heifa_csv(
        heifa_scores_dict, 
        food_composition_dict, 
        user_daily_intake, 
        user_heifa_scores,
    )

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

heifa_food_file = st.file_uploader(
    "Upload HEIFA food composition list",
    type="csv"
)

heifa_score_file = st.file_uploader(
    "Upload HEIFA scoring rules file",
    type="csv"
)

# Get the serves
if (intake24_file and heifa_recipe_file) and (heifa_food_file and heifa_score_file):

    # Get the loaded CSV
    missing_ids_list, transformed_df = get_csv_heifa_scores(
        intake24_file, 
        heifa_recipe_file, 
        heifa_food_file, 
        heifa_score_file,
    )

    # For missing HEIFA files
    if missing_ids_list:
        combined_ids = " ".join(missing_ids_list)
        st.write(f'Following HEIFA IDs not found: {combined_ids}')

    st.download_button(
        label="Download scoring file",
        data=_convert_df(transformed_df),
        file_name=_get_file_name(),
        mime='text/csv',
    )

    st.write(transformed_df)
    st.balloons()

