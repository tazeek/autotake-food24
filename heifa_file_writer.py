

class HeifaFileWriter():

    def __init__(self, scores_dict, composition_dict):

        self._scores = scores_dict
        self._composition = composition_dict

        self._column_names = [
            'Survey_ID', 'User_ID', 
            'HEIFA total score (Male)',	
            'HEIFA total score (Female)'
        ]

        self._row_data = {}
    
    @property
    def scores(self):
        return self._scores

    @property
    def composition(self):
        return self._composition
    
    @property
    def column_names(self):
        return self._column_names
    
    @property
    def row_data(self):
        return self._row_data
    
    @row_data.setter
    def row_data(self, input_info):

        # Reseting the information
        if isinstance(input_info, dict):
            self._row_data = input_info
            return None
        
        key, value = input_info
        self._row_data[key] = value

        return None
    
    @column_names.setter
    def column_names(self, name: list):
        self.column_names.extend(name)

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
    
    def _handle_variations_servings(self, food_group, variations_dict):
        
        for sub_group, serving_size in variations_dict.items():

            key_name = "Legumes" if sub_group == "Legumes" \
                else f"{food_group}/{sub_group}"
            
            self.row_data = (key_name, serving_size)
    
    def _fill_up_data(self, heifa_scores, food_group_dict):

        # Get the dictionaries
        total_dict = food_group_dict['total']
        variations_dict = food_group_dict['variations']

        for food_group, total_serving in total_dict.items():

            # Key for the main group
            key_name = f"{food_group} - serves size"
            if key_name not in self.row_data:
                continue
            
            # Add to the row (serving size)
            self.row_data = (key_name, total_serving)

            # Get the HEIFA scores
            heifa_key_name_male = f"{food_group} - HEIFA score (Male)"
            heifa_key_name_female = f"{food_group} - HEIFA score (Female)"

            gender_scores = heifa_scores['breakdown'][food_group]

            self.row_data = (heifa_key_name_male, gender_scores['male_score'])
            self.row_data = (heifa_key_name_female, gender_scores['female_score'])

            if food_group in variations_dict:

                self._handle_variations_servings(
                    food_group, variations_dict[food_group]
                )

    def _create_column_names(self):

        # Then we create the keys in the format:
        # - Serving count (We will call this Discretionary) ("Food group")
        structure_dict = self._extract_groups_structure()

        # Create a dictionary on the metric measurement
        # Example: Sodium -> mg (milligrams)
        group_metrics = {
            'Sodium': 'mg (milligrams)',
            'Alcohol': 'standard serves',
            'Water': '%'
        }

        # Storage order: HEIFA scores, Serve size, Sub-groups
        for main_group, sub_group in structure_dict.items():
            
            heifa_keys = [
                f"{main_group} - HEIFA score ({gender})" 
                for gender in ['Male', 'Female']
            ]

            # Get the key name
            # Default: " serves size"
            metric = group_metrics.get(main_group, "serve size")
            main_group_key = f"{main_group} - {metric}"

            self.column_names = heifa_keys + [main_group_key]

            if len(sub_group) != 0:
                self.column_names = sub_group
    
    def create_row_data(self, user_intake, user_scores):

        # Create the columns
        self._create_column_names()

        # Default row
        empty_row = {
            key: None
            for key in self.column_names
        }

        rows_list = []

        for user_id, daily_intake_dict in user_intake.items():

            for survey_id, food_group_dict in daily_intake_dict.items():

                # Initialize the empty row
                self.row_data = empty_row.copy()

                # Fill up User ID and Survey ID
                self.row_data = ('User_ID', user_id)
                self.row_data = ('Survey_ID', survey_id)

                heifa_scores = user_scores[user_id][survey_id]

                # Move to groups and sub-groups
                self._fill_up_data(heifa_scores, food_group_dict)

                self.row_data = ('HEIFA total score (Male)', heifa_scores['male_total'])
                self.row_data = ('HEIFA total score (Female)', heifa_scores['female_total'])

                # Add to the row
                rows_list.append(self.row_data)
        
        return self.column_names, rows_list
