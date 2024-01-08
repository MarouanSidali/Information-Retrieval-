# query_processor.py
import re
from nltk.stem import PorterStemmer

class QueryProcessor:
    @staticmethod
    def preprocess_query(query, do_stemming=True, do_ner=False):
        query = query.lower()

        if do_stemming:
            stemmer = PorterStemmer()
            query = " ".join(stemmer.stem(word) for word in query.split())

        # Include NER processing here if needed (currently disabled)
        

        return query

    @staticmethod
    def process_phrase_query(phrase, index):
        print("phrase")
        phrase = QueryProcessor.preprocess_query(phrase)
        print(phrase)
        words = re.findall(r'\b\w+\b', phrase)
        print(words)
        if not all(word in index for word in words):
            return set()
        common_docs = set.intersection(*[set(index[word]['positions'].keys()) for word in words])
        results = set()
        for doc in common_docs:
            positions = [index[word]['positions'][doc] for word in words]
            for i in range(len(positions[0])):
                if all((positions[0][i] + j) in positions[j] for j in range(1, len(positions))):
                    results.add(doc)
                    break

        with open('/workspace/Information-Retrieval-/SearchEngine/NewResults//results.txt', 'a') as file:
            for doc_id in results:
                file.write(f"{phrase}, {doc_id}\n")

        return results


    @staticmethod
    def process_boolean_query(query, index):
        query = QueryProcessor.preprocess_query(query)
        print(query)

        # If there are no double quotes, treat it as a boolean search
        if '"' not in query:
            # Separate the query into words and operators
            components = re.findall(r'\b(?:and|or|not)\b|\b\w+\b', query)
            print(components)

            # Extract words and operators
            words = [comp.lower() for comp in components if comp not in ['and', 'or', 'not']]
            operators = [comp for comp in components if comp in ['and', 'or', 'not']]

            # Process each word and operator
            results = []
            for word in words:
                if word in index:
                    results.append(set(index[word]['positions'].keys()))
                else:
                    results.append(set())

            # Apply boolean operators
            final_result = results[0]
            i = 1
            while i < len(results):
                if i < len(operators) and operators[i - 1] == 'not':
                    results[i] = set(index.keys()) - results[i]
                if i - 1 < len(operators) and operators[i - 1] == 'and':
                    final_result = final_result & results[i]
                elif i - 1 < len(operators) and operators[i - 1] == 'or':
                    final_result = final_result | results[i]
                i += 1

        else:
            # Separate the query into phrases and operators
            components = re.findall(r'"[^"]+"|\b(?:and|or|not)\b', query)
            print(components)

            # Extract phrases and operators
            phrases = [comp.strip('"') for comp in components if '"' in comp]
            operators = [comp for comp in components if comp in ['and', 'or', 'not']]

            # Process each phrase and operator
            results = []
            for component in components:
                if '"' in component:
                    phrase_result = QueryProcessor.process_phrase_query(component, index)
                    results.append(phrase_result)

            # Apply boolean operators
            final_result = set(results[0])
            i = 1
            while i < len(results):
                if i < len(operators) and operators[i // 2] == 'not':
                    results[i] = set(index.keys()) - results[i]
                if i - 1 < len(operators) and operators[i // 2] == 'and':
                    final_result = final_result & results[i]
                elif i - 1 < len(operators) and operators[i // 2] == 'or':
                    final_result = final_result | results[i]
                i += 1

        # Write the results to a file
        with open('/workspace/Information-Retrieval-/SearchEngine/NewResults/results.txt', 'a') as file:
            for doc_id in final_result:
                file.write(f"{query}, {doc_id}\n")

        return final_result





    @staticmethod
    def process_proximity_query(query, proximity, index):
        query = QueryProcessor.preprocess_query(query)
        words = query.split()
        if not all(word in index for word in words):
            return set()
        common_docs = set.intersection(*[set(index[word]['positions'].keys()) for word in words])
        results = set()
        for doc in common_docs:
            positions = [index[word]['positions'][doc] for word in words]
            for i in range(len(positions[0])):
                if all(any(abs(positions[0][i] - pos) <= proximity for pos in positions[j]) for j in range(1, len(positions))):
                    results.add(doc)
                    break

        with open('/workspace/Information-Retrieval-/SearchEngine/NewResults/results.txt', 'a') as file:
            for doc_id in results:
                file.write(f"{query}, {doc_id}\n")

        return results

