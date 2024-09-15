from file_loaders import *
from utils import *
from exception_class import ProcessFailed
from datetime import datetime

import streamlit as st
import pandas as pd

@st.cache_data(ttl="1hr")
def _load_recipes_ingredients():

    # Get the URL
    ingredients_file = get_file_google(st.secrets['ingredients_file'])
    recipes_file = get_file_google(st.secrets['recipe_file'])

    return ingredients_file, recipes_file

def _validate_password(entered_password):

    if st.secrets['password'] != entered_password:
        st.error(f"Wrong password entered.")
        st.stop()

    return True

def _dataframe_transformer(function_loader):
    return {
        'intake24': [load_intake24, create_user_objects],
        'food_compo': [load_heifa_ingredients, create_food_objects],
        'recipe': [load_heifa_recipes, create_recipe_objects],
        'heifa_scores': [load_heifa_scores, create_scores_objects],
    }[function_loader]

@st.cache_data(ttl=60)
def _get_file_name():

    # Get the current date and time
    datetime_obj = datetime.now()
    
    date = datetime_obj.strftime("%Y_%m_%d")
    time = datetime_obj.strftime("%H-%M")

    return f"HEIFA Scores {date} - {time}.csv"

@st.cache_data(ttl="1hr", max_entries=20)
def _convert_df(df):
    return df.to_csv(sep=",", index=False).encode('utf-8')

@st.cache_data(ttl=60)
def _convert_csv_dataframe(possible_file, function_loader) -> pd.DataFrame:

    if possible_file is None:
        return None
    
    file = pd.read_csv(possible_file)

    # Step 1: Load the CSV properly (Cleaner)
    # Step 2: Convert from CSV to objects (Transformer)
    cleaner_function, transformer_function = \
        _dataframe_transformer(function_loader)
    
    cleaned_df = cleaner_function(file)
    
    return transformer_function(cleaned_df)

@st.cache_data(ttl=60)
def get_csv_heifa_scores(*args):

    intake24_file, heifa_recipe_file, heifa_food_file, heifa_score_file = args

    user_dict, recipe_dict, food_composition_dict, heifa_scores_dict = None, None, None, None
    missing_ids_list, user_daily_intake = None, None
    user_heifa_scores = None

    # 1. Load the files
    my_bar = st.progress(0, text="Loading files..")
    try:
        user_dict = _convert_csv_dataframe(intake24_file, 'intake24')
        recipe_dict = _convert_csv_dataframe(heifa_recipe_file, 'recipe')
        food_composition_dict = _convert_csv_dataframe(heifa_food_file, 'food_compo')
        heifa_scores_dict = _convert_csv_dataframe(heifa_score_file, 'heifa_scores')
    except Exception as e:
        raise ProcessFailed("One or more files have columns mismatch")

    # 2. Get the user servings
    my_bar.progress(25, text="Calculating User Servings..")

    try:
        missing_ids_list, user_daily_intake = calculate_user_servings(
            user_dict,
            food_composition_dict,
            recipe_dict
        )
    except Exception as e:
        raise ProcessFailed("Error occured upon calculating servings.")

    # 3. Convert to HEIFA scores
    my_bar.progress(50, text="Converting to HEIFA scores.")

    try:
        user_heifa_scores = calculate_heifa_scores(
            heifa_scores_dict, user_daily_intake
        )
    except Exception as e:
        raise ProcessFailed("Error occured upon calculating HEIFA scores.")

    # 4. Create the CSV file
    my_bar.progress(75, text="Creating CSV file.")
    csv_file = create_heifa_csv(
        heifa_scores_dict, 
        food_composition_dict, 
        user_daily_intake, 
        user_heifa_scores,
    )

    my_bar.progress(100, text="CSV file creation done.")

    # 4. Return the created CSV file
    return missing_ids_list, csv_file

# Page configurations
st.set_page_config(
    page_title="Autotake24 - Get your scores calculated!",
    page_icon="🍊",
    layout="wide"
)

st.title('Welcome to Autotake24.')
st.header("File upload section")

st.markdown("""
    If this is your first time, please have a read at the following link 
    in regards to the column names for this dashboard: 
    https://github.com/tazeek/autotake-food24/tree/master#criteria-for-files-column-names       
""")

# Just in case
cache_clear_button = st.button(
    "Clear cache data",
    type = "primary",
    help = "Clear all in-memory data. Refresh the page after clicking this button"
)

if cache_clear_button:
    st.cache_data.clear()

# Upload:
# - Intake24
# - Recipes
# - Food Composition
# - Scoring file

intake24_file = st.file_uploader(
    "Upload Intake24 file",
    type="csv"
)

#heifa_recipe_file = st.file_uploader(
#    "Upload HEIFA recipe list",
#    type="csv"
#)

#heifa_food_file = st.file_uploader(
#    "Upload HEIFA food composition list",
#    type="csv"
#)

heifa_score_file = st.file_uploader(
    "Upload HEIFA scoring rules file",
    type="csv"
)

password = st.text_input("Enter Password to generate results", "")

heifa_recipe_file, heifa_food_file = _load_recipes_ingredients()

if st.button("Generate results"):
    _validate_password(password)

# Get the serves
if (intake24_file and heifa_recipe_file) and (heifa_food_file and heifa_score_file):

    missing_ids_list = None
    transformed_df = None
    
    # Get the loaded CSV
    # Check for error messages
    try:
        missing_ids_list, transformed_df = get_csv_heifa_scores(
            intake24_file, 
            heifa_recipe_file, 
            heifa_food_file, 
            heifa_score_file,
        )
    except Exception as e:
        st.error(f"Caught an error: {str(e)}")
        st.stop()


    # For missing HEIFA files
    if missing_ids_list:
        combined_ids = " ".join(missing_ids_list)
        st.write(f'Following nutrient IDs not found: {combined_ids}')

    st.download_button(
        label="Download scoring file",
        data=_convert_df(transformed_df),
        file_name=_get_file_name(),
        mime='text/csv',
    )

    st.write(transformed_df)
    st.balloons()

