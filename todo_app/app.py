from flask import Flask, render_template, request, redirect
from todo_app.data.item import Item
import todo_app.data.trello_items as trello_items
import os

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

todo_list_id = os.environ.get('TODO_LIST_ID')
todo_list = trello_items.get_list_from_board(todo_list_id)

done_list_id = os.environ.get('DONE_LIST_ID')
done_list = trello_items.get_list_from_board(done_list_id)


@app.route('/')
def index():
    board_items = trello_items.get_cards_from_board()
    items = []
    for item in board_items:
        items.append(Item.from_trello_card(
            item, todo_list if item["idList"] == todo_list_id else done_list))
    return render_template('index.html', items=items)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('item')
    trello_items.add_item(title)
    return redirect('/')


@app.route('/complete_item/<item_id>')
def complete_item(item_id):
    trello_items.move_item_to_list(item_id, done_list_id)
    return redirect('/')


@app.route('/reopen_item/<item_id>')
def reopen_item(item_id):
    trello_items.move_item_to_list(item_id, todo_list_id)
    return redirect('/')
