from classes.Intake import Intake

class Survey:

    def __init__(self):

        self._meals_intake = {}

    @property
    def meals(self):
        return self._meals_intake
    
    @meals.setter
    def meals(self, meal_id):
        # Check if ID exists
        # If it does, no need to do anything
        if meal_id not in self.meals:
            self.meals[meal_id] = Intake()
        
        return None
    
    def get_meal(self, meal_id) -> Intake:

        # Use the setter, regardless
        # The setter will handle it
        self.meals = meal_id

        return self.meals[meal_id]

    def print_meals(self):

        for meal_obj in self.meals.values():

            meal_obj.print_nutrition()

        return None
    