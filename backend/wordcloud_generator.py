import base64
import io

import matplotlib.pyplot as plt
from wordcloud import WordCloud


def create_wordcloud(text_data: str) -> str:
    """
    Generates a word cloud image and returns it as a Base64 encoded string.
    """
    if not text_data.strip():
        return ""

    # Initialize WordCloud object
    # We use a simple circular/rectangular layout for maximum generation speed
    wc = WordCloud(
        width=800, height=400, background_color="white", colormap="viridis", max_words=100
    ).generate(text_data)

    # Save the plot to a BytesIO object instead of a file
    img_buffer = io.BytesIO()

    # Create a matplotlib figure to handle the image export
    plt.figure(figsize=(10, 5), facecolor=None)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)

    # Export to buffer as PNG
    plt.savefig(img_buffer, format="png")
    plt.close()  # Close plot to free memory

    img_buffer.seek(0)

    # Encode the binary data to Base64
    base64_image = base64.b64encode(img_buffer.read()).decode("utf-8")

    return f"data:image/png;base64,{base64_image}"
