import requests

# Define the URL for the POST request
url = "http://localhost:8000/"  # Replace with your server URL

# Define the data to be sent in the request body
data = {
    "id": 3,
    "zipcode": 12345,
    "city": "New City",
    "price": 99.99,
    "category": "tv"
}

# Send the POST request
response = requests.post(url, json=data)

# Check the response status code
if response.status_code == 200:
    result = response.json()
    print("Item added successfully:", result)
else:
    print("Failed to add item:", response.text)
