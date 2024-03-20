import pytest
from todo_app.data.item import Item
from todo_app.data.view_model import ViewModel

# Arrange


@pytest.fixture
def todo_item():
    return Item(1, "Test Todo Item", "Test Todo Desc", "To Do")


@pytest.fixture
def done_item():
    return Item(2, "Test Done Item", "Test Done Desc", "Done")


@pytest.fixture
def items(todo_item, done_item):
    return [todo_item, done_item]


@pytest.fixture
def view_model(items):
    return ViewModel(items)


def test_view_model_done_items_returns_only_done_items(view_model, done_item):
    # Act
    returned_items = view_model.done_items

    # Assert
    assert len(returned_items) == 1
    assert returned_items[0] == done_item


def test_view_model_todo_items_returns_only_todo_items(view_model, todo_item):
    # Act
    returned_items = view_model.todo_items

    # Assert
    assert len(returned_items) == 1
    assert returned_items[0] == todo_item
