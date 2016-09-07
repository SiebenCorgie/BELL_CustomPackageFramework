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

	global stage
	stage = 'root'

	global Plist

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
	print('OpeningMain: ' + SelectedItem)
		
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
		print('Showing SUbcategorie')

	#Upadte to Programs in Database on Click if in Subcategorie
	elif stage == 'Sub':
		print('StartTryingToShowPrograms')
		go_Sub(builder,iconview,treepath, SelectedItem)

	elif stage == 'Prog':
		#Hide View and show template with filled in Stuff
		print('teddy')

	

def go_Sub(builder,iconview,treepath,main):
	
	global stage
	global SubCategoryList
	
	SelectedSubCat = SubCategoryList[treepath.get_indices()[0]]
	print('Selected Subcategorie: ' + SelectedSubCat)
	
	print('Main: ' + main)
	#Clear Icons
	liststore = iconview.get_model()
	liststore.clear()
	print('Cleared!')

	#get list from selected main
	ProgrammList = db.db_read(SelectedSubCat, False)

	for i in ProgrammList:
		print('Programmlist: ' + str(i))
		pixbuf = Gtk.IconTheme.get_default().load_icon('gtk-dialog-error', 64, 0)
		liststore.append([pixbuf, i])
	iconview.show_all()

	stage = 'Prog'

	
		
	
