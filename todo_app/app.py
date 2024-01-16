from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import *

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('item')
    add_item(title)
    return redirect('/')
