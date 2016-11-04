import CPFConf as conf
import CPFDatabase as db
import SystemInteraction as SI
import Install_System as install


###MassInstall Funktion fuer CPF

def AddEntry(builder):
	#Ein Programm zur Liste hinzufügen
	NameEntry = builder.get_object('MIADD_FileName')
	FilenName = NameEntry.get_text()
	ProgramChooser = builder.get_object('MIADD_LChooseProgram')
	
	print('Add')
	File = open(conf.get_entry('DB','dblocation') + '/' + FilenName + '.mass', 'a')
	File.write(ProgramChooser.get_active_text() + ',')
	File.close()

	

def Execute(builder):
	#Installationsanweisung ausführen
	print('exe')
	FileChooser = builder.get_object('MIInstall_Chooser')
	File = FileChooser.get_filename()
	print('MassFile is: ' + File)
	MassFile = open(File, 'r')
	MassLine = MassFile.readline()
	print('FileContent: ' + MassLine)
	MassNames = MassLine.split(',')
	MassNames.pop(len(MassNames) - 1)
	print(MassNames)
	install.Install(MassNames, False, True)
	print('Finished MassInstall')

	DialogWindow = builder.get_object('MIInsall')
	DialogWindow.hide()



def AddDialogInit(builder):
	#Aufrufen des AddDialog

	AddDialog = builder.get_object('MIADD')
	MainCooser = builder.get_object('MIADD_LChooseMain')

	MainList = conf.get_entry('DB','main')
	MainList = MainList.split(',')
	MainList

	MainCooser.remove_all()
	
	for i in MainList:
		print(i)
		MainCooser.append_text(i)

	
	AddDialog.show_all()
		
def AddDialogUpdateSub(builder):
	#Updaten der Unterkategorien
	MainCooser = builder.get_object('MIADD_LChooseMain')
	SubCooser = builder.get_object('MIADD_LChooserSubCategor')

	CurrentMainCategory = MainCooser.get_active_text()

	SubCategorys = conf.get_entry('DBSub',CurrentMainCategory.lower())
	SubCategorys = SubCategorys.split(',')

	SubCooser.remove_all()
	
	for i in SubCategorys:
		SubCooser.append_text(i)
		

def AddDialogUpdateProgram(builder):
	#Updaten der Verfügbaren Programme
	SubCooser = builder.get_object('MIADD_LChooserSubCategor')
	ProgramChooser = builder.get_object('MIADD_LChooseProgram')

	Programs = db.db_read(SubCooser.get_active_text())

	ProgramChooser.remove_all()
	
	for i in Programs:
		ProgramChooser.append_text(i)
		
	