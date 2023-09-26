from Food import Food

import pandas as pd

class Intake:

    def __init__(self):

        self._nutrients_info = {}
        self._heifa_list = []
        self._meal_intake = ''

    @property
    def nutrition_info(self):
        return self._nutrients_info

    def _print_food_info(self, heifa_id: str):
        
        nutrient = self._nutrients_info[heifa_id]

        print(
            f"Details for {heifa_id}:\n",
            f"Portion size of {nutrient.portion_size}g/ml\n"
            f" Energy (Dietary Fibre included): {nutrient.energy_with_fibre} kJ\n"
        )
        
        return None

    def print_nutrition(self):

        print(f"HEIFA code(s) for {self._meal_intake_type}: {self._heifa_list}\n")

        for code in self._heifa_list:

            self._print_food_info(code)
        
        return None
    
    def add_food_information(self, intake_df: pd.DataFrame) -> None:

        # Fetch HEIFA codes
        self._heifa_list = intake_df['heifa_nutrient_id'].values.tolist()

        # Determine the type of intake
        self._meal_intake_type = intake_df['meal_name'].values[0]

        # Fetch the respective columns
        # - Portion size consumed
        # - Energy (with dietary fibre)
        portion_size_list = intake_df['portion_size_consumed'].values.tolist()
        energy_fibre_list = intake_df['energy_with_fibre'].values.tolist()

        zipped_ingredients = zip(self._heifa_list, portion_size_list, energy_fibre_list)

        for heifa_id, portion_size, energy_with_fibre in zipped_ingredients:

            # Create dictionary and add to food object
            nutrient_info = {
                'portion_size': portion_size,
                'energy_with_fibre': energy_with_fibre
            }

            # Add the food object to the list
            self._nutrients_info[heifa_id] = Food(nutrient_info)


        return None

