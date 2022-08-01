import sqlite3

# conn = sqlite3.connect('database.db')
# def createTable():
#     conn = sqlite3.connect('database.db')
#     c= conn.cursor()
#     c.execute('''CREATE TABLE users(name text, username text primary key, password text,email text not null unique, Slogin text, spassword text, sorgurl text, driverindex integer)''')
#     print('table has created')
#     conn.commit()

# createTable()
    

def insertRe(name, username, password,email):
    try:
        conn = sqlite3.connect('database.db')
        c= conn.cursor()
        string = 'insert into users values('+"'"+name+"', '"+username+"' ,  '"+password+"', "+"'"+email+"','','','','')"
        print(string)
        c.execute(string)
        conn.commit()
        print('record Inserted')
        conn.close()
        return True
    except:
        return False
        

# result = insertRe('test', 'test', 'test','test@test.com')
# print(result)

def verifylogin(username, password):
    try:
        conn = sqlite3.connect('database.db')
        query= 'SELECT password from users where username='+"'"+username+"'"
        print(query)
        c = conn.cursor()
        x = c.execute(query).fetchone()[0]
        print(x)
        conn.close()
        if x == password:
            return True
        else :
            return False
    except:
        return False

# res = verifylogin('ghans@007','ghans@007' )
# print(res)

def updateSinfo(username,slogin, spassword, sorgurl, driverIndex):
    try:
        conn = sqlite3.connect('database.db')
        query = 'Update users set slogin ='+"'" +slogin+"', spassword='"+spassword+"', sorgurl='"+sorgurl+"',  driverindex='"+str(driverIndex)+"' where username = '"+username+"'"
        print(query)
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e: 
        print(e)
        return False

# result =updateSinfo('ghanshyam', 'ghanshaymchaturvedi@vyomlabs.com','Radha#Me1', 'vyomlabs126-dev-ed.my.salesforce.com',0)
# print(result)

def fetchDriverindex(username):
    try:
        conn = sqlite3.connect('database.db')
        query='SELECT driverindex from users where username = '+"'"+username+"'"
        print(query)
        c = conn.cursor()
        x = c.execute(query).fetchone()[0]
        conn.close()
        print(x)
        return x
    except:
        return None

#result = fetchDriverindex('chaturvedi@007')
#print(result)

def updateDriverIndex(username, driverindex):
    try:
        conn = sqlite3.connect('database.db')
        query='update users set driverindex='+str(driverindex)+' where username='+"'"+username+"'"
        print(query)
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()
        return True
    except:
        return False

#result = updateDriverIndex('chaturvedi@007', 2)
#print(result)