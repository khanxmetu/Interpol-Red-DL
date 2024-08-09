from notice_saver.models import _OffenseType
from notice_saver.repositories import OffenseTypeRepository
from abc import ABC, abstractmethod

# See:
# scripts/data_cleaning/get_offense_strings.json
# https://chatgpt.com/share/7212fdd6-b6b3-4c9b-9bdb-9233b381bad5
# notice_saver/preload_data/offense_types.json

class OffenseClassifier(ABC):
    """
    An abstract class to handle the classification of arrest warrants' charges/offenses
    into discrete categories as specified in notice_saver/preload_data/offense_types.json
    """
    @abstractmethod
    def classify(self, offense_explanation: str) -> list[_OffenseType]:
        """
        Get offense types based on offense explanation
        """

class GPTOffenseClassifier(OffenseClassifier):
    """
    Classification of offenses using GPT from OpenAI's API
    """
    def classify(self, offense_explanation: str) -> list:
        raise NotImplementedError
    
class BasicOffenseClassifier(OffenseClassifier):
    """
    A class to handle the classification of arrest warrants' charges/offenses
    into discrete categories as specified in notice_saver/preload_data/offense_types.json

    This implementation classifies the offense explanation into offense types by using basic word matching technique.
    If the string as described by offense type is found in the offense explanation, 
     the correspond offense type is assigned to it
    """
    def __init__(self, offense_type_repository: OffenseTypeRepository):
        self._all_offense_type_objs = offense_type_repository.get_all()

    def classify(self, offense_explanation: str) -> list[_OffenseType]:
        related_offense_type_objs = []
        for offense_type_obj in self._all_offense_type_objs:
            offense_type_name = offense_type_obj.value
            if offense_type_name.lower() in offense_explanation.lower():
                related_offense_type_objs.append(offense_type_obj)
        return related_offense_type_objs