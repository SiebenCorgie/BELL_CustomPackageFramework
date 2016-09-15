import cpf
import SystemInteraction as SI
import CPFConf as conf
import CPFDatabase as db


SupportArch = ('arch','manjaro','antergos')
SupportUbuntu = ('ubuntu','"elementary"','lubuntu','xubuntu','kubuntu')
SupportDebian = ('debian','deepin')

def Install(ProgramName):
	#Get all ProgramData from DatabaseEntry

	ProgramData = db.read_atributes(ProgramName)
	#read release information
	Distribution = SI.execute('cat /etc/*-release',True)
	#Distribution[1]
	Distribution = Distribution.split('\n')
	for name in Distribution:
		if 'ID=' in name:
			IDName = name
			
	IDName = IDName[3:]
	print('ID IS: ' + IDName)

	if IDName in SupportArch:
		bInstall = True
		print('StartInstalling on: Arch')
		ArchName = ProgramData[7]
		print('Installing as: ' + ArchName)
	elif IDName in SupportUbuntu:
		bInstall = True
		print('StartInstalling on Ubuntu')
		UbunutName = ProgramData[5]
		print('Installing as: ' + UbunutName)
	elif IDName in SupportDebian:
		bInstall = True
		print('StartInstalling on Debian')
		DebianName = ProgramData[6]
		print('Installing as: ' + DebianName)
	else:
		bInstall = False
		print('Not Supported Distribution')
