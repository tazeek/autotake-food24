class Food:

    def __init__(self, food_info_dict: dict):

        self._portion_size = food_info_dict['portion_size']
        self._energy_with_fibre = food_info_dict['energy_with_fibre']

