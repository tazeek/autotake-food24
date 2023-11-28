# autotake-food24

Automate process calculation of Intake24 data with the HEIFA scoring. \
Purpose of this project is to reduce the time taken to calculate the recal
of a single survey.

## Criteria for files' column names

**Important**: Please read this document to have a proper understanding of how columns should be named for the processing to work.

**NOTE**: '\n' denotes a line break. This means that anything after '\n' should start in a newline.

**Intake24**: The following columns are needed and should be named accurately:
- 'Energy, with dietary fibre': Energy with dietary fibre
- 'Survey ID': The unique number for each recall.
- 'User ID': The user ID of the survey.
- 'Meal ID': The meal number within each recall.
- 'Nutrient table code': The food code given to each food/drink item.
- 'Portion size (g/ml)': Portion size of the food/drink.
- 'Sodium': The amount of sodium in the food/drink.
- 'Alcohol': The amount of alcohol in the food/drink.
- 'Total sugars': The amount of added sugar in the food/drink.
- 'Satd FA': The amount of saturated fat in the food/drink.
- 'Monounsaturated fatty acids (g)': The amount of monounsaturated fat in the food/drink.
- 'Polyunsaturated fatty acids (g)': The amount of polyunsaturated fat in the food/drink.

**HEIFA Food Composition**:
- 'Nutrient table code': The nutrient ID of the given food item. 
- '8 digit code': The HEIFA 8 digit code (recipe).
- 'HEIFA-2013 Food Group': The relevant food group.
- 'Energy or grams per Serve \n(HEIFA food groups)': The energy per serving size.
- 'Serving size unit of measure': The serving unit of measurement.
- 'Non-alcoholic beverage Flag\n(1=Non-alcoholic beverage)': Check whether it is an alcoholic beverage or not.

**HEIFA Recipe list**:
- 'Recipe AUSNUT 8-digit code': The HEIFA 8 digit code (recipe) in the file.
- 'Ingredient Nutrient table code': The nutrient ID of the given food of the recipe.
- 'Proportion of ingredients in the recipe': The proportion amount in the recipe.
- 'Energy, with dietary fibre (kJ) per 100g': The amount of energy in the given ingredient.

**HEIFA Score rules**:
- 'Food group': The relevant food group.
- 'Minimum serves per day (Male)': The minimum number of serves for the given food group (Male).
- 'Maximum serves per day (Male)': The maximum of serves for the given food group (Male).
- 'Minimum serves per day (Female)': The minimum number of serves for the given food group (Female).
- 'Maximum serves per day (Female)': The maximum of serves for the given food group (Female).
- 'HEIFA Score': The HEIFA score, based on the given range of minimum and maximum serves.
- **NOTE**: Some of the maximum serves are left empty in the CSV file. This is to denote that there is NO upper bound.

**How they all map together**:
- _Intake24_ and _HEIFA Food Composition_: They are mapped by the **Nutrient table code** field. Any field not present is shown in the dashboard as output.
- _HEIFA Food Composition_ and _HEIFA Recipe list_: They are mapped by the **Recipe AUSNUT 8-digit code** field.

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
