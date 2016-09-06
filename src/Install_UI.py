import cpf
import SystemInteraction as SI
import CPFConf as conf
import CPFDatabase as db

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf


def set_to_start(builder):
	
	category = 0
	Plist = ['Video/Photo', 'Development','Education','Games','Graphics','Iternet','Office','Science','System','Utilities','Misc']
	#Plist = ['Teddy','Rolf','Micke']
	liststore = Gtk.ListStore(Pixbuf, str)
	view = builder.get_object('PS_IconList')	
	view.set_model(liststore)
	view.set_pixbuf_column(0)
	view.set_text_column(1)

	for icon in (Plist):
		pixbuf = Gtk.IconTheme.get_default().load_icon('gtk-dialog-error', 64, 0)
		liststore.append([pixbuf, icon])

	view.show_all()