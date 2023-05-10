import requests
from urllib.parse import quote

def get_category_members(category, current_depth, cmcontinue=None, lang='en'):
    query_params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtitle': f'Category:{category}',
        'cmtype': 'page|subcat',
        'cmlimit': 'max',
        'format': 'json',
    }
    if cmcontinue:
        query_params['cmcontinue'] = cmcontinue

    response = requests.get(f'https://{lang}.wikipedia.org/w/api.php', params=query_params).json()

    if 'error' in response:
        print(f"Error: {response['error']['info']}")
        return

    for member in response.get('query', {}).get('categorymembers', []):
        yield member, current_depth

    if 'continue' in response:
        cmcontinue = response['continue']['cmcontinue']
        yield from get_category_members(category, current_depth, cmcontinue, lang)

def get_pages_and_subcategories(categories, depth=0, lang='en'):
    def process_category_members(category, current_depth):
        for member, current_depth in get_category_members(category, current_depth):
            title = member['title']
            encoded = quote(title.replace(' ', '_'))
            ns = member['ns']
            if ns == 14 and current_depth < depth:  # Namespace 14 corresponds to categories
                subcategory = title.replace("Category:", "")
                results['categories'].add(subcategory)
                process_category_members(subcategory, current_depth + 1)
            elif ns == 0:  # Namespace 0 corresponds to main articles
                results['pages'].add(f"https://{lang}.wikipedia.org/wiki/{encoded}")

    results = {
        'pages': set(),
        'categories': set()
    }

    for category in categories:
        process_category_members(category, 0)

    return results
