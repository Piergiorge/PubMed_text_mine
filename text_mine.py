import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import nltk

"""
This code is a Python script that uses the NLTK (Natural Language Toolkit)
library and the PubMed API to extract and analyze information from a
scientific paper. The script starts by setting up a request to the PubMed
API by defining an API key, the PubMed ID of the paper to be analyzed,
and the URL of the API endpoint. The script then sends the request and
parses the XML data returned by the API using the ElementTree library.
The script extracts the full text of the paper by traversing the XML
tree structure and searching for the Abstract and Article elements.

"""

# Set up the API request
api_key = "YOUR_API_KEY"
pmid = "12345678"  # Replace with the PubMed ID of the paper you want to text mine
url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml&api_key={api_key}"

# Send the request and parse the XML data
response = requests.get(url)
xml_data = response.text
root = ET.fromstring(xml_data)

# Extract the full text of the paper
article_xml = root.find("./PubmedArticle/MedlineCitation/Article")
full_text = ""
for element in article_xml:
    if element.tag == "Abstract":
        for abstract_section in element:
            full_text += abstract_section.text
    else:
        full_text += element.text

# Preprocess the text data
full_text = full_text.lower()  # Convert to lowercase
full_text = BeautifulSoup(full_text, "lxml").get_text()  # Remove HTML tags
tokens = nltk.word_tokenize(full_text)  # Tokenize the text
tokens = [token for token in tokens if token.isalpha()]  # Remove punctuation
stop_words = set(nltk.corpus.stopwords.words("english"))  # Load stop words
tokens = [token for token in tokens if token not in stop_words]  # Remove stop words

# Extract named entities
tags = nltk.pos_tag(tokens)
named_entities = nltk.ne_chunk(tags)

# Print the named entities
for entity in named_entities:
    if hasattr(entity, "label"):
        print(f"{entity.label()}: {' '.join(c[0] for c in entity)}")
