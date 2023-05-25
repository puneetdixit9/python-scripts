import time
import requests
from multiprocessing import Process


def call_api(method: str, url: str, headers: dict = dict, data: dict = dict, json: dict = dict):
    if method == "get":
        response = requests.get(url, headers=headers)
    elif method == "post":
        response = requests.post(url, headers=headers, data=data, json=json)
    elif method == "put":
        response = requests.put(url, headers=headers, data=data, json=json)
    elif method == "delete":
        response = requests.delete(url, headers=headers)
    else:
        response = {
            "error": "Invalid Method"
        }
    print(f"Response : {response.text}")
    return response


# request_method = "get"
# request_url = "http://127.0.0.1:5000/wmp/demands/1?start_date=2023-05-24&end_date=2023-05-31"

request_method = "post"
request_url = "http://127.0.0.1:5000/wmp/warehouses"

request_headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NTAwMTc4MCwianRpIjoiNzk1YmVhZTktMjYwNC00OWRhLThkNTQtOTY2YmQ0Y2YyNzFjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VyX2lkIjo0LCJyb2xlIjpudWxsfSwibmJmIjoxNjg1MDAxNzgwLCJleHAiOjE2ODUwODgxODB9.FhKQRXkCCx7v_pY3f4fvFbE_I3DDmtHoZWZMbdUUlUA"
}
data = {}
json = {
    "warehouses": [
        {
            "name": "Warehouse F",
            "description": "Warehouse F"
        }
    ]
}


number_of_api_calls = 100


process_list = []

start_time = time.time()  # Start time

for i in range(number_of_api_calls+1):
    p = Process(target=call_api, args=(request_method, request_url, request_headers, data, json))
    p.start()
    process_list.append(p)

for p in process_list:
    p.join()

# End time
print(f"Total time to call {request_url} {number_of_api_calls} times :-> {time.time() - start_time}")
