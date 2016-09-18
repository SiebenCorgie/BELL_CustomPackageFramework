import cpf
import CPFConf as conf
import CPFWeb as web
import SystemInteraction as SI

import gi.repository
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

#database sql
import sqlite3


#Verbindung Herstellen
def db_connect():
	
	global c
	global db

	dblocation = conf.get_entry('DB','currentdb')

	#Datenbank
	db = sqlite3.connect(dblocation)
	#Zeiger
	c = db.cursor()

#MainCategory anzeige im Datensatz Dialog	
def db_add_Init(builder):

	
	#laden der liste aus konfiguration
	MainCat = builder.get_object('DB_A_Main')
	#basierend auf sprache
	if conf.get_entry('main','language') == 'GER':
		MainStringList = conf.get_entry('DB','GERMain')
	else:
		MainStringList = conf.get_entry('DB','ENMain')

	MainStringList = MainStringList.split(',')
	MainCategoryList = []

	#Einfügen in Box
	for CatName in MainStringList:
		MainCategoryList.append(CatName)

	MainCat.remove_all()
	#add to Main Window
	for i in MainCategoryList:
		MainCat.append_text(i)


#SubCategory Anzeige iim Datensatz-Dialog
def update_sub_category(builder):
	SubCat = builder.get_object('DB_Sub')
	maincategory = builder.get_object('DB_A_Main')
	maincat = maincategory.get_active_text()

	if conf.get_entry('main','language') == 'GER':
		SubCategoryList = conf.get_entry('DBSub','ger' + maincat.lower())
	else:
		SubCategoryList = conf.get_entry('DBSub','en' + maincat.lower())
	#convertToList
	SubCategoryList = SubCategoryList.split(',')
	#AddToLists
	SubCat.remove_all()
	for subindex in SubCategoryList:
		SubCat.append_text(subindex)
	

#Datenbankerstellung
def add_db(builder):

	locationL = builder.get_object('CND_Locatio')
	nameL = builder.get_object('CND_Name')
	dblocation = locationL.get_filename() + '/' + nameL.get_text()
	dbfolderlocation = locationL.get_current_folder()
	print(dblocation)

	#create and read db

	db = sqlite3.connect(dblocation)
	c = db.cursor()
	
	#Erstellung Der Ordner für Screenshots und Symbole
	locationstruct = locationL.get_filename()
	try:
		SI.execute('cd ' + locationstruct + ' && mkdir Screenshots && mkdir Symbols', False)
	except:
		print("there was a problem when creating the database file structure")

	
	#Erstellung Tabelle, Fester Name
	c.execute('''create table CPFDB
	(id INTEGER PRIMARY KEY, 
	name text,
	description_short text, 
	description_long text, 
	screenshotloc text, 
	ubuntu_id text,
	debian_id text, 
	arch_id text, 
	symbol text, 
	maincategory text, 
	subcategory text,
	URL text)''')

	db.commit()
	db.close()

	#Wenn aktiviert eintragung der Neuen Datebank in Konfigurationsdatei
	bUseB = builder.get_object('CND_bUseNew')
	bUse = bUseB.get_active()

	if bUse == True:
		conf.set_entry('DB','currentdb', dblocation)
		conf.set_entry('DB','dblocation', dbfolderlocation)
	

#Daten einfügen
def db_add_entry(builder):
	global c
	global db
	db_connect()

	nameL = builder.get_object('DB_A_NameEdit')
	name =  nameL.get_text()

	desc_sL = builder.get_object('DB_A_DescS_Edit')
	desc_s = desc_sL.get_text()

	desc_lL = builder.get_object('DB_A_DescL_Edit')
	desc_l = desc_lL.get_text()

	#ScreenshotFile_____________________________________________________________
	#Kopieren des Screenshots in Datenbank
	screenshotchooser = builder.get_object('DB_A_ScreenChooser')
	LocalScreenLocation = screenshotchooser.get_filename()
	if LocalScreenLocation == None:
		ErrorMessage(builder)
		return
		
	LocalScreenName = LocalScreenLocation[len(screenshotchooser.get_current_folder())+1:]

	#make final name
	screenshotloc = '/Screenshots/' + LocalScreenName

	#copy to local git repo
	DatabaseLocation = SI.execute('dirname ' + conf.get_entry('DB','currentdb'), True)
	#print('DatabaseLoc = ' + DatabaseLocation )
	ScreenshotLocations = DatabaseLocation + '/Screenshots/'
	#print('ScreenLocation: ' + ScreenshotLocations)
	try:
		SI.execute('cp ' + LocalScreenLocation + ' ' + ScreenshotLocations, False) 
	except:
		SI.execute('cd ' + DatabaseLocation + ' && mkdir Screenshots')
		try:
			SI.execute('cp -r ' + LocalScreenLocation + ' ' + ScreenshotLocations, False) 	
		except:
			ErrorMessage(builder)
			
	print('Copied Screenshot file')

	#SymbolFile_________________________________________________________________
	#Kopieren des Symbol in Datenbank
	SymbolChooser = builder.get_object('DB_A_SymbolChooser')
	LocalSymbolLocation = SymbolChooser.get_filename()
	if LocalSymbolLocation == None:
		ErrorMessage(builder)
		return
		
	LocalSymbolName = LocalSymbolLocation[len(SymbolChooser.get_current_folder())+1:]

	#make final symbol name
	symbol = '/Symbols/' + LocalSymbolName

	#copy symbol to git repo
	try:
		SI.execute('cp -r ' + LocalSymbolLocation + ' ' + DatabaseLocation + '/Symbols/', False)
	except:
		SI.execute('cd ' + DatabaseLocation + ' && mkdir Symbols')
		try:
			SI.execute('cp -r ' + LocalSymbolLocation + ' ' + DatabaseLocation + '/Symbols/', False)	
		except:
			ErrorMessage(builder)
	print('Copied Symbol file')
	#___________________________________________________________________________
		
	UbuntuID_L = builder.get_object('DB_A_UbuntuName')
	ubuntu_id = UbuntuID_L.get_text()

	
	DebianID_L = builder.get_object('DB_A_DebianName')
	debian_id  = DebianID_L.get_text()

	ArchID_L = builder.get_object('DB_A_ArchName')
	arch_id  = ArchID_L.get_text()

	MainCategory_L = builder.get_object('DB_A_Main')
	maincategory =MainCategory_L.get_active_text()

	SubCategory_L = builder.get_object('DB_Sub')
	subcategory = SubCategory_L.get_active_text()

	URLL = builder.get_object('DB_A_URL')
	url = URLL.get_text()


	#Prüfen ob alle Daten angegeben sind

	if name == None or desc_s == None or desc_l == None or screenshotloc == None or ubuntu_id == None or debian_id == None or arch_id == None or symbol == None or maincategory == None or subcategory == None or url == None:
		ErrorMessage(builder)
		return

	c.execute('''INSERT INTO CPFDB(
				name, 
				description_short, 
				description_long, 
				screenshotloc, 
				ubuntu_id, 
				debian_id, 
				arch_id, 
				symbol, 
				maincategory, 
				subcategory,
				URL)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)''', (name, desc_s, desc_l, screenshotloc, ubuntu_id, debian_id, arch_id, symbol, maincategory, subcategory, url))
	db.commit()
	db.close()
	print('Added DatabaseEntry')

#Lesen eines ganzen Datensatzes oder des namens
def db_read(subcategory, bAll):
	global c
	global db
	db_connect()
	if bAll != True:
		c.execute('SELECT name FROM CPFDB WHERE subcategory=?', (str(subcategory),))
	else: 		
		c.execute('SELECT * FROM CPFDB WHERE subcategory=?', (str(subcategory),))

	CleanOutput = []
	output = c.fetchall()
	#Kuerzen der ausgabe
	for i in output:
		i = str(i)[2:]
		i = str(i)[:-3]
		print('out: ' + str(i))
		CleanOutput.append(i)
	
	return CleanOutput
	
#Lesen eines ganzen Datensatzes
def read_atributes(name):
	global c
	global db
	db_connect()
	
	returnvalue = None
	c.execute('SELECT * FROM CPFDB WHERE name=?', (name,))
	returnvalue = c.fetchone()

	print('returnvalue: ' + str(returnvalue))	
	return returnvalue



#Loeschen eines Datensatzes__________________________________________________________________

#Laden hauptkategorie
def remove_entry(builder):
	Window = builder.get_object('Remove_Entry')

	#populate Main Categorys
	if conf.get_entry('main','language') == 'GER':
		MainList = conf.get_entry('DB','germain')
	else:
		MainList = conf.get_entry('DB','enmain')

	MainList = MainList.split(',')
	MainCategoryChooser = builder.get_object('GE_Main_Choose')
	MainCategoryChooser.remove_all()
	for i in MainList:
		MainCategoryChooser.append_text(i)
	
	
	Window.show_all()

#Laden Unterkategorie basierend auf Hauptkategorie
def Remove_Update_SubList(builder):
	MainChooser = builder.get_object('GE_Main_Choose')
	MainCategory = MainChooser.get_active_text()

	if conf.get_entry('main','language') == 'GER':
		SubList = conf.get_entry('DBSub','ger' + MainCategory.lower())
	else:
		SubList = conf.get_entry('DBSub','en' + MainCategory.lower())

	SubList = SubList.split(',')
	print('SubList is: ' + str(SubList))

	SubChooser = builder.get_object('GE_SubChoose')
	SubChooser.remove_all()

	for i in SubList:
		SubChooser.append_text(i)

#Laden der Programme basierend auf Kategorien
def UpdateProgramList(builder):
	global c
	global db
	db_connect()
	
	MainChooser = builder.get_object('GE_Main_Choose')
	MainCategory = MainChooser.get_active_text()

	SubChooser = builder.get_object('GE_SubChoose')
	SubCategory = SubChooser.get_active_text()

	MatchingProgram = []
	
	for row in c.execute('SELECT name FROM CPFDB WHERE subcategory=? AND maincategory=?',(SubCategory,MainCategory)):
		MatchingProgram.append(row[0])



	ProgramChooser = builder.get_object('GE_ProgramName')
	ProgramChooser.remove_all()

	for i in MatchingProgram:
		ProgramChooser.append_text(i)

#Entfernen basiernd auf haupt und Unterkategorie sowie namen
def RemoveExecute(builder):
	global c
	global db
	db_connect()
	
	
	MainChooser = builder.get_object('GE_Main_Choose')
	MainCategory = MainChooser.get_active_text()

	SubChooser = builder.get_object('GE_SubChoose')
	SubCategory = SubChooser.get_active_text()	

	ProgramChooser = builder.get_object('GE_ProgramName')
	ProgramName = ProgramChooser.get_active_text()
	try:
		c.execute('DELETE FROM CPFDB WHERE name=? AND subcategory=? AND maincategory=?',(ProgramName, SubCategory, MainCategory))
		db.commit()
	except:
		print('Could not delete entry')
		return
	print('Remove Successfull')

#Fehler Dialog		
def ErrorMessage(builder):
	Message = builder.get_object('DB_ErrorMessage')
	Message.show_all()
	