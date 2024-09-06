import requests

api_url = "https://query-api.orbopengraph.com"
api_endpoint = "/data/"

def get_articles_from_query_id(query_id):
    response = requests.get(api_url + api_endpoint + query_id)

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
        print("Request: " + api_url + api_endpoint + query_id)
        print(response.text)
        return []

#print(get_articles_from_query_id('osh-hazards-chemical-with-exposure-items'))
