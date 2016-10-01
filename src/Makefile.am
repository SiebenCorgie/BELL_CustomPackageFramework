## Process this file with automake to produce Makefile.in
## Created by Anjuta


uidir = $(pkgdatadir)/ui
ui_DATA = cpf.ui


## The main script
bin_SCRIPTS = cpf.py \
	CPFWeb.py \
	CPFConf.py \
	SystemInteraction.py \
	CPFDatabase.py \
	Install_UI.py \
	Install_System.py \
	VTE_Interaction.py

## Directory where .class files will be installed
cpfdir = $(pythondir)/cpf


cpf_PYTHON = \
	cpf.py


EXTRA_DIST = $(ui_DATA)


# Remove ui directory on uninstall
uninstall-local:

	-rm -r $(uidir)

	-rm -r $(pkgdatadir)
