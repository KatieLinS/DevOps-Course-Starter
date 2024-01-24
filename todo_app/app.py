from flask import Flask, render_template, request, redirect
from operator import itemgetter
import todo_app.data.session_items as session_items

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = session_items.get_items()
    sorted_items = sorted(items, key=itemgetter('status'), reverse=True) 
    return render_template('index.html', items=sorted_items)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('item')
    session_items.add_item(title)
    return redirect('/')

@app.route('/update_status/<item_id>', methods=['POST'])
def update_status(item_id):
    item = session_items.get_item(item_id)
    item['status'] = 'Completed' if item['status'] == 'Not Started' else 'Not Started'
    session_items.save_item(item)
    return redirect('/')

@app.route('/delete_item/<item_id>', methods=['POST'])
def delete(item_id):
    item = session_items.get_item(item_id)
    session_items.delete_item(item)
    return redirect('/')