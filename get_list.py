from . import category
from . import wikidata

def get_vsafe_set():
    search_depth = 2

    # Vaccine- and vaccine hesitancy-related categories on English Wikipedia
    categories_list = [
        "Vaccines",
        "Vaccine hesitancy",
        "World Health Organization essential medicines (vaccines)",
        "Anti-vaccination activists",
        "Anti-vaccination in the United States",
        "Anti-vaccination media",
        "Anti-vaccination organizations",
        "COVID-19 vaccine misinformation and hesitancy",
        "Animal vaccines",
        "Cancer vaccines",
        "Combination vaccines",
        "COVID-19 vaccines",
        "COVID-19 vaccines by country",
        "Deployment of COVID-19 vaccines",
        "COVID-19 vaccination by continent",
        "Hepatitis vaccines",
        "HIV vaccine research",
        "Inactivated vaccines",
        "Influenza vaccines",
        "Live vaccines",
        "Meningococcal vaccines",
        "MMR vaccine and autism",
        "Nucleic acid vaccines",
        "DNA vaccines",
        "RNA vaccines",
        "Smallpox vaccines",
        "Subunit vaccines",
        "Toxoid vaccines",
        "Tuberculosis vaccines",
        "Vaccines against drugs",
        "Vaccinia",
        "Viral vector vaccines"
    ]

    # Instance of "vaccine type"
    sparql_query_1 = """
    SELECT ?item ?article WHERE {
      ?item wdt:P31* wd:Q105967696.
      ?article schema:about ?item;
               schema:isPartOf <https://en.wikipedia.org/>.
    }
    """

    # Journals with "Vaccine" in their name
    sparql_query_2 = """
    SELECT DISTINCT ?item ?article WHERE {
      ?item wdt:P31 wd:Q5633421;
      rdfs:label ?itemLabel.
      FILTER(CONTAINS(?itemLabel, "Vaccine"))
      ?article schema:about ?item;
               schema:isPartOf <https://en.wikipedia.org/>.
    }
    """

    category_set = category.get_pages_and_subcategories(categories_list, search_depth)['pages']
    sparql_set_1 = set(wikidata.get_articles_from_sparql(sparql_query_1))
    sparql_set_2 = set(wikidata.get_articles_from_sparql(sparql_query_2))

    pageset = category_set | sparql_set_1 | sparql_set_2
    return sorted(list(pageset))

if __name__ == '__main__':
    L = get_vsafe_set()
    for p in L:
        print(p)
