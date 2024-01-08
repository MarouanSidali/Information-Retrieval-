# search_engine.py
from index_loader import IndexLoader
from query_processor import QueryProcessor
import re

class SearchEngine:
    def __init__(self, index_file):
        self.index = IndexLoader.load_index(index_file)

    def boolean_search(self, query):
        return QueryProcessor.process_boolean_query(query, self.index)

    def phrase_search(self, phrase):
        return QueryProcessor.process_phrase_query(phrase, self.index)

    def proximity_search(self, query, proximity):
        return QueryProcessor.process_proximity_query(query, proximity, self.index)

# Load the stemmed positional inverted index file
index_file = '/workspace/Information-Retrieval-/positional_inverted_index_v1.txt'

# Create the search engine
engine = SearchEngine(index_file)

# Sample queries
queries = {
    'q1': 'Sandstone',
    'q2': 'landmark',
    'q3': 'Heritage',
    'q4': 'Cleopatra',
    'q5': 'Antony',
    'q6': 'Antony OR Cleopatra',
    'q7': 'Cleopatra AND Antony',
    'q8': '"ancient ruins"',
    'q9': '#10(ancient, ruins)',  # Proximity search
    'q10': '"national park" AND wildlife',
    'q11': '"Murchison Falls"'

}

for query_name, query_text in queries.items():
    print(query_text)

    if 'OR' in query_text or 'AND' in query_text or 'NOT' in query_text:
        # Boolean search
        result = engine.boolean_search(query_text)
    elif '"' in query_text:
        # Phrase search
        result = engine.phrase_search(query_text.strip('"'))
    elif '#' in query_text:
        # Proximity search
        query_parts = re.search(r'#(\d+)\(([^,]+),\s*([^)]+)\)', query_text)
        proximity = int(query_parts.group(1))
        terms = [query_parts.group(2), query_parts.group(3)]
        result = engine.proximity_search(" ".join(terms), proximity)
    else:
        # Regular word search
        result = engine.phrase_search(query_text)

    print(f"Query {query_name}: {query_text}\nResult: {result}\n")
