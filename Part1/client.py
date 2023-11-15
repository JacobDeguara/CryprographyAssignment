import requests
import json

myobj = {"token": 0}


login_loop: bool = True
while login_loop:
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    response = requests.post(
        "http://127.0.0.1:8000/login?username=" + username + "&password=" + password
    )
    if response.status_code == 200:
        login_loop = False
    else:
        print("ERR -- Wrong user or username --")

response_json = json.loads(response.text)
user_token = response_json["token"]

loop: bool = True
while loop:
    input_loop = True
    while input_loop:
        print("--------------")
        print("1. Change drone position")
        print("2. Get drone position")
        print("3. Logout")
        print("--------------")

        choice = input("Enter Choice: ")
        try:
            choice = int(choice)
            input_loop = False
        except Exception as ex:
            print("ERR -- Input a number please -- ")

    if choice == 1:
        response = requests.get(
            "http://127.0.0.1:8000/drone/setup?access_token=" + user_token
        )
        if response.status_code == 200:
            print("The drones have been give new positions")
        else:
            print("ERR -- This function has failed to work --")

    if choice == 2:
        drone_name = input("\nEnter drone name: ")
        response = requests.get(
            "http://127.0.0.1:8000/drone/getpos?access_token="
            + user_token
            + "&drone_number="
            + drone_name
        )
        if response.status_code == 200:
            response_json = json.loads(response.text)
            print("" + drone_name + " Pos:" + response_json["token"])
        else:
            print("ERR -- This function has failed to work --")

    if choice == 3:
        response = requests.get(
            "http://127.0.0.1:8000/logout?access_token=" + user_token
        )
        loop = False
