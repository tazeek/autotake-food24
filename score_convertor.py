

class ScoreConvertor:

    def __init__(self, heifa_scores_dict):

        self._heifa_scores_dict = heifa_scores_dict
        self._variations_list = ['Fruit', 'Vegetables']
        return None
    
    @property
    def scores_dict(self):
        return self._heifa_scores_dict
    
    @property
    def variations_list(self):
        return self._variations_list
    
    def _within_range(self, minimum, maximum, serving_size):

        return ((serving_size >= minimum) and (serving_size <= maximum))

    def _find_by_gender(self, keys, serving_size, score_dict):
        
        minimum_serve, maximum_serve = [score_dict[key] for key in keys]
        return self._within_range(minimum_serve, maximum_serve, serving_size)
    
    def _fruit_variation_score(self, variation_dict):
        print("FRUIT!")
        return None

    def _vegetables_variation_score(self, variation_dict):

        print(variation_dict)
        variation_score = sum(
            [1 for _, serving in variation_dict.items() if serving >= 1]
        )
        print(variation_score)
        print("VEGGIE!\n")
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

        # Round to 1 decimal place
        serving = round(serving, 1)

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

        # Check if group is in the variation list
        # If it is, find the breakdown
        if food_group in self.variations_list:
            variation_function = self._get_variation_function(food_group)
            variation_function(variations_serving[food_group])

        return {
            'male_score': male_score,
            'female_score': female_score
        }
        
    def transform_servings_score(self, daily_servings: dict):

        heifa_scores = {}

        for date, servings_dict in daily_servings.items():

            total_servings_dict = servings_dict['total']
            variations_serving = servings_dict['variations']

            scores_converted_dict = {
                food_group: self._find_score(food_group, serving, variations_serving)
                for food_group, serving in total_servings_dict.items()
                if food_group in self.scores_dict
            }

            heifa_scores[date] = scores_converted_dict
        
        return heifa_scores