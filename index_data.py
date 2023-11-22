#!/usr/bin/env python

INDEX_DIR = "index"

import sys, os, lucene, time
from datetime import datetime
import json

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import NIOFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader


"""
This class is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = NIOFSDirectory(Paths.get(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        print('indexing')
        self.indexDocs(root, writer)
        print('commit index',)
        writer.commit()
        writer.close()
        print('done')

    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

        t2 = FieldType()
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        json_file = os.path.join("results", "data", "all_cleaned.json")
        with open(json_file, 'r') as file:
            data = json.load(file)


        for doc_id, entry in enumerate(data):
            text = data[entry]['text']  
            try:
                doc = Document()
                doc.add(Field(entry, text, t1))
                writer.addDocument(doc)
            except:
                print(f"Error with {entry}")    
            
                
        # for root, dirnames, filenames in os.walk(root):
        #     for filename in filenames:
        #         if not filename.endswith('.json'):
        #             continue
        #         print("adding", filename)

        #         path = os.path.join(root, filename)
        #         file = open(path, "r", encoding="utf-8")
        #         contents = file.read()
        #         file.close()
        #         doc = Document()
        #         doc.add(Field("name", filename, t1))
        #         doc.add(Field("path", root, t1))
        #         if len(contents) > 0:
        #             doc.add(Field("contents", contents, t2))
        #         else:
        #             print("warning: no content in %s" % filename)
        #         writer.addDocument(doc)
                
                
def run(searcher, analyzer):
    while True:
        print
        print("Hit enter with no input to quit.")
        command = input("Query:")
        if command == '':
            return

        print
        print("Searching for:", command)
        query = QueryParser("contents", analyzer).parse(command)
        scoreDocs = searcher.search(query, 50).scoreDocs
        print("%s total matching documents." % len(scoreDocs))

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print('path:', doc.get("path"), 'name:', doc.get("name"))

if __name__ == '__main__':

    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    start = datetime.now()
    base_dir = ""
    IndexFiles("", os.path.join(base_dir, INDEX_DIR), StandardAnalyzer())
    
    directory = NIOFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    run(searcher, analyzer)
        
    end = datetime.now()
    print(end - start)