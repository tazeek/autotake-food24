

class FoodComposition:

    def __init__(self, info_dict) -> None:

        self._heifa_code = info_dict['heifa_code']
        self._8_digit_code = info_dict['eight_digit_code']

        self._is_recipe = self._is_recipe(info_dict['food_group'])

        # We will add them in regardless
        self._serving_size = info_dict['serving_size']
        self._serving_measure = info_dict['serving_measure']
        self._food_group = info_dict['food_group']
        
        return None
    
    @property
    def serving_size(self):
        return self._serving_size
    
    @property
    def serving_measure(self):
        return self._serving_measure
    
    @property
    def is_recipe(self):
        return self._is_recipe
    
    @property
    def food_group(self):
        return self._food_group
    
    def skip_portion_size_calculation(self):


        if self._food_group == 'No food group':
            return True
        
        return False
    
    def _is_recipe(self, food_group):

        if "Recipe" in food_group:

            return True
        
        return False
    
    def print_full_details(self):

        print(
            f"Heifa Code: {self._heifa_code}\n"
            f"8 Digit Code: {self._8_digit_code}\n"
            f"Is a recipe: {self._is_recipe}\n"
            f"Serving Size: {self._serving_size}\n"
            f"Serving measure: {self._serving_measure}\n"
        )

        return None


class RecipeComposition:

    def __init__(self, info_dict):

        self._breakdown = {}

        self._recipe_id = info_dict['recipe_id']
        self._recipe_name = info_dict['recipe_name']

        return None
        
    def add_pieces(self, ingredients_dict):

        self._breakdown = ingredients_dict
        
        return None

    def print_ingredients_information(self):

        for ingred_in_rec_obj in self._breakdown.values():

            print(
                f"Print for {ingred_in_rec_obj._ingredient_name}\n"
                f"Propotion: {ingred_in_rec_obj._proportion_recipe:.2f}\n\n"
            )

        return None

class IngredientInRecipe:

    def __init__(self, info_dict):
        
        self._proportion_recipe = info_dict['proportion']
        self._ingredient_name = info_dict['ingredient_name']

        return None


