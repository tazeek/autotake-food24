

class FoodComposition:

    def __init__(self, info_dict) -> None:

        self._heifa_code = info_dict['heifa_code']
        self._8_digit_code = info_dict['eight_digit_code']

        # We will add them in regardless
        self._serving_size = info_dict['serving_size']
        self._serving_measure = info_dict['serving_measure']
        self._food_group = info_dict['food_group']


        self._is_recipe = self._check_if_recipe(info_dict['food_group'])
        self._required_portion_calculation = self._is_required_portion_calculation(info_dict['food_group'])
        
        return None
    
    @property
    def eight_digit_code(self):
        return self._8_digit_code
    
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
    def required_portion_calculation(self):
        return self._required_portion_calculation
    
    @property
    def food_group(self):
        return self._food_group
    
    def _is_required_portion_calculation(self, food_group):

        # As per Dr. Heidi: Skip for those with no food groups
        # Trial-error checks: Skip for Water
        skip_group_list = ['No food group', 'Water']

        if food_group not in skip_group_list:
            return True
        
        return False
    
    def _check_if_recipe(self, food_group):

        if "Recipe" in food_group:

            return True
        
        return False
    
    def calculate_serving_size(self, energy_with_fibre, weight):

        serving_size = 0

        # Check if calculation is required or not
        # If not, just return 0
        if not self.required_portion_calculation:
            return serving_size

        # Check the serving measure and round to 2 decimal place
        # - kJ: Use energy_with_fibre
        # - g: Use weight
        if self._serving_measure == "g":
            serving_size = round(weight/self._serving_size, 2)
        else:
            serving_size = round(energy_with_fibre/self._serving_size, 2)
        
        return serving_size
    
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

        self._recipe_pieces = {}

        self._recipe_id = info_dict['eight_digit_code']
        self._recipe_name = info_dict['recipe_name']

        return None
    
    @property
    def recipe_pieces(self):
        return self._recipe_pieces
    
    @recipe_pieces.setter
    def recipe_pieces(self, ingredient_dict):
        self._recipe_pieces.update(ingredient_dict)

    def print_ingredients_information(self):

        for ingred_in_rec_obj in self._recipe_pieces.values():

            print(
                f"Print for {ingred_in_rec_obj._ingredient_name}\n"
                f"Propotion: {ingred_in_rec_obj._proportion_recipe:.2f}\n\n"
            )

        return None

class IngredientInRecipe:

    def __init__(self, info_dict):
        
        self._proportion_recipe = info_dict['proportion']
        self._ingredient_name = info_dict['ingredient_name']
        self._energy_fibre_100g = info_dict['energy_fibre_100g']

        return None
    
    @property
    def proportion(self):
        return self._proportion_recipe
    
    @property
    def ingredient_name(self):
        return self._ingredient_name
    
    @property
    def energy_with_fibre(self):
        return self._energy_fibre_100g


