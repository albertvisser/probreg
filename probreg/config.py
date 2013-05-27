"""config.py - gecombineerde configuratie voor probreg xml en sql versie

definieert de default waarden voor de settings dictionaries:
kopdict - dictionary van tabs in de vorm                 volgorde: (tab titel,  link naam)
statdict: dictionary van mogelijke statussen in de vorm  volgorde: (omschrijving, code, id in tabel)
catdict: dictionary van mogelijke soorten in de vorm     volgorde: (omschrijving, code, id in tabel)

en specifiek voor de SQL versie een aantal constanten:
DBLOC - waar de database staat
USER - default userid om in te vullen waar nodig
APPS - waar de lijst met apps staat
"""
DBLOC = "/home/albert/www/django/actiereg/actiereg.db"
USER = 2
APPS = "/home/albert/www/django/actiereg/apps.dat"

kopdict_xml = {
    "0": "Lijst",
    "1": "Titel/Status",
    "2": "Probleem/Wens",
    "3": "Oorzaak/Analyse",
    "4": "Oplossing/Svz",
    "5": "Vervolgactie",
    "6": "Voortgang"
}
statdict_xml = {
    "0": ("gemeld", 0),
    "1": ("in behandeling", 1),
    "2": ("oplossing controleren",2),
    "3": ("nog niet opgelost",3),
    "4": ("afgehandeld", 4),
    "5": ("afgehandeld - vervolg",5)
}
catdict_xml = {
    "P": ("probleem", 1),
    "W": ("wens", 2),
    "": ("onbekend", 0),
    "V": ("vraag", 3),
    "I": ("idee", 4),
    "F": ("div. informatie", 5)
}

titels = ('index', 'detail', 'meld', 'oorz', 'opl', 'verv', 'voortg')
kopdict_sql = {x: (y, titels[int(x)]) for x, y in kopdict_xml.items()}
statdict_sql = {x: (y[0], y[1], -1) for x, y in statdict_xml.items()}
catdict_sql = {x: (y[0], y[1], -1) for x, y in catdict_xml.items()}
catdict_sql[' '] = catdict_sql['']
del catdict_sql['']
