Files in this directory
=======================

pr_start.py
    starter voor file(s) in package "probreg" (the subdirectory)
prsql_start.py
    starter voor de sql versie
readme.rst
    description and usage notes
files.rst
    this file

package directory
-----------------
__init__.py
    (lege) package indicator
compare.py
    standalone programma bedoeld om twee probreg xml bestanden te vergelijken/
    synchroniseren
    gebruikt xml.etree.ElementTree
config_sql.py
    constanten voor dml_sql.py, inclusief page/soort/stat defaults
config_xml.py
    constanten voor dml_xml.py
config.py
    voorstudie om de voorgaande twee te combineren
dml_xml.py
    data manipulatie routines
    gebruikt xml.etree.ElementTree, shutil, datetime
dml_sql.py
    dml.py omgebouwd naar gebruik sql voor compatibiliteit met dajngo versie
    gebruikt sqlite
dml.py
    voorstudie om de voorgaande twee te combineren, waarschijnlijk geen goed idee
images.py
    programma voor het genereren van de in het programma gebruikte images
pr_globals.py
    menu-id's voor probreg wx versie
pr_globals_ppg.py
    menu-id's , teksten en helpinfo voor probreg ppg versie
probreg.py
    tussenschakel tussen pr_start en de gui-specifieke variant
probreg_qt.py
    main GUI program, PyQt5 versie
probreg_qt4.py
    main GUI program, PyQt4 versie
probreg_wx.py
    main GUI program, wxPython versie
    gebruikt wx, datetime
    importeert images, pr_globals, dml
probreg_ppg.py
    main GUI program, PocketPyGui versie
    gebruikt ppygui,
    importeert pr_globals/pr_globals_ppg, dml, templates
probreg_sql.py
    probrge.py aangepast voor gebruik dml_sql.py en wat andere zaken
pr_test.py
    testprogramma tbv verschillende manieren van opstarten
templates.py
    printopmaak via templates in plaats van hard geprogrammeerde html
    gebruikt jinja
    niet compleet (mist templates), niet af
task.ico
    applicatie-icon voor probreg
test/test_dml.py
    testscriptje voor dml_xml routines
test/test_dml_sql.py
    testscriptje voor dml_sql routines
