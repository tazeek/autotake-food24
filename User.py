

class User:

    def __init__(self, id):

        self._id = id
        self._surveys = {}
    
    def add_survey(self, survey_id, survey):

        self._surveys[survey_id] = survey

    def print_user_nutrition(self):

        for survey_obj in self._surveys.values():
            
            # Go meal by meal in surveys
            meals_obj_list = survey_obj.meals_intake.values()

        # Print out
        ...
