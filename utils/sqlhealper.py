import pymysql

def get_list(sql,args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', database='db3')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def modify(sql,args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', database='db3')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    conn.commit()
    cursor.close()
    conn.close()


def get_one(sql,args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', database='db3')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result