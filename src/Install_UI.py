import cpf
import SystemInteraction as SI
import CPFConf as conf
import CPFDatabase as db

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

global stage

#clear shown View

#Set to root
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
		pixbuf = Gtk.IconTheme.get_default().load_icon('gtk-dialog-error', 64, 0)
		liststore.append([pixbuf, icon])

	view.show_all()


def Go_Down(builder,iconview,treepath):

	global stage
	global SelectedItem

	#get list
	global Plist
	global SubCategoryList


	#get index of seleted List Item
	SelectedItem = Plist[treepath.get_indices()[0]]

	if stage !='Prog':
		#removing Icon View
		liststore = iconview.get_model()
		liststore.clear()

	if stage == 'root':
		#get list of all SubKategories
		if conf.get_entry('main','language') == 'GER':
			SubCategoryList = conf.get_entry('DBSub','ger' + SelectedItem.lower())
		else:
			SubCategoryList = conf.get_entry('DBSub','en' + SelectedItem.lower())
			
		SubCategoryList = SubCategoryList.split(',')

		for entry in SubCategoryList:
			pixbuf = Gtk.IconTheme.get_default().load_icon('gtk-dialog-error', 64, 0)
			liststore.append([pixbuf, entry])
		stage = 'Sub'
		iconview.show_all()
		print('Showing Subcategorie')

	#Upadte to Programs in Database on Click if in Subcategorie
	elif stage == 'Sub':
		print('Start Trying To Show Programs')
		go_Sub(builder,iconview,treepath, SelectedItem)

	elif stage == 'Prog':
		#Hide View and show template with filled in Stuff
		print('Showing App Window')
		show_app(builder,iconview,treepath)

	

def go_Sub(builder,iconview,treepath,main):
	
	global stage
	global SubCategoryList
	global ProgramList
	
	global SelectedSubCat
	
	SelectedSubCat = SubCategoryList[treepath.get_indices()[0]]
	print('Selected Subcategorie: ' + SelectedSubCat)
	
	print('Main: ' + main)
	#Clear Icons
	liststore = iconview.get_model()
	liststore.clear()
	print('Cleared!')

	#get list from selected main
	ProgramList = db.db_read(SelectedSubCat, False)

	for i in ProgramList:
		print('Programmlist: ' + str(i))
		pixbuf = Gtk.IconTheme.get_default().load_icon('gtk-dialog-error', 64, 0)
		liststore.append([pixbuf, i])
	iconview.show_all()
	print('Showing Apps Now!') 

	stage = 'Prog'

def show_app(builder,iconview,treepath):

	global stage
	global SubCategoryList
	global ProgramList

	#Is AlreadyOpen Bool
	global ProgramViewOpen
	#Which Subcategory



	
	#ShowDialog if not already open
	if ProgramViewOpen != True:
		print('Show Application Chooser')
		AppWin = builder.get_object('ApplicationDialog_Install')

		ProgramName = ProgramList[treepath.get_indices()[0]]
		print('Selected Program: ' + str(ProgramName))

		#Set Name, Short and Long description, Symbol, Screenshot
		Title = builder.get_object('AD_App_Label')
		Title.set_text(str(db.read_atributes(ProgramName, 'name')))

		#Short Description
		ShortDescription = builder.get_object('AD_ShortDescription')
		ShortDescription.set_text(str(db.read_atributes(ProgramName, 'description_short')))

		#Long Description
		LongDescription = builder.get_object('AD_LongDescription')
		LongDescription.set_text(str(db.read_atributes(ProgramName, 'description_long')))

		#Symbol
		Symbol = builder.get_object('AD_Symbol')


		#Screenshot
		
		
		AppWin.show_all()
		ProgramViewOpen = True
	else:
		ErrorWinAppView = builder.get_object('AD_AVIsOpen')
		ErrorWinAppView.show_all()
		
def CloseView(builder):
	ErrorWinAppView = builder.get_object('AD_AVIsOpen')
	ErrorWinAppView.hide()

def CloseAppView(builder):
	global ProgramViewOpen
	AppView = builder.get_object('ApplicationDialog_Install')
	AppView.hide()
	ProgramViewOpen = False
