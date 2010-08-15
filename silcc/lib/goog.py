#!/usr/bin/python
import json
import sys
import urllib
from yahoo.search.web import WebSearch

def ser(query_):
    query = urllib.urlencode({'q': query_})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.urlopen(url)
    search_results = search_response.read()
    results = json.loads(search_results)
    data = results['responseData']
    return data['cursor']['estimatedResultCount']

def sery(query_):
    srch = WebSearch('YahooDemo',query = query_)
    res = srch.parse_results()
    return res.total_results_available


