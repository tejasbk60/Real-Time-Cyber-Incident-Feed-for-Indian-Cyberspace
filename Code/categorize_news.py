import joblib
from text_preprocessing import preprocess_text

def categorize_news(news_headlines):
    vectorizer, model = joblib.load("cybersecurity_news_classifier.pkl")  # Load AI model

    processed_news = [preprocess_text(title) for title in news_headlines]  # Clean text
    X_new = vectorizer.transform(processed_news)  # Convert text to numbers
    predictions = model.predict(X_new)  # Predict categories

    return list(zip(news_headlines, predictions))  # Return (news, category)

if __name__ == "__main__":
    test_news = ["New malware attack on Windows PCs", "Government passes cybersecurity bill"]
    results = categorize_news(test_news)
    
    for title, category in results:
        print(f"📰 {title} → 📌 {category}")
