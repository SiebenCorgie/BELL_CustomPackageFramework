#Vte interaction for CPF

import CPFFeedback as feedback

#Set VTE Status
VTEStatus = False


import CPFConf as conf
import CPFDatabase as db
import os
import SystemInteraction as SI

#import VTE
import gi.repository
try:
	gi.require_version('Vte', '2.90')
	VTEver = 290
except:
	gi.require_version('Vte', '2.91')
	VTEver = 291	
from gi.repository import Vte, GLib

#_______________________________________________________________________________
#Terminal zu Fenster hinzufügen

def Init_VTE(builder):

	global VTE
	global VTEStatus
	
	VTEDialog = builder.get_object('VTE_Dialog')

#Add VTE
	VTEView = builder.get_object('VTE_MainWin')
	VTE = Vte.Terminal()

#decide the vte version
	if VTEver == 290:
			
		VTE.fork_command_full(
			Vte.PtyFlags.DEFAULT,
			os.environ['HOME'],
			["/bin/sh"],
			[],
			GLib.SpawnFlags.DO_NOT_REAP_CHILD,
			None,
			None,
			)
		print("old VTE used! (v 2.90) *WINDOW_INIT*")
	else:
		
		VTE.spawn_sync(
			Vte.PtyFlags.DEFAULT,
			os.environ['HOME'],
			["/bin/sh"],
			[],
			GLib.SpawnFlags.DO_NOT_REAP_CHILD,
			None,
			None,
			)
		print("New VTE Used () v. 2.91 *WINDOW_INIT*")
		
	VTEView.add(VTE)
#Show
	VTEDialog.show_all()

	VTEStatus = True
	
def VTE_execute(command):
	global VTE
	
	VTE.feed_child(TerminalCommand(command), TerminalCommandLength(command))


def TerminalCommand(command):
	return command + '\n'

def TerminalCommandLength(command):
	return len(command) + 1


#Upload to Git
def upload_database(builder):

	global VTEStatus
	if conf.get_entry('DB','notgitbased') == 'True':
		return
	
	if VTEStatus == False:
		Init_VTE(builder)
	else:
		VTEDialog = builder.get_object('VTE_Dialog')
		VTEDialog.show_all()

	feedback.status_push(conf.get_entry("Status","uploaddb"))
	
	VTE_execute('cd ' + conf.get_entry('DB','dblocation') + ' && git add * && git commit -a && git push')


#Refresh from git
def refresh_database(builder):
	global VTEStatus
	if conf.get_entry('DB','notgitbased') == 'True':
		return
	
	if VTEStatus == False:
		Init_VTE(builder)
	else:
		VTEDialog = builder.get_object('VTE_Dialog')
		VTEDialog.show_all()

	SI.execute('cd ~/.local/share/ && mkdir cpf',False)

	feedback.status_push(conf.get_entry("Status","refreshdb"))

	VTE_execute('cd ' + conf.get_entry('DB','dblocation') + ' && git pull')


#Download from git
def download_database(builder):
	global VTEStatus
	if conf.get_entry('DB','notgitbased') == 'True':
		return
	
	if VTEStatus == False:
		Init_VTE(builder)
	else:
		VTEDialog = builder.get_object('VTE_Dialog')
		VTEDialog.show_all()
		
	SI.execute('cd ~/.local/share/ && mkdir cpf',False)

	feedback.status_push(conf.get_entry("Status","downloaddb"))

	VTE_execute('cd ~/.local/share/cpf/' + ' && git clone ' + conf.get_entry('DB','databasegiturl'))


	