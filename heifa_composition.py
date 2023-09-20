

class FoodComposition:

    def __init__(self, info_dict) -> None:

        self._heifa_code = info_dict['heifa_code']
        self._8_digit_code = info_dict['8_digit_code']
        
        return None
    
    def print_full_details(self):

        print(
            f"Heifa Code: {self._heifa_code}\n",
            f"8 Digit Code: {self._8_digit_code}\n"
        )
        
        return None


