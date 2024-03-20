from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config
from todo_app.data.trello_service import TrelloService
from todo_app.data.view_model import ViewModel


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    trelloService = TrelloService()

    @app.route('/')
    def index():
        board_items = trelloService.get_cards_from_board()
        item_view_model = ViewModel(board_items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    def add():
        title = request.form.get('item')
        trelloService.add_item(title)
        return redirect('/')

    @app.route('/complete_item/<item_id>')
    def complete_item(item_id):
        trelloService.move_item_to_list(item_id, trelloService.done_list_id)
        return redirect('/')

    @app.route('/reopen_item/<item_id>')
    def reopen_item(item_id):
        trelloService.move_item_to_list(item_id, trelloService.todo_list_id)
        return redirect('/')

    return app
