from classes.Food import Food

import random
import string

class Intake:

    def __init__(self):

        self._nutrients_info = {}
        self._heifa_list = []

    @property
    def nutrition(self):
        return self._nutrients_info
    
    @property
    def heifa_list(self):
        return self._heifa_list
    
    @heifa_list.setter
    def heifa_list(self, heifa_id) -> None:
        self.heifa_list.append(heifa_id)

        return None
    
    @nutrition.setter
    def nutrition(self, intake24_row) -> None: 

        heifa_code = intake24_row['heifa_nutrient_id']

        # Just in case there is a duplicate
        if heifa_code in self.nutrition:
            random_id = ''.join(random.choices(
                string.ascii_uppercase + string.digits, 
                k=8
            ))

            heifa_code = heifa_code + "_" + random_id

        self.nutrition[heifa_code] = Food(intake24_row)

        return None

    def print_nutrition(self):

        print(f"HEIFA code(s): {self.heifa_list}\n")

        for code in self._heifa_list:

            nutrient = self.nutrition[code]

            print(
                f"Details for {code}:\n"
                f"Portion size of {nutrient.portion_size}g/ml\n"
                f"Energy (Dietary Fibre included): {nutrient.energy_with_fibre} kJ\n"
                f"Sodium consumed (in mg): {nutrient.sodium_consumed} mg\n"
                f"Alcohol consumed (in g): {nutrient.alcohol_amount} g\n"
            )
        
        return None
    
