import requests

API_KEY = "AIzaSyAxJa_f1f5FhqyY_JhZ42JBijy4dXNgGQA"

def get_distance():
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins=Boston%2CMA%7&destinations=Lexington%2CMA%7&departure_time=now&key={API_KEY}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)