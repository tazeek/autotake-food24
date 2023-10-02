

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
    
    def _calculate_serving(self, meal):
        
        ingredients_dict = self.ingredients
        recipes_dict = self.recipes

        for heifa_id, ingredient_obj in meal.items():

            # Just in case....
            if heifa_id not in ingredients_dict:
                print(f"\nHEIFA ID {heifa_id} not found")
                continue

            portion_size = ingredient_obj.portion_size
            energy_with_fibre = ingredient_obj.energy_with_fibre

            heifa_obj = ingredients_dict[heifa_id]
            food_group = heifa_obj.food_group

            if heifa_obj.is_recipe:
                ...

        return None
    
    def _find_servings(self, meals_list):

        for meal in meals_list:

            self._calculate_serving(meal)

        return None

    
    def calculate_daily_servings(self, meals_daily_list):

        # Store in this hierarchy: Date -> Food group -> Serving size
        for date, meals_list in meals_daily_list.items():

            # Initialize empty date with dictionary
            self._daily_servings[date] = {}

            # Calculate the servings
            self._find_servings(meals_list)
        
        print(self._daily_servings)

        return None