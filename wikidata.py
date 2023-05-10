import requests

def get_articles_from_sparql(sparql_query):
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
