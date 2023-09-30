from Intake import Intake

class Survey:

    def __init__(self):

        self.meals_intake = {}

    @property
    def meals(self):
        return self.meals_intake.values()
    
    @meals.setter
    def meals(self, meal_id):
        # Check if ID exists
        # If it does, no need to do anything
        if meal_id in self.meals_intake:
            self.meals_intake[meal_id] = Intake()
        
        return None
    
    def get_meal(self, meal_id) -> Intake:

        # Use the setter, regardless
        # The setter will handle it
        self.meals = meal_id

        return self.meals_intake[meal_id]

    def print_meals(self):

        for meal_obj in self.meals_intake.values():

            meal_obj.print_nutrition()

        return None
    
    def add_meal(self, meal_id, meals):

        self.meals_intake[meal_id] = meals

        return None