
import string
import re
import numpy as np
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
# from sklearn.feature_extraction.text import TfidfVectorizer
# from gensim.models import Word2Vec
from gensim import corpora, models

# import gensim.downloader as api
import gensim
from api.index import db
import time
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')




def compareData(abstract):
    begin = time.time()
    # path_word2vec_model = 'word2vec.model'

    
    def preprocess_data(contents):
        stemmer = PorterStemmer()
        wordnet.ensure_loaded()
        stop_words = set(stopwords.words('english'))
        preprocessed_data = []
        for content in contents:
            lemmatizer = WordNetLemmatizer()  # Define lemmatizer here
            sentence = content[1].lower()
            sentence = re.sub(r'\d+', '', sentence)  # Remove numbers
            sentence = sentence.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
            tokens = word_tokenize(sentence)
            tokens = [stemmer.stem(token) for token in tokens if token not in stop_words and token.isalpha()]
            lemmatized_synonyms = []
            for token in tokens:
                synsets = wordnet.synsets(token)
                lemmas = [lemma for synset in synsets for lemma in synset.lemmas()]
                if lemmas:
                    lemmatized_synonyms.extend([lemmatizer.lemmatize(lemma.name()) for lemma in lemmas])
            tokens.extend(lemmatized_synonyms)
            preprocessed_data.append(tokens)
        data_time = time.time()
        print(f"preprocess time2: {data_time-begin}")
        return preprocessed_data

    def preprocess_query(query):
        stemmer = PorterStemmer()
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()  # Define lemmatizer here
        query = query.lower()
        query = re.sub(r'\d+', '', query)  # Remove numbers
        query = query.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
        tokens = word_tokenize(query)
        tokens = [stemmer.stem(token) for token in tokens if token not in stop_words and token.isalpha()]
        lemmatized_synonyms = []
        for token in tokens:
            synsets = wordnet.synsets(token)
            lemmas = [lemma for synset in synsets for lemma in synset.lemmas()]
            if lemmas:
                lemmatized_synonyms.extend([lemmatizer.lemmatize(lemma.name()) for lemma in lemmas])
        tokens.extend(lemmatized_synonyms)
        print("query time",time.time()-begin)
        return tokens

    def calculate_euclidean_distance(query, documents):
        dictionary = corpora.Dictionary(documents)
        corpus = [dictionary.doc2bow(doc) for doc in documents]

        model = models.TfidfModel(corpus)
        tfidf_corpus = model[corpus]

        # Convert the query to a tf-idf vector
        query_bow = dictionary.doc2bow(query)
        query_tfidf = model[query_bow]

        # Create a matrix of tf-idf vectors for all documents
        document_matrix = gensim.matutils.corpus2dense(tfidf_corpus, num_terms=len(dictionary)).T

        # Convert the query and document vectors to numpy arrays
        query_vector = gensim.matutils.corpus2dense([query_tfidf], num_terms=len(dictionary)).T

        # Calculate Euclidean distance between the query vector and each document vector
        euclidean_distances = np.linalg.norm(document_matrix - query_vector, axis=1)

        return euclidean_distances

    def read_data():
        contents = [(int(obj["id"]),obj["sentence"]) for obj in db.Projects.find()]
        return contents

    # Read data from mongo
    data = read_data()
    print(data[:10])
    end_read = time.time()
    # Preprocess data
    preprocessed_data = preprocess_data(data)



    # Preprocess query
    preprocessed_query = preprocess_query(abstract)

    # Calculate similarity using Euclidean distance
    query_distances = calculate_euclidean_distance(preprocessed_query, preprocessed_data)

    end_eu = time.time()
    # Rank documents
    ranked_docs = sorted(enumerate(query_distances, start=1), key=lambda x: x[1])

    result_docs=[]
    # Display top-ranked similar documents
    for doc_id, distance in ranked_docs[:10]:
        original_doc_id = data[doc_id - 1][0]
        similarity = 1 / (1 + distance)  # Convert distance to similarity (values closer to 1 are more similar)
        sim_score= f'{similarity*100:.2f}%'
        print(f"Doc {original_doc_id}: Similarity {similarity*100:.2f}%")
        result_docs.append((original_doc_id,sim_score))
    
    end = time.time()
    print(f"read: {end_read-begin}")
    print(f"eu: {end_eu-begin}")
    print(f"end: {end-begin}")
    
    return result_docs
