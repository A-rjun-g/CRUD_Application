import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String(200))
    complete=db.Column(db.Boolean)

    def __repr__(self) -> str:
        return f'<Todo {self.text}>'

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home/")
def home():
    incomplete=Todo.query.filter_by(complete=False).all()
    complete=Todo.query.filter_by(complete=True).all()
    return render_template("home.html",incompleteTasks=incomplete,completedTasks=complete)


@app.route("/add/",methods=['POST'])
def add():
    todoWork=Todo(text=request.form['todoitem'],complete=False)
    db.session.add(todoWork)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/complete/<id>")
def complete(id):
    todo=Todo.query.filter_by(id=int(id)).first()
    todo.complete=True
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete/<id>")
def delete(id):
    todo=Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

if __name__=='__main__' :
    app.run(debug=True)