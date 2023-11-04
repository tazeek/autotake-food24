

class DailyCalculator:

    def __init__(self, ingredients_dict, recipe_dict):
        
        self._ingredients = ingredients_dict
        self._recipes = recipe_dict

        self._total_energy = 0
        self._daily_servings = {}
        self._group_servings = {}
        self._variation_servings = {}

        self._missing_nutrition_ids = []

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
    
    @property
    def missing_nutrition_ids(self):
        return self._missing_nutrition_ids
    
    @total_energy.setter
    def total_energy(self, energy_amount):
        self._total_energy += energy_amount

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
    
    @missing_nutrition_ids.setter
    def missing_nutrition_ids(self, heifa_id):

        if heifa_id not in self._missing_nutrition_ids:
            self._missing_nutrition_ids.append(heifa_id)
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
        self._total_energy = 0
        return None
    
    def _liquid_calculation(self, heifa_obj, ingredient_obj, portion_size):

        # For Alcohol
        if heifa_obj.is_alcohol:
            self.daily_servings = ("Alcohol", ingredient_obj.alcohol_amount)

        # For non-alcoholic beverage
        if heifa_obj.plain_beverage:
            self.daily_servings = ("Non-Alcohol", portion_size)

        # For water:
        if heifa_obj.is_water:
            self.daily_servings = ("Water", portion_size)

        return None

    def _recipe_traversal_breakdown(self, recipe_obj, portion_size, alcohol_amount):

        eight_digit_code = recipe_obj.eight_digit_code
        recipe_is_beverage = recipe_obj.plain_beverage

        # Get the recipe pieces
        pieces = self.recipes[eight_digit_code].recipe_pieces

        # Begin breakdown
        for heifa_id, piece_obj in pieces.items():
            
            # Break it into the respective piece portion
            piece_amount = portion_size * piece_obj.proportion
            heifa_obj = self.ingredients[heifa_id]

            # Some ingredients can be a recipe themselves
            # Keep repeating until no more. Hence 
            # it becomes a tree traversal problem
            # If being recursive, use the portion size 
            # of the ingredient, instead of the actual one
            if heifa_obj.is_recipe:
                self._recipe_traversal_breakdown(
                    heifa_obj,
                    piece_amount,
                    alcohol_amount
                )

                continue

            piece_energy = (piece_amount * piece_obj.energy_with_fibre) / 100

            food_group = heifa_obj.food_group
            serving_size = heifa_obj.calculate_serving_size(piece_energy, piece_amount)

            # Beverage: Check for main recipe beverage flag and ingredient flag
            if recipe_is_beverage and heifa_obj.plain_beverage:
                self.daily_servings = ("Non-Alcohol", piece_amount)

            # Water: Check for main recipe beverage flag and ingredient flag
            if recipe_is_beverage and heifa_obj.is_water:
                self.daily_servings = ("Water", piece_amount)

            # Alcohol: As long as the ingredient is alcohol, we move
            if heifa_obj.is_alcohol and (not self._alcohol_added):
                self.daily_servings = ("Alcohol", alcohol_amount)
                self._alcohol_added = True

            # Add to the daily servings attribute
            self.daily_servings = (food_group, serving_size)

        return None
        
    def _calculate_serving(self, meal):
        
        ingredients_dict = self.ingredients

        for heifa_id, ingredient_obj in meal.items():

            heifa_id = heifa_id.split('_')[0] if '_' in heifa_id else heifa_id

            # Just in case....
            if heifa_id not in ingredients_dict:
                self.missing_nutrition_ids = heifa_id
                continue

            portion_size = ingredient_obj.portion_size
            energy_with_fibre = ingredient_obj.energy_with_fibre
            heifa_obj = ingredients_dict[heifa_id]
            food_group = heifa_obj.food_group

            # Add in the energy for sugar and fats calculation
            self.total_energy = energy_with_fibre

            # For Sodium
            self.daily_servings = ("Sodium", ingredient_obj.sodium_consumed)

            # For Sugar
            self.daily_servings = ("Sugar", ingredient_obj.sugar_amount)

            # For the Fats: Saturated, Unsaturated (Mono), Unsaturdated (Poly)
            self.daily_servings = ("Saturated Fat", ingredient_obj.saturated_fat_amount)
            self.daily_servings = ("Unsaturated Fat", ingredient_obj.unsaturated_fat_mono_amount)
            self.daily_servings = ("Unsaturated Fat", ingredient_obj.unsaturated_fat_poly_amount)

            # Seperate calculation for recipes
            if heifa_obj.is_recipe:

                # This flag is for recipe calculation. We only 
                # add the alcohol once as long as one ingredient
                # is an alcohol.
                self._alcohol_added = False

                self._recipe_traversal_breakdown(
                    heifa_obj, 
                    portion_size, 
                    ingredient_obj.alcohol_amount
                )

                continue
            
            # For Alcohol, Beverage and/or Water
            self._liquid_calculation(heifa_obj, ingredient_obj, portion_size)
            
            # Calculation for non-recipes
            serving_size = heifa_obj.calculate_serving_size(
                energy_with_fibre, portion_size
            )

            # Add to the daily servings attribute, based on food group
            self.daily_servings = (food_group, serving_size)

        return None

    def _update_single_groups(self, food_group, serving_size):

        # Handle for Alcohol
        if food_group == "Alcohol":
            alcohol_amount = self.daily_servings.get(food_group, 0)
            standard_serves = alcohol_amount / 10
            self.group_servings = ("Alcohol", standard_serves)

            return None

        # Handle for saturated fat
        if food_group == "Saturated Fat":
            sat_fat_amount = self.daily_servings.get(food_group, 0)

            # Convert to energy
            sat_fat_energy = sat_fat_amount * self._grams_to_calories["Fat"]

            # Percentage amount
            # NOTE: Some days, the energy amount can be 0. Don't ask
            total_energy = max(self.total_energy, 1)
            percentage_fat = (sat_fat_energy/total_energy) * 100

            self.group_servings = ("Saturated Fat", percentage_fat)

            return None

        # Handle for unsaturated fat
        if food_group == "Unsaturated Fat":
            
            unsat_fat_amount = self.daily_servings.get(food_group, 0)

            # 1 serving size = 10g
            serve_size = unsat_fat_amount / 10
            self.group_servings = ("Unsaturated Fat", serve_size)

            return None
        
        # Handle for sugar
        if food_group == "Sugar":
            sugar_amount = self.daily_servings.get(food_group, 0)

            sugar_energy = sugar_amount * self._grams_to_calories[food_group]

            # Percentage amount
            # NOTE: Some days, the energy amount can be 0. Don't ask
            total_energy = max(self.total_energy, 1)
            percentage_sugar = (sugar_energy/total_energy) * 100

            self.group_servings = ("Sugar", percentage_sugar)

            return None

         # Handle for water
        if food_group == "Water":
            beverage_amount = self.daily_servings.get("Non-Alcohol", 1)
            amount = (serving_size/beverage_amount) * 100

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

        # Store in this hierarchy: Survey ID -> Food group -> Serving size
        for survey_id, meals_list in meals_daily_list.items():

            # Calculate the servings
            self._find_servings(meals_list)

            # Store individual group servings and total group
            # servings
            total_daily_servings[survey_id] = {
                'individual': self.daily_servings,
                'total': self.group_servings,
                'variations': self.variation_servings
            }

            # Initialize with new dictionary for new date
            # and for energy as well
            del self.daily_servings
            del self.group_servings
            del self.variation_servings
            del self.total_energy

        return total_daily_servings