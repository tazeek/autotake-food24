

class DailyCalculator:

    def __init__(self, ingredients_dict, recipe_dict):
        
        self._ingredients = ingredients_dict
        self._recipes = recipe_dict

        self._daily_servings = {}

        return None

    @property
    def ingredients(self):
        return self._ingredients
    
    @property
    def recipes(self):
        return self._recipes
    
    @property
    def daily_servings(self):
        return self._daily_servings
    
    def calculate_daily_servings(self, meals_daily_list):

        # Store in this hierarchy: Date -> Food group -> Serving size
        for date, meals_list in meals_daily_list.items():

            # Initialize empty date with dictionary
            self._daily_servings[date] = {}

            # Calculate the servings
            ...
        ...