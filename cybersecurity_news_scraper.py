import requests
from bs4 import BeautifulSoup

def get_hackernews():
    """Fetch cybersecurity news from The Hacker News."""
    url = "https://thehackernews.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    articles = []
    for item in soup.find_all("div", class_="body-post")[:5]:  # Limiting to 5 articles
        title = item.find("h2").text.strip()
        link = item.find("a")["href"]
        articles.append((title, link))
    
    return articles

def get_bleepingcomputer():
    """Fetch cybersecurity news from Bleeping Computer."""
    url = "https://www.bleepingcomputer.com/news/security/"
    headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a real browser request
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch Bleeping Computer news.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.select("article .bc_latest_news_title a")[:5]:  # Updated CSS selector
        title = item.text.strip()
        link = item["href"]
        if not link.startswith("http"):
            link = "https://www.bleepingcomputer.com" + link  # Convert relative to absolute URL
        articles.append((title, link))

    return articles


def get_krebsonsecurity():
    """Fetch cybersecurity news from Krebs on Security."""
    url = "https://krebsonsecurity.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.find_all("h2", class_="entry-title")[:5]:  # Limiting to 5 articles
        title = item.text.strip()
        link = item.find("a")["href"]
        articles.append((title, link))

    return articles

def get_cybersecurity_news(multiple_sources=True):
    """Fetch cybersecurity news from multiple sources."""
    news = []

    # Fetch from The Hacker News
    news.extend(get_hackernews())

    if multiple_sources:
        # Fetch from other cybersecurity sources
        news.extend(get_bleepingcomputer())
        news.extend(get_krebsonsecurity())

    return news

# Test the script
if __name__ == "__main__":
    news_articles = get_cybersecurity_news(multiple_sources=True)
    for title, link in news_articles:
        print(f"📰 {title}\n🔗 {link}\n")
