

class FoodComposition:

    def __init__(self, info_dict) -> None:

        alcohol_flag = info_dict['is_alcohol']
        water_flag = info_dict['is_water'] 
        food_group = info_dict['food_group']

        # As per Dr. Heidi: Skip for those with no food groups
        # Trial-error checks: Skip for Water
        skip_group_list = ['No food group', 'Water']

        self._heifa_code = info_dict['heifa_code']
        self._8_digit_code = info_dict['eight_digit_code']

        # We will add them in regardless
        self._serving_size = info_dict['serving_size']
        self._serving_measure = info_dict['serving_measure']
        self._food_group = info_dict['food_group']

        self._is_recipe = 'Recipe' in food_group
        self._required_portion_calculation = \
            food_group not in skip_group_list
        
        self._alcohol_serving_size = info_dict['alcohol_serving_size']

        self._is_alcohol = alcohol_flag == 1
        self._plain_beverage = alcohol_flag == 0
        self._is_water = water_flag == 1
        
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
    
    @property
    def is_water(self):
        return self._is_water
    
    @property
    def plain_beverage(self):
        return self._plain_beverage
    
    @property
    def is_alcohol(self):
        return self._is_alcohol
    
    @property
    def alcohol_serving_size(self):
        return self._alcohol_serving_size
    
    def calculate_serving_size(self, energy_with_fibre, weight):

        serving_size = 0

        energy_with_fibre = float(energy_with_fibre)
        weight = float(weight)

        # Check if calculation is required or not
        # If not, just return 0
        if not self.required_portion_calculation:
            return serving_size
        
        serving_function = lambda measure: round(measure / self.serving_size, 2)

        # Check the serving measure and round to 2 decimal place
        # - kJ: Use energy_with_fibre
        # - g: Use weight
        measure = weight if self.serving_measure == "g" else energy_with_fibre
        
        return serving_function(measure)
    
    def print_full_details(self):

        print(
            f"Heifa Code: {self._heifa_code}\n"
            f"8 Digit Code: {self._8_digit_code}\n"
            f"Is a recipe: {self._is_recipe}\n"
            f"Serving Size: {self._serving_size}\n"
            f"Recipe: {self.food_group}\n"
            f"Serving measure: {self._serving_measure}\n"
            f"Is Beverage: {self.plain_beverage}\n"
            f"Is Plain Water: {self.is_water}\n"
        )


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

class IngredientInRecipe:

    def __init__(self, info_dict):
        
        self._proportion_recipe = info_dict['proportion']
        self._ingredient_name = info_dict['ingredient_name']
        self._energy_fibre_100g = info_dict['energy_fibre_100g']
    
    @property
    def proportion(self):
        return self._proportion_recipe
    
    @property
    def ingredient_name(self):
        return self._ingredient_name
    
    @property
    def energy_with_fibre(self):
        return self._energy_fibre_100g
