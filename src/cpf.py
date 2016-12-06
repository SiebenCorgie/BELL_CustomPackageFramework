#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# Copyright (C) 2016 tendsin mende <siebencorgie@googlemail.com>
# 
# CPF is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# CPF is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#______________________________________________________________________________


#Sprache Festlegen
import locale

#locale.setlocale(locale.LC_ALL, locale.getlocale())
#locale.bindtextdomain("cpf", "/usr/share/locale")

print(locale.getlocale())



#Richtige Gtk Version (3) importieren
import gi.repository
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

#haupt Biblitheken (module) importieren
from gi.repository import Gtk, GdkPixbuf, Gdk 
import os, sys

#Eigene Module Importieren
#import CPFWeb as web
import CPFConf as conf
import SystemInteraction as SI
import CPFDatabase as db
import Install_UI as InstUI
import VTE_Interaction as vte
import CPFFeedback as feedback
import CPFMassInstall as MI

#Je nach einstellung WebKit importieren
if conf.get_entry('Internet','online') == 'True':
	from gi.repository import WebKit
else:
	print("Start in Offline Mode")


#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)

print("Locale: " + locale.getlocale()[0])

if locale.getlocale()[0] == 'de_DE':
	UI_FILE = "src/UI_DE.ui"
	print('Using DE')
else:
	UI_FILE = "src/cpf.ui"
	print("Using EN")

#UI_FILE = "src/cpf.ui"
#UI_FILE = "/usr/local/share/cpf/ui/cpf.ui"


class GUI:
	def __init__(self):
#initialisierung
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)
		self.builder.set_translation_domain('cpf')


		window = self.builder.get_object('window')

#Zeige CPFFeedback builder Objekt for der UI initialisierung
		feedback.set_builder(self.builder)
		
#Documentation Browser
		if conf.get_entry('Internet','Online') == 'True':
			self.DocURL = conf.get_entry('Internet','docurl')
			self.DocBrowser = WebKit.WebView()
			self.DocBrowser.load_uri(self.DocURL)
			DocHostWin = self.builder.get_object('Docs_View')
			DocHostWin.add(self.DocBrowser)
			DocHostWin.show_all()
		else:
			DocHostWin = self.builder.get_object('Docs_View')
			SorryIcon1= Gtk.Image.new_from_icon_name('dialog-error' , Gtk.IconSize.DIALOG)
			DocHostWin.add(SorryIcon1)
			DocHostWin.show_all()

#InfoBrowser
		if conf.get_entry('Internet','Online') == 'True':
			self.InfoURL = conf.get_entry('Internet','infourl')
			self.InfoBrowser = WebKit.WebView()
			self.InfoBrowser.load_uri(self.InfoURL)
			InfoHostWin = self.builder.get_object('Info_View')
			InfoHostWin.add(self.InfoBrowser)
			DocHostWin.show_all()
		else:
			InfoHostWin = self.builder.get_object('Info_View')
			SorryIcon2= Gtk.Image.new_from_icon_name('dialog-error' , Gtk.IconSize.DIALOG)
			InfoHostWin.add(SorryIcon2)
			InfoHostWin.show_all()
			
#Verscheidenes
		self.FastOnlineSwitch = self.builder.get_object('M_File_OfflineMain')
		if conf.get_entry('Internet','online') == 'True':
			self.FastOnlineSwitch.set_active(True)
		else:
			self.FastOnlineSwitch.set_active(False)


		
#class variables
		InstUI.set_to_start(self.builder)
		
#init end
		print("init end")
		window.show_all()


#StartEvents
#MainWindow_IconView____________________________________________________________

#On IconActivation
	def on_PS_IconList_item_activated (self, iconview, treepath):
		InstUI.Go_Down(self.builder,iconview,treepath)

#Go To Root
	def on_MN_PS_Home_clicked (self, button):
		print('Go Home!')
		InstUI.go_home(self.builder)

#Go Back
	def on_MN_PS_Back_clicked (self, button):
		InstUI.go_back(self.builder)
#Refresh
	def on_MN_PS_Reload_clicked (self, button):
		vte.refresh_database(self.builder)
#Reset View
	def on_M_View_Reset_select (self, menuitem):
		print("Reset")
		InstUI.go_home(self.builder)




#Close ViewError
	def on_ADAV_OK_clicked (self, button):
		InstUI.CloseView(self.builder)

#Destroy App-View
	def on_ApplicationDialog_Install_destroy (self, widget):
		print("Destroy Appview")
		InstUI.CloseAppView(self.builder)


		
#CloseAppView
	def on_AD_Close_clicked (self, button):
		InstUI.CloseAppView(self.builder)

#Start Installing
	def on_AD_B_Install_clicked (self, button):
		InstUI.StartInstalling()

#Start Removing
	def on_AD_B_Uninstall_clicked (self, button):
		InstUI.StartUnistalling()

#Show Developer Page in Browser
	def on_AD_DevLink_clicked (self, button):
		InstUI.show_web_page()



#DocBrowser
#DocBrwoser zu Startseite
	def on_B_Docs_Home_clicked (self, button):
		self.DocBrowser.load_uri(self.DocURL)
#DocBrowser zurueck
	def on_B_Docs_Back_clicked (self, button):
		self.DocBrowser.go_back()
#DocBrowser forwaerts
	def on_B_Docs_Forward_clicked (self, button):
		self.DocBrowser.go_forward()

#InfoBrowser
#zu Startseite
	def on_B_Info_Home_clicked (self, button):
		self.InfoBrowser.load_uri(self.InfoURL)
#zurueck
	def on_B_Info_Back_clicked (self, button):
		self.InfoBrowser.go_back()
#forwaerts
	def on_B_Info_Forward_clicked (self, button):
		self.InfoBrowser.go_forward()

#MainMenu
#OpenPreferences
	def on_M_File_Preferences_activate (self, menuitem):
		self.Preferences = self.builder.get_object('Preferences')
		conf.load_config(self.builder)
		self.Preferences.show_all()
#Quit_File
	def on_M_File_Quit_activate (self, menuitem):
		Gtk.main_quit()

#Quit "x" button
	def on_window_destroy(self, window):
		Gtk.main_quit()

#SchnellEinstellung "Online" in File-Menu
	def on_M_File_OfflineMain_toggled (self, checkmenuitem):
		#set entry in Conifg
		self.FastOnlineSwitch = self.builder.get_object('M_File_OfflineMain')
		if self.FastOnlineSwitch.get_active() == True:
			conf.set_entry('Internet','Online','True')
		else:
			conf.set_entry('Internet','Online','False')

		
#Preferences
#Discard
	def on_Pref_Discard_clicked (self, button):
		self.Preferences.hide()
#Save
	def on_Pref_Save_clicked (self, button):
		conf.save_config(self.builder)
		self.Preferences.hide()
		
#Tools Database
#_______________________________________________________________________________
#Create A Mass Install File

	#init AddDialog
	def on_M_Tools_CreateMass_activate (self, menuitem):
		MI.AddDialogInit(self.builder)
		
	#UpdateSubCategorys
	def on_MIADD_LChooseMain_changed (self, combobox):
		MI.AddDialogUpdateSub(self.builder)

	#UpdateProgramms
	def on_MIADD_LChooserSubCategor_changed (self, combobox):
		MI.AddDialogUpdateProgram(self.builder)

	#Aktuelles Programm Hinzufügen
	def on_MIADD_LAdd_clicked (self, button):
		MI.AddEntry(self.builder)
		
	#Schliesse AddDialog
	def on_MIADD_Close_clicked (self, button):
		MassAddDialog = self.builder.get_object('MIADD')
		MassAddDialog.hide()

	#Installieren von MassInstall Datei
	#Oeffnen des Dialogs
	def on_M_Tools_MassInstall_activate (self, menuitem):
		MassInstallDialog = self.builder.get_object('MIInsall')
		MassInstallDialog.show_all()

	#Schließen
	def on_MIInstall_Close_clicked (self, button):
		MassInstallDialog = self.builder.get_object('MIInsall')
		MassInstallDialog.hide()		
	

	#Installieren
	def on_MIInstall_Install_clicked (self, button):
		MI.Execute(self.builder)



#add database entry 'show window'
	def on_M_Tools_AddDatabaseEntry_activate (self, menuitem):
		self.db_add_Dialog = self.builder.get_object('DB_Add_Win')
		feedback.status_push(conf.get_entry("Status","dbadd"))
		db.db_add_Init(self.builder)
		self.db_add_Dialog.show_all()
		
#update Sub Category
	def on_DB_A_Main_changed (self, combobox):
		db.update_sub_category(self.builder)

#add entry
	def on_DB_Add_Add_clicked (self, button):
		db.db_add_entry(self.builder)
		feedback.status_push(conf.get_entry("Status","dbadded"))
		self.db_add_Dialog.hide()

#close db add entry dialog
	def on_DB_Add_Close_clicked (self, button):
		self.db_add_Dialog.hide()

#"OK" DB ErrorMessage
	def on_DB_EM_OK_clicked (self, button):
		DBerror = self.builder.get_object('DB_ErrorMessage')
		DBerror.hide()

#Remove Database Entry 'Show Window'
	def on_M_Tools_Remove_Entry_activate (self, menuitem):
		db.remove_entry(self.builder)

#Remove Database Entry 'Update View Main'
	def on_GE_Main_Choose_changed (self, combobox):
		db.Remove_Update_SubList(self.builder)

#Remove Database Entry 'Update View Sub'
	def on_GE_SubChoose_changed (self, combobox):
		db.UpdateProgramList(self.builder)

#Remove Database Entry 'Remove'
	def on_GE_Remove_clicked (self, button):
		db.RemoveExecute(self.builder)
		
#Remove Database Entry 'Close'
	def on_GE_Close_clicked (self, button):
		window = self.builder.get_object('Remove_Entry')
		window.hide()

#UploadDatabase
	def on_M_Tools_UploadDatabase_activate (self, menuitem):
		vte.upload_database(self.builder)

#Download Database
	def on_M_Tools_DownloadNewDatabase_activate (self, menuitem):
		vte.download_database(self.builder)


#Close VTE View
	def on_VTE_Close_clicked (self, button):
		VTEDialog = self.builder.get_object('VTE_Dialog')
		VTEDialog.hide()

#CreateDatabase
	def on_M_Tools_AddDB_activate (self, menuitem):
		self.NewDBWin = self.builder.get_object('CreateNewDatabase')
		self.NewDBWin.show_all()

#close without adding
	def on_CND_Close_clicked (self, button):
		self.NewDBWin.hide()

#Add new Database
	def on_CND_Add_clicked (self, button):
		db.add_db(self.builder)
		self.NewDBWin.hide()
		
		
#Help___________________________________________________________________________		
#Open CPF Documentation
	def on_M_Help_OpenCPFDocs_activate (self, menuitem):
		SI.execute('xdg-open ' + conf.get_entry('Internet','cpf_docurl') , False)

#Open Custom Documentation
	def on_M_Help_OpenCustomDocs_activate (self, menuitem):
		SI.execute('xdg-open ' + conf.get_entry('Internet','docurl'), False)




#Else
#_______________________________________________________________________________
#Show AboutDialog

	def on_AboutDialogButton_activate (self, menuitem):
		AboutDialog = self.builder.get_object('AboutDialog')
		AboutDialog.show_all()

#CloseAboutDialog
	def on_AboutOK_clicked (self, button):
		AboutDialog = self.builder.get_object('AboutDialog')
		AboutDialog.hide()



		
def main():
	app = GUI()
	Gtk.main()
		
if __name__ == "__main__":
	sys.exit(main())
