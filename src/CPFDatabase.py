import cpf
import CPFConf as conf
import CPFWeb as web
import SystemInteraction as SI
import configparser


def create_new_DB(builder):
	nameEntry = builder.get_object('CND_Name')
	NewDBName = nameEntry.get_text()
	if NewDBName == None:
		print('NoName')
		return
	else:
		LocationDialog = builder.get_object('CND_Locatio')
		NewDBLocation = LocationDialog.get_filename()
		print('________________________________________________________________')
		print(NewDBLocation)
		UpdateConfTick = builder.get_object('CND_bUseNew')
		if UpdateConfTick.get_active() == True:
			conf.set_entry('DB','currentdb', NewDBLocation)
			print('Updated')

		MainCategoryList = conf.get_entry('DB','enmain')
		MainCategoryList = MainCategoryList.split(',')

		for MainCat in MainCategoryList:
			SI.execute('cd ' + NewDBLocation + ' && mkdir ' + MainCat,False)
			CurrentSubCatList = conf.get_entry('DBSub','en' + MainCat.lower())
			CurrentSubCatList = CurrentSubCatList.split(',')
			for SubCatItem in CurrentSubCatList:
				SI.execute('cd ' + NewDBLocation + '/' + MainCat + '&& mkdir ' + SubCatItem,False)
			print('Wrote ' + MainCat)

def Create_New_Entry(builder):	
	
	try:
		#name
		NameEntry = builder.get_object('DB_A_NameEdit')
		Name = NameEntry.get_text()

		#Short Desc
		SDEntry = builder.get_object('DB_A_DescS_Edit')
		ShortDesciption = SDEntry.get_text()

		#Long Desc
		LDEntry = builder.get_object('DB_A_DescL_Edit')
		LongDescription = LDEntry.get_text()

		#ubuntu
		ubuntuEntry = builder.get_object('DB_A_UbuntuName')
		Ubuntu = ubuntuEntry.get_text()

		#debian
		debianEntry = builder.get_object('DB_A_DebianName')
		Debian = debianEntry.get_text()

		#arch
		archEntry = builder.get_object('DB_A_ArchName')
		Arch = archEntry.get_text()

		#MainCategory
		MainCategorynEntry = builder.get_object('DB_A_Main')
		MainCategory = MainCategorynEntry.get_active_text()

		#SubCategory
		SubCategoryEntry = builder.get_object('DB_Sub')
		SubCategory = SubCategoryEntry.get_active_text()

		#URl
		urlEntry = builder.get_object('DB_A_URL')
		URL = urlEntry.get_text()

		if URL == None or SubCategory == None or MainCategory == None or Arch == None or Debian == None or Ubuntu == None or LongDescription == None or ShortDesciption == None or Name == None:
			ErrorDialog = builder.get_object('DB_ErrorMessage')
			ErrorDialog.show_all()
			return
		#create Program Directory ________________________________________________________________

		SI.execute('cd ' + conf.get_entry('DB','currentdb') + '/' + MainCategory + '/' + SubCategory + '/ && mkdir ' + Name, False)



		#screenshot
		ScreenshotEntry = builder.get_object('DB_A_ScreenChooser')
		ScreenshotLocation = ScreenshotEntry.get_filename()
		if ScreenshotLocation == None:
			ScreenshotStatus = 'False'
		else:
			SI.execute('cp ' + ScreenshotLocation + ' ' + conf.get_entry('DB','currentdb') + '/' + MainCategory + '/' + SubCategory + '/' + Name + '/Screenshot.image', False)
			ScreenshotStatus = 'True'
			
		#symbol
		SymbolEntry = builder.get_object('DB_A_SymbolChooser')
		SymbolLocation = SymbolEntry.get_filename()
		if SymbolLocation == None:
			SymbolStatus = 'False'
		else:
			SymbolStatus = 'True'
			SI.execute('cp ' + SymbolLocation + ' ' + conf.get_entry('DB','currentdb') + '/' + MainCategory + '/' + SubCategory + '/' + Name + '/Symbol.image', False)

		#CreateEntryFile
		programConf = configparser.ConfigParser()
		programConf['main'] = {'name': str(Name),
								'shortdescription' : str(ShortDesciption),
								'longdescription' : str(LongDescription),
								'ubuntu' : str(Ubuntu),
								'debian' : str(Debian),
								'arch' : str(Arch),
								'maincategory' : MainCategory,
								'subcategory' : SubCategory,
								'URL' : URL,
								'Screenshot' : ScreenshotStatus,
								'Symbol' : SymbolStatus}
								
		with open(conf.get_entry('DB','currentdb') + '/' + MainCategory + '/' + SubCategory + '/' + Name + '/' + Name + '.info' , 'w') as configFile:
			programConf.write(configFile)
	#exit if anythong happens
	except:
		ErrorDialog = builder.get_object('DB_ErrorMessage')
		ErrorDialog.show_all()
		return


#Update The Main Category Box
def InitAddDialog(builder):
	
	#UpdateMainCategorys
	MainCategorysEntryBox = builder.get_object('DB_A_Main')
	MainCategorysEntryBox.remove_all()

	MainCategoryList = conf.get_entry('DB','enmain')
	MainCategoryList = MainCategoryList.split(',')

	for mainItem in MainCategoryList:
		MainCategorysEntryBox.append_text(mainItem)

#Update The SubCategory Box
def update_SubList(builder):

	MainCategorysEntryBox = builder.get_object('DB_A_Main')
	CurrentEntry = MainCategorysEntryBox.get_active_text()

	CurrentSubList = conf.get_entry('DBSub','en' + CurrentEntry.lower())
	CurrentSubList = CurrentSubList.split(',')

	SubCategoryBox = builder.get_object('DB_Sub')
	SubCategoryBox.remove_all()

	for subItem in CurrentSubList:
		SubCategoryBox.append_text(subItem)







	
	
	