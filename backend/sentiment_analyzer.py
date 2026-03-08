import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def analyze_sentiment(cleaned_comments: list) -> dict:
    """
    Classifies comments into Positive, Neutral, and Negative.
    Returns individual labels and overall distribution percentages.
    """
    if not cleaned_comments:
        return {"labels": [], "distribution": {}}

    analyzer = SentimentIntensityAnalyzer()

    # Process sentiments
    results = []
    for comment in cleaned_comments:
        score = analyzer.polarity_scores(comment)
        compound = score["compound"]

        # Standard VADER thresholds
        if compound >= 0.05:
            label = "Positive"
        elif compound <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"

        results.append(label)

    # Calculate distribution using Pandas for speed
    df = pd.Series(results)
    counts = df.value_counts(normalize=True) * 100

    # Ensure all categories exist in distribution even if 0%
    distribution = {
        "Positive": round(counts.get("Positive", 0), 2),
        "Neutral": round(counts.get("Neutral", 0), 2),
        "Negative": round(counts.get("Negative", 0), 2),
    }

    return {"labels": results, "distribution": distribution}
