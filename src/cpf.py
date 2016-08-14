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

from gi.repository import Gtk, GdkPixbuf, Gdk, WebKit
import os, sys
import CPFWeb, CPFConf


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
		self.DocURL = 'https://github.com/SiebenCorgie/BELL_CustomPackageFramework/wiki'
		self.DocBrowser = WebKit.WebView()
		self.DocBrowser.load_uri(self.DocURL)
		DocHostWin = self.builder.get_object('Docs_View')
		DocHostWin.add(self.DocBrowser)
		DocHostWin.show_all()

#InfoBrowser
		self.InfoURL = 'https://www.lernsax.de/'
		self.InfoBrowser = WebKit.WebView()
		self.InfoBrowser.load_uri(self.InfoURL)
		InfoHostWin = self.builder.get_object('Info_View')
		InfoHostWin.add(self.InfoBrowser)
		DocHostWin.show_all()

		
#init end
		window.show_all()


#StartEvents

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


#Menue

#Quit_File
	def on_M_File_Quit_activate (self, menuitem):
		Gtk.main_quit()

#Quit "x" button
	def on_window_destroy(self, window):
		Gtk.main_quit()



def main():
	app = GUI()
	Gtk.main()
		
if __name__ == "__main__":
	sys.exit(main())