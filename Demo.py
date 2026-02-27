import pymysql
con = pymysql.connect(
        user='root',
        host='localhost',
        database='15yrs',
        passwd='Zuckerberg1'
    )
cur = con.cursor()
cur.execute("CREATE TABLE chicken (name VARCHAR(255), ID INT)")
con.commit()