Python functions to retrieve lists of article URLs. Currently this includes:

* Category membership, including custom category depth
* Wikidata Query Service queries, with "?item" for the Wikidata item ID and "?article" for the article URL

Future plans include:
* Compositions, which are either unions or intersections of existing lists, including other compositions

## Setup

1. `git clone https://github.com/scatter-llc/pageset`

2. `cd pageset`

3. `python3 -m venv venv`

4. `source venv/bin/activate`

5. `pip3 install -r requirements.txt`

## Operation

Generate list of vaccine safety-related pages:

```
python3 get_list.py
```
