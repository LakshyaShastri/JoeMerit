import MySQLdb

db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
cursor = db.cursor()




######---:sunglasses:---######
def qwe(query):
    cursor.execute(query)



def get_test_name_dict():

    cursor.execute("USE admin")
    cursor.execute("SHOW TABLES")
    test_names = cursor.fetchall()
    
    temp_list = []

    for test_name in test_names:

        final_str = test_name[1:(len(test_name)-2)]

        temp_list.append(final_str)

    #going back to the student db
    cursor.execute("USE students")

    return dict(list(enumerate(temp_list)))

    