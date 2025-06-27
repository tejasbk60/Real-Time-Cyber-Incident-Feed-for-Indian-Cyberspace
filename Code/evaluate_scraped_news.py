from cybersecurity_news_scraper import get_cybersecurity_news
from categorize_news import categorize_news
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
import random

# Step 1: Scrape fresh cybersecurity news
articles = get_cybersecurity_news(multiple_sources=True)
headlines = [title for title, _ in articles]

# Step 2: Auto-label the headlines using your trained model
auto_labeled = categorize_news(headlines)

# Step 3: (Optional) Add label noise to simulate real-world imperfections
def add_label_noise(data, noise_rate=0.15):
    categories = list(set(label for _, label in data))
    noisy_data = []
    for text, label in data:
        if random.random() < noise_rate:
            new_label = random.choice([c for c in categories if c != label])
            noisy_data.append((text, new_label))
        else:
            noisy_data.append((text, label))
    return noisy_data

auto_labeled = add_label_noise(auto_labeled, noise_rate=0.15)

# Step 4: Prepare data
texts, labels = zip(*auto_labeled)
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.3, random_state=42)

# Step 5: Define models
models = {
    "Naive Bayes": MultinomialNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Linear SVM": LinearSVC(),
    "Random Forest": RandomForestClassifier(),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "SGD Classifier": SGDClassifier(loss="log_loss", max_iter=1000),
}

results = []

# Step 6: Train and evaluate
for name, model in models.items():
    pipeline = make_pipeline(TfidfVectorizer(stop_words="english", ngram_range=(1, 2)), model)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred) * 100  # Convert to percentage
    acc_str = f"{acc:.2f}%"  # Add percentage symbol
    results.append((name, acc_str))
    print(f"\n📊 {name} Accuracy: {acc_str}")
    print(classification_report(y_test, y_pred))

# Step 7: Show Summary Table
df = pd.DataFrame(results, columns=["Model", "Accuracy"])
print("\n✅ Model Accuracy Comparison (Auto-labeled Scraped News with Noise):")
print(df.sort_values(by="Accuracy", ascending=False).to_string(index=False))
