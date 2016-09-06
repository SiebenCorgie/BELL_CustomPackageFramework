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

#Richtige Gtk Version (3) importieren
import gi.repository
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

#haupt Biblitheken (module) importieren
from gi.repository import Gtk, GdkPixbuf, Gdk 
import os, sys

#Eigene Module Importieren
import CPFWeb as web
import CPFConf as conf
import SystemInteraction as SI
import CPFDatabase as db
import Install_UI as InstUI

#Je nach einstellung WebKit importieren
if conf.get_entry('Internet','online') == 'True':
	from gi.repository import WebKit
else:
	print("Start in Offline Mode")


#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "src/cpf.ui"
#UI_FILE = "/usr/local/share/cpf/ui/cpf.ui"


class GUI:
	def __init__(self):
#initialisierung
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		window = self.builder.get_object('window')

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
		window.show_all()


#StartEvents
#MainWindow_IconView____________________________________________________________








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
		
#Tools
#_______________________________________________________________________________
#add database entry
	def on_M_Tools_AddDatabaseEntry_activate (self, menuitem):
		self.db_add_Dialog = self.builder.get_object('DB_Add_Win')
		db.db_add_Init(self.builder)
		self.db_add_Dialog.show_all()
#update Sub Category
	def on_DB_A_Main_changed (self, combobox):
		db.update_sub_category(self.builder)

#add entry
	def on_DB_Add_Add_clicked (self, button):
		db.db_add_entry(self.builder)
		self.db_add_Dialog.hide()

#close db add entry dialog
	def on_DB_Add_Close_clicked (self, button):
		db.db_read()
		self.db_add_Dialog.hide()

#"OK" DB ErrorMessage
	def on_DB_EM_OK_clicked (self, button):
		DBerror = self.builder.get_object('DB_ErrorMessage')
		DBerror.hide()
#_______________________________________________________________________________
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
		db.db_read()
		self.NewDBWin.hide()



		
def main():
	app = GUI()
	Gtk.main()
		
if __name__ == "__main__":
	sys.exit(main())