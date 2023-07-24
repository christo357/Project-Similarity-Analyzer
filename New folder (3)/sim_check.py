import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the preprocessed dataset and abstract CSV files
dataset_file = "preprocessed_dataset.csv"
abstract_file = "preprocessed_abstract.csv"

# Load the datasets into pandas DataFrames
dataset_df = pd.read_csv(dataset_file)
abstract_df = pd.read_csv(abstract_file)

# Ensure there's only one row in the preprocessed_abstract DataFrame
if len(abstract_df) != 1:
    raise ValueError("preprocessed_abstract should contain only one row.")

# Get the preprocessed abstract sentence
abstract_sentence = abstract_df["preprocessed_sentence"].iloc[0]

# Create a CountVectorizer to convert sentences to vectors
vectorizer = CountVectorizer()

# Fit and transform the dataset sentences to vectors
dataset_vectors = vectorizer.fit_transform(dataset_df["preprocessed_sentence"])
abstract_vector = vectorizer.transform([abstract_sentence])

# Calculate cosine similarity between the abstract sentence and each dataset sentence
cosine_similarities = cosine_similarity(abstract_vector, dataset_vectors).flatten()

# Add the similarity scores as a new column in the dataset DataFrame
dataset_df["similarity_score"] = cosine_similarities

# Sort the DataFrame based on the similarity scores in descending order
dataset_df.sort_values(by="similarity_score", ascending=False, inplace=True)

# Display the top 10 most similar sentences with their ids and similarity percentages
top_10_results = dataset_df.head(10)[["id", "similarity_score"]]
top_10_results["similarity_percentage"] = top_10_results["similarity_score"] * 100

print(top_10_results)

