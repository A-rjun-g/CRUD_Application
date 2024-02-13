import pytest
from src.routesTodo import app
from src import db
from src.models import Todo


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h1>Todo App</h1>' in response.data

def test_home_route(client):
    response = client.get('/home/')
    assert response.status_code == 200
    assert b'<h1>TODO LIST</h1>' in response.data

def test_add_route(client):
    response = client.post('/addItemTotheList/', data={'todoitem': 'Test Todo'})
    assert response.status_code == 302

    with app.app_context():
        last_todo = Todo.query.order_by(Todo.id.desc()).first()
        assert last_todo is not None
        assert last_todo.text == 'Test Todo'
        assert last_todo.complete == False

    #Deleting the Entered test Query    
    with app.app_context():
        db.session.query(Todo).delete()
        db.session.commit()

def test_complete_route(client):
    response = client.post('/addItemTotheList/', data={'todoitem': 'Test Todo'})
    assert response.status_code == 302

    with app.app_context():
        last_todo = Todo.query.order_by(Todo.id.desc()).first()
        todo_id = last_todo.id

    response = client.get(f'/completeTask/{todo_id}')
    assert response.status_code == 302

    with app.app_context():
        completed_todo = Todo.query.get(todo_id)
        assert completed_todo is not None
        assert completed_todo.complete == True

    #Deleting the Entered test Query    
    with app.app_context():
        db.session.query(Todo).delete()
        db.session.commit()

def test_delete_route():
    with app.app_context():
        newTodo = Todo(text='Test Todo', complete=False)
        db.session.add(newTodo)
        db.session.commit()
        todoId=newTodo.id

        todoToDelete = Todo.query.get(todoId)
        if todoToDelete:
            db.session.delete(todoToDelete)
            db.session.commit()