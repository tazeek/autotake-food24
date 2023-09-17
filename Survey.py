

class Survey:

    def __init__(self):

        self.meals_intake = {}

    def _print_meals(self):

        for id, meal_obj in self.meals_intake.items():

            meal_obj.print_nutrition()

        return None
    
    def add_meal(self, meal_id, meals):

        self.meals_intake[meal_id] = meals