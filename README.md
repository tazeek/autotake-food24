# autotake-food24

Automate process calculation of Intake24 data with the HEIFA scoring. \
Purpose of this project is to reduce the time taken to calculate the recal
of a single survey.

## Criteria for files' column names

**Important**: Please read this document to have a proper understanding of how columns should be named for the processing to work.

**Intake24**: The following columns are needed and should be named accurately:
- 'Energy, with dietary fibre': Energy with dietary fibre
- 'Survey ID': The survey ID of the recall data.
- 'User ID': The user ID of the survey.
- 'Meal ID': The meal ID of the recall data.
- 'Nutrient table code': The nutrient ID of the given food item.
- 'Portion size (g/ml)': Portion size of the food.
- 'Sodium': The amount of sodium in the food.
- 'Alcohol': The amount of alcohol in the food.
- 'Total sugars': The amount of sugars in the food.
- 'Satd FA': The amount of saturated fat in the food.
- 'Monounsaturated fatty acids (g)': The amount of monosaturated fat in the food.
- 'Polyunsaturated fatty acids (g)': The amount of polysaturated fat in the food.

**HEIFA Food Composition**:

**HEIFA Recipe list**:
- 'Recipe AUSNUT 8-digit code': The HEIFA 8 digit code in the file.
- 'Ingredient Nutrient table code': The nutrient ID of the given food of the recipe.
- 'Proportion of ingredients in the recipe': The proportion amount in the recipe.
- 'Energy, with dietary fibre (kJ) per 100g': The amount of energy in the given ingredient.

**HEIFA Score rules**:

## Steps involved

**Uploading files**: Upload and clean the raw files of Intake24 and HEIFA-related files.

**Processing files**: Extract the important pieces of information required for the calculations.

**Calculating the serves**: Calculate the serves, per survey ID, for each of the food groups involved. \
In addition, find the total of the main groups and sub-groups. \
Example of main group: Vegetables \
Example of sub-groups: Vegetables/Green, Vegetables/Cruciferous

**Conversion to HEIFA scores**: Convert the serves to the respective HEIFA scores, based on range and gender. \
In addition, sum up all the HEIFA scores, based on gender.

**Writing to CSV file**: Write the HEIFA scores and serve sizes to a CSV file for further analysis.

## Website

Website link: https://autotake-food24.streamlit.app/
