from Food import Food

import pandas as pd

class Intake:

    def __init__(self):

        self.nutrients_info = {}
        self.heifa_list = []

    def _print_nutritent_info(self, id):
        
        nutrient = self.nutrients_info[id]

        print(
            f"Printing for {id}: Code {nutrient['food_code']}",
            f" with {nutrient['portion_size']}g/ml portion size.\n"
        )
        
        return None

    def print_nutrition(self, id):

        heifa_codes = self.heifa_list

        print(f"HEIFA code for {id}: {heifa_codes}\n")

        for code in heifa_codes:

            self._print_nutritent_info(code)
        
        return None
    
    def add_food_information(self, intake_df: pd.DataFrame) -> None:

        # Fetch HEIFA codes
        self.heifa_list = intake_df['heifa_nutrient_id'].values.tolist()

        # Fetch the respective columns
        meal_name = intake_df['meal_name'].values.tolist()
        portion_size_list = intake_df['portion_size_consumed'].values.tolist()

        zipped_ingredients = zip(self.heifa_list, meal_name, portion_size_list)

        for heifa_id, meal_name, portion_size in zipped_ingredients:

            # Create dictionary and add to food object
            nutrient_info = {
                'food_code': meal_name,
                'portion_size': portion_size
            }

            food_obj = Food(nutrient_info)

            # Add the food object to the list
            self.nutrients_info[heifa_id] = nutrient_info


        ...

