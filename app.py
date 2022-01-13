from dataclasses import dataclass
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yousra/Desktop/apps/todo-test-back/database.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email


@dataclass
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description =db.Column(db.String(500))
    date = db.Column(db.Date)
    done = db.Column(db.Boolean)

    def __repr__(self):
        return '<Todo %r>' % self.title

    
@app.route("/user", methods=["POST"])
def signup():
    new = User(email=request.json['email'])
    db.session.add(new)
    db.session.commit()
    data = {'message': 'Created', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 201)

@app.route("/todo", methods=["POST"])
def addTodo():
    if request.json['description'] != '':
        new = Todo(title=request.json['title'],
                description=request.json['description'],
                date=datetime.strptime(request.json['date'], "%Y-%m-%d"),
                done=False)
    else:
        new=Todo(title=request.json['title'],
                description=request.json['description'],
                done=False)
    
    db.session.add(new)
    db.session.commit()
    data = {'message': 'Created', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 201)

@app.route("/todos", methods=["GET"])
def GetTodos():
    todos=Todo.query.all()
    return make_response(jsonify(todos), 200)