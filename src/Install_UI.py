import cpf
import SystemInteraction as SI
import CPFConf as conf
import CPFDatabase as db

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
import configparser

#Read A ProgramFile

def read_program_file(path, entry):
	ProgramFile = configparser.ConfigParser()
	ProgramFile.read(path)
	return ProgramFile['main'][str(entry)]
	

#Set to root
def set_to_start(builder):

	#close App-View
	CloseView(builder)
	
	global ProgramViewOpen
	ProgramViewOpen = False
	
	global stage
	stage = 'root'

	global MainList
	global liststore
	global view

	#give log output
	print('OpeningMain')

	MainList = SI.get_folder_content(conf.get_entry('DB','currentdb'))

	liststore = Gtk.ListStore(Pixbuf, str)
	view = builder.get_object('PS_IconList')	
	view.set_model(liststore)
	view.set_pixbuf_column(0)
	view.set_text_column(1)

	for icon in MainList:
		pixbuf = Gtk.IconTheme.get_default().load_icon('gtk-dialog-error', 64, 0)
		liststore.append([pixbuf, icon])

	view.show_all()
		
def CloseView(builder):
	ErrorWinAppView = builder.get_object('AD_AVIsOpen')
	ErrorWinAppView.hide()

def CloseAppView(builder):
	global ProgramViewOpen
	AppView = builder.get_object('ApplicationDialog_Install')
	AppView.hide()
	ProgramViewOpen = False


def Go_Down(builder,iconview,treepath):

	#Common
	global stage
	global liststore
	global view
	global ProgramViewOpen
	
	#MainList
	global MainList
	global SelectedCategory

	#SubCategory
	global SelectedSubCategory
	global SubCategoryList

	#Program
	global ProgramList
	global ProgramFile
	global SelectedProgram

	#Show Main Categorys in DB-Struct
	if stage == 'root':
		SelectedCategory = MainList[treepath.get_indices()[0]]
		print('SELCTED MAIN: ' + SelectedCategory)

		liststore.clear()

		SubCategoryList = SI.get_folder_content(conf.get_entry('DB','currentdb') + '/' + SelectedCategory)

		for subitem in SubCategoryList:
			pixbuf = Gtk.IconTheme.get_default().load_icon('gtk-dialog-error', 64, 0)
			liststore.append([pixbuf, subitem])

		stage = 'SubCategory'
		view.show_all()
		
	#show sub categorys in DB_Struct
	elif stage == 'SubCategory':
		print('GoingToShowPrograms')
		SelectedSubCategory = SubCategoryList[treepath.get_indices()[0]]
		ProgramList = SI.get_folder_content(conf.get_entry('DB','currentdb') + '/' + SelectedCategory + '/' + SelectedSubCategory + '/' )

		liststore.clear()

		if ProgramList != []:
			for program in ProgramList:
				pixbuf = Gtk.IconTheme.get_default().load_icon('gtk-dialog-error', 64, 0)
				liststore.append([pixbuf,program])
		else:
				pixbuf = Gtk.IconTheme.get_default().load_icon('gtk-dialog-error', 64, 0)
				liststore.append([pixbuf,'NothingFound :('])	
				print('There are no entries in this Category')
		stage = 'ProgramView'
		view.show_all()

	#Show Selected Program
	elif stage  == 'ProgramView':
		print('Showing Program Now')
		try:
			SelectedProgram = ProgramList[treepath.get_indices()[0]]
		except:
			SelectedProgram = 'NoProgramFileFound'
			
		ProgramFile = str(conf.get_entry('DB','currentdb') + '/' + SelectedCategory + '/' + SelectedSubCategory + '/' + SelectedProgram + '/' + SelectedProgram + '.info')
		print('ProgramFile: ' + ProgramFile)





		if ProgramViewOpen == False:

			if SelectedProgram == 'NoProgramFileFound':
				print('No Program Selected')
				return

			#Title
			name = read_program_file(ProgramFile, 'name')
			nameWidget = builder.get_object('AD_App_Label')
			nameWidget.set_text(name)

			#Short Description
			ShortDescription = read_program_file(ProgramFile, 'shortdescription')
			SDWidget = builder.get_object('AD_ShortDescription')
			SDWidget.set_text(ShortDescription)

			#long Description
			LongDescription = read_program_file(ProgramFile, 'longdescription')
			LDWidget = builder.get_object('AD_LongDescription')
			LDWidget.set_text(LongDescription)

			#Screenshot
			if read_program_file(ProgramFile, 'screenshot') == 'True':
				Screenshot = str(conf.get_entry('DB','currentdb') + '/' + SelectedCategory + '/' + SelectedSubCategory + '/' + SelectedProgram + '/Screenshot.image')
				ImageWidget = builder.get_object('AD_Screenshot')
				ScreenPixBuf = Pixbuf.new_from_file_at_size(Screenshot,1024 ,1024)
				ImageWidget.set_from_pixbuf(ScreenPixBuf)
			else:
				ImageWidget = builder.get_object('AD_Screenshot')
				ImageWidget.set_from_icon_name('applications-system', 64)

			#Symbol
			if read_program_file(ProgramFile, 'symbol') == 'True':
				Symbol = str(conf.get_entry('DB','currentdb') + '/' + SelectedCategory + '/' + SelectedSubCategory + '/' + SelectedProgram + '/Symbol.image')
				SymbolWidget = builder.get_object('AD_Symbol')
				SymbolPixbuf = Pixbuf.new_from_file_at_size(Symbol,64 ,64)
				SymbolWidget.set_from_pixbuf(SymbolPixbuf)
			else:
				SymbolWidget = builder.get_object('AD_Symbol')
				SymbolWidget.set_from_icon_name('applications-system', 64)
				
			

			
			ProgramView = builder.get_object('ApplicationDialog_Install')
			ProgramViewOpen = True
			ProgramView.show_all()
			
		else:
			ErrorView = builder.get_object('AD_AVIsOpen')
			ErrorView.show_all()













	