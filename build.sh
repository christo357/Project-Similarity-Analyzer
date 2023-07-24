pip install --upgrade pip
pip install -r requirements.txt

RUN python -m import nltk
RUN python -mnltk.download('stopwords')
RUN python -m nltk.download('wordnet')