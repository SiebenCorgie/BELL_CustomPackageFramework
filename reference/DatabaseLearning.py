import sqlite3


# Creates or opens a file called mydb with a SQLite3 DB
db = sqlite3.connect('myTestdb.db')
curser = db.cursor()

def Create():
    curser.execute('''
    CREATE TABLE program(
    id INTEGER PRIMARY KEY,
    name TEXT,
    net TEXT,
    screenlocation TEXT)
    ''')
    db.commit()

def add_entry(Sname,Snet,Sscreenloc):
    curser.execute('''INSERT INTO program(name, net, screenlocation) VALUES(?,?,?)''', (Sname, Snet, Sscreenloc))
    db.commit()


#Create()

print("executing")
add_entry('teddy', 'true', 'home/teddy/baer')
add_entry('rolf2', 'false','home/rolf/screen.png')
add_entry('lol', 'false','/ich/war/hier')
add_entry('geht','true','Loooks')

print('get all with teddy')

teddy = ('teddy',)

curser.execute('''SELECT ? FROM program WHERE name=? ''',('screenlocation', 'teddy'))
out = curser.fetchone()

print(out[0])

#for row in curser.execute('''SELECT screenlocation FROM program WHERE name=? ''', teddy):
#    for i in row:
#        print(i)
#    break

db.close()