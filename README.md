# NLP-boolean-retrival-and-tf-idf
Implementation of NLP(IR) tasks including tf-idf scoring system, linguistic processing, and boolean retrieval, operated on a corpus of >30,000 government site descriptions.
(The data set could not be not uploaded due to file size limitations)
File descriptions:
- indexer: constructing the index list of vocabulary for each document within the corpus
- query_tfidf: calculating the tf-idf consine similarity for all the documents
- evaluate: evaluation of tf-idf scoring system using matrices including Precision at K, Mean Reciprocal Rank (MRR), and Mean Average Precision (MAP)
- query_boolean: Boolean query system to retrive documents satisfying the boolean query
- string_processing: pre-processing raw documents using methods including stemming, lemmatizing, and text cleaning with ntlk library
