import os
import requests


class TrelloService():

    def __init__(self):
        self.api_key = os.environ.get('TRELLO_API_KEY')
        self.api_token = os.environ.get('TRELLO_API_TOKEN')
        self.board_id = os.getenv('BOARD_ID')
        self.todo_list_id = os.environ.get('TODO_LIST_ID')
        self.done_list_id = os.environ.get('DONE_LIST_ID')

        self.base_url = "https://api.trello.com/"
        self.base_query = {
            'key': self.api_key,
            'token': self.api_token
        }
        self.headers = {
            "Accept": "application/json"
        }

    def send_request(self, url, query, action="GET"):
        return requests.request(action, url, headers=self.headers, params=query)

    def get_cards_from_board(self):
        url = f"{self.base_url}1/boards/{self.board_id}/cards"
        response = self.send_request(url, self.base_query)

        return response.json()

    def get_list_from_board(self, list_id):
        url = f"{self.base_url}1/lists/{list_id}"
        response = self.send_request(url, self.base_query)

        return response.json()

    def add_item(self, title):
        url = f"{self.base_url}1/cards"
        query = self.base_query | {
            'idList': self.todo_list_id,
            'name': title
        }

        self.send_request(url, query, "POST")

    def move_item_to_list(self, id, list_id):
        url = f"{self.base_url}1/cards/{id}"
        query = self.base_query | {
            'idList': list_id
        }

        self.send_request(url, query, "PUT")
