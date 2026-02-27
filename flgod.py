from flask import Flask,jsonify
import pymysql
app=Flask(__name__)
con= pymysql.connect(
    host='localhost',
    user='root',
    password='Zuckerberg1',
    database='15yrs'
    )
@app.route('/getTable',methods=['GET'])
def get_tables():
    cur=con.cursor()
    cur.execute("SHOW TABLES;")
    tables=cur.fetchall()
    cur.close()
    con.close()
    table_names=[table[0] for table in tables]
    return jsonify({"tables":table_names}),200
if __name__=="__main__":
    print("conecting to DB...")
    app.run(debug=True)