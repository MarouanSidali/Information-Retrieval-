import xml.etree.ElementTree as ET
import re
import os
import json
import spacy
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

def initialize_nltk():
    import nltk
    nltk.download('stopwords')

def initialize_spacy():
    return spacy.load("en_core_web_sm")

def tokenize(text):
    # Tokenize the text using a simple regex (you can enhance it based on your requirements)
    return re.findall(r'\b\w+\b', text.lower())

def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    return [token for token in tokens if token not in stop_words]

def perform_stemming(tokens):
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]

def extract_named_entities(text, nlp):
    doc = nlp(text)
    return [ent.text for ent in doc.ents]

def build_positional_inverted_index(xml_file, do_stemming=True, do_stopword_removal=True, do_ner=True):
    inverted_index = {}
    doc_id = 0
    nlp = initialize_spacy()

    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for location in root.findall('location'):
        doc_id += 1
        content = location.find('Content').text
        description = location.find('Description').text

        # Extract named entities if enabled
        if do_ner:
            entities = extract_named_entities(content, nlp)
        else:
            entities = []

        # Tokenize
        tokens = tokenize(f"{content} {description}")

        # Remove stopwords if enabled
        if do_stopword_removal:
            tokens = remove_stopwords(tokens)

        # Perform stemming if enabled
        if do_stemming:
            tokens = perform_stemming(tokens)

        # Combine tokens and entities
        terms = tokens + entities

        # Build the inverted index
        for position, term in enumerate(terms, start=1):
            if term not in inverted_index:
                inverted_index[term] = {'df': 1, 'positions': {doc_id: [position]}}
            else:
                inverted_index[term]['df'] += 1
                if doc_id not in inverted_index[term]['positions']:
                    inverted_index[term]['positions'][doc_id] = [position]
                else:
                    inverted_index[term]['positions'][doc_id].append(position)

    return inverted_index

def save_inverted_index_to_file(inverted_index, output_file):
    with open(output_file, 'w') as f:
        for term, info in inverted_index.items():
            df = info['df']
            positions = info['positions']
            f.write(f"{term} (df: {df}):\n")
            for doc_id, pos_list in positions.items():
                f.write(f"  DocID: {doc_id}, Positions: {pos_list}\n")

if __name__ == "__main__":
    initialize_nltk()

    xml_file = "./Data Collection/Project_RIW_XML/output_files/combined_20231227.xml"
    output_file = "positional_inverted_index.txt"

    # For the time being I think those are the most important variables to work with

    do_stemming = False  # Set to False to disable stemming
    do_stopword_removal = True  # Set to False to disable stopword removal
    do_ner = False  # Set to False to disable named entity recognition

    inverted_index = build_positional_inverted_index(xml_file, do_stemming, do_stopword_removal, do_ner)
    save_inverted_index_to_file(inverted_index, output_file)

    print("Positional inverted index has been successfully created and saved.")
