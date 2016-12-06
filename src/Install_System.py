
import SystemInteraction as SI
import CPFConf as conf
import CPFDatabase as db
import CPFFeedback as feedback
import time

SupportArch = ('arch','manjaro','antergos')
SupportUbuntu = ('ubuntu','elementary','lubuntu','xubuntu','kubuntu')
SupportDebian = ('debian','deepin')



#Herausfinden der Distribution, aufrufen des richtigen eintrags in der Datenbank
#Starten des installier odre deinstalliervorgangs
def Install(ProgramName, Uninstall, Massinstall):


	print('START INSTALLING')
	feedback.status_push(conf.get_entry('Status','startinstall'))

	feedback.set_progress(True)

	time.sleep(0.2)

	

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

	feedback.status_push(conf.get_entry('Status','startinstall'))
		
	if Massinstall == False:
		PrepareSingleInstall(ProgramName, Uninstall, IDName)
	elif Massinstall == True:
		MakeMassInstall(ProgramName, IDName)
	else:
		print("Wrong parameter")


#Masseninstallation
def MakeMassInstall(ProgramName, IDName):

	feedback.set_progress(True)

	print('Starting MassInstall')
	#Zusammenstellen der richtigen Programm namen 
	DistributionNameList = []
	#ubuntu
	if IDName == 'ubuntu':
		for u in ProgramName:
			ProgramData = db.read_attributes(u)
			DistributionNameList.append(ProgramData[5])
			
	#debian
	elif IDName == 'debian':
		for d in ProgramName:
			ProgramData = db.read_attributes(d)
			DistributionNameList.append(ProgramData[6])

	#arch
	elif IDName == 'arch':
		for a in ProgramName:
			ProgramData = db.read_attributes(a)
			DistributionNameList.append(ProgramData[7])

	InstallString = ' '.join(DistributionNameList)

	#Jetzt wird anhand der richtigen Liste installiert
	username = conf.get_entry("Installation","installusername")

	feedback.status_push(conf.get_entry('Status','startinstall'))
	
	if IDName == 'ubuntu' or IDName == 'debian':
		output = SI.execute('pkexec --user ' + username +  ' apt-get install -y ' + InstallString, True)
		
	elif IDName == 'arch':
		output = SI.execute('pkexec --user ' + username + ' pacman -S ' + InstallString + ' --noconfirm' , True)

	feedback.status_push(conf.get_entry('Status','installfinishedmass'))

	feedback.set_progress(True)		

	time.sleep(0.5)
	feedback.set_progress(False)
		
		
#Raussuchen des des richigen Parameters 
#und dann installieren bzw. deinstallieren
def PrepareSingleInstall(ProgramName, Uninstall, IDName):

	ProgramData = db.read_attributes(ProgramName)

	feedback.set_progress(True)
	feedback.status_push(conf.get_entry('Status','startinstall'))
	
	#Arch
	if IDName == 'arch':
		bInstall = True
		print('StartInstalling on: Arch')
		Name = ProgramData[7]
		print('Installing as: ' + Name)
		execute_install(Name, 'arch',Uninstall)

	#Ubuntu
	elif IDName == 'ubuntu':
		bInstall = True
		print('StartInstalling on Ubuntu')
		Name = ProgramData[5]
		print('Installing as: ' + Name)
		execute_install(Name, 'ubuntu',Uninstall)

	#Debian
	elif IDName == 'debian':
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
	if bInstall == False:
		print('Something went wrong')



#Installation oder deinstallation anhand der Parameter
def execute_install(Name, Distribution,Uninstall):

	username = conf.get_entry("Installation","installusername")

	#nachrricht wenn deinstallieren
	if Uninstall == True:
		print('Uninstalling: '  + Name)

	#Debian und Ubuntu
	print('Name: ' + Name + ' AND Distribution is: ' + Distribution)
	if Distribution == 'debian' or Distribution == 'ubuntu':
		if Uninstall == False:
			output = SI.execute('pkexec --user ' + username +  ' apt-get install -y ' + Name, True)
		
		elif Uninstall == True:
			output = SI.execute('pkexec --user ' + username + ' apt-get remove -y ' + Name, True)
		
		else:
			print('Dont uninstall or install')



	#Arch
	elif Distribution == 'arch':
		if Distribution == 'arch' and Uninstall == False:
			output = SI.execute('pkexec --user ' + username + ' pacman -S ' + Name + ' --noconfirm' , True)

			
		elif Distribution == 'arch' and Uninstall == True:
			output = SI.execute('pkexec --user ' + username + ' pacman -R ' + Name + ' --noconfirm' , True)


			
	else:
		print('dont do anything, there was a problem')

	#Interner Pacman Error auf Arch
	if 'error: failed to init transaction (unable to lock database)' in output:
		print('Could not lock database on Arch, check that no other program is \n using pacman or remove /var/lib/pacman/db.lck')

	feedback.status_push(conf.get_entry('Status','installfinishedsingle'))
	feedback.set_progress(True)

	time.sleep(0.5)
	feedback.set_progress(False)
