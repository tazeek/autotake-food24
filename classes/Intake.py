from classes.Food import Food

class Intake:

    def __init__(self):

        self._nutrients_info = {}
        self._heifa_list = []
        self._meal_name = ''

    @property
    def nutrition(self):
        return self._nutrients_info
    
    @property
    def heifa_list(self):
        return self._heifa_list
    
    @property
    def meal_name(self):
        return self._meal_name
    
    @meal_name.setter
    def meal_name(self, meal_name) -> None:
        self._meal_name = meal_name
        
        return None
    
    @heifa_list.setter
    def heifa_list(self, heifa_id) -> None:
        self.heifa_list.append(heifa_id)

        return None
    
    @nutrition.setter
    def nutrition(self, intake24_row) -> None: 
        
        # Create food object and add to the list
        self.meal_type = intake24_row['meal_name']

        heifa_code = intake24_row['heifa_nutrient_id']
        self.nutrition[heifa_code] = Food(intake24_row)

        return None

    def print_nutrition(self):

        print(f"HEIFA code(s) for {self.meal_type}: {self.heifa_list}\n")

        for code in self._heifa_list:

            nutrient = self.nutrition[code]

            print(
                f"Details for {code}:\n"
                f"Portion size of {nutrient.portion_size}g/ml\n"
                f"Energy (Dietary Fibre included): {nutrient.energy_with_fibre} kJ\n"
                f"Sodium consumed (in mg): {nutrient.sodium_consumed}\n"
            )
        
        return None
    
