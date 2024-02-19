import os
import requests
import json

api_key = os.environ.get('TRELLO_API_KEY')
api_token = os.environ.get('TRELLO_API_TOKEN')
board_id = os.environ.get('BOARD_ID')
todo_list_id = os.environ.get('TODO_LIST_ID')

base_url = "https://api.trello.com/"
base_query = {
    'key': api_key,
    'token': api_token
}
headers = {
    "Accept": "application/json"
}


def send_request(url, action="GET", query=base_query):
    return requests.request(action, url, headers=headers, params=query)


def get_cards_from_board():
    url = f"{base_url}1/boards/{board_id}/cards"
    response = send_request(url)

    return json.loads(response.text)


def get_list_from_board(list_id):
    url = f"{base_url}1/lists/{list_id}"
    response = send_request(url)

    return json.loads(response.text)


def add_item(title):
    url = f"{base_url}1/cards"
    query = base_query | {
        'idList': todo_list_id,
        'name': title
    }

    send_request(url, "POST", query)


def move_item_to_list(id, list_id):
    url = f"{base_url}1/cards/{id}"
    query = base_query | {
        'idList': list_id
    }

    send_request(url, "PUT", query)
