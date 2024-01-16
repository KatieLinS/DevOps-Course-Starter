from flask import Flask, render_template, request, redirect
from operator import itemgetter
from todo_app.data.session_items import *

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    sorted_items = sorted(items, key=itemgetter('status'), reverse=True) 
    return render_template('index.html', items=sorted_items)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('item')
    add_item(title)
    return redirect('/')

@app.route('/update_status/<item_id>', methods=['POST'])
def update_status(item_id):
    item_checked = False if not request.form.get('checkbox') else True
    item = get_item(item_id)
    item['status'] = 'Completed' if item_checked else 'Not Started'
    save_item(item)
    return redirect('/')

@app.route('/delete_item/<item_id>', methods=['POST'])
def delete(item_id):
    item = get_item(item_id)
    delete_item(item)
    return redirect('/')