from api import db
import os
import pandas as pd
import string
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
from gensim.similarities import SoftCosineSimilarity
from gensim import corpora
import gensim.downloader as api
from gensim import corpora
from gensim.models import TfidfModel
from gensim.similarities import SoftCosineSimilarity



def compareData(abstract):
 

  

  # path_data = './cransfield.csv'
  # path_query = 'query.txt'
  # path_relevant = './relevance.txt'
  path_word2vec_model = 'word2vec.model'

  def preprocess_data(contents):
      lemmatizer = WordNetLemmatizer()
      stop_words = set(stopwords.words('english'))
      preprocessed_data = []
      for content in contents:
          sentence = content[1].lower()
          sentence = re.sub(r'\d+', '', sentence)  # Remove numbers
          tokens = word_tokenize(sentence)
          tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words and token.isalpha()]
          preprocessed_data.append(tokens)
      return preprocessed_data

  def preprocess_query(query):
      lemmatizer = WordNetLemmatizer()
      stop_words = set(stopwords.words('english'))
      query = query.lower()
      query = re.sub(r'\d+', '', query)  # Remove numbers
      tokens = word_tokenize(query)
      tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words and token.isalpha()]
      print(tokens)
      return tokens
      

  import gensim.downloader as api
  from gensim import corpora, models, similarities

  # ...

  def calculate_similarity(query, documents):
      dictionary = corpora.Dictionary(documents)
      corpus = [dictionary.doc2bow(doc) for doc in documents]

      model = models.TfidfModel(corpus)
      tfidf_corpus = model[corpus]

      index = similarities.Similarity(None, tfidf_corpus, num_features=len(dictionary))

      query_bow = dictionary.doc2bow(query)
      query_tfidf = model[query_bow]

      query_scores = index[query_tfidf]

      return query_scores

  # ...


  def read_csv_data():
      
      # contents = [(int(obj[1]), obj[2]) for obj in db.Projects.find({},{'_id':1,'sentence':1})]
      contents = [((int(obj["id"]),obj["sentence"])) for obj in db.Projects.find()]
      # print(type(contents[0]))
      return contents

  # def get_relevance(path):
  #     relevances = {}
  #     with open(path, 'r') as f:
  #         for line in f:
  #             query_id, doc_id = map(int, line.split())
  #             relevances.setdefault(query_id, []).append(doc_id)
  #     return relevances

  # def calculate_precision_recall(relevances, docList):
  #     relevant_docs = len([doc for doc in docList if doc in relevances])
  #     total_relevant = len(relevances)
  #     total_docs = len(docList)
  #     precision = relevant_docs / total_docs
  #     recall = relevant_docs / total_relevant
  #     return precision, recall

  # Read data from CSV
  data = read_csv_data()

  # Preprocess data
  preprocessed_data = preprocess_data(data)

  # Train Word2Vec model
  word2vec_model = Word2Vec(sentences=preprocessed_data, vector_size=100, window=5, min_count=1, workers=4)
  word2vec_model.save(path_word2vec_model)


  # Read query from file
  # with open(path_query, 'r') as f:
  #     query = f.read()

  # Preprocess query
  preprocessed_query = preprocess_query(abstract)

  # Calculate similarity
  query_scores = calculate_similarity(preprocessed_query, preprocessed_data)

  # Rank documents
  ranked_docs = sorted(enumerate(query_scores, start=1), key=lambda x: x[1], reverse=True)
  
  
  result_docs=[]
  # Display top-ranked similar documents
  for doc_id, similarity in ranked_docs[:10]:
    original_doc_id = data[doc_id - 1][0]
    sim_score= f'{similarity*100:.2f}'
    print(f"Doc {original_doc_id}: Similarity {similarity*100:.2f}%")
    result_docs.append((original_doc_id,sim_score))
      
  return result_docs
  