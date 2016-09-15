import cpf
import subprocess
import configparser
import SystemInteraction as SI

#Konfiguration einlesen und schreiben

configpath = 'CPFConfig.conf'

config = configparser.ConfigParser()
config.read(configpath)

#in konfiguration schreiben
def set_entry(section, entry, newentry):
	config.set(section,entry,newentry)
	with open(configpath, 'w') as configfile:
		config.write(configfile)
		
#aus konfiguration lesen
def get_entry(section, entry):
	return config [str(section)][str(entry)]
	
#Grosses ConfigurationLoading
#_______________________________________________________________________________

def load_config(builder):
	#Internet
	#online status
	OnlineStatus = builder.get_object('Pref_NB_Internet_CBOnline')
	if get_entry('Internet', 'Online') == 'True':
		OnlineStatus.set_active(True)
	else:
		OnlineStatus.set_active(False)

	#CheckOnline
	CheckCheckBox = builder.get_object('Pref_NB_Internet_CheckCB')
	if get_entry('Internet', 'CheckRepo') == 'True':
		CheckCheckBox.set_active(True)
	else:
		CheckCheckBox.set_active(False)

	#Runterladen Erlauben
	DownloadBox = builder.get_object('Pref_NB_Internet_DLCB')
	if get_entry('Internet', 'AllowDownload') == 'True':
		DownloadBox.set_active(True)
	else:
		DownloadBox.set_active(False)

	#Dokumentations und Info URL Auslesen
	DocURL = builder.get_object('Pref_NB_Internet_DBE')
	DocURL.set_text(str(get_entry('Internet','DocURL')))

	InfoURL = builder.get_object('Pref_NB_Internet_HBE')
	InfoURL.set_text(str(get_entry('Internet','InfoURL')))

	#Datenbank
	#GitURL
	GitURL = builder.get_object('Pref_NB_DB_GitUrlEdit')
	GitURL.set_text(str(get_entry('DB','DataBaseGitURL')))

	#Datenbank File
	DBFileChooser = builder.get_object('Pref_NB_DB_CurrentDirFC')
	DBFileChooser.set_filename(str(get_entry('DB','currentdb')))
	
	#Setzte wert ob nicht-GitHub Quelle genutzt wird
	NoGitSource = builder.get_object('Pref_NB_DB_NotGitCB')
	if get_entry('DB','NotGitBased') == 'True':
		NoGitSource.set_active(True)
	else:
		NoGitSource.set_active(False)


	#Installation
	#Terminal bei Installation anzeigen
	InstallTerm = builder.get_object('Pref_NB_Inst_TerminalCB')
	if get_entry('Installation','ShowInstTerminal') == 'True':
		InstallTerm.set_active(True)
	else:
		InstallTerm.set_active(False)

	#Der Installierende benutzer
	InstallUserName = builder.get_object('Pref_NB_Inst_NameEdit')
	InstallUserName.set_text(str(get_entry('Installation','InstallUsername')))


	#Massen Installation
	MassInstallTerm = builder.get_object('Pref_NB_Mass_TermWin_CB')
	if get_entry('MassInstall', 'ShowMassTerminal') == 'True':
		MassInstallTerm.set_active(True)
	else:
		MassInstallTerm.set_active(False)

	#Zeige Erfolgsnachricht
	SuccessDisplay = builder.get_object('Pref_NB_Mass_SuccesCB')
	if get_entry('MassInstall', 'ShowSuccess') == 'True':
		SuccessDisplay.set_active(True)
	else:
		SuccessDisplay.set_active(False)

#Grosses ConfigurationSaving
#_______________________________________________________________________________
def save_config(builder):
	
	#Internet
	#online status
	OnlineStatus = builder.get_object('Pref_NB_Internet_CBOnline')
	set_entry('Internet', 'Online', str(OnlineStatus.get_active()))


	#CheckOnline
	CheckCheckBox = builder.get_object('Pref_NB_Internet_CheckCB')
	set_entry('Internet', 'CheckRepo', str(CheckCheckBox.get_active()))


	#Runterladen Erlauben
	DownloadBox = builder.get_object('Pref_NB_Internet_DLCB')
	set_entry('Internet', 'AllowDownload', str(DownloadBox.get_active()))


	#Dokumentations und Info URL Auslesen
	DocURL = builder.get_object('Pref_NB_Internet_DBE')
	set_entry('Internet','DocURL', DocURL.get_text())

	InfoURL = builder.get_object('Pref_NB_Internet_HBE')
	set_entry('Internet','InfoURL', InfoURL.get_text())

	#Datenbank
	#GitURL
	GitURL = builder.get_object('Pref_NB_DB_GitUrlEdit')
	set_entry('DB','DataBaseGitURL', GitURL.get_text())

	#Datenbank Datei
	DBFileChooser = builder.get_object('Pref_NB_DB_CurrentDirFC')
	print("Current File: " + DBFileChooser.get_filename())
	if DBFileChooser.get_filename() == None:
		print('DontWriteFolder')
	else:
		set_entry('DB','currentdb', str(DBFileChooser.get_filename()))

	#Datenbank Ordner
	if DBFileChooser.get_filename() == None:
		print('DontWriteFile')
	else:
		set_entry('DB','dblocation', str(DBFileChooser.get_current_folder()))
		
	#Setzte wert ob nicht-GitHub Quelle genutzt wird
	NoGitSource = builder.get_object('Pref_NB_DB_NotGitCB')
	set_entry('DB','NotGitBased', str(NoGitSource.get_active()))


	
	#Installation
	#Terminal bei Installation anzeigen
	InstallTerm = builder.get_object('Pref_NB_Inst_TerminalCB')
	set_entry('Installation','ShowInstTerminal', str(InstallTerm.get_active()))

	#Der Installierende benutzer
	InstallUserName = builder.get_object('Pref_NB_Inst_NameEdit')
	set_entry('Installation','InstallUsername', InstallUserName.get_text())


	#Massen Installation
	MassInstallTerm = builder.get_object('Pref_NB_Mass_TermWin_CB')
	set_entry('MassInstall', 'ShowMassTerminal', str(MassInstallTerm.get_active()))

	#Zeige Erfolgsnachricht
	SuccessDisplay = builder.get_object('Pref_NB_Mass_SuccesCB')
	set_entry('MassInstall', 'ShowSuccess', str(SuccessDisplay.get_active()))
	