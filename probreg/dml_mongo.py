"data managenent voor ProbReg mongodb versie"
## import sys
import os
import pathlib
import base64  # gzip
import datetime as dt
from shutil import copyfile
from pymongo import MongoClient
from pymongo.collection import Collection
# ingekopieerd vanwege cirular import, hetzelfde geldt voor logging
# from probreg.shared import DataError, kopdict, statdict, catdict
cl = MongoClient()
db = cl.probreg_database
coll = db.default  # for now we only do one collection per database

datapad = os.getcwd()
dtformat = '%d-%m-%Y %H:%I:%S'  # zelfde als in shared.get_dts()


kopdict = {
    "0": ("Lijst", 'index'),
    "1": ("Titel/Status", 'detail'),
    "2": ("Voortgang", 'voortg')
}

statdict = {
    "0": ("gemeld", 0, -1),
    "1": ("in behandeling", 1, -1),
    "2": ("oplossing controleren", 2, -1),
    "3": ("nog niet opgelost", 3, -1),
    "4": ("afgehandeld", 4, -1),
    "5": ("afgehandeld - vervolg", 5, -1)
}

catdict = {
    "P": ("probleem", 1, -1),
    "W": ("wens", 2, -1),
    " ": ("onbekend", 0, -1),
    "V": ("vraag", 3, -1),
    "I": ("idee", 4, -1),
    "F": ("div. informatie", 5, -1)
}


class DataError(ValueError):    # Exception):
    "Eigen all-purpose exception - maakt resultaat testen eenvoudiger"
    pass


def get_nieuwetitel(fnaam, jaar=None):
    "bepaal nieuw uit te geven actienummer"
    if jaar is None:
        jaar = str(dt.date.today().year)
    # zoek laatst uitgegeven actienummer voor het huidige jaar (voor nu even simuleren)
    acties_van_jaar = list(coll.find({'jaar': jaar}))
    if acties_van_jaar:
        last_action = max([x['nummer'] for x in acties_van_jaar])
        action = last_action + 1
    else:
        action = 1
    return f'{jaar}-{action:04}'


def get_acties(fnaam, select=None, arch="", user=None):
    """ lijst alle items van een bepaald soort

    fnaam is a pathlib.Path object

    zoeken mogelijk op id (groter dan / kleiner dan), soort, status, (deel van) titel
    een selecteer-key mag een van de volgende waarden zijn:
    "idlt" - in dat geval moet de waarde een string zijn waarmee vergeleken wordt,
    "idgt" - in dat geval moet de waarde een string zijn waarmee vergeleken wordt,
    "soort" - in dat geval moet de waarde een list zijn van mogelijke soorten,
    "status" - in dat geval moet de waarde een list zijn van mogelijke statussen,
    "titel" - in dat geval moet de waarde een string zijn die in de titel moet voorkomen
    eventueel wildcards:
        als de string niet begint met een * dan moet de titel ermee beginnen
        als de string niet eindigt met een * dan moet de titel ermee eindigen
        als er een * in zit moet wat ervoor zit en erna komt in de titel zitten
    het laatste argument `user` wordt hier niet gebruikt maar is voor compatibiliteit
    met de django versie
    """
    if select is None:
        select = {}
        # if not arch:
        #     return []
    if arch not in ("", "arch", "alles"):
        raise DataError("Foutieve waarde voor archief opgegeven "
                        "(moet niks, 'arch'  of 'alles' zijn)")
    lijst = []
    # if select:
    #     keyfout = False
    #     for x in list(select.keys()):
    #         if x not in ("idlt", "id", "idgt", "soort", "status", "titel"):
    #             keyfout = True
    #             break
    #     if keyfout:
    #         raise DataError("Foutief selectie-argument opgegeven")
    selections = []

    idclause = ''
    item_lt = select.pop('idlt', '')
    enof = select.pop('id', '')
    item_gt = select.pop('idgt', '')
    if enof not in ('', 'en', 'of'):
        raise DataError('Foutieve waarde voor id-operator opgegeven')
    if enof and not all((item_lt, item_gt)):
        raise DataError("Operator alleen opgeven bij twee grenswaarden voor id")
    if all((item_lt, item_gt)) and not enof:
        raise DataError("Geen operator opgegeven bij twee grenswaarden voor id")
    if item_lt:
        idclause += f'"lt": "{item_lt}"'
    if item_gt:
        if item_lt:
            idclause += ', '
        idclause += f'"gt": "{item_gt}"'
    if idclause:
        idclause = idclause.join(('{', '}'))
        if enof == 'of':
            idclause = idclause.join(('{"or": ', '}'))
        idclause = '"nummer": ' + idclause
        selections.append(idclause)

    soortclause = select.pop('soort', '')
    if soortclause:
        soortclause = '"soort": "' + soortclause + '"'
        selections.append(soortclause)

    statclause = select.pop('status', '')
    if statclause:
        statclause = '"status": "' + statclause + '"'
        selections.append(statclause)

    textclause = select.pop('titel', '')
    if textclause:
        textclause = '"titel": {"regex": "\.*' + textclause + '\.*"}'
        selections.append(textclause)
    # TODO ook op onderwerp kunnen zoeken

    if select:
        raise DataError("Foutief selectie-argument opgegeven")

    archclause = '"arch": true' if arch == "arch" else '"arch": false' if arch == "" else ''
    if archclause:
        selections.append(archclause)

    if selections:
        selections = '{' + ', '.join(selections) + '}'
        return selections

    # sett = Settings(fnaam) - heb ik dit nodig?
    # zoeken gaat t.z.t. met mongodb, nu maar even net doen alsof
    # TODO: afmaken
    # ik wil ook een rubriek 'onderwerp' teruggeven net als bij django, als ik dan status en soort
    # in twee rubrieken doorgeef heb ik net zoveel velden als de django versie
    # of ik moet dat daar ook anders doen
    lijst = [('2022-0001', 'vandaag', 'nieuw', 'idee', 'iets', 'vandaag', ''),
             ('2022-0002', 'vandaag', 'nieuw', 'idee', 'iets', 'vandaag', '')]
    return lijst


class Settings:
    """instellingen voor pagina's, soorten en statussen
        argument = filenaam
        mag leeg zijn, pathlib.Path object met suffix ".xml" (anders: DataError exception)
        de soorten hebben een numeriek id en alfanumerieke code
        de categorieen hebben een numeriek id en een numerieke code
        de id's bepalen de volgorde in de listboxen en de codes worden in de xml opgeslagen
    """
    def __init__(self, fnaam=""):
        if not fnaam:
            fnaam = 'default'
        self.kop = {x: (y[0],) for x, y in kopdict.items()}
        self.stat = {x: (y[0], y[1]) for x, y in statdict.items()}
        self.cat = {x: (y[0], y[1]) for x, y in catdict.items()}
        self.imagecount = 0
        self.startitem = ''
        self.exists = self.read()

    def read(self):
        "settings lezen"
        settings = coll.find_one({'name': 'settings'})
        exists = settings is not None
        if exists:
            self.settings_id = settings['_id']
            self.kop = {x: (y[0],) for x, y in settings['headings'].items()}
            self.stat = {x: y for x, y in settings['statuses'].items()}
            self.cat = {x: y for x, y in settings['categories'].items()}
            self.imagecount = settings['imagecount']
            self.startitem = settings['startitem']
        return exists

    def write(self, srt=None):  # extra argument ivm compat sql-versie
        "settings terugschrijven"
        if not self.exists:
            self.settings_id = coll.insert_one({'name': 'settings'}).inserted_id
            self.exists = True
        coll.update_one({'_id': self.settings_id}, {'$set': {'headings': self.kop}})
        coll.update_one({'_id': self.settings_id}, {'$set': {'statuses': self.stat}})
        coll.update_one({'_id': self.settings_id}, {'$set': {'categories': self.cat}})
        coll.update_one({'_id': self.settings_id}, {'$set': {'imagecount': self.imagecount}})
        coll.update_one({'_id': self.settings_id}, {'$set': {'startitem': self.startitem}})


class Actie:
    """lijst alle gegevens van een bepaald item

    fnaam is a pathlib.Path object
    user is only for compatibilty with the Django version
    """
    def __init__(self, fnaam, actiekey, user=None):
        self.fn = fnaam
        self.settings = Settings(fnaam)
        self.imagecount = int(self.settings.imagecount)
        self.imagelist = []
        self.actie_id, self.exists = actiekey, False
        self.datum = self.updated = self.soort = self.titel = ''
        self.status, self.arch = '0', False
        self.melding = ''
        self.events = []
        if actiekey == 0 or actiekey == "0":
            self.nieuw()
        else:
            self.read()

    def nieuwfile(self):
        "nieuw projectbestand aanmaken"
        # nieuwe momgo database aanmaken of gaan we ervan uit dat die al bestaat?
        # bij een eerste actie moeten we in elk geval ook de settings wegschrijvem

    def nieuw(self):
        "nieuwe actie initialiseren"
        now = dt.datetime.today()
        self.nummer = get_nieuwetitel(self.fn, now.year)
        self.datum = now.isoformat(' ')[:19]

    def read(self):
        "gegevens lezen van een bepaalde actie"
        self.exists = False
        actie = coll.find_one({'_id': self.actie_id})
        if actie is None:
            raise DataError('Actie object does not exist')
        self.nummer = '-'.join((actie['jaar'], actie['nummer']))
        self.datum = actie['gemeld']
        self.status = actie['status']
        self.soort = actie['soort']
        self.updated = actie['bijgewerkt']
        self.titel = actie['titel']
        self.melding = actie['melding']
        self.stand = ''
        self.events = actie['events']
        self.imagelist = []
        self.exists = True

    def get_statustext(self):
        "geef tekst bij statuscode"
        waarde = self.status
        ## if str(waarde) in statdict:
        try:
            return self.settings.stat[str(waarde)][0]

        ## else:
        except KeyError:
            raise DataError("Geen tekst gevonden bij statuscode {}".format(waarde))

    def get_soorttext(self):
        "geef tekst bij soortcode"
        waarde = self.soort
        ## if waarde in catdict:
        try:
            return self.settings.cat[waarde][0]
        ## else:
        except KeyError:
            raise DataError("Geen tekst gevonden bij soortcode {}".format(waarde))

    def add_event(self, txt):
        "voeg tekstregel toe aan events"
        now = dt.datetime.today()
        self.events.append((now.strftime(dtformat), txt))

    def write(self):
        "actiegegevens terugschrijven"
        if not self.exists:
            self.actie_id = coll.insert_one({}).inserted_id
            self.exists = True
        self.settings.imagecount = str(self.imagecount)  # moet dit niet parent.parent.imagecount zijn?
        self.settings.startitem = str(self.actie_id)
        self.settings.write()
        jaar, nummer = self.nummer.split('-')
        coll.update_one({'_id': self.actie_id}, {'$set': {'jaar': jaar, 'nummer': nummer,
                                                          'gemeld': self.datum,
                                                          'status': self.status,
                                                          'soort': self.soort,
                                                          'bijgewerkt': self.updated,
                                                          'titel': self.titel,
                                                          'melding': self.melding,
                                                          'events': self.events}})

    def cleanup(self):
        "images opruimen"
        for fname in self.imagelist:
            os.remove(fname)
