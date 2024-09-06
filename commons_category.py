import requests
from urllib.parse import quote

def get_commons_category_files(category, cmcontinue=None):
    """
    A generator function that yields file names in a Wikimedia Commons category.

    Args:
        category (str): The name of the category to fetch files from.
        cmcontinue (str, optional): The cmcontinue token from the Wikimedia API
                                    for pagination.

    Yields:
        str: The title of each file in the category.
    """
    query_params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtitle': f'Category:{category}',
        'cmtype': 'file',
        'cmlimit': 'max',
        'format': 'json',
    }
    if cmcontinue:
        query_params['cmcontinue'] = cmcontinue

    response = requests.get('https://commons.wikimedia.org/w/api.php',
                            params=query_params).json()

    if 'error' in response:
        print(f"Error: {response['error']['info']}")
        return

    for member in response.get('query', {}).get('categorymembers', []):
        yield member['title']

    if 'continue' in response:
        cmcontinue = response['continue']['cmcontinue']
        yield from get_commons_category_files(category, cmcontinue)


def get_file_usage(file_title):
    """
    Retrieves the usage of a file on Wikimedia projects, excluding usages in
    the User namespace or any Talk namespaces.

    Args:
        file_title (str): The title of the file to check for usage.

    Returns:
        list: A list of dictionaries containing the project and page title
              where the file is used.
    """
    query_params = {
        'action': 'query',
        'prop': 'globalusage',
        'titles': file_title,
        'format': 'json',
        'gulimit': 'max',
    }

    response = requests.get('https://commons.wikimedia.org/w/api.php',
                            params=query_params).json()

    pages_using_file = []

    pages = response.get('query', {}).get('pages', {})
    for page_id, page_data in pages.items():
        global_usage = page_data.get('globalusage', [])
        for usage in global_usage:
            # Exclude user pages
            if usage['title'].startswith('User:') or usage['title'].startswith('User_talk:'):
                continue
            pages_using_file.append({
                'wiki': usage['wiki'],
                'title': usage['title'],
                'url': usage['url']
            })

    return pages_using_file

def get_pages_using_commons_files(category, depth=0):
    """
    Generates a report of pages using files from a Wikimedia Commons category.

    Args:
        category (str): The Commons category to start with.
        depth (int, optional): The maximum depth of subcategories to fetch.
                               Defaults to 0.

    Returns:
        dict: A dictionary containing the file usage report.
    """
    def process_category_files(category, current_depth):
        if current_depth > depth:
            return

        for file in get_commons_category_files(category):
            file_usage = get_file_usage(file)
            results[file] = file_usage

    results = {}

    process_category_files(category, 0)

    return results

if __name__ == "__main__":
    print(get_pages_using_commons_files("National Institute for Occupational Safety and Health facilities", depth=2))
