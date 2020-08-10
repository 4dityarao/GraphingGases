import sqlite3
conn = sqlite3.connect('login.db')
print('Database opened successfully')
cursor=conn.execute("SELECT username , password FROM LoginDetails")
u=input('Enter USERNAME')
p=input('Enter PASSWORD')
flag=0
for row in cursor:
    if row[0] == u:
        if row[1] == p:
            print('LOGIN SUCCESSFUL!')
            flag+=1
            break
        else:
            print('Incorrect USERNAME OR PASSWORD')
            break
if flag != 1:
    print('LOGIN UNSUCCESSFUL!')
cursor.close()
conn.close()

    
    

