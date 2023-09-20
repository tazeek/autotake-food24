class Food:

    def __init__(self, heifa_id: str, food_info_dict: dict):

        self._heifa_id = heifa_id

        self._portion_size = food_info_dict['portion_size']
        self._meal_name = food_info_dict['meal_name']

