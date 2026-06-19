# from transformers import pipeline

# sentiment_model = None

# def analyze_sentiment(text: str):
#     global sentiment_model
#     if sentiment_model is None:
#         sentiment_model = pipeline("sentiment-analysis")
    
#     result = sentiment_model(text)[0]
#     label = result['label']
#     score = result['score']
#     stress_prob = round(1 - score, 4) if label == "POSITIVE" else round(score, 4)
#     return label, stress_prob

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str):
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]  # -1 (very negative) to +1 (very positive)

    label = "Positive" if compound >= 0 else "Negative"

    # stress_probability: negative score ko 0-100% mein convert karo
    if compound >= 0:
        stress_prob = int(max(0, (1 - compound) * 30))   # positive text → low stress
    else:
        stress_prob = int(min(100, abs(compound) * 100))  # negative text → high stress

    return label, stress_prob