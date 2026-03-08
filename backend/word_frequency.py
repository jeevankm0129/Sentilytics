from collections import Counter

import pandas as pd


def get_top_keywords(cleaned_comments: list, top_n: int = 10) -> list:
    """
    Performs keyword extraction and frequency analysis.
    Returns a list of dictionaries with word and count for easy frontend consumption.
    """
    if not cleaned_comments:
        return []

    # Combine all cleaned comments into one large string of words
    all_words = " ".join(cleaned_comments).split()

    # Calculate frequencies using Counter
    word_counts = Counter(all_words)

    # Get the most common words
    most_common = word_counts.most_common(top_n)

    # Format for JSON response: [{"word": "service", "count": 450}, ...]
    formatted_keywords = [{"word": word, "count": count} for word, count in most_common]

    return formatted_keywords
