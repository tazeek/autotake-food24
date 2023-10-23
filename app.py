from file_loaders import *

import streamlit as st
import pandas as pd

def convert_file_csv(possible_file) -> pd.DataFrame:

    # Check if the file is uploaded
    return pd.read_csv(possible_file) \
        if possible_file is not None else None

st.title('Hello World. Welcome to Autotake24.')

# Upload the Intake24 file
st.header("File upload section")
intake24_file = st.file_uploader(
    "Upload Intake24 file",
    type="csv"
)

#if intake24_file is not None:
#    intake_df = pd.read_csv(intake24_file)
#    print(intake24_file.name)
#    st.write(intake_df)

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

intake_df = convert_file_csv(intake24_file)
recipe_df = convert_file_csv(heifa_recipe_file)
food_comp_df = convert_file_csv(heifa_food_composition_file)
score_convert_df = convert_file_csv(heifa_score_converter)

if intake_df is not None:
    intake_df = load_intake24(intake_df)
    st.write(intake_df.columns)

if recipe_df is not None:
    recipe_df = load_heifa_recipes(recipe_df)
    st.write(recipe_df.columns)

if food_comp_df is not None:
    food_comp_df = load_heifa_ingredients(food_comp_df)
    st.write(food_comp_df.columns)

if score_convert_df is not None:
    score_convert_df = load_heifa_scores(score_convert_df)
    st.write(score_convert_df.columns)



