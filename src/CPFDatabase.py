import cpf
import CPFConf as conf
import CPFWeb as web

#database sql
import sqlite3

def db_connect():
	global c
	dblocation = conf.get_entry('DB','currentdb')
	#Datenbank
	db = sqlite3.connect(dblocation)
	#Zeiger
	c = db.cursor()

def add_db():
	db_connect()
	c.execute('''create table CPFDB
	(id INTEGER PRIMARY KEY, name text,describtion_short text, describtion_long text, screenshotloc text, ubuntu_id text,
	debian_id text, arch_id text, symbol text, category text)''')

	db.commit()
	selfdb.close()

#Daten einfügen
def db_add_entry(name, desc_s, desc_l, screenshotloc, ubuntu_id, debian_id, arch_id, symbol, category):
	db_connect()
	
	c.execute('''INSERT INTO CPFDB(name, describtion_short, describtion_long, screenshotloc, ubuntu_id, debian_id, arch_id, symbol, category)
                  VALUES(?,?,?,?,?,?,?,?,?)''', (name, desc_s, desc_l, screenshotloc, ubuntu_id, debian_id, arch_id, symbol, category))
	db.commit()
	db.close()

#read entrys
def db_read():
	global c
	db_connect()
	for row in c.execute('SELECT * FROM CPFDB ORDER BY name'):
		print(row)