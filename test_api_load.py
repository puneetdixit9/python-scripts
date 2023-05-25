import time
import requests
from multiprocessing import Process, Value

response_count = Value('i', 0)
api_call_count = Value('i', 0)


def call_api(method: str, url: str, headers: dict = dict, data: dict = dict, json: dict = dict):
    with api_call_count.get_lock():
        api_call_count.value += 1

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

    with response_count.get_lock():
        response_count.value += 1
        
    return response


def get_request_data():
    request_headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NTAwMTc4MCwianRpIjoiNzk1YmVhZTktMjYwNC00OWRhLThkNTQtOTY2YmQ0Y2YyNzFjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VyX2lkIjo0LCJyb2xlIjpudWxsfSwibmJmIjoxNjg1MDAxNzgwLCJleHAiOjE2ODUwODgxODB9.FhKQRXkCCx7v_pY3f4fvFbE_I3DDmtHoZWZMbdUUlUA"
    }
    request_method = "get"
    request_url = "http://127.0.0.1:5000/wmp/demands/1?start_date=2023-05-24&end_date=2023-05-31"
    return request_method, request_url, request_headers, {}, {}


def post_request_data():
    request_headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NTAwMTc4MCwianRpIjoiNzk1YmVhZTktMjYwNC00OWRhLThkNTQtOTY2YmQ0Y2YyNzFjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VyX2lkIjo0LCJyb2xlIjpudWxsfSwibmJmIjoxNjg1MDAxNzgwLCJleHAiOjE2ODUwODgxODB9.FhKQRXkCCx7v_pY3f4fvFbE_I3DDmtHoZWZMbdUUlUA"
    }
    request_method = "post"
    request_url = "http://127.0.0.1:5000/wmp/warehouses"
    data = {}
    request_body = {
        "warehouses": [
            {
                "name": "Warehouse F",
                "description": "Warehouse F"
            }
        ]
    }
    return request_method, request_url, request_headers, data, request_body


def put_request_data():
    request_headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NTAwMTc4MCwianRpIjoiNzk1YmVhZTktMjYwNC00OWRhLThkNTQtOTY2YmQ0Y2YyNzFjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VyX2lkIjo0LCJyb2xlIjpudWxsfSwibmJmIjoxNjg1MDAxNzgwLCJleHAiOjE2ODUwODgxODB9.FhKQRXkCCx7v_pY3f4fvFbE_I3DDmtHoZWZMbdUUlUA"
    }
    request_method = "put"
    request_url = "http://127.0.0.1:5000/wmp/demands"
    data = {}
    request_body ={
        "demands": [
            {
                "id": 1,
                "demand": 100
            }
        ]
    }
    return request_method, request_url, request_headers, data, request_body


def start_process(args: tuple, process_list: list):
    p = Process(target=call_api, args=args)
    p.start()
    process_list.append(p)


def call_api_n_times_in_parllel(n=1):
    process_list = []
    args = put_request_data()
    start_time = time.time()
    for i in range(n):
        start_process(args, process_list)

    for p in process_list:
        p.join()
    print(f"Total time taken to call a api {n} times parallelly : {time.time()-start_time}")


def call_unlimited_times_within_a_time_period(minutes=0, seconds=1):
    global api_call_count
    global response_count

    total_seconds = (60 * minutes) + seconds
    end_time = time.time() + total_seconds
    process_list = []
    args = put_request_data()
    while end_time > time.time():
        start_process(args, process_list)

    print(f"Total API called in {total_seconds} seconds {api_call_count} and response received for {response_count}")


call_api_n_times_in_parllel(10)
call_unlimited_times_within_a_time_period(seconds=10)