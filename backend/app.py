# app.py
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # Use SQLite database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app, origins="*", resources=r'/*', supports_credentials= True)
app.config['CORS_HEADERS'] = 'Content-Type'

from database import *

headers = {
    'Cache-Control' : 'no-cache, no-store, must-revalidate',
    'Pragma' : 'no-cache' ,
    'Expires': '0' ,
    # 'Access-Control-Allow-Origin' : 'http://localhost:3000',
    # 'Access-Control-Allow-Origin' : '*',
    'Access-Control-Allow-Methods': 'GET, POST, PATCH, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'
}


@app.route('/login', methods=['POST'])
@cross_origin(origins="*", supports_credentials= True)
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        response = make_response(jsonify({'message': '缺少用户名或密码'}), 400)
    else:
        user = User.query.filter_by(username=username).first()
        if user is None or user.password != password:
            response = make_response(jsonify({'message': '用户名或密码不正确'}), 401)
        else:
            response = make_response(jsonify({'message': '登录成功'}), 200)
    
    response.headers = headers
    return response

@app.route('/register', methods=['POST'])
@cross_origin(origins="*", supports_credentials= True)
def register():
    print("Registering...")
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    code = data.get('code')
    # Used to compare with the auth code
    # email = data.get('email')
    phone = data.get('phone')
    # if not username or not password or not email or not phone:
    if not username or not password or not phone:
        response = make_response(jsonify({'message': '缺少用户名、密码或手机号'}), 400)
    elif not code:
        response = make_response(jsonify({'message': '缺少验证码'}), 400)
    else:
        if User.query.filter_by(username=username).first():
            response = make_response(jsonify({'message': '该用户名已被注册，请更换其他用户名'}), 400)
        else:
            # new_user = User(username=username, password=password, email=email, phone=phone)
            new_user = User(username=username, password=password, phone=phone)
            db.session.add(new_user)
            db.session.commit()
            response = make_response(jsonify({'message': '注册成功'}), 200)
    
    response.headers = headers
    
    return response

# @app.route('/changepwd', methods=['POST'])
# @cross_origin(origins="*", supports_credentials= True)
# def register():
#     print("Changing Password...")
#     data = request.get_json()
#     username = data.get('username')
#     newpassword1 = data.get('newpassword1')
#     newpassword2 = data.get('newpassword2')
#     code = data.get('code')
#     # email = data.get('email')
#     phone = data.get('phone')
#     # if not username or not password or not email or not phone:
#     if not username or not newpassword1 or not newpassword2 or not phone:
#         response = make_response(jsonify({'message': 'Missing data'}), 400)
#     else:
#         if User.query.filter_by(username=username).first():
#             response = make_response(jsonify({'message': 'Username already taken'}), 400)
#         else:
#             # new_user = User(username=username, password=password, email=email, phone=phone)
#             new_user = User(username=username, password=password, phone=phone)
#             db.session.add(new_user)
#             db.session.commit()
#             response = make_response(jsonify({'message': 'Registration successful'}), 200)
    
#     response.headers = headers
    
#     return response



if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True)
