from abc import ABC, abstractmethod
from itertools import product

from api_poller.models.query_options import QueryOptions
from api_poller.models.country import Country


class Strategy(ABC):
    """Abstract class representing a strategy to query notice lists"""

    @abstractmethod
    def get_query_options_list(self) -> list[QueryOptions]:
        """Return a list of parameters to be used per notice list search"""


class SimpleDefaultSearch(Strategy):
    """Lookup only the main default notice list page"""

    def get_query_options_list(self) -> list[QueryOptions]:
        query_without_filters = QueryOptions()
        return [query_without_filters]


class SimpleBruteforceSearch(Strategy):
    """Bruteforce the results by using selected filters
    namely: nationality and age"""

    def __init__(
        self,
        nationalities: list[Country] = list(Country),
        ages: list[int] = range(18, 90)
    ) -> None:
        self._nationalities = nationalities
        self._ages = ages

    def get_query_options_list(self) -> list[QueryOptions]:
        values = (product(self._nationalities, self._ages))
        query_options_list = [
            QueryOptions(nationality=country, ageMin=age, ageMax=age)
            for country, age in values
        ]
        return query_options_list
