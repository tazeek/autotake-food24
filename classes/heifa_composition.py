

class FoodComposition:

    def __init__(self, info_dict) -> None:

        beverage_flag = info_dict['is_beverage']
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

        self._is_alcohol = 'Alcohol' in food_group
        self._plain_beverage = beverage_flag == 1
        self._is_water = 'Water' in food_group
        
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
    
    def calculate_serving_size(self, energy_with_fibre, weight):

        serving_size = 0

        energy_with_fibre = float(energy_with_fibre)
        weight = float(weight)

        # Check if calculation is required or not
        # If not, just return 0
        if not self.required_portion_calculation:
            return serving_size
        
        serving_function = lambda measure: measure / self.serving_size

        # Check the serving measure and round to 2 decimal place
        # - kJ: Use energy_with_fibre
        # - g: Use weight
        measure = weight if self.serving_measure == "g" else energy_with_fibre
        
        return serving_function(measure)

class RecipeComposition:

    def __init__(self, info_dict):

        self._recipe_pieces = {}
        self._recipe_id = info_dict['eight_digit_code']

        return None
    
    @property
    def recipe_pieces(self):
        return self._recipe_pieces
    
    @recipe_pieces.setter
    def recipe_pieces(self, ingredient_dict):
        self._recipe_pieces.update(ingredient_dict)
        return None

class IngredientInRecipe:

    def __init__(self, info_dict):
        
        self._proportion_recipe = info_dict['proportion']
        self._energy_fibre_100g = info_dict['energy_fibre_100g']
    
    @property
    def proportion(self):
        return self._proportion_recipe
    
    @property
    def energy_with_fibre(self):
        return self._energy_fibre_100g
