from abc import ABC, abstractmethod

from api_poller.models.query_options import QueryOptions


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