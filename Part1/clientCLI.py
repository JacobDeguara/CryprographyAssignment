import requests
import json
from urllib.parse import quote_plus
from urllib.parse import quote

try:
    # Login
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        response = requests.get(
            "http://127.0.0.1:8000/login?username=" + username + "&password=" + password
        )
        if response.status_code == 200:
            break
        else:
            print("ERR -- Wrong username or password --\n")

    response_json = json.loads(response.text)
    user_token = response_json["Token"]

    while True:
        while True:
            print("--------------")
            print("1. Change drones positions")
            print("2. Get drone position")
            print("3. Get All drone names")
            print("4. Get All drone positions")
            print("5. Logout")
            print("--------------")

            choice = input("Enter Choice: ")
            try:
                choice = int(choice)
                break
            except Exception as ex:
                print("ERR -- Input a number please -- ")

        if choice == 5:
            break

        if choice == 1:
            token_url = quote(user_token)
            response = requests.get(
                "http://127.0.0.1:8000/drone/setup?access_token=" + token_url
            )
            if response.status_code == 200:
                print("All the drones have been give new positions")
            else:
                print(
                    "ERR -- Access Code has failed -- IMP: please logout and login --"
                )

        if choice == 2:
            drone_name = input("\nEnter drone name: ")
            response = requests.get(
                "http://127.0.0.1:8000/drone/getpos?drone_name=" + drone_name
            )
            if response.status_code == 200:
                response_json = json.loads(response.text)
                print("" + drone_name + " Pos:" + str(response_json["Drone_position"]))
            else:
                print("ERR -- Drone with " + drone_name + " doesnt exist  --")

        if choice == 3:
            response = requests.get("http://127.0.0.1:8000/drone/getalldronenames")
            if response.status_code == 200:
                response_json = json.loads(response.text)
                print(response_json["Drone_names"])

        if choice == 4:
            response = requests.get("http://127.0.0.1:8000/drone/getalldronepositions")
            if response.status_code == 200:
                response_json = json.loads(response.text)
                print(response_json["Drone_positions"])

except:
    print("error occured")

    # Removeing Access token / logout
token_url = quote(user_token)
response = requests.get("http://127.0.0.1:8000/logout?access_token=" + token_url)
if not response.status_code == 200:
    print(
        "ERR -- Access Code was not removed -- IMP: this is a possible breach of access --"
    )
