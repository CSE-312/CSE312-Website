import base64
import json
import random
from urllib.parse import urlencode

from flask import Flask, send_from_directory, render_template, request, make_response
from pymongo import MongoClient
import requests

import autolab_config

mongo_client = MongoClient("mongo")
db = mongo_client["autolab"]
users_collection = db["users"]


def start_session():
    token = "121wqwefwef4thisistotallyrandom" + str(random.random())
    state = "somerandomthing" + str(random.random())
    users_collection.insert_one({"token": token, "state": state})
    return [token, state]


def handle_code_after_redirect(req: request):
    cookie_token = req.cookies.get("token")
    user_record = users_collection.find_one({"token": cookie_token})

    if user_record:
        code = req.values.get("code")
        state = req.values.get("state")
        if state != user_record.get("state"):
            print("shit's broke yo. You might even be under attack")
        else:
            users_collection.update_one({"token": cookie_token}, {"$set": {"code": code}})
            token = cash_in_code_for_token(code, cookie_token)
            [users_email, users_name] = user_info(token, cookie_token)
            return [users_email, users_name]

    else:
        print("where did this user come from??")
        print("just crash")
        return ["unknown", "Something went wrong. Where's your cookie?"]


def cash_in_code_for_token(code, token):
    token_url = "https://autolab.cse.buffalo.edu/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "client_id": autolab_config.client_id,
        "client_secret": autolab_config.client_secret,
        "redirect_uri": autolab_config.redirect_uri
    })

    response = requests.post(token_url, headers=headers, data=data)
    print(response)
    the_good_stuff = json.loads(response.content.decode())
    access_token = the_good_stuff.get("access_token")
    refresh_token = the_good_stuff.get("refresh_token")
    scope = the_good_stuff.get("scope")
    expires_in = the_good_stuff.get("expires_in")
    created_at = the_good_stuff.get("created_at")

    users_collection.update_one({"token": token}, {"$set": the_good_stuff})

    return access_token


def user_info(access_token, token):
    user_url = "https://autolab.cse.buffalo.edu/api/v1/user"
    headers = {
        "Authorization": "Bearer " + access_token
    }
    response = requests.get(user_url, headers=headers)
    print(response)
    user_data = json.loads(response.content.decode())
    email = user_data.get("email")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    users_collection.update_one({"token": token}, {"$set": user_data})
    return [email, first_name + " " + last_name]


def check_token(token):
    user_record = users_collection.find_one({"token": token})
    if user_record and "email" in user_record:
        return [user_record.get("email"),
                user_record.get("first_name") + " " + user_record.get("last_name")]
    else:
        return [None, None]


if __name__ == '__main__':
    pass
    print(urlencode({"re": " "}))
    # users_collection.insert_one({"token": "token", "state": "state"})

    # cash_in_code_for_token()
    # dic = {}
    # x = dic.get("code")
    # print(x)
    # user_info()
