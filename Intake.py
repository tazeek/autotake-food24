from Food import Food

import pandas as pd

class Intake:

    def __init__(self):

        self._nutrients_info = {}
        self._heifa_list = []

    def _print_food_info(self, heifa_id: str):
        
        nutrient = self._nutrients_info[heifa_id]

        print(
            f"Printing for {id}: For {nutrient._meal_name}",
            f" with {nutrient._portion_size}g/ml portion size.\n"
        )
        
        return None

    def print_nutrition(self, id):

        print(f"HEIFA code for {id}: {self.heifa_list}\n")

        for code in self.heifa_list:

            self._print_food_info(code)
        
        return None
    
    def add_food_information(self, intake_df: pd.DataFrame) -> None:

        # Fetch HEIFA codes
        self._heifa_list = intake_df['heifa_nutrient_id'].values.tolist()

        # Fetch the respective columns
        # - The meal name: Breakfast, snack, etc
        # - Portion size consumed
        meal_name = intake_df['meal_name'].values.tolist()
        portion_size_list = intake_df['portion_size_consumed'].values.tolist()

        zipped_ingredients = zip(self._heifa_list, meal_name, portion_size_list)

        for heifa_id, meal_name, portion_size in zipped_ingredients:

            # Create dictionary and add to food object
            nutrient_info = {
                'food_code': meal_name,
                'portion_size': portion_size
            }

            # Add the food object to the list
            self._nutrients_info[heifa_id] = Food(nutrient_info)


        return None

