import cpf
import SystemInteraction as SI
import CPFConf as conf
import CPFDatabase as db
import CPFFeedback as feedback

SupportArch = ('arch','manjaro','antergos')
SupportUbuntu = ('ubuntu','elementary','lubuntu','xubuntu','kubuntu')
SupportDebian = ('debian','deepin')



#Herausfinden der Distribution, aufrufen des richtigen eintrags in der Datenbank
#Starten des installier odre deinstalliervorgangs
def Install(ProgramName, Uninstall):
	
	#Get all ProgramData from DatabaseEntry
	ProgramData = db.read_attributes(ProgramName)

	
	#read release information

	Distribution = SI.execute('cat /etc/*-release',True)
	Distribution = Distribution.split('\n')

	#Teste in welchem der eintraege  'ID=' + Name einer supporteten Distribution
	#stehe.
	Distribution = SI.execute('cat /etc/os-release',True)
	#Distribution[1]
	Distribution = Distribution.split('\n')
	IDName = "notfound"

	for name in Distribution:
		for a in SupportArch:
			if 'ID=' + a in name:
				IDName = 'arch'
				print("We are Arch based")

		for u in SupportUbuntu:
			if 'ID=' + u in name:
				IDName = 'ubuntu'
				print("We are Ubuntu based")

		for d in SupportDebian:
			if 'ID=' + d in name:
				IDName = 'debian'
				print("We are Debian based")
			
	print('We Are On: ' + IDName + '-like system')

#	if type(ProgramName) == list:
#		print('We Got a MassInstall')
#	else:
		

	#Arch
	if IDName in SupportArch:
		bInstall = True
		print('StartInstalling on: Arch')
		Name = ProgramData[7]
		print('Installing as: ' + Name)
		execute_install(Name, 'arch',Uninstall)

	#Ubuntu
	elif IDName in SupportUbuntu:
		bInstall = True
		print('StartInstalling on Ubuntu')
		Name = ProgramData[5]
		print('Installing as: ' + Name)
		execute_install(Name, 'ubuntu',Uninstall)

	#Debian
	elif IDName in SupportDebian:
		bInstall = True
		print('StartInstalling on Debian')
		Name = ProgramData[6]
		execute_install(Name, 'debian', Uninstall)
		print('Installing as: ' + Name)

	#Nachrricht wenn auf nicht unterstützter Distribution
	else:
		bInstall = False
		print('Not Supported Distribution') 

	#Debug Nachrricht
	if bInstall == True:
		print('Start Installing!')
	else:
		print('Something went wrong')


#Installation oder deinstallation anhand der Parameter
def execute_install(Name, Distribution,Uninstall):

	username = conf.get_entry("Installation","installusername")

	#nachrricht wenn deinstallieren
	if Uninstall == True:
		print('Uninstalling: '  + Name)

	#Debian
	print('Name: ' + Name + ' AND Distribution is: ' + Distribution)
	if Distribution == 'debian':
		if Distribution == 'debian' and Uninstall == False:
			output = SI.execute('pkexec --user ' + username +  ' apt-get install -y ' + Name, True)
		
		elif Distribution == 'debian' and Uninstall == True:
			output = SI.execute('pkexec --user ' + username + ' apt-get remove -y ' + Name, True)
		
		else:
			print('Dont uninstall or install')

	#Ubuntu
	elif Distribution == 'ubuntu':
		if Distribution == 'ubuntu' and Uninstall == False:
			output = SI.execute('pkexec --user ' + username + ' apt-get install -y ' + Name, True)
		
		elif Distribution == 'ubuntu' and Uninstall == True:
			output = SI.execute('pkexec --user ' + username + ' apt-get remove -y ' + Name, True)	
		
		else:
			print('Dont uninstall or install')

	#Arch
	elif Distribution == 'arch':
		if Distribution == 'arch' and Uninstall == False:
			output = SI.execute('pkexec --user ' + username + ' pacman -S ' + Name + ' --noconfirm' , True)

			
		elif Distribution == 'arch' and Uninstall == True:
			output = SI.execute('pkexec --user ' + username + ' pacman -Rs ' + Name + ' --noconfirm' , True)


			
	else:
		print('dont do anythong, there was a problem')

	#Interner Pacman Error auf Arch
	if 'error: failed to init transaction (unable to lock database)' in output:
		print('Could not lock database on Arch, please remove /var/lib/pacman/db.lck')
