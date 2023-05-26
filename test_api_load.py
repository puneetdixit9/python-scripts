"""
Change request_headers, request_url, request_body and data according to your requirement in below functions.
1. get_request_data
2. post_request_data
3. put_request_data
"""

import time
import requests
from multiprocessing import Process, Value

response_count = Value('i', 0)
api_call_count = Value('i', 0)


def call_api(method: str, url: str, headers: dict = dict, data: dict = dict, json: dict = dict, print_response=False):
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
    if print_response:
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
    return p


def call_api_in_parallel_n_times(n=1):
    process_list = []
    args = put_request_data()  # change the method according to your requirement (get, put or post)
    start_time = time.time()
    for i in range(n):
        start_process(args, process_list)

    for p in process_list:
        p.join()
    print(f"Total time taken to call a api {n} times parallely : {time.time()-start_time}")


def call_api_in_parallel_unlimited_times_within_a_time_period(minutes=0, seconds=1):
    total_seconds = (60 * minutes) + seconds
    end_time = time.time() + total_seconds
    process_list = []
    args = put_request_data()  # change the method according to your requirement (get, put or post)
    while end_time > time.time():
        p =start_process(args, process_list)
        p.join()

    print(f"Number of times API called in {total_seconds} seconds is {api_call_count.value} and response received for {response_count.value}")

    # remaining_response = api_call_count.value - response_count.value
    # print("Waiting to received response of remaining APIs...")
    # response_time_start = time.time()
    # for p in process_list:
    #     p.join()
    # print(f"Time taken to received response of remaining {remaining_response} APIs is {time.time()-response_time_start}")


# CALL THESE FUNCTION TO TEST.

call_api_in_parallel_n_times(30)
call_api_in_parallel_unlimited_times_within_a_time_period(seconds=10)