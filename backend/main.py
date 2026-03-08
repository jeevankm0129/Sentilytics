import io
from typing import Optional

import pandas as pd
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sentiment_analyzer import analyze_sentiment
from summarizer import generate_summary

# Import internal modules
from text_cleaner import preprocess_comments
from utils import format_response
from word_frequency import get_top_keywords
from wordcloud_generator import create_wordcloud

app = FastAPI(title="Sentiment Analysis Dashboard API")

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze_feedback(
    file: Optional[UploadFile] = File(None), raw_text: Optional[str] = Form(None)
):
    """
    Main entry point for comment ingestion and processing.
    Supports CSV/JSON uploads or raw text input.
    """
    comments_list = []

    try:
        # 1. Receive and Parse Comments
        if file and file.filename:
            contents = await file.read()
            filename = file.filename.lower()  # Safe now, as we checked if file exists

            if filename.endswith(".csv"):
                df = pd.read_csv(io.BytesIO(contents))
                col = "comment" if "comment" in df.columns else df.columns[0]
                comments_list = df[col].dropna().astype(str).tolist()

            elif filename.endswith(".json"):
                df = pd.read_json(io.BytesIO(contents))
                col = "comment" if "comment" in df.columns else df.columns[0]
                comments_list = df[col].dropna().astype(str).tolist()

            else:
                raise HTTPException(status_code=400, detail="Unsupported file format.")

        elif raw_text:
            # Handle raw text split by newlines
            comments_list = [line.strip() for line in raw_text.split("\n") if line.strip()]

        if not comments_list:
            raise HTTPException(status_code=400, detail="No comments provided.")

        # 2. Clean and Preprocess Text (Vectorized)
        cleaned_comments = preprocess_comments(comments_list)

        # 3. Perform Sentiment Analysis
        sentiment_results = analyze_sentiment(cleaned_comments)

        # 4. Generate Summary (Extractive/Lightweight)
        summary = generate_summary(cleaned_comments, sentiment_results)

        # 5. Keyword Frequency Analysis
        top_keywords = get_top_keywords(cleaned_comments)

        # 6. Generate Word Cloud (Base64 Image)
        wordcloud_base64 = create_wordcloud(" ".join(cleaned_comments))

        # 7. Send results to frontend
        return format_response(
            count=len(comments_list),
            sentiment=sentiment_results,
            summary=summary,
            keywords=top_keywords,
            wordcloud=wordcloud_base64,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
