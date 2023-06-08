import requests
from enum import Enum

class Category(Enum):
    INTERNET = "internet"
    CABLE = "cable"
    TV = "tv"

# Define the URL for the POST request
url = "http://localhost:8000/items/"

# Define the data to be sent in the request body
data = {
    "id": 2,
    "zipcode": 12425,
    "city": "Clifton Park",
    "price": 80.99,
    "category": Category.INTERNET.value
}

# Send the POST request
response = requests.post(url, json=data)

# Check the response status code
if response.status_code == 200:
    result = response.json()
    print("Item added successfully:", result)
else:
    print("Failed to add item:", response.text)
