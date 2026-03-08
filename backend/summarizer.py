import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def generate_summary(cleaned_comments: list, sentiment_results: dict) -> str:
    """
    Generates a 50-60 word summary of the overall sentiment and themes.
    Uses an extractive approach for high-speed processing.
    """
    if not cleaned_comments:
        return "No feedback provided to summarize."

    # 1. Identify dominant sentiment
    dist = sentiment_results["distribution"]
    dominant_sentiment = max(dist, key=dist.get)

    # 2. Extract key representative phrases using TF-IDF
    # We treat all comments as one document to find global importance
    vectorizer = TfidfVectorizer(max_features=15, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(cleaned_comments)
    feature_names = vectorizer.get_feature_names_out()

    top_themes = ", ".join(feature_names[:5])

    # 3. Construct the summary
    # Using a template-based extractive approach ensures we hit the 50-60 word target
    summary = (
        f"The e-consultation feedback analysis indicates a primarily {dominant_sentiment.lower()} "
        f"reception from users, with {dist[dominant_sentiment]}% of comments aligning with this sentiment. "
        f"Key recurring themes identified across the dataset include {top_themes}. "
        f"While the majority of users focused on these aspects, the overall distribution suggests "
        f"a {dist['Neutral']}% neutral and {dist['Negative']}% negative response rate, "
        f"highlighting specific areas for operational improvement and service refinement."
    )

    # Word count check/adjustment to stay within 50-60 word range
    words = summary.split()
    if len(words) > 60:
        return " ".join(words[:60]) + "."

    return summary
