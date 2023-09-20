

class FoodComposition:

    def __init__(self, info_dict) -> None:

        self._heifa_code = info_dict['heifa_code']
        self._8_digit_code = info_dict['8_digit_code']

        self._is_recipe = self._is_recipe(info_dict['food_group'])
        
        return None
    
    def _is_recipe(self, food_group):

        if "Recipe" in food_group:

            return True
        
        return False
    
    def print_full_details(self):

        print(
            f"Heifa Code: {self._heifa_code}\n",
            f"8 Digit Code: {self._8_digit_code}\n",
            f"Is a recipe: {self._is_recipe}\n"
        )

        return None


