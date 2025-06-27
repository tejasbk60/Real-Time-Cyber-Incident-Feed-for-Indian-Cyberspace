from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

# Sample cybersecurity news training data
news_data = [
    ("Massive phishing attack on banking sector", "Phishing"),
    ("New ransomware strain targets healthcare", "Ransomware"),
    ("Government announces new cybersecurity laws", "Regulations"),
    ("Data breach exposes millions of records", "Data Breach"),
    ("Malware attack shuts down corporate servers", "Malware"),
]

texts, labels = zip(*news_data)  # Separate text and labels

vectorizer = TfidfVectorizer(stop_words="english")  # Convert text to numbers
X = vectorizer.fit_transform(texts)

model = MultinomialNB()  # Train a simple AI model
model.fit(X, labels)

# Save the model
joblib.dump((vectorizer, model), "cybersecurity_news_classifier.pkl")
print("✅ AI Model Trained and Saved!")
