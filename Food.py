class Food:

    def __init__(self, food_info_dict: dict):

        self._portion_size = food_info_dict['portion_size']
        self._meal_name = food_info_dict['meal_name']

