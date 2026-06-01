# from transformers import pipeline

# # load AI sentiment model
# sentiment_model = pipeline("sentiment-analysis")


# def analyze_sentiment(text):

#     result = sentiment_model(text)

#     sentiment = result[0]["label"]
#     score = result[0]["score"]

#     if sentiment == "NEGATIVE":
#         stress_probability = int(score * 100)
#     else:
#         stress_probability = int((1 - score) * 100)

#     print("\nText Sentiment Analysis")
#     print("Sentiment:", sentiment)
#     print("Stress probability:", stress_probability, "%")

#     return sentiment, stress_probability

from transformers import pipeline

sentiment_model = None

def analyze_sentiment(text: str):
    global sentiment_model
    if sentiment_model is None:
        sentiment_model = pipeline("sentiment-analysis")
    
    result = sentiment_model(text)[0]
    label = result['label']
    score = result['score']
    stress_prob = round(1 - score, 4) if label == "POSITIVE" else round(score, 4)
    return label, stress_prob