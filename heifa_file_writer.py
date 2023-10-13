

class HeifaFileWriter():

    def __init__(self, scores_dict, composition_dict):

        self._scores = scores_dict
        self._composition = composition_dict

        return None
    
    @property
    def scores(self):
        return self._scores

    @property
    def composition(self):
        return self._composition

    def create_column_names(self):
        ...