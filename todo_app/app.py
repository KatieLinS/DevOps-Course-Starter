from flask import Flask, render_template, request, redirect, url_for
from flask_dance.contrib.github import github
from werkzeug.middleware.proxy_fix import ProxyFix
from todo_app.flask_config import Config
from todo_app.data.mongo_service import MongoService
from todo_app.data.view_model import ViewModel
from todo_app.data.status_enum import Status
from todo_app.oauth import blueprint
from loggly.handlers import HTTPSHandler
from logging import Formatter
import functools


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(Config())
    app.register_blueprint(blueprint, url_prefix="/login")
    mongoService = MongoService()

    app.logger.setLevel(app.config['LOG_LEVEL'])
    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        handler.setFormatter(
            Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
        )
        app.logger.addHandler(handler)


    def login_required(func):
        @functools.wraps(func)
        def wrapper_login_required(*args, **kwargs):
            if not github.authorized:
                return redirect(url_for("github.login"))
            return func(*args, **kwargs)
        return wrapper_login_required

    @app.route('/')
    @login_required
    def index():
        board_items = mongoService.get_items()
        item_view_model = ViewModel(board_items)
        app.logger.info("Logged in to homepage")
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    @login_required
    def add():
        title = request.form.get('item')
        mongoService.add_item(title)
        app.logger.info(f"Added an item: {title}")
        return redirect('/')

    @app.route('/complete_item/<item_id>')
    @login_required
    def complete_item(item_id):
        mongoService.move_item_to_list(item_id, Status.DONE.value)
        app.logger.info(f"Completed an item: {item_id}")
        return redirect('/')

    @app.route('/reopen_item/<item_id>')
    @login_required
    def reopen_item(item_id):
        mongoService.move_item_to_list(item_id, Status.TODO.value)
        app.logger.info(f"Reopened an item: {item_id}")
        return redirect('/')

    return app
