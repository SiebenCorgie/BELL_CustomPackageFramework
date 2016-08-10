## Process this file with automake to produce Makefile.in
## Created by Anjuta


uidir = $(pkgdatadir)/ui
ui_DATA = cpf.ui


## The main script
bin_SCRIPTS = cpf.py

## Directory where .class files will be installed
cpfdir = $(pythondir)/cpf


cpf_PYTHON = \
	cpf.py


EXTRA_DIST = $(ui_DATA)


# Remove ui directory on uninstall
uninstall-local:

	-rm -r $(uidir)

	-rm -r $(pkgdatadir)
