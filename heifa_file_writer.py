

class HeifaFileWriter():

    def __init__(self, scores_dict, composition_dict):

        self._scores = scores_dict
        self._composition = composition_dict

        self._column_names = ['Survey_ID', 'User_ID']

        return None
    
    @property
    def scores(self):
        return self._scores

    @property
    def composition(self):
        return self._composition
    
    @property
    def column_names(self):
        return self._column_names
    
    @column_names.setter
    def column_names(self, name: list):
        self.extend(name)

    def _extract_groups_structure(self):

        # First we extract all the groups
        groups_dict = {
            food_group: set()
            for food_group in self.scores.keys()
        }

        # Then, we store the sub-groups for the given groups
        for food_comp_obj in self.composition.values():

            food_group = food_comp_obj.food_group

            # Handle for legumes
            if food_group == "Legumes":
                groups_dict['Vegetables'].add(food_group)

            # Skip over no backslashes
            if '/' not in food_group:
                continue

            main_group, sub_group = food_group.split('/')

            # Watch out for Wholegrains
            if (main_group not in groups_dict) \
                or (sub_group in groups_dict):
                continue

            groups_dict[main_group].add(food_group)

        return groups_dict

    def create_column_names(self):

        # Then we create the keys in the format:
        # - Serving count (We will call this Discretionary) ("Food group")
        structure_dict = self._extract_groups_structure()

        # - Male (We will call this Discretionary - HEIFA score (Male)) ("Food group - HEIFA score (Male)")
        # - Female (We will call this Discretionary - HEIFA score (Female)) ("Food group - HEIFA score (Female)")
        # Storage order: HEIFA scores, Serve size, Sub-groups
        for main_group, sub_group in structure_dict.items():
            ...
        ...