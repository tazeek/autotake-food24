

class DailyCalculator:

    def __init__(self, ingredients_dict, recipe_dict):
        
        self._ingredients = ingredients_dict
        self._recipes = recipe_dict

        self._daily_servings = {}
        self._group_servings = {}

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

    @property
    def group_servings(self):
        return self._group_servings
    
    @group_servings.setter
    def group_servings(self, group_tuple):
        food_group, serving_size = group_tuple

        group_serve_total = self._group_servings.get(food_group, 0)
        group_serve_total += serving_size
        self._group_servings[food_group] = group_serve_total

        return None
    
    
    @daily_servings.setter
    def daily_servings(self, group_tuple):

        food_group, serving_size = group_tuple

        group_serve_total = self._daily_servings.get(food_group, 0)
        group_serve_total += serving_size
        self._daily_servings[food_group] = group_serve_total

        return None
    
    @group_servings.deleter
    def group_servings(self):
        self._group_servings = {}

        return None
    
    @daily_servings.deleter
    def daily_servings(self):
        self._daily_servings = {}

        return None
    
    def _perform_recipe_calculation(self, eight_digit_code, portion_size):

        ingredients_dict = self.ingredients
        recipes_dict = self.recipes

        # Get the original list of ingredients
        pieces = self.recipes[eight_digit_code].recipe_pieces

        # Time to break down further
        while True:

            extra_pieces = {
                heifa_id: ingredient_obj for (heifa_id, ingredient_obj)
                in pieces.items() if ingredients_dict[heifa_id].is_recipe
            }

            # If nothing is found we break out
            if len(extra_pieces) == 0:
                break

            # Break down to extra pieces
            for nutrient_code in extra_pieces.keys():
                
                # Get the eight digit code
                eight_digit_code = ingredients_dict[nutrient_code].eight_digit_code

                # Update the original list
                pieces.update(recipes_dict[eight_digit_code].recipe_pieces)

                # Delete from original
                del pieces[nutrient_code]

            # Repeat until no recipe ingredients in the list

        # Calculate the food group individually
        for heifa_id, piece_obj in pieces.items():

            piece_amount = round(portion_size * piece_obj.proportion, 2)
            piece_energy = round((piece_amount * piece_obj.energy_with_fibre) / 100, 2)

            heifa_obj = ingredients_dict[heifa_id]
            food_group = heifa_obj.food_group
            serving_size = heifa_obj.calculate_serving_size(piece_energy, piece_amount)

            # Add to the daily servings attribute
            self.daily_servings = (food_group, serving_size)

        return None
    
    def _calculate_serving(self, meal):
        
        ingredients_dict = self.ingredients

        for heifa_id, ingredient_obj in meal.items():

            # Just in case....
            if heifa_id not in ingredients_dict:
                print(f"\nHEIFA ID {heifa_id} not found")
                continue

            portion_size = ingredient_obj.portion_size
            energy_with_fibre = ingredient_obj.energy_with_fibre

            heifa_obj = ingredients_dict[heifa_id]
            food_group = heifa_obj.food_group

            # Seperate calculation for recipes
            if heifa_obj.is_recipe:
                self._perform_recipe_calculation(
                    heifa_obj.eight_digit_code, portion_size
                )
                continue
            
            # Calculation for non-recipes
            serving_size = heifa_obj.calculate_serving_size(
                energy_with_fibre, portion_size
            )

            # Add to the daily servings attribute
            self.daily_servings = (food_group, serving_size)

        return None

    def _find_group_total(self):

        for food_group, serving_size in self.daily_servings.items():

            # For those without backslashes, just update and move on
            if "/" not in food_group:
                self.group_servings = (food_group, serving_size)
                continue

            food_group, sub_group = food_group.split("/")

            # Whole grains are the exceptions as a main group
            if sub_group == "Wholegrains":
                self.group_servings = (sub_group, serving_size)

            self.group_servings = (food_group, serving_size)
        
        return None
    
    def _find_servings(self, meals_list):

        for meal in meals_list:

            self._calculate_serving(meal)
            self._find_group_total()

        return None

    
    def calculate_daily_servings(self, meals_daily_list):

        total_daily_servings = {}

        # Store in this hierarchy: Date -> Food group -> Serving size
        for date, meals_list in meals_daily_list.items():

            # Initialize with new dictionary for new date
            del self.daily_servings

            # Calculate the servings
            self._find_servings(meals_list)

            # Store individual group servings and total group
            # servings
            total_daily_servings[date] = {
                'individual': self.daily_servings,
                'total': self.daily_servings
            }

        return total_daily_servings