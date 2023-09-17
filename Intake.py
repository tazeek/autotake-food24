

class Intake:

    def __init__(self):

        self.nutrients_info = {}
        self.heifa_list = []

    def _print_nutritent_info(self, id):
        
        nutrient = self.nutrients_info[id]

        print(f"Printing for {id}: Code {nutrient['food_code']} \
               with {nutrient['portion_size']}g/ml portion size.\n")
        
        return None

    def print_nutrition(self):

        heifa_codes = self.heifa_list

        print(f"HEIFA code for Meal {id}: {heifa_codes}\n")

        for code in heifa_codes:

            self._print_nutritent_info(code)
            print("\n\n")
        
        return None
    
    def add_nutrient(self, nutrient_id, nutrient_info):

        self.nutrients_info[nutrient_id] = nutrient_info

        return None

    def add_nutrient_heifa_list(self, heifa_list):

        self.heifa_list = heifa_list

        return None

