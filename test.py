import pymysql

print("step 1")

con = pymysql.connect(
    host='localhost',
    user='root',
    password='Zuckerberg1',
    database='15yrs'
)

print("step 2 - connected!")

cur = con.cursor()
cur.execute("CREATE TABLE customers (name VARCHAR(255), ID INT)")
con.commit()
print("Table created!")
con.close()