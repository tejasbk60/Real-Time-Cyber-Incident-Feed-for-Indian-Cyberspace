from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# 🔸 Sample cybersecurity news data
news_data = [
    ("Massive phishing attack on banking sector", "Phishing"),
    ("New ransomware strain targets healthcare", "Ransomware"),
    ("Government announces new cybersecurity laws", "Regulations"),
    ("Data breach exposes millions of records", "Data Breach"),
    ("Malware attack shuts down corporate servers", "Malware"),
    ("Cyberattack forces schools to go offline", "Malware"),
    ("Phishing emails flood inboxes after breach", "Phishing"),
    ("Ransomware locks down city infrastructure", "Ransomware"),
    ("Regulatory board reviews cyber policies", "Regulations"),
    ("Millions affected by recent data leak", "Data Breach"),
]

texts, labels = zip(*news_data)

# 🔸 Train-test split
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.3, random_state=42)

# 🔸 Models to compare
models = {
    "Naive Bayes": MultinomialNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Linear SVM": LinearSVC(),
    "Random Forest": RandomForestClassifier(),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "SGD Classifier": SGDClassifier(loss="log_loss", max_iter=1000),
}

results = []

# 🔍 Evaluate each model
for name, model in models.items():
    pipeline = make_pipeline(TfidfVectorizer(stop_words="english"), model)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    results.append((name, accuracy))
    print(f"\n📊 {name} Accuracy: {accuracy:.2f}")
    print(classification_report(y_test, y_pred))

# 📋 Summary
df = pd.DataFrame(results, columns=["Model", "Accuracy"])
print("\n✅ Accuracy Comparison:")
print(df.sort_values(by="Accuracy", ascending=False).to_string(index=False))
