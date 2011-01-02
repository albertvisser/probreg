Files in this directory
=======================

pr_start.pyw
    starter voor file(s) in package "probreg":

package directory
-----------------
__init__.py
    (lege) package indicator
compare.py
    standalone programma bedoeld om twee probreg xml bestanden te vergelijken/
    synchroniseren
    gebruikt xml.etree.ElementTree
config.py
    constanten voor dml_sql.py, inclusief page/soort/stat defaults
dml.py
    data manipulatie routines
    gebruikt xml.etree.ElementTree, shutil, datetime
dml_sql.py
    dml.py omgebouwd naar gebruik sql voor compatibiliteit met dajngo versie
images.py
    programma voor het genereren van de in het programma gebruikte images
pr_globals.py
    menu-id's voor probreg wx versie
pr_globals_ppg.py
    menu-id's , teksten en helpinfo voor probreg ppg versie
probreg.py
    main GUI program, wxPython versie
    gebruikt wx, datetime
    importeert images, pr_globals, dml
probreg_ppg.py
    main GUI program, PocketPyGui versie
    gebruikt ppygui,
    importeert pr_globals/pr_globals_ppg, dml, templates
probreg_sql.py
    probrge.py aangepast voor gebruik dml_sql.py en wat andere zaken
templates.py
    printopmaak via templates in plaats van hard geprogrammeerde html
    gebruikt jinja
task.ico
    applicatie-icon voor probreg
