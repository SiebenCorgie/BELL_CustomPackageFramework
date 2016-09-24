import cpf
import SystemInteraction as SI
import CPFConf as conf
import CPFDatabase as db
import Install_System as install

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

global stage


#Category Umgebung auf Wurzel setzen
def set_to_start(builder):
	#close App-View
	CloseView(builder)
	global ProgramViewOpen
	ProgramViewOpen = False
	
	global stage
	stage = 'root'

	global Plist

	#give log output
	print('OpeningMain')
	
	if conf.get_entry('main','language') == 'GER':
		Plist = conf.get_entry('DB','germain')
	else:
		Plist = conf.get_entry('DB','enmain')

	Plist=Plist.split(',')
	liststore = Gtk.ListStore(Pixbuf, str)
	view = builder.get_object('PS_IconList')	
	view.set_model(liststore)
	view.set_pixbuf_column(0)
	view.set_text_column(1)

	for icon in (Plist):
		if conf.get_entry('main','language') == 'GER':
			if icon == 'Video/Foto':
				medianame = 'multimedia'
			elif icon == 'Entwicklung':
				medianame = 'development'
			elif icon == 'Bildung':
				medianame = 'education'
			elif icon == 'Spiele':
				medianame = 'games'
			elif icon == 'Grafik':
				medianame = 'graphics'
			elif icon == 'Internet':
				medianame = 'internet'
			elif icon == 'Arbeit':
				medianame = 'office'
			elif icon == 'Wissenschaft':
				medianame == 'science'
			elif icon == 'System':
				medianame = 'system'
			elif icon == 'Werkzeuge':
				medianame = 'tools'
			elif icon == 'Verschiedenes':
				medianame = 'other'
			else:
				medianame = 'other'

		else:
			if icon == 'Video/Photo':
				medianame = 'multimedia'
			elif icon == 'Misc':
				medianame = 'other'
			else:
				medianame = icon.lower()

		#load icon of category
		try:
			pixbuf = Gtk.IconTheme.get_default().load_icon('applications-'+ medianame, 64, 0)
		except:
			pixbuf = Gtk.IconTheme.get_default().load_icon('applications-other', 64, 0)
		liststore.append([pixbuf, icon])

	view.show_all()


#Funktion wenn Icon geklickt wird
def Go_Down(builder,iconview,treepath):

	global stage
	global SelectedMain

	#get list
	global Plist
	global SubCategoryList

	
	#global IconView und treepath für das Zurueckgehen
	global ProgIconview
	ProgIconview = iconview

	global ProgTreepath
	ProgTreepath = treepath


	
	#get index of seleted List Item
	SelectedMain = Plist[treepath.get_indices()[0]]
		
	if stage !='Prog':
		#removing Icon View
		liststore = iconview.get_model()
		liststore.clear()

	#Umgebung mit Untekategorie Laden
	if stage == 'root':
		#get list of all Categories
		if conf.get_entry('main','language') == 'GER':
			SubCategoryList = conf.get_entry('DBSub','ger' + SelectedMain.lower())
		else:
			SubCategoryList = conf.get_entry('DBSub','en' + SelectedMain.lower())
			
		SubCategoryList = SubCategoryList.split(',')

		for entry in SubCategoryList:
			try:
				pixbuf = Gtk.IconTheme.get_default().load_icon('applications-' + entry, 64, 0)				
			except:
				pixbuf = Gtk.IconTheme.get_default().load_icon('applications-other', 64, 0)
			liststore.append([pixbuf, entry])
		stage = 'Sub'
		iconview.show_all()
		print('Showing Subcategorie')

	#Umgebung mit Programmen der Unterkategorie Laden
	elif stage == 'Sub':
		print('Showing Programs')
		go_Sub(builder,iconview,treepath, SelectedMain)

	#Zeigen des Programmfensters wenn Programm gewählt ist
	elif stage == 'Prog':
		print('Showing App Window')
		show_app(builder,iconview,treepath)


	

#Zeigen der Programme der Unterkategorie, passierend auf der Ueberkategorie
def go_Sub(builder,iconview,treepath,SelectedMain):
	
	global stage
	global SubCategoryList
	global ProgramList
	global liststore
	
	global SelectedSubCat
	
	SelectedSubCat = SubCategoryList[treepath.get_indices()[0]]
	
	#Clear Icons
	liststore = iconview.get_model()
	liststore.clear()

	#get list from selected main
	ProgramList = db.db_read(SelectedSubCat, False)

	for i in ProgramList:
		pixbuf = Pixbuf.new_from_file_at_size(str(conf.get_entry('DB','dblocation') + db.read_atributes(i)[8]),64,64)
		liststore.append([pixbuf, i])
	iconview.show_all()


	stage = 'Prog'

#Zeigen des Programmfensters mit allen informationen
def show_app(builder,iconview,treepath):

	global stage
	global SubCategoryList
	global ProgramList

	#Is AlreadyOpen Bool
	global ProgramViewOpen
	#Which Subcategory
	global ProgramName


	
	#ShowDialog if not already open
	if ProgramViewOpen != True:
		AppWin = builder.get_object('ApplicationDialog_Install')

		ProgramName = ProgramList[treepath.get_indices()[0]]

		Data = db.read_atributes(ProgramName)

		#Set Name, Short and Long description, Symbol, Screenshot
		Title = builder.get_object('AD_App_Label')
		Title.set_text(Data[1])

		#Short Description
		ShortDescription = builder.get_object('AD_ShortDescription')
		ShortDescription.set_text(Data[2])

		#Long Description
		LongDescription = builder.get_object('AD_LongDescription')
		LongDescription.set_text(Data[3])

		#Symbol
		Symbol = builder.get_object('AD_Symbol')
		try:
			SymbolPixbuf = Pixbuf.new_from_file_at_size(conf.get_entry('DB','dblocation') + Data[8],64 ,64)
			Symbol.set_from_pixbuf(SymbolPixbuf)
		except:
			Symbol.set_from_icon_name('error-dialog',10)
			print('Failed To Load Symbol')

		#Screenshot
		Screenshot = builder.get_object('AD_Screenshot')
		try:
			ScreenshotPixbuf = Pixbuf.new_from_file_at_size(conf.get_entry('DB','dblocation') + Data[4],512 ,512)
			Screenshot.set_from_pixbuf(ScreenshotPixbuf)
		except:
			Screenshot.set_from_icon_name('error-dialog',10)
			print('Failed to load Screenshot')
		
		
		AppWin.show_all()
		ProgramViewOpen = True
	else:
		ErrorWinAppView = builder.get_object('AD_AVIsOpen')
		ErrorWinAppView.show_all()

#PassCommandsToInstallSystem____________________________________________________
#InstallierAnweisung fuer "Install_System"

def StartInstalling():
	global ProgramName
	install.Install(ProgramName,False)

def StartUnistalling():
	global ProgramName
	install.Install(ProgramName,True)



#InstallWindowVarious___________________________________________________________

#Schliessen des Error-Dialog
def CloseView(builder):
	ErrorWinAppView = builder.get_object('AD_AVIsOpen')
	ErrorWinAppView.hide()

#Schließen des Programm-View
def CloseAppView(builder):
	global ProgramViewOpen
	AppView = builder.get_object('ApplicationDialog_Install')
	AppView.hide()
	ProgramViewOpen = False

#Laden der Wurzel
def go_home(builder):
	set_to_start(builder)

#ZurückGehen
def go_back(builder):
	global stage
	global SubCategoryList
	global ProgramList

	#Is AlreadyOpen Bool
	global ProgramViewOpen
	#Which Subcategory
	global ProgramName

	#global IconView und treepath für das Zurueckgehen
	global ProgIconview

	global ProgTreepath

	if stage == 'root':
		print('Already Root')

	elif stage == 'Sub':
		set_to_start(builder)	


	elif stage == 'Prog':
		liststore = ProgIconview.get_model()
		liststore.clear()

		#Lade Icons der vorher angeklickten SubCategory
		for entry in SubCategoryList:
			try:
				pixbuf = Gtk.IconTheme.get_default().load_icon('applications-' + entry, 64, 0)				
			except:
				pixbuf = Gtk.IconTheme.get_default().load_icon('applications-other', 64, 0)
			liststore.append([pixbuf, entry])

		
		stage = 'Sub'
		iconview.show_all()
		print('Showing Subcategorie')		

#WebSeite anzeigen
def show_web_page():
	global ProgramName
	webpage = db.read_atributes(ProgramName)
	webpage = webpage[11]
	SI.execute('xdg-open ' + webpage, False)
	
	
