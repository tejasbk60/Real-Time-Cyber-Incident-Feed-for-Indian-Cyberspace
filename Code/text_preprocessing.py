import re
import string

def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"http\S+", "", text)  # Remove links
    text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
    text = text.strip()
    return text

if __name__ == "__main__":
    sample_text = "New Ransomware Attack! http://bad-link.com"
    print("Before:", sample_text)
    print("After:", preprocess_text(sample_text))
