

class User:

    def __init__(self, id):

        self._id = id
        self._surveys = {}
    
    def add_survey(self, survey_id, survey):

        self._surveys[survey_id] = survey

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
            meals_obj = survey_obj.get_meals()

            # Store in array
            all_food_information += [meal.get_food_information() for meal in meals_obj]

        return all_food_information
