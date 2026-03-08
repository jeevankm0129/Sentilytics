def format_response(
    count: int, sentiment: dict, summary: str, keywords: list, wordcloud: str
) -> dict:
    """
    Standardizes the API response format.
    """
    return {
        "number_of_comments_processed": count,
        "sentiment_distribution": sentiment["distribution"],
        "summary_text": summary,
        "top_keywords": keywords,
        "wordcloud_image": wordcloud,
    }
