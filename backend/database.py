from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 开启sql语句的显示
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

        
class User(db.Model):
    __tablename = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    # email = db.Column(db.String(128), nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, username, password, phone):
        print("Initializing database...")
        self.username = username
        self.password = password
        self.phone = phone

    def __repr__(self):
        return '<User %r>' % self.username


# class Classes(db.Model):
#     __tablename = 'classes'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True, nullable=False)
#     users = db.relationship("User", backref="classes")

#     def __repr__(self):
#         return '<Classes %r>' % self.name

