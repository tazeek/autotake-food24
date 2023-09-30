from Survey import Survey

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
        # The setter will handle it
        self.surveys = survey_id

        return self.surveys[survey_id]

    def print_information(self):

        for id, survey_obj in self.surveys.items():
            
            # Go by surveys
            print(f"Printing for Survey ID {id}\n")

            # Print out one meal per survey
            survey_obj.print_meals()
            print("\n\n")
            
        return None


    def get_meals_information(self):

        all_food_information = []

        # Go by surveys
        for survey_obj in self.surveys.values():

            # Get the meal objects
            meals_obj = survey_obj.meals

            # Store in array
            all_food_information += [meal.nutrition for meal in meals_obj]

        return all_food_information
