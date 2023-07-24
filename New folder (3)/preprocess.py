import pandas as pd
import string
import contractions
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy
import re

# Download necessary resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load the spaCy NER model
nlp = spacy.load("en_core_web_sm")

# Function to preprocess the text
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    # Expand contractions
    text = contractions.fix(text)
    # Remove punctuation, numbers, and special characters
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize text
    words = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word, pos='v') for word in words]
    # Remove duplicates and return list of tokens
    preprocessed_tokens = list(set(words))
    return preprocessed_tokens

# Load your CSV file into a pandas DataFrame
df = pd.read_csv('abstract_dataset.csv')

# Create a new DataFrame to store preprocessed data
preprocessed_data = []

# Process each row in the original DataFrame
for index, row in df.iterrows():
    # Preprocess the sentence
    preprocessed_tokens = preprocess_text(row['sentence'])
    
    # Add the preprocessed data to the new DataFrame
    preprocessed_data.append({'id': row['id'], 'preprocessed_sentence': preprocessed_tokens})

# Convert the preprocessed data list into a DataFrame
preprocessed_df = pd.DataFrame(preprocessed_data)

# Save the preprocessed DataFrame to a new CSV file
preprocessed_df.to_csv('preprocessed_dataset.csv', index=False)

print("Preprocessing completed and data saved to 'preprocessed_dataset.csv'.")
