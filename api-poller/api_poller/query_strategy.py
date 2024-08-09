from abc import ABC, abstractmethod
from itertools import product
import string
from typing import Optional

from api_poller.models.query_options import QueryOptions
from api_poller.models.country import Country
from api_poller.models.sex import Sex


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


class BruteforceSearch(Strategy):
    """
    Bruteforce the results by using selected filters namely:
        arrest warrant issuing country, age, nationality, gender and name
    in that order.

    A filter can be disabled by simply setting it to None.
    """

    def __init__(
        self,
        wanted_by_countries: Optional[list[Country]] = None,
        ages: Optional[list[int]] = None,
        nationalities: Optional[list[Country]] = None,
        genders: Optional[list[Sex]] = None,
        names: Optional[list[str]] = None,
    ):
        self._wanted_by_countries = wanted_by_countries
        self._ages = ages
        self._nationalities = nationalities
        self._genders = genders
        self._names = names

    def get_query_options_list(self) -> list[QueryOptions]:
        wanted_buy_countries = (
            self._wanted_by_countries if self._wanted_by_countries else [None]
        )
        ages = self._ages if self._ages else [None]
        nationalities = self._nationalities if self._nationalities else [None]
        genders = self._genders if self._genders else [None]
        names = self._names if self._names else [None]
        values = product(
            wanted_buy_countries,
            ages,
            nationalities,
            genders,
            names,
        )
        query_options_list = [
            QueryOptions(
                nationality=nationality,
                ageMin=age,
                ageMax=age,
                arrestWarrantCountryId=wanted_by_country,
                sexId=gender,
                name=name,
            )
            for wanted_by_country, age, nationality, gender, name in values
        ]
        return query_options_list


class CompositeStrategy(Strategy):
    def __init__(self, strategies: list[Strategy]):
        self._strategies = strategies

    def get_query_options_list(self) -> list[QueryOptions]:
        query_options_list = []
        for strategy in self._strategies:
            query_options_list.extend(strategy.get_query_options_list())
        return query_options_list


wanted_by_countries_exceeding_limit = [
    Country.AR,
    Country.IN,
    Country.RU,
    Country.SV,
    Country.US,
]


class QueryStrategyFactory:
    minimal_bruteforce_search = CompositeStrategy(
        [
            # Countries with notices within limit
            BruteforceSearch(
                wanted_by_countries=[
                    country
                    for country in Country
                    if country not in wanted_by_countries_exceeding_limit
                ]
            ),
            # where additionally adding all ages filter is enough to get notices within limit
            BruteforceSearch(
                wanted_by_countries=[
                    country
                    for country in wanted_by_countries_exceeding_limit
                    if country != Country.RU
                ],
                ages=range(18, 100),
            ),
            # where additionally adding all ages filter was not enough but limited ages can be added
            # limited ages added
            BruteforceSearch(
                wanted_by_countries=[Country.RU],
                ages=[age for age in range(18, 100) if age not in range(31, 39)],
            ),
            # where additionally adding ages filter was not enough (extra filter needed)
            # nationalities filter added
            BruteforceSearch(
                wanted_by_countries=[Country.RU],
                ages=range(31, 39),
                nationalities=[
                    country for country in list(Country) if country != Country.RU
                ],
            ),
            # where additionally adding nationalities filter was not enough (extra filter needed)
            # all filters are added for them
            BruteforceSearch(
                wanted_by_countries=[Country.RU],
                ages=range(31, 39),
                nationalities=[Country.RU],
                genders=list(Sex),
                names=list(string.ascii_lowercase),
            ),
        ]
    )

    simple_default_search = SimpleDefaultSearch()

    @classmethod
    def get_by_id(cls, id: int) -> Strategy:
        if id == 0:
            return cls.simple_default_search
        else:
            return cls.minimal_bruteforce_search

    @classmethod
    def get_minimal_bruteforce_search(cls) -> CompositeStrategy:
        return cls.minimal_bruteforce_search

    @classmethod
    def get_simple_default_search(cls) -> SimpleDefaultSearch:
        return cls.simple_default_search
