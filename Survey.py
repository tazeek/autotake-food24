

class Survey:

    def __init__(self, id):

        self._id = id
        self.meals_intake = {}
    
    def add_meal(self, meal_id, meals):

        self.meals_intake[meal_id] = meals