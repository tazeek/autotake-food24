class Food:

    def __init__(self, food_info_dict: dict):

        self._portion_size = food_info_dict['portion_size_consumed']
        self._energy_with_fibre = food_info_dict['energy_with_fibre']

    @property
    def portion_size(self):
        return self._portion_size
    
    @property
    def energy_with_fibre(self):
        return self._energy_with_fibre

