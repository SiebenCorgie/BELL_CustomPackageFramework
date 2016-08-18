import sqlite3


# Creates or opens a file called mydb with a SQLite3 DB
db = sqlite3.connect('myTestdb.db')

curser = db.cursor()
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


print("executing")
add_entry('teddy', 'true', 'home/teddy/baer')
add_entry('rolf2', 'false','home/rolf/screen.png')

db.commit()


print('get first')

curser.execute('''SELECT name, net , screenlocation FROM program''')
for row in curser:
    print ('name: {0} , state: {1} , loc: {2}'.format(row[0], row[1] , row[2]))
print()

db.close()