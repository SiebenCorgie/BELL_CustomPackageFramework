import cpf
import CPFConf as conf
import CPFWeb as web

import subprocess

def get_folder_content(directory):
	content = []
	#versuche über "ls" inhalt in liste(array) zu speichern
	try:
		
		#rufe unterprogramm "ls" auf
		subprocess.call('ls '+ directory, shell=True)
		#speicher output in eigener variable
		output = subprocess.check_output('ls ' + directory, shell=True)
		#trenne byte-string stream an leerzeichen
		bytelist = output.split()
		#convertiere byte items zu strin liste

		#muss eigene aufzeilung nehmen
		for entry in range(len(bytelist)):
			bytesring = bytelist[entry]
			EndString = bytesring.decode('utf-8')
			#zu liste hinzufügen
			content.append(EndString)
			
	except:
		content = []
		content = ['No content']

	print('entrys are: ' + str(content))
	
	return content

def execute(command, passoutput):
	subprocess.call(command, shell=True)
	if passoutput == True:
		#convert to UTF
		returnstring = subprocess.check_output(command, shell=True)
		#remove \n from last part of string
		returnstring = returnstring.decode('utf-8')[:-1]
		print('returnstring: ' + returnstring)
		return returnstring