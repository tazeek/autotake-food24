from classes.Survey import Survey

class User:

    def __init__(self, id):

        self._id = id
        self._surveys = {}

    @property
    def surveys(self):
        return self._surveys
    
    @surveys.setter
    def surveys(self, survey_id):

        # Add if it does not exist
        if survey_id not in self.surveys:
            self.surveys[survey_id] = Survey()

        return None

    def get_survey(self, survey_id) -> Survey:

        # Use the setter, regardless
        # The setter will handle i
        self.surveys = survey_id

        return self.surveys[survey_id]

    def get_meals_information(self):

        all_food_information = {}

        # Go by surveys
        for survey_id, survey_obj in self.surveys.items():

            # Get the meal objects dictionary
            meals_obj = survey_obj.meals

            #all_food_information[survey_date] = meal_date_list
            all_food_information[survey_id] = [meal.nutrition for meal in meals_obj.values()]

        return all_food_information
