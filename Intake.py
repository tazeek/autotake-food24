

class Intake:

    def __init__(self):

        self.nutrients_info = {}
        self.heifa_list = []
    
    def add_nutrient(self, nutrient_id, nutrient_info):

        self.nutrients_info[nutrient_id] = nutrient_info

    def add_nutrient_heifa_list(self, heifa_list):

        self.heifa_list = heifa_list

