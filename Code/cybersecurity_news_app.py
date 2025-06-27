from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextBrowser, QVBoxLayout, QWidget, QCheckBox, QComboBox, QLabel, QFrame, QGraphicsOpacityEffect, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QRect, QSize
from cybersecurity_news_scraper import get_cybersecurity_news
from categorize_news import categorize_news
import time

class NewsFetcherThread(QThread):
    newsFetched = pyqtSignal(list)

    def run(self):
        time.sleep(2)  # Simulating loading delay
        articles = get_cybersecurity_news()
        self.newsFetched.emit(articles)

class NewsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cybersecurity News Categorizer")
        self.setGeometry(100, 100, 800, 600)
        self.dark_mode = True
        self.setStyleSheet("background-color: #1e1e2e; color: white;")
        
        self.layout = QVBoxLayout()
        
        # Loading label with opacity effect
        self.loading_label = QLabel("", self)
        self.loading_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("color: #ffcc00;")
        
        # Set the opacity effect on the loading label
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.loading_label.setGraphicsEffect(self.opacity_effect)
        
        self.textbox = QTextBrowser(self)
        self.textbox.setOpenExternalLinks(True)  # Enable clickable links
        self.textbox.setFont(QFont("Arial", 12))
        self.textbox.setStyleSheet("background-color: #2e2e3e; color: white; padding: 10px; border-radius: 10px;")

        # Adding an icon to the button
        self.button = QPushButton("Fetch and Categorize News", self)
        self.button.setFont(QFont("Arial", 14, QFont.Bold))
        self.button.setStyleSheet("""
            background-color: #ff6600; color: white; 
            padding: 12px; border-radius: 12px;
        """)
        self.button.setIcon(QIcon('fetch_icon.png'))  # Use your own icon
        self.button.setIconSize(QSize(24, 24))  # Set icon size
        self.button.clicked.connect(self.fetch_and_display_news)
        self.button.setCursor(Qt.PointingHandCursor)

        # Adding hover animation to button (this is done using QPropertyAnimation)
        self.button_animation = QPropertyAnimation(self.button, b"geometry")
        self.button_animation.setDuration(300)
        self.button_animation.setStartValue(self.button.geometry())
        self.button_animation.setEndValue(QRect(250, 450, 300, 50))  # Animating position on click (for example)
        
        self.category_filter = QComboBox(self)
        self.category_filter.addItem("All Categories")
        self.category_filter.setStyleSheet("""
            background-color: #444; color: white; padding: 8px; 
            border-radius: 8px; font-size: 14px;
        """)
        self.category_filter.currentIndexChanged.connect(self.filter_news)

        self.dark_mode_toggle = QCheckBox("Dark Mode", self)
        self.dark_mode_toggle.setChecked(True)
        self.dark_mode_toggle.setStyleSheet("color: white;")
        self.dark_mode_toggle.stateChanged.connect(self.toggle_dark_mode)

        self.divider = QFrame(self)
        self.divider.setFrameShape(QFrame.HLine)
        self.divider.setStyleSheet("color: gray;")

        container = QWidget()
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.loading_label)
        top_layout.addWidget(self.textbox)
        top_layout.addWidget(self.divider)
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.button)
        bottom_layout.addWidget(self.category_filter)
        bottom_layout.addWidget(self.dark_mode_toggle)
        
        top_layout.addLayout(bottom_layout)
        
        container.setLayout(top_layout)
        self.setCentralWidget(container)

    def fetch_and_display_news(self):
        # Fading in the loading label with animation
        self.loading_label.setText("🔄 Fetching latest news... Please wait!")
        
        fade_in_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_in_animation.setDuration(1000)  # Animation time in milliseconds
        fade_in_animation.setStartValue(0)  # Start with 0 opacity
        fade_in_animation.setEndValue(1)  # End with full opacity
        fade_in_animation.start()

        self.textbox.clear()
        self.thread = NewsFetcherThread()
        self.thread.newsFetched.connect(self.display_news)
        self.thread.start()

    def display_news(self, articles):
        self.loading_label.setText("")  # Clear loading message
        self.articles = articles
        headlines = [title for title, _ in articles]
        self.categorized_news = categorize_news(headlines)

        categories = set(category for _, category in self.categorized_news)
        self.category_filter.clear()
        self.category_filter.addItem("All Categories")
        self.category_filter.addItems(sorted(categories))

        self.filter_news()

    def filter_news(self):
        selected_category = self.category_filter.currentText()
        output_text = ""
        for (title, category), (_, link) in zip(self.categorized_news, self.articles):
            if selected_category == "All Categories" or category == selected_category:
                output_text += ("<div style='border: 1px solid gray; padding: 10px; margin: 5px; border-radius: 5px; background-color: #333;'>"
                                f"📰 <b>{title}</b><br>"
                                f"📌 <font color='#ffcc00'><b>Category:</b> {category}</font><br>"
                                f"🔗 <a href='{link}'>{link}</a>"
                                "</div><br>")

        self.textbox.setHtml(output_text)

    def toggle_dark_mode(self):
        if self.dark_mode_toggle.isChecked():
            self.setStyleSheet("background-color: #1e1e2e; color: white;")
            self.textbox.setStyleSheet("background-color: #2e2e3e; color: white; padding: 10px; border-radius: 10px;")
            self.dark_mode_toggle.setStyleSheet("color: white;")
        else:
            self.setStyleSheet("background-color: white; color: black;")
            self.textbox.setStyleSheet("background-color: #f0f0f0; color: black; padding: 10px; border-radius: 10px;")
            self.dark_mode_toggle.setStyleSheet("color: black;")

# Run the App
app = QApplication([])
window = NewsApp()
window.show()
app.exec_()
