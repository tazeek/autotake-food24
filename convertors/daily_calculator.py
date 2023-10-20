

class DailyCalculator:

    def __init__(self, ingredients_dict, recipe_dict):
        
        self._ingredients = ingredients_dict
        self._recipes = recipe_dict

        self._total_energy = 0

        self._daily_servings = {}
        self._group_servings = {}
        self._variation_servings = {}

        self._sub_as_main = ['Wholegrains']

        # For some of the conversions
        # Reference: Samara's video
        self._grams_to_calories = {
            'Sugar': 16.7,
            'Fat': 37.7
        }

        return None

    @property
    def variation_servings(self):
        return self._variation_servings
    
    @property
    def total_energy(self):
        return self._total_energy

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

    @property
    def sub_groups_main(self):
        return self._sub_as_main
    
    @total_energy.setter
    def total_energy(self, energy_amount):
        self.total_energy += energy_amount

        return None
    
    @variation_servings.setter
    def variation_servings(self, group_tuple):
        main_group, sub_group, serving_size = group_tuple

        # Get the main group
        main_group_dict = self._variation_servings.get(main_group, {})

        # Sum up the variations
        serve_total = main_group_dict.get(sub_group, 0)
        serve_total += serving_size
        main_group_dict[sub_group] = serve_total

        # Return back
        self._variation_servings[main_group] = main_group_dict

        return None
    
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

        group_serve_total += float(serving_size)
        self._daily_servings[food_group] = group_serve_total

        return None

    @variation_servings.deleter
    def variation_servings(self):
        self._variation_servings = {}

        return None
    
    @group_servings.deleter
    def group_servings(self):
        self._group_servings = {}

        return None
    
    @daily_servings.deleter
    def daily_servings(self):
        self._daily_servings = {}

        return None
    
    @total_energy.deleter
    def total_energy(self):
        self.total_energy = 0

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

            # Add in the energy for sugar and fats calculation
            self.total_energy = energy_with_fibre

            # For Alcohol (PENDING CONFIRMATION)
            if ingredient_obj.alcohol_amount > 0:
                standard_size_drinks = round(ingredient_obj.alcohol_amount / 10, 1)
                self.daily_servings = ("Alcohol", standard_size_drinks)

            # For non-alcoholic beverage
            if heifa_obj.plain_beverage:
                self.daily_servings = ("Non-Alcohol", portion_size)

            # For water:
            if heifa_obj.is_water:
                self.daily_servings = ("Water", portion_size)

            # For Sodium
            self.daily_servings = ("Sodium", ingredient_obj.sodium_consumed)

            # For Sugar
            self.daily_servings = ("Sugar", ingredient_obj.sugar_amount)

            # For the Fats

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

            # Add to the daily servings attribute, based on food group
            self.daily_servings = (food_group, serving_size)

        return None

    def _update_single_groups(self, food_group, serving_size):

        # Handle for sugar
        if food_group == "Sugar":
            sugar_amount = self.daily_servings.get("Sugar", 0)
            sugar_energy = round(sugar_amount * self._grams_to_calories[food_group], 2)

            # Percentage amount
            percentage_sugar = round((sugar_energy/self._total_energy) * 100, 2)

            self.group_servings = ("Sugar", percentage_sugar)

        # Handle for fats

         # Handle for water
        if food_group == "Water":
            beverage_amount = self.daily_servings.get("Non-Alcohol", 0)
            amount = round((serving_size/beverage_amount) * 100, 1)

            # Has to be more than 1.5L else default to 0
            amount = amount if beverage_amount >= 1500 else 0
            self.group_servings = ("Water", amount)

            return None

        # Legumes falls under Vegetables, as per HEIFA guideline
        # Otherwise, do the usual for the rest
        if food_group == "Legumes":
            self.variation_servings = ("Vegetables", food_group, serving_size)
            return None
        
        self.group_servings = (food_group, serving_size)

        return None

    def _find_group_total(self):

        for food_group, serving_size in self.daily_servings.items():

            # For those without backslashes, just update and move on
            if "/" not in food_group:
                self._update_single_groups(food_group, serving_size)
                continue

            # Reduce whitespace within the food group
            food_group, sub_group = food_group.split("/")
            food_group, sub_group = food_group.strip(), sub_group.strip()

            self.group_servings = (food_group, serving_size)

            # Whole grains and Alcohol are the exceptions as a main group
            # They have a separate HEIFA score
            if sub_group in self.sub_groups_main:
                self.group_servings = (sub_group, serving_size)
                continue

            self.variation_servings = (food_group, sub_group, serving_size)
        
        return None
    
    def _find_servings(self, meals_list):

        for meal in meals_list:

            self._calculate_serving(meal)

        # We calculate after all the meals are done    
        self._find_group_total()

        return None

    
    def calculate_daily_servings(self, meals_daily_list):

        total_daily_servings = {}

        # Store in this hierarchy: Date -> Food group -> Serving size
        for survey_id, meals_list in meals_daily_list.items():

            # Initialize with new dictionary for new date
            del self.daily_servings
            del self.group_servings
            del self.variation_servings

            # Calculate the servings
            self._find_servings(meals_list)

            # Store individual group servings and total group
            # servings
            total_daily_servings[survey_id] = {
                'individual': self.daily_servings,
                'total': self.group_servings,
                'variations': self.variation_servings
            }

        return total_daily_servings