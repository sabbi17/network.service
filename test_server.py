# Created this file to quickly running the server. So, here fastapi is handling json Serializaton no matter
# if I have Item dictionary or padentic objects that is containing the item objects..


import requests

print(requests.get("http://127.0.0.1:8000/items").json())
#Below are different printing statements I used to develop step by step.
print(requests.get("http://127.0.0.1:8000/items/1").json())
print(requests.get("http://127.0.0.1:8000/items/?zipcode=83716&price=80&category=tv").json())
print(requests.get("http://127.0.0.1:8000/").json())

print(requests.get("http://127.0.0.1:8000/items/1").json())
print(requests.get("http://127.0.0.1:8000/items/?zipcode=83716&price=80&category=tv").json())

# print("Adding an item:")
print(
    requests.post(
        "http://127.0.0.1:8000/",
        json={"zipcode": 83710, "city": "Helloworld3", "price": 30.99, "id": 3, "category": "tv" },
    ).json()
 )
print(requests.get("http://127.0.0.1:8000/").json())
print()

# print("Updating an item:")
print(requests.put("http://127.0.0.1:8000/update/0?zipcode=9001").json())
print(requests.get("http://127.0.0.1:8000/").json())
print()

# print("Deleting an item:")
print(requests.delete("http://127.0.0.1:8000/delete/0").json())
print(requests.get("http://127.0.0.1:8000/").json())

#testing for Validations
# These requests will result in an error, since price and count are negative:
print(requests.put("http://127.0.0.1:8000/update/0?zipcode=-1").json())
print(requests.put("http://127.0.0.1:8000/update/0?price=-1").json())

# Similarly, an item_id must not be negative:
print(requests.put("http://127.0.0.1:8000/update/-1").json())

# And name cannot exceed 8 characters:
print(requests.put("http://127.0.0.1:8000/update/0?city=SuperDuperHammer").json())
