

class User:

    def __init__(self, id):

        self._id = id
        self._surveys = {}
    
    def add_survey(self, survey_id, survey):

        self._surveys[survey_id] = survey

    def _print_meals(self, survey_obj):

        for id, meal_obj in survey_obj.items():


            heifa_codes = meal_obj.heifa_list

            print(f"HEIFA code for Meal {id}: {heifa_codes}\n")

        return None

    def print_nutrition(self):

        for id, survey_obj in self._surveys.items():
            
            # Go by surveys
            print(f"Printing for Survey ID {id}\n")

            # Print out one meal per survey
            self._print_meals(survey_obj)
            
        return None
