from Survey import Survey

class User:

    def __init__(self, id):

        self._id = id
        self._surveys = {}

    @property
    def surveys(self):
        return self._surveys
    
    @surveys.setter
    def surveys(self, survey_tuple):

        # Unpack the tuples
        survey_id, survey_date = survey_tuple

        # Add if it does not exist
        if survey_id not in self.surveys:
            self.surveys[survey_id] = Survey(survey_date)

        return None

    def get_survey(self, survey_id, survey_date=None) -> Survey:

        # Use the setter, regardless
        # The setter will handle it
        self.surveys = (survey_id, survey_date)

        return self.surveys[survey_id]

    def print_information(self):

        for id, survey_obj in self.surveys.items():
            
            # Go by surveys
            print(f"Printing for Survey ID {id} on date {survey_obj.date}\n")

            # Print out one meal per survey
            survey_obj.print_meals()
            print("\n\n")
            
        return None


    def get_meals_information(self):

        all_food_information = {}

        # Go by surveys
        for survey_id, survey_obj in self.surveys.items():

            # Get the meal objects dictionary
            meals_obj = survey_obj.meals

            #all_food_information[survey_date] = meal_date_list
            all_food_information[survey_id] = [meal.nutrition for meal in meals_obj.values()]

        return all_food_information
