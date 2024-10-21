from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config
from todo_app.data.mongo_service import MongoService
from todo_app.data.view_model import ViewModel
from todo_app.data.status_enum import Status


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    mongoService = MongoService()

    @app.route('/')
    def index():
        board_items = mongoService.get_items()
        item_view_model = ViewModel(board_items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    def add():
        title = request.form.get('item')
        mongoService.add_item(title)
        return redirect('/')

    @app.route('/complete_item/<item_id>')
    def complete_item(item_id):
        mongoService.move_item_to_list(item_id, Status.DONE.value)
        return redirect('/')

    @app.route('/reopen_item/<item_id>')
    def reopen_item(item_id):
        mongoService.move_item_to_list(item_id, Status.TODO.value)
        return redirect('/')

    return app
