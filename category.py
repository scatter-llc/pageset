"""
Retrieves lists of Wikipedia articles and subcategories based on category
membership.

Functions:
    get_category_members(category, current_depth, cmcontinue=None, lang='en')
    get_pages_and_subcategories(categories, depth=0, lang='en')
"""

import requests
from urllib.parse import quote


def get_category_members(category, current_depth, cmcontinue=None, lang='en'):
    """
    A generator function that yields Wikipedia category members (pages and
    subcategories) for a given category and language.

    Args:
        category (str): The name of the category to fetch members from.
        current_depth (int): The current depth of category recursion.
        cmcontinue (str, optional): The cmcontinue token from the Wikipedia API
                                    for pagination.
        lang (str, optional): The language of the Wikipedia edition to fetch
                              data from. Defaults to 'en'.

    Yields:
        tuple: A tuple containing the member dictionary and the current depth.
    """
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

    response = requests.get(f'https://{lang}.wikipedia.org/w/api.php',
                                params=query_params).json()

    if 'error' in response:
        print(f"Error: {response['error']['info']}")
        return

    for member in response.get('query', {}).get('categorymembers', []):
        yield member, current_depth

    if 'continue' in response:
        cmcontinue = response['continue']['cmcontinue']
        yield from get_category_members(category, current_depth,
                                            cmcontinue, lang)


def get_pages_and_subcategories(categories, depth=0, lang='en'):
    """
    Retrieves the Wikipedia pages and subcategories for a list of categories up
    to a specified depth.

    Args:
        categories (list of str): A list of category names to fetch pages and
                                  subcategories from.
        depth (int, optional): The maximum depth of subcategories to fetch.
                                Defaults to 0.
        lang (str, optional): The language of the Wikipedia edition to fetch
                              data from. Defaults to 'en'.

    Returns:
        dict: A dictionary containing two sets: 'pages' and 'categories'.
              'pages' contains the URLs of the Wikipedia pages,
              'categories' contains the names of the subcategories.
    """
    def process_category_members(category, current_depth):
        for member, current_depth in get_category_members(category, current_depth):
            title = member['title']
            encoded = quote(title.replace(' ', '_'))
            ns = member['ns']
            # Namespace 14 corresponds to categories
            if ns == 14 and current_depth < depth:
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
