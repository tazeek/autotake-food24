from Survey import Survey

class User:

    def __init__(self, id):

        self._id = id
        self._surveys = {}

    @property
    def surveys(self):
        return self._surveys
    
    @surveys.setter
    def add_survey(self, survey_id):

        # Check if ID exists
        # If it does, no need to do anything
        if survey_id in self.surveys:
            return None
        
        self._surveys[survey_id] = Survey()

        return None

    def get_survey(self, survey_id) -> Survey:

        # Use the setter, regardless
        # The setter will handle it
        self.surveys = survey_id

        return self.surveys[survey_id]

    def print_information(self):

        for id, survey_obj in self._surveys.items():
            
            # Go by surveys
            print(f"Printing for Survey ID {id}\n")

            # Print out one meal per survey
            survey_obj.print_meals()
            print("\n\n")
            
        return None


    def get_meals_information(self):

        all_food_information = []

        # Go by surveys
        for survey_obj in self._surveys.values():

            # Get the meal objects
            meals_obj = survey_obj.get_meals

            # Store in array
            all_food_information += [meal.nutrition_info for meal in meals_obj]

        return all_food_information
