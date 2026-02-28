from dotenv import load_dotenv
load_dotenv(override=True)
import os
print("HOST:", os.environ.get('MYSQLHOST'))
print("USER:", os.environ.get('MYSQLUSER'))
print("PASS:", os.environ.get('MYSQLPASSWORD'))
from flask import Flask, jsonify, request
import pymysql
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'Zuckerberg123456789_ExpenseTracker_2026'
jwt = JWTManager(app)
con = pymysql.connect(
    host=os.environ.get('MYSQLHOST'),
    user=os.environ.get('MYSQLUSER'),
    password=os.environ.get('MYSQLPASSWORD'),
    database=os.environ.get('MYSQLDATABASE'),
    port=int(os.environ.get('MYSQLPORT', 3306)),
    cursorclass=pymysql.cursors.DictCursor
)
@app.route('/register',methods=['POST'])
def register():
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']
    password_hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    cur=con.cursor()
    cur.execute('INSERT INTO users(user_name,user_email,password_hash) VALUES(%s,%s,%s)',(username,email,password_hash))
    con.commit()
    return jsonify({'Message':'User registered succesfully'}),201
@app.route('/login',methods=['POST'])
def login():
    email=request.json['email']
    password=request.json['password']
    cur=con.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM users WHERE user_email=%s',(email,))
    user=cur.fetchone()
    if not user:
        return jsonify({'Message':'User not found'}),404
    if user:
        if bcrypt.checkpw(password.encode('utf-8'),user['password_hash'].encode('utf-8')):
            token=create_access_token(identity=str(user['user_ID']))
            return jsonify({'Message':'Login Successful','token':token}),200
        else:
            return jsonify({'Message':'Wrong password'}),401
@app.route('/addcategory',methods=['POST'])
@jwt_required()
def addcategory():
    category_name=request.json['category_name']
    category_type=request.json['category_type']
    user_ID=get_jwt_identity()
    cur=con.cursor()
    cur.execute('INSERT INTO categories(category_name,category_type,user_ID) VALUES(%s,%s,%s)',(category_name,category_type,user_ID))
    con.commit()
    return jsonify({'Message':'Category saved'}),201
@app.route('/addtransaction',methods=['POST'])
@jwt_required()
def addtransaction():
    category_ID=request.json['category_ID']
    category_type=request.json['category_type']
    user_ID=get_jwt_identity()
    amount=request.json['amount']
    cur=con.cursor()
    cur.execute('INSERT INTO transactions(category_ID,category_type,user_ID,amount,created_at) VALUES(%s,%s,%s,%s,NOW())',(category_ID,category_type,user_ID,amount))
    con.commit()
    return jsonify({'Message':'New transaction added'})
@app.route('/get_transactions',methods=['GET'])
@jwt_required()
def get_transactions():
    user_ID=get_jwt_identity()
    cur=con.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM transactions WHERE user_ID=%s',(user_ID,))
    total=cur.fetchall()
    return jsonify({'Message':total})
@app.route('/search',methods=['GET'])
@jwt_required()
def search():
    user_ID=get_jwt_identity()
    category_type=request.args.get('category_type')
    category_ID=request.args.get('category_ID')
    start_date=request.args.get('start_date')
    end_date=request.args.get('end_date')
    query='SELECT * FROM transactions WHERE user_ID=%s'
    values=[user_ID]
    if category_type:
        query+=' AND category_type=%s'
        values.append(category_type)
    if category_ID:
        query+=' AND category_ID=%s'
        values.append(category_ID)
    if start_date:
        query+=' AND created_at>=%s'
        values.append(start_date)
    if end_date:
        query+=' AND created_at<=%s'
        values.append(end_date)
    cur=con.cursor(pymysql.cursors.DictCursor)
    cur.execute(query,tuple(values))
    output=cur.fetchall()
    return jsonify({'Message':output})
if __name__=="__main__":
    app.run(debug=True)