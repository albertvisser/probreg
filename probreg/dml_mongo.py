"data managenent voor ProbReg mongodb versie"
## import sys
import os
import pathlib
import base64  # gzip
import datetime as dt
from shutil import copyfile
import logging
from pymongo import MongoClient
from pymongo.collection import Collection
# from probreg.shared import DataError, kopdict, statdict, catdict -- even ingekopieerd
cl = MongoClient()
db = cl.probreg_database
coll = db.default  # for now we only do one collection per database

datapad = os.getcwd()


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


def log(msg, *args, **kwargs):
    "schrijf logregel indien debuggen gewenst"
    if 'DEBUG' in os.environ and os.environ['DEBUG']:
        logging.info(msg, *args, **kwargs)


def check_filename(fnaam):
    """check for correct filename and return short and long version

    fnaam is a pathlib.Path object
    """
    return fnaam, fnaam, True, ''


def checkfile(fn, new=False):
    raise NotImplementedError


def get_nieuwetitel(fnaam, jaar=None):
    "bepaal nieuw uit te geven actienummer"
    if jaar is None:
        jaar = str(dt.date.today().year)
    # zoek laatst uitgegeven actienummer voor het huidige jaar (voor nu even simuleren)
    acties_van_jaar = coll.find({'jaar': jaar})
    last_action = max([x['nummer'] for x in acties_van_jaar])
    action = last_action + 1
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
        self.kop = {x: y[0] for x, y in kopdict.items()}
        self.stat = {x: (y[0], y[1]) for x, y in statdict.items()}
        self.cat = {x: (y[0], y[1]) for x, y in catdict.items()}
        self.imagecount = 0
        self.startitem = ''
        self.meld = ''
        self.fn, self.fnaam, self.exists, self.meld = check_filename(fnaam)
        if self.meld:
            raise DataError(self.meld)
        if self.exists:
            self.read()

    def read(self):
        "settings lezen"
        settings = coll.find_one({'name': 'settings'})
        self.settings_id = settings['_id']
        for item, value in settings['headings'].items():
            self.kop[item] = value[0]
        for item, value in settings['statuses'].items():
            self.stat[item] = value
        for item in settings['categories'].items():
            self.cat[item] = value
        self.imagecount = settings['imagecount']
        self.startitem = settings['startitem']

    def write(self, srt=None):  # extra argument ivm compat sql-versie
        "settings terugschrijven"
        coll.update_one({'_id': self.settings_id}, {'$set': {'headings': self.headings}})
        coll.update_one({'_id': self.settings_id}, {'$set': {'statuses': self.statuses}})
        coll.update_one({'_id': self.settings_id}, {'$set': {'categories': self.categories}})
        coll.update_one({'_id': self.settings_id}, {'$set': {'imagecount': self.imagecount}})
        coll.update_one({'_id': self.settings_id}, {'$set': {'startitem': self.startitem}})
        self.exists = True

    def set(self, naam, key=None, waarde=None):
        "settings waarde instellen"
        if naam not in ("stat", "cat", "kop"):
            self.meld = 'Foutieve soort opgegeven'
            raise DataError(self.meld)
        elif key is None:
            self.meld = 'Geen sleutel opgegeven'
            raise DataError(self.meld)
        elif waarde is None:
            self.meld = 'Geen waarde voor sleutel opgegeven'
            raise DataError(self.meld)
        elif naam == "stat":
            if not isinstance(waarde, tuple):
                self.meld = 'Sleutelwaarde moet bestaan uit tekst en sortvolgnummer'
                raise DataError(self.meld)
            self.stat[key] = waarde
        elif naam == "cat":
            if not isinstance(waarde, tuple):
                self.meld = 'Sleutelwaarde moet bestaan uit tekst en sortvolgnummer'
                raise DataError(self.meld)
            self.cat[key] = waarde
        elif naam == "kop":
            if not isinstance(waarde, str):
                self.meld = 'Sleutelwaarde moet bestaan uit alleen tekst'
                raise DataError(self.meld)
            self.kop[key] = waarde

    def get(self, naam, key=None):
        "settings waarde lezen"
        if naam not in ("stat", "cat", "kop"):
            self.meld = 'Foutieve soort opgegeven'
            raise DataError(self.meld)
        elif naam == "stat":
            if key is None:
                return self.stat
            else:
                if isinstance(key, int):
                    key = str(key)
                if key not in self.stat:
                    self.meld = 'Sleutel bestaat niet voor status'
                    raise DataError(self.meld)
                return self.stat[key]
        elif naam == "cat":
            if key is None:
                return self.cat
            else:
                if key not in self.cat:
                    self.meld = 'Sleutel bestaat niet voor soort'
                    raise DataError(self.meld)
                return self.cat[key]
        elif naam == "kop":
            if key is None:
                return self.kop
            else:
                if isinstance(key, int):
                    key = str(key)
                if key not in self.kop:
                    self.meld = 'Sleutel bestaat niet voor kop'
                    raise DataError(self.meld)
                return self.kop[key]


class Actie:
    """lijst alle gegevens van een bepaald item

    fnaam is a pathlib.Path object
    user is only for compatibilty with the Django version
    """
    def __init__(self, fnaam, actiekey, user=None):
        self.fn, self.fnaam, self.file_exists, self.meld = check_filename(fnaam)
        if self.meld:
            raise DataError(self.meld)
        self.settings = Settings(fnaam)
        self.imagecount = int(self.settings.imagecount)
        self.imagelist = []
        self.actie_id, self.exists = actiekey, False
        self.datum = self.soort = self.titel = ''
        self.status, self.arch = '0', False
        self.melding = self.oorzaak = self.oplossing = self.vervolg = self.stand = ''
        self.events = []
        new_item = actiekey == 0 or actiekey == "0"
        if new_item:
            self.nieuw()
        elif self.file_exists:
            self.read()

    def nieuwfile(self):
        "nieuw projectbestand aanmaken"
        # nieuwe momgo database aanmaken of gaan we ervan uit dat die al bestaat?
        # bij een eerste actie moeten we in elk geval ook de settings wegschrijvem

    def nieuw(self):
        "nieuwe actie initialiseren"
        self.nummer = get_nieuwetitel(self.fn)
        self.datum = dt.datetime.today().isoformat(' ')[:19]

    def read(self):
        "gegevens lezen van een bepaalde actie"
        # tzt via mongodb doen; nu geven we een setje standaard waarden terug
        # self.id is meegegeven in de instantiëring
        actie = coll.find_one({'_id': self.actie_id})
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
        waarde = self.status[0]
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

    def set_status(self, waarde):
        "stel status in (code of tekst)"
        if isinstance(waarde, int):
            if str(waarde) in statdict:
                self.status = waarde
            else:
                raise DataError("Foutieve numerieke waarde voor status")
        elif isinstance(waarde, str):
            found = False
            for x, y in list(statdict.values()):
                log('%s %s %s', waarde, x, y)
                # if x == waarde:  # FIXME: moet dit soms y zijn?
                if y == waarde:
                    found = True
                    self.status = x
                    break
            if not found:
                raise DataError("Foutieve tekstwaarde voor status")
        else:
            raise DataError("Foutief datatype voor status")

    def set_soort(self, waarde):
        "stel soort in (code of tekst)"
        log(waarde)
        if isinstance(waarde, str):
            if waarde in catdict:
                self.soort = waarde
            else:
                found = False
                for x, y in list(catdict.items()):
                    log(y)
                    if y[0] == waarde:
                        found = True
                        self.soort = x
                        break
                if not found:
                    raise DataError("Foutieve tekstwaarde voor categorie")
        else:
            raise DataError("Foutief datatype voor categorie")

    def set_arch(self, waarde):
        "stel archiefstatus in"
        if not isinstance(waarde, bool):
            raise DataError("Foutief datatype voor archiveren")
        self.arch = waarde

    def write(self):
        "actiegegevens terugschrijven"
        self.settings['imagecount'] = str(self.imagecount)  # moet dit niet parent.parent.imagecount zijn?
        if self.startitem:
            self.settings['startitem'] = str(self.startitem)
        self.settings.write()
        jaar, nummer = self.nummer.split('-')
        actie = coll.update_one({'_id': self.actie_id}, {'$set': {'jaar': jaar, 'nummer': nummer,
                                                                  'gemeld': self.datum,
                                                                  'status': self.status,
                                                                  'soort': self.soort,
                                                                  'bijgewerkt': self.updated,
                                                                  'titel': self.titel,
                                                                  'melding': self.melding,
                                                                  'events': self.events}})
        return found


    def clear(self):
        "images opruimen"
        for fname in self.imagelist:
            os.remove(fname)

    def list(self):
        "actie uitlijsten naar print"
        try:
            soort = self.get_soorttext()
        except DataError:
            soort = self.soort
        status = self.status
        try:
            status = status + ' ' + self.get_statustext()
        except DataError:
            pass
        result = ["%s %s gemeld op %s status %s" % (soort,
                                                    self.id,
                                                    self.datum,
                                                    status)]
        result.append("Titel: {}".format(self.titel))
        result.append("Melding: {}".format(self.melding))
        result.append("Oorzaak: {}".format(self.oorzaak))
        result.append("Oplossing: {}".format(self.oplossing))
        result.append("Vervolg: {}".format(self.vervolg))
        result.append("Stand: {}".format(self.stand))
        result.append("Verslag:")
        for date, text in self.events:
            result.append("\t{} - {}".format(date, text))
        if self.arch:
            result.append("Actie is gearchiveerd.")
        # for now
        return result
