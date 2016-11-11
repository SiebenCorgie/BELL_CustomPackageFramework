#Uneingeordnete Funktionen fuer feedback

global builder
global pID


def set_builder(OffBuilder):

	global pID

	pID = 0
	
	global builder
	builder = OffBuilder
	status_push("welcome")

def status_push(text):
	global builder
	global pID


	Statusbar = builder.get_object("Statusbar")
	Statusbar.push(pID,text)
	pID = pID+1

def set_progress(ammount):

	global builder
	Progressbar = builder.get_object('Status_Progressbar')
	if ammount == True:
		
		Progressbar.start()
	else:
		Progressbar.stop()

	Progressbar.show()