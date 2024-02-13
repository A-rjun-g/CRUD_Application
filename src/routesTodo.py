from flask import render_template, request, url_for, redirect
from src import create_app, db
from src.models import Todo

app = create_app()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home/")
def home():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    return render_template("home.html", incompleteTasks=incomplete, completedTasks=complete)

@app.route("/addTaskToList/", methods=['POST'])
def addTask():
    todoWork = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todoWork)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/completeTask/<int:id>")
def completeTask(id):
    todo = Todo.query.get(id)
    todo.complete = True
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/deleteTask/<int:id>")
def deleteTask(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
