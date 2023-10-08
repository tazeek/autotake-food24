

class ScoreConvertor:

    def __init__(self, heifa_scores_dict):

        self._heifa_scores_dict = heifa_scores_dict

        return None
    
    @property
    def scores_dict(self):
        return self._heifa_scores_dict
    
    def _within_range(self, minimum, maximum, serving_size):

        return ((serving_size >= minimum) and (serving_size <= maximum))
    
    def _find_score(self, food_group, serving_size):

        male_score, female_score = False, False

        # Extract the given group
        scores_list = self.scores_dict[food_group]

        print(f"Food group: {food_group}")

        for score_dict in scores_list:

            # Find the scores (male)
            minimum_serve = score_dict['minimum_serves_male']
            maximum_serve = score_dict['maximum_serves_male']
            
            range_found_male = self._within_range(minimum_serve, maximum_serve, serving_size)

            if range_found_male and not male_score:
                print(f"Minimum (Male): {minimum_serve}")
                print(f"Maximum (Male): {maximum_serve}")
                
                male_score = score_dict['heifa_score']
                print(f"- HEIFA Score (Male): {male_score}\n")

            # Find the scores (female)
            minimum_serve_female = score_dict['minimum_serves_female']
            maximum_serve_female = score_dict['maximum_serves_female']
            
            range_found_female = self._within_range(minimum_serve_female, maximum_serve_female, serving_size)

            if range_found_female and not female_score:
                print(f"Minimum (Female): {minimum_serve_female}")
                print(f"Maximum (Female): {maximum_serve_female}")

                female_score = score_dict['heifa_score']
                print(f"- HEIFA Score (Female): {female_score}")

            # Break if both are found
            if male_score and female_score:
                break
        
        return {
            'male_score': male_score,
            'female_score': female_score
        }
        
    def transform_servings_score(self, daily_servings: dict):

        heifa_scores = {}

        for date, total_servings_dict in daily_servings.items():

            #self._find_score(food_group, serving_size)
            #for food_group, serving_size in total_servings_dict.items()

            #male_score, female_score = self._find_score()
            heifa_scores[date] = {
                food_group: self._find_score(food_group, serving_size)
                for food_group, serving_size in total_servings_dict.items()
                if food_group in self.scores_dict
            }
        
        return heifa_scores