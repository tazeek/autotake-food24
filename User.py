

class User:

    def __init__(self, id):

        self._id = id
        self._surveys = {}
    
    def add_survey(self, survey_id, survey):

        self._surveys[survey_id] = survey

    def _meals_output(self, meal_obj):

        heifa_codes = meal_obj.heifa_list
        print(heifa_codes)
        print("\n")
        return None

    def print_user_nutrition(self):

        for id, survey_obj in self._surveys.items():
            
            # Go meal by meal in surveys
            print(f"Printing for Survey ID {id}\n")
            meals_obj_list = survey_obj.meals_intake.values()

            # Print out
            [self._meals_output(meal_obj) for meal_obj in meals_obj_list]
        
        return None
