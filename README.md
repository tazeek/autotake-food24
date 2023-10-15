# autotake-food24

Collaboration with Intake24 and automate some processes.

## Breakdown of Intake 24:

- The file has many users.
- Each user has many surveys.
- Each survey has many meal intake.
- Each intake consists of many food components.
- Every food component is marked with a "Nutrition ID code".

## Breakdown of HEIFA (Food Composition)

Every row in the file is a unique ingredient.

Every ingredient:
- has it's own attributes.
- can be mapped to a 8-digit code (for HEIFA Recipe)
- is used as a divisor for either energy (kilo joules) or grams (g)

## Breakdown of HEIFA (Recipes)

- Every recipe has multiple ingredients
- Keys are repeated across rows (similar to Survey ID of Intake24)
- Every ingredient has respective proportion to the recipe

## Mapping between Intake24 and HEIFA Ingredients

- For each user, extract the given nutrients and store in an array.
- This is from ALL the survey data.
- We don't care about the order here.
- The array will contain a list of dictionaries/JSON.

In the array:

- Use the HEIFA ID (from user) to map to the HEIFA Ingredients' HEIFA ID.
- Check if a result is found or not.
- Check if it requires a recipe or not.

## Mapping between Intake24 and HEIFA Recipes

This is in case a recipe is found (The second step).

- For the given recipe, extract the given nutrients ID and proportion, store in an array.
- We don't care about the order here.
- The array will contain a list of dictionaries.

In the array:

- Use the HEIFA ID (from the recipes) to map the HEIFA Ingredients' HEIFA ID.
- Check the energy and serving size.

## Calculating the HEIFA Scores

Heifa scores are to be calculated on a **daily basis**.

To calculate them, let's break them down:

- Break down by user
- Break down by date
- Break down by major food group (Example: Vegetables/Green -> Vegetables is the major food group)
- Break down by sub-food group of the major (Example: Vegetables/Green -> Green is the sub-food group)
- Compare the scores by gender (male and female)

There are some exceptions to the rule, based on the HEIFA scores guideline:

- Grains and cereals/Wholegrains -> This is to be calculated separately as "Grains and cereals" and "Wholegrains".

Varieties:

- Store the variety score in a different dictionary
- Find the score of each variety group separately (based on the HEIFA rule book)
