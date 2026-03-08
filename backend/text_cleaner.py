import re

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources once at startup
try:
    nltk.data.find("corpora/stopwords")
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("stopwords")
    nltk.download("wordnet")
    nltk.download("omw-1.4")


def preprocess_comments(comments_list: list) -> list:
    """
    Cleans 10,000+ comments using vectorized operations for maximum speed.
    """
    if not comments_list:
        return []

    # Convert to Pandas Series for vectorized string operations
    s = pd.Series(comments_list).astype(str)

    # 1. Lowercasing
    s = s.str.lower()

    # 2. Punctuation Removal (using regex)
    s = s.str.replace(r"[^\w\s]", "", regex=True)

    # 3. Stopword Removal
    stop = set(stopwords.words("english"))
    # Vectorized approach: splitting strings, filtering, and joining back
    s = s.apply(lambda x: " ".join([word for word in x.split() if word not in stop]))

    # 4. Lemmatization
    lemmatizer = WordNetLemmatizer()
    s = s.apply(lambda x: " ".join([lemmatizer.lemmatize(word) for word in x.split()]))

    # Remove empty strings resulting from cleaning
    s = s[s.str.strip() != ""]

    return s.tolist()
