

class Intake:

    def __init__(self, id):

        self._id = id
        self.nutrients_info = {}
    
    def add_nutrient(self, nutrient_id, nutrient_info):

        self.meals_intake[nutrient_id] = nutrient_info

        
