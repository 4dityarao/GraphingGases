import sqlite3
conn = sqlite3.connect('login.db')
print('Database opened successfully')
def does_exists(user):
    global conn
    flag=0
    cursor=conn.execute('SELECT username FROM LoginDetails')
    for row in cursor:
        if row[0] == user:
            flag+=1
            break    
    if flag == 1:
        return True
    else:
        return False
    cursor.close()
    
def insert_user(user,passwd):
    global conn
    c=conn.cursor()
    c.execute("INSERT INTO LoginDetails (username , password ) VALUES (?,?)",(user,passwd))
    conn.commit()
    c.close()
name=input('Enter Username')
if does_exists(name):
    print('Username is already registered')
else:
    password=input('Enter PASSWORD')
    insert_user(name,password)
    print('USER SUCCESSFULLY REGISTERED!')
conn.close()



    
    

