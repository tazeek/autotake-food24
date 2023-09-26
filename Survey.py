

class Survey:

    def __init__(self):

        self.meals_intake = {}

    def print_meals(self):

        for meal_obj in self.meals_intake.values():

            meal_obj.print_nutrition()

        return None
    
    def add_meal(self, meal_id, meals):

        self.meals_intake[meal_id] = meals

        return None

    def get_meals(self):

        return self.meals_intake.values()