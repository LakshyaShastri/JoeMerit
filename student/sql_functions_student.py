import MySQLdb
import os

db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
cursor = db.cursor()

def get_test_name_dict():

    cursor.execute("USE admin")
    cursor.execute("SHOW TABLES")
    test_names = cursor.fetchall()
    
    temp_list = []

    for test_name in test_names:
        final_str = test_name[1:(len(test_name)-2)]
        temp_list.append(final_str)

    return dict(list(enumerate(temp_list, start=1)))
