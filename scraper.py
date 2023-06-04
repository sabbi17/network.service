import requests
from bs4 import BeautifulSoup

url = "https://www.kaggle.com/datasets/latentheat/att-network-data"
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")

# Example: Extract text from an HTML element with a specific class
element = soup.find("div", class_="my-class")
extracted_data = element.text




