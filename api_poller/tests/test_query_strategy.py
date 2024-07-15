from api_poller.query_strategy import SimpleDefaultSearch
from api_poller.models.query_options import QueryOptions

def test_simple_default_search_get_query_options_list():
    query_options_lst: QueryOptions = SimpleDefaultSearch().get_query_options_list()
    assert len(query_options_lst) == 1
    assert type(query_options_lst[0]) == QueryOptions
    assert query_options_lst[0].get_options_dict() == {"resultPerPage": 160}