import lucene
import os 
import json
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.store import NIOFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser

from org.apache.lucene.search import IndexSearcher
from java.nio.file import Paths

def create_index(index_path, json_file):
    # Read data from the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Create an index
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    directory = NIOFSDirectory(Paths.get(index_path))
    writer = IndexWriter(directory, config)

    # Define a field type for storing text
    text_field_type = FieldType()
    text_field_type.setStored(True)
    text_field_type.setTokenized(True)


    for doc_id, entry in enumerate(data):
        text = data[entry]['text']  
        doc = Document()
        doc.add(Field(entry, text, text_field_type))
        writer.addDocument(doc)


    # Close the index writer
    writer.commit()
    writer.close()

def search_index(index_path, query_str):
    # Open the index for searching
    index_dir = NIOFSDirectory(Paths.get(index_path))
    reader = DirectoryReader.open(index_dir)
    searcher = IndexSearcher(reader)
    # Print terms in the index

    # Create a query parser
    analyzer = StandardAnalyzer()
    query_parser = QueryParser("content", analyzer)

    # Parse the user's query string
    query = query_parser.parse(query_str)
    print(query)

    # Execute the query
    top_docs = searcher.search(query, 20)  # Adjust the number of results as needed

    # Process the results
    print(f"Top docs: {top_docs}, {len(top_docs.scoreDocs)}")
    print("Search results:")
    for score_doc in top_docs.scoreDocs:
        doc_id = score_doc.doc
        doc = searcher.doc(doc_id)
        print(f"Doc ID: {doc_id}, content: {doc.get('content')}")

    # Close the reader
    reader.close()

if __name__ == "__main__":
    # Set the path to the index directory
    lucene.initVM()
    index_path = "/indexed"

    # Path to your JSON file
    json_file_path = os.path.join("results", "data", "all_cleaned.json")

    #Create the index
    create_index(index_path, json_file_path)

    # Perform the search
    while True:
        user_query = input()
        search_index(index_path, user_query)

    print("Indexing complete.")



