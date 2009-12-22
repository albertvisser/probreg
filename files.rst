Files in this directory
=======================

pr_start.pyw
    starter voor file(s) in package "probreg":

__init__.py
    (lege) package indicator
compare.py
    standalone programma bedoeld om twee probreg xml bestanden te vergelijken/
    synchroniseren
    gebruikt xml.etree.ElementTree
dml.py
    data manipulatie routines
    gebruikt xml.etree.ElementTree, shutil, datetime
images.py
    programma voor het genereren van de in het programma gebruikte images
pr_globals.py
    menu-id's voor probreg wx versie
pr_globals_ppg.py
    menu-id's , teksten en helpinfo voor probreg ppg versie
probreg.pyw
    main GUI program, wxPython versie
    gebruikt wx, datetime
    importeert images, pr_globals, dml
probreg_ppg.pyw
    main GUI program, PocketPyGui versie
    gebruikt ppygui,
    importeert pr_globals/pr_globals_ppg, dml, templates
templates.py
    printopmaak via templates in plaats van hard geprogrammeerde html
    gebruikt jinja

task.ico
    applicatie-icon voor probreg