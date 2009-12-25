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

Django versie
-------------
__init__.py
    (lege) package indicator
copyover.py
    utility programma om xml over te halen naar sqlite database
loaddata.py
    utility programma; onderdeel van newapp
manage.py
    controle module
newapp.py
    utility programma: realiseren nieuw project
settings.py
    site instellingen
urls.py
    root url dispatcher
views.py
    root views voor django
wsgi_handler.py
    maakt het mogelijk deze site via wsgi te draaien

_basic/
.......
    bevat de programmatuur voor een specifiek project
    moet vooralsnog per project gekopieerd worden naar aparte map
    dat biedt bovendien de mogelijkheid om dat per project specifieker
    te maken
__init__.py
    (lege) package indicator
admin.py
    registratie van models tbv admin site
initial_data.json
    bevat initiele data voor de status soort en tit-header tabellen
models.py
    data mappings
sample_data.py
    voorbeeld gegevens
urls.py
     url dispatcher voor project
views.py
    project views

_basic/templatetags/
....................
    bevat zelfgedefinieerde tags
__init__.py
    (lege) package indicator
extratags.py
    de eigenlijke code

templates/
..........
base.html
    elementair template
base_site.html
    algemene uitbrieding van base
index.html
    startpagina
logged_out.html
    standaard pagina na uitloggen
nieuw.html
    pagina voor aanmelden nieuw project

templates/basic/
................
    bevat de templates voor een project
    deze voor elk project apart kopieren geeft de mogelijkheid om de
    templates specifieker te maken zonder de andere projecten te raken
actie.html
    pagina voor weergave actiegegevens
base_site.html
    project uitbreiding van base en algemene base_site
index.html
    pagina voor weergave lijst met acties
order.html
    pagina voor definieren sortering van de lijst
probreg.css
select.html
    pagina voor definieren selectie van de lijst
settings.html
    pagina voor definieren project instellingen
tekst.html
    pagina voor tonen/aanpassen gegevens actie-onderdeel
voortgang.html
    pagina voor tonen/aanpassen voortgangsmomenten

templates/registration/
.......................
login.html
    aanlog pagina