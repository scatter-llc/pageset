"""
Defines a function `get_articles_from_sparql` that retrieves articles
from Wikidata using a given SPARQL query.

Functions:
    get_articles_from_sparql(sparql_query: str) -> List[str]:
        Sends a SPARQL query to the Wikidata query service and returns a list of article URIs.
"""

import requests


def get_articles_from_sparql(sparql_query):
    """
    Sends a SPARQL query to the Wikidata query service and returns a list of articles.

    Args:
        sparql_query (str): A string containing the SPARQL query to execute.

    Returns:
        List[str]: A list of article URLs from the query results, or an empty list if the query fails.
    """

    url = 'https://query.wikidata.org/sparql'
    headers = {
        'User-Agent': 'Pageset/0.0.1',
        'Accept': 'application/sparql-results+json'
    }
    
    response = requests.get(url, headers=headers, params={'query': sparql_query})
    
    if response.status_code == 200:
        json_response = response.json()
        bindings = json_response.get('results', {}).get('bindings', [])
        
        articles = []
        for binding in bindings:
            article = binding.get('article', {}).get('value')
            if article:
                articles.append(article)
                
        return articles
    else:
        print(f"Error: {response.status_code}")
        return []
