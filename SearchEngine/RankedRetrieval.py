import math
import re
from index_loader import IndexLoader
from collections import defaultdict

class TFIDFRankedRetrieval:
    def __init__(self, index_file, queries_file, results_file):
        self.index = IndexLoader.load_index(index_file)
        self.queries = self.load_queries(queries_file)
        self.results_file = results_file

    def load_queries(self, queries_file):
        queries = {}
        with open(queries_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split(' ', 1)
                    query_number = int(parts[0])
                    query_text = parts[1]
                    queries[query_number] = query_text
        return queries

    def calculate_tfidf(self, term, doc_id):
        tf = len(self.index[term]['positions'][doc_id])
        idf = math.log10(len(self.index) / self.index[term]['df'])
        return (1 + math.log10(tf)) * idf

    def process_query(self, query_number, query_text):
        query_terms = re.findall(r'\b\w+\b', query_text.lower())
        scores = defaultdict(float)

        for term in query_terms:
            if term in self.index:
                for doc_id in self.index[term]['positions']:
                    scores[doc_id] += self.calculate_tfidf(term, doc_id)

        # Sort scores in descending order
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Write the top 150 results to the results file
        with open(self.results_file, 'a') as file:
            for rank, (doc_id, score) in enumerate(sorted_results[:150], start=1):
                file.write(f"{query_number},{doc_id},{score:.4f}\n")

    def run_ranked_retrieval(self):
        for query_number, query_text in self.queries.items():
            self.process_query(query_number, query_text)

# Example usage
index_file = './SearchEngine/positional_inverted_index_v3.txt'
queries_file = './SearchEngine/queries.ranked.txt'
results_file = './SearchEngine/results.ranked.txt'

ranked_retrieval = TFIDFRankedRetrieval(index_file, queries_file, results_file)
ranked_retrieval.run_ranked_retrieval()