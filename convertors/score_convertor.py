

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

        self._beverage_survey = 0

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
    def _find_by_gender(cls, keys, serving_size, score_dict):
        minimum_serve, maximum_serve = [score_dict[key] for key in keys]
        return minimum_serve <= serving_size <= maximum_serve

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
    
    def _legumes_allocation_logic(self, *args):

        scores_dict, servings_dict, variations_serving = args

        legumes_alloc_dict = {
            'Vegetables': 0,
            'Meat and alternatives': 0
        }

        # Get the legumes amount
        legumes_amount = variations_serving.get('Vegetables', {}).get('Legumes', 0)

        if legumes_amount == 0:
            return scores_dict, legumes_alloc_dict

        # Get the scores of meat and veg
        meat_scores = scores_dict['Meat and alternatives']
        veg_scores = scores_dict['Vegetables']

        # Find the female score
        # ASSUMPTION: If the female score is maxed out,
        # the male score will be maxed out too (HEIFA Scoring)
        female_score_meat = meat_scores['female_score']
        female_score_veg = veg_scores['female_score']

        def _perform_legumes_logic():
            # Permutations: 
            # Meat max, Veg max -> Allocate all to Veg
            # Meat max, Veg not -> Allocate all to Veg
            # Meat not, Veg max -> Allocate all to Meat
            # Meat not, Veg not -> Split the servings
            veg_allocation = 0
            meat_allocation = 0

            # Check if meat maxed out
            if female_score_meat >= self._max_meat_score:
                veg_allocation = legumes_amount
                return meat_allocation, veg_allocation

            # Check if veg maxed out
            if female_score_veg >= self._max_veg_score:
                meat_allocation = legumes_amount
                return meat_allocation, veg_allocation

            # Do the split (neither meat or veg maxed out)
            veg_allocation = legumes_amount / 2
            meat_allocation = legumes_amount / 4

            return meat_allocation, veg_allocation
        
        # Do the logic. Separate function for return early
        meat_extra, veg_extra = _perform_legumes_logic()

        servings_dict['Meat and alternatives'] += meat_extra
        servings_dict['Vegetables'] += veg_extra

        legumes_alloc_dict['Meat and alternatives'] += meat_extra
        legumes_alloc_dict['Vegetables'] += veg_extra

        # Deduct the existing scores (both male and female)
        # We will re-add them in the scoring function again

        self.male_total = - (meat_scores['male_score'] \
                             + veg_scores['male_score'])
        
        self.female_total = - (meat_scores['female_score'] \
                               + veg_scores['female_score'])

        # Re-run the score for respective food group
        lambda_score_find = lambda group: self._find_score(
            group, servings_dict[group], variations_serving
        )

        scores_dict['Vegetables'] = lambda_score_find('Vegetables')

        scores_dict['Meat and alternatives'] = \
            lambda_score_find('Meat and alternatives')

        return scores_dict, legumes_alloc_dict

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

        # Check if the minimum amount of beverage is fulfilled or not
        if food_group == "Water":

            # Get the beverage range
            beverage_range = self.scores_dict['Total Beverage'][0]

            # Check if fulfilled for both genders
            minimum_fulfilled_male = self._find_by_gender(
                ['minimum_serves_male', 'maximum_serves_male'], self._beverage_survey, beverage_range
            )

            minimum_fulfilled_female = self._find_by_gender(
                ['minimum_serves_female', 'maximum_serves_female'], self._beverage_survey, beverage_range
            )

            # Add in the score if only it is fulfilled
            male_score = male_score if minimum_fulfilled_male else 0
            female_score = female_score if minimum_fulfilled_female else 0

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

            total_servings_dict = servings_dict['total']
            variations_serving = servings_dict['variations']

            # Add in the beverage amount
            self._beverage_survey = total_servings_dict.get('Beverage', 0)

            # Add the keys not in the variations
            # We want to calculate all the groups, regardless of their prescence
            missing_variations = {
                key: 0 for key in self.scores_dict.keys()
                if key not in total_servings_dict
            }

            total_servings_dict.update(missing_variations)

            # We only iterate what is in the HEIFA scores CSV
            scores_converted_dict = {
                food_group: self._find_score(food_group, serving, variations_serving)
                for food_group, serving in total_servings_dict.items()
                if food_group in self.scores_dict
            }

            # Add the variations list
            scores_converted_dict.update(self.variations_total)

            # Perform Legumes logic
            scores_converted_dict, legumes_alloc_dict = \
                self._legumes_allocation_logic(
                    scores_converted_dict.copy(), 
                    total_servings_dict,
                    variations_serving
                )

            heifa_scores[survey_id] = {
                'breakdown': scores_converted_dict,
                'legumes_amount': legumes_alloc_dict,
                'male_total': self.male_total,
                'female_total': self.female_total
            }

            # Reset again
            del self.male_total
            del self.female_total
            del self.variations_total

        return heifa_scores
    