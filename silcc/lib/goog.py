"""ser and sery functions return number of search results for goog/yahoo"""

import json
import urllib
from yahoo.search.web import WebSearch

def ser(query_):
    """Returns estimated number of results from Google Web Search"""
    query = urllib.urlencode({'q': query_})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.urlopen(url)
    search_results = search_response.read()
    results = json.loads(search_results)
    data = results['responseData']
    return data['cursor']['estimatedResultCount']

#Add Python PySearch Package for this to work
def sery(query_):
    """Returns estimated number of results from Yahoo Web Search"""
    srch = WebSearch('YahooDemo', query = query_)
    res = srch.parse_results()
    return res.total_results_available


