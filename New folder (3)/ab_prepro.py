import pandas as pd
import csv
import string
import contractions
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Function to preprocess the text
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    # Expand contractions
    text = contractions.fix(text)
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize text
    words = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word, pos='v') for word in words]
    # Return list of tokens
    preprocessed_tokens = words
    return preprocessed_tokens

# Load your abstract file into a string variable
with open('abstract.txt', 'r') as file:
    abstract_text = file.read()

# Preprocess the abstract
preprocessed_tokens = preprocess_text(abstract_text)

# Create a DataFrame with the 'preprocessed_sentence' column
df = pd.DataFrame({'preprocessed_sentence': [preprocessed_tokens]})

# Save the preprocessed DataFrame to a new CSV file
df.to_csv('preprocessed_abstract.csv', index=False, header=True, quoting=csv.QUOTE_NONNUMERIC)

print("Preprocessing completed and data saved to 'preprocessed_abstract.csv'.")
