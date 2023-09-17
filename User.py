

class User:

    def __init__(self, id):

        self._id = id
        self._surveys = {}
    
    def add_survey(self, survey_id, survey):

        self._surveys[survey_id] = survey

    def print_user_nutrition(self):

        # Extract the surveys

        # Go meal by meal in surveys

        # Print out
        ...
