

class ScoreConvertor:

    def __init__(self, heifa_scores_dict):

        self._heifa_scores_dict = heifa_scores_dict
        self._variations_list = ['Fruit', 'Vegetables']

        self._variations_total = {}
        self._male_total = 0
        self._female_total = 0

        self._max_meat_score = self._get_max_score(
            heifa_scores_dict['Meat and alternatives']
        )

        self._max_veg_score = self._get_max_score(
            heifa_scores_dict['Vegetables']
        )

    @property
    def scores_dict(self):
        return self._heifa_scores_dict

    @property
    def variations_list(self):
        return self._variations_list

    @property
    def male_total(self):
        return self._male_total
    
    @property
    def variations_total(self):
        return self._variations_total

    @property
    def female_total(self):
        return self._female_total

    @male_total.setter
    def male_total(self, heifa_score):
        self._male_total += heifa_score

    @female_total.setter
    def female_total(self, heifa_score):
        self._female_total += heifa_score

    @variations_total.setter
    def variations_total(self, setter_tuple):
        name, total = setter_tuple
        self.variations_total[name] = total

    @male_total.deleter
    def male_total(self):
        self._male_total = 0

    @female_total.deleter
    def female_total(self):
        self._female_total = 0

    @variations_total.deleter
    def variations_total(self):
        self._variations_total = {}

    @classmethod
    def _within_range(cls, minimum, maximum, serving_size):
        return minimum <= serving_size <= maximum
    
    def _find_by_gender(self, keys, serving_size, score_dict):

        minimum_serve, maximum_serve = [score_dict[key] for key in keys]
        return self._within_range(minimum_serve, maximum_serve, serving_size)

    @classmethod
    def _fruit_variation_score(cls, variation_dict):
        return 5 if len(variation_dict) >= 2 else 0
    
    @classmethod
    def _get_max_score(cls, scores_range_list):
        return max([score['heifa_score'] for score in scores_range_list])

    @classmethod
    def _vegetables_variation_score(cls, variation_dict):

        # Legumes are a different kind
        legumes_score = 0
        if "Legumes" in variation_dict:
            legumes_servings = variation_dict['Legumes']
            legumes_score = 1 if legumes_servings >= 0.5 else 0
            del variation_dict['Legumes']

        variation_score = sum(
            [1 for serving in variation_dict.values() if serving >= 1]
        ) + legumes_score

        return min(variation_score, 5)
    
    def _allocate_legumes_groups(self, scores_converted_dict):


        def perform_allocation_logic(current_score):
            # Deduct for now

            # Check for legumes logic via the permutations
            # - Veg max, Meat not -> Allocate to meat
            # - Veg max, Meat max -> Allocate to vegetables
            # - Veg not, Meat not -> Allocate half
            # - Veg not, Meat max -> Allocate to vegetables

            # If meat is max, we allocate to vegetables 
            # regardless of how much vegetables serving it is
            if current_score >= self._max_meat_score:

                return None
                ...

            # If vegetables is max, we allocate all to meat
            if current_score >= self._max_veg_score:

                return None
                ...

            # If neither, we divide based on:
            # - Vegetables: divide by 2
            # - Meat: divide by 4
            # Reference: HEIFA calculation

            return None

        # Get the current scores of vegetables and meat (both)
        heifa_meat = scores_converted_dict['Meat and alternatives']
        heifa_veg = scores_converted_dict['Vegetables']

        return None

    def _get_variation_function(self, variation_key):
        return {
            'Vegetables': self._vegetables_variation_score,
            'Fruit': self._fruit_variation_score
        }[variation_key]
    
    def _find_score(self, food_group, serving, variations_serving):

        male_score, female_score = None, None

        # Extract the given group from the HEIFA scores
        scores_list = self.scores_dict[food_group]

        # Round to 2 decimal places
        serving = round(serving, 2)

        for score_dict in scores_list:

            # Find the scores (male)
            range_found_male = self._find_by_gender(
                ['minimum_serves_male', 'maximum_serves_male'], serving, score_dict
            )

            if (range_found_male) and (not male_score):
                male_score = score_dict['heifa_score']

            # Find the scores (female)
            range_found_female = self._find_by_gender(
                ['minimum_serves_female', 'maximum_serves_female'], serving, score_dict
            )

            if (range_found_female) and (not female_score):
                female_score = score_dict['heifa_score']

            # Break if both are found
            if male_score and female_score:
                break

        # Assign default value of 0 if nothing is found
        male_score = 0 if male_score is None else male_score
        female_score = 0 if female_score is None else female_score

        # Check if group is in the variation list
        # If it is, find the breakdown
        if (food_group in self.variations_list) and (food_group in variations_serving):

            variation_function = self._get_variation_function(food_group)
            bonus_points = variation_function(variations_serving[food_group].copy())

            # Add to the total of variations
            key_name = f"{food_group} - variations score"
            self.variations_total = (key_name, bonus_points)

            male_score += bonus_points
            female_score += bonus_points

        # Sum up the grand total
        self.male_total = male_score
        self.female_total = female_score

        return {
            'male_score': male_score,
            'female_score': female_score
        }
        
    def transform_servings_score(self, daily_servings: dict) -> dict:

        heifa_scores = {}

        for survey_id, servings_dict in daily_servings.items():
            print(servings_dict)
            total_servings_dict = servings_dict['total']
            variations_serving = servings_dict['variations']

            # Add the keys not in the variations
            # We want to calculate all the groups, regardless of their prescence
            missing_variations = {
                key: 0 for key in self.scores_dict.keys()
                if key not in total_servings_dict
            }

            total_servings_dict.update(missing_variations)

            scores_converted_dict = {
                food_group: self._find_score(food_group, serving, variations_serving)
                for food_group, serving in total_servings_dict.items()
                if food_group in self.scores_dict
            }

            # Add the variations list
            scores_converted_dict.update(self.variations_total)

            # Handle legumes, if it is present
            if 'Legumes' != 0:
                self._allocate_legumes_groups(scores_converted_dict)

            heifa_scores[survey_id] = {
                'breakdown': scores_converted_dict,
                'male_total': self.male_total,
                'female_total': self.female_total
            }

            # Reset again
            del self.male_total
            del self.female_total
            del self.variations_total

        return heifa_scores
    