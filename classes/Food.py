class Food:

    def __init__(self, food_info_dict: dict):

        self._portion_size = food_info_dict['portion_size_consumed']
        self._energy_with_fibre = food_info_dict['energy_with_fibre']
        self._sodium_consumed = food_info_dict['sodium_consumed']
        self._alcohol_amount = food_info_dict['alcohol_consumed']
        self._sugar_amount = food_info_dict['sugar_amount']
        self._saturated_fat_amount = food_info_dict['saturated_fat_amount']
        self._unsaturated_fat_mono_amount = food_info_dict['unsaturated_fat_mono_amount']
        self._unsaturated_fat_poly_amount = food_info_dict['unsaturated_fat_poly_amount']

    @property
    def portion_size(self):
        return float(self._portion_size)
    
    @property
    def energy_with_fibre(self):
        return float(self._energy_with_fibre)
    
    @property
    def sodium_consumed(self):
        return float(self._sodium_consumed)

    @property
    def alcohol_amount(self):
        return float(self._alcohol_amount)
    
    @property
    def sugar_amount(self):
        return float(self._sugar_amount)
    
    @property
    def saturated_fat_amount(self):
        return float(self._saturated_fat_amount)
    
    @property
    def unsaturated_fat_mono_amount(self):
        return float(self._unsaturated_fat_mono_amount)

    @property
    def unsaturated_fat_poly_amount(self):
        return float(self._unsaturated_fat_poly_amount)

