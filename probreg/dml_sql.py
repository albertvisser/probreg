# -*- coding: utf-8 -*-
"""dml voor probreg met gebruikmaking van de django orm functionaliteit

nee we gaan toch maar directe sql gebruiken, anders moet ik de import van
models.py in allerlei classes apart doen
LaatsteActie is opgenomen in Actie
Settings is aangepast mhoo direct sql gebruik;
    de get en set methoden werden niet gebruikt en zijn verwijderd
Acties is van een class een functie geworden (get_acties)
Actie is aangepast mhoo direct sql gebruik

testen:
- checkfile is ok
- get_acties is ok
- Settings s ok
- Actie
"""

from __future__ import print_function
## import sys
## import os
import pprint as pp
#sys.path.append("/home/visser/django")
#os.environ["DJANGO_SETTINGS_MODULE"] = 'actiereg.settings'
import sqlite3 as sql
#import settings
#import actiereg._basic.models as my
# from django.contrib.auth.models import User, Group
import datetime as dt
from config import DBLOC, USER

def getsql(con, cmd, item=None):
    """retrieval sql uitvoeren en resultaat teruggeven

    resultaat = []: query mislukt
    """
    print("getsql tweede argument: {0}".format(cmd))
    print("getsql derde  argument: {0}".format(item))
    if item is None:
        item = ()
    try:
        result = con.execute(cmd, item)
    except (sql.ProgrammingError, sql.OperationalError):
        raise
    return result

def doesql(con, cmd, item=None):
    """update sql uitvoeren en resultaat terugmelden

    resultaat == "" : alles ok - anders foutmelding
    """
    print("doesql tweede argument: {0}".format(cmd))
    print("doesql derde  argument: {0}".format(item))
    if item is None:
        item = ()
    err = ""
    try:
        con.execute(cmd, item)
    except (TypeError, ValueError, sql.IntegrityError,
            sql.ProgrammingError, sql.OperationalError) as msg:
        err = msg
    return err


# onderstaande definities zijn overgenomen uit dml.py voor de xml

kopdict = {
    "0": "Lijst",
    "1": "Titel/Status",
    "2": "Probleem/Wens",
    "3": "Oorzaak/Analyse",
    "4": "Oplossing",
    "5": "Vervolgactie",
    "6": "Voortgang"
}
statdict = {
    "0": ("gemeld", 0),
    "1": ("in behandeling", 1),
    "2": ("oplossing controleren",2),
    "3": ("nog niet opgelost",3),
    "4": ("afgehandeld", 4),
    "5": ("afgehandeld - vervolg",5)
}
catdict = {
    "P": ("probleem",1),
    "W": ("wens",2),
    "": ("onbekend",0),
    "V": ("vraag",3),
    "I": ("idee",4),
    "F": ("div. informatie",5)
}

def checkfile(naam, new=False):
    """Controleert of het opgegeven project al bestaat in de database

    Geeft True of False terug, tenzij het tweede argument de waarde True heeft
    In dat geval wordt (nog niet) een nieuw setje tabellen aangemaakt"""
    if new:
        # voeg tabellen toe conform bovenstaande dicts
        # zie ook newapp.py in de django versie
        return "Sorry, new = True is voorlopig nog even niet mogelijk"
    con = sql.connect(DBLOC)
    try:
        getsql(con, "select count(*) from {0}_actie".format(naam))
        r = True
    except sql.OperationalError:
        r = False
    con.close()
    return r

class DataError(Exception):
    """Eigen all-purpose exception - met de nieuwe dml misschien helemaal niet nodig"""
    pass

class Settings:
    """instellingen voor project ophalen

    argument = projectnaam, mag leeg zijn
    """
    def __init__(self, fnaam=""):
        self.kop = kopdict
        self.stat = statdict
        self.cat = catdict
        self.meld = ''
        if fnaam == "":
            self.meld = "Standaard waarden opgehaald"
            return
        self.naam = fnaam
        self.read()

    def read(self):
        "settings lezen"
        con = sql.connect(DBLOC)
        con.row_factory = sql.Row
        h = getsql(con,
            'select * from {0}_page order by "order"'.format(self.naam))
        if not h:
            self.meld = self.naam + " bestaat niet"
            self.exists = False
            return
        self.exists = True
        for y in h:
            self.kop[str(y["order"])] = y["title"]
        h = getsql(con, "select * from {0}_status" \
            " order by value".format(self.naam))
        for y in h:
            self.stat[str(y["value"])] = (y["title"], y["order"])
        h = getsql(con, "select * from {0}_soort" \
            " order by value".format(self.naam))
        for y in h:
            self.cat[y["value"]] = (y["title"], y["order"])
        con.close()

    def write(self):
        "settings terugschrijven"
        con = sql.connect(DBLOC)
        con.row_factory = sql.Row
        if not self.exists:
            # zouden in de nieuwe situatie drie settings tabellen voor moeten worden opgericht
            self.exists = True
        _pages = getsql(con,
            'select * from {0}_page order by "order"'.format(self.naam))
        rtn = 0
        for item in _pages:
            ix = str(item["order"])
            if self.kop[ix] != item["title"]:
                rtn = doesql(con, "update {0}_page set title = ?" \
                    ' where "order" = ?'.format(self.naam),
                    (self.kop[ix], ix))
        if rtn:
            con.rollback()
            con.close()
            raise DataError(rtn)
        namen = []
        max_id = 0
        _stats = getsql(con, "select * from {0}_status" \
            " order by value".format(self.naam))
        for item in _stats:
            if item["id"] > max_id:
                max_id = int(item["id"])
            ix = str(item["value"])
            if ix not in self.stat.keys():
                rtn = doesql(con, "delete from {0}_status" \
                    " where value = ?".format(self.naam),
                    (ix,))
            else:
                namen.append(ix)
                if self.stat[ix] != (item["title"], item["order"]):
                    rtn = doesql(con, 'update {0}_status set title = ?, "order" = ?' \
                        ' where value = ?'.format(self.naam),
                        (self.stat[ix][0], self.stat[ix][1], ix))
        ## print namen
        for key, value in self.stat.items():
            ## print key, value
            if key not in namen:
                max_id += 1
                rtn = doesql(con, 'insert into {0}_status (id, title, "order", value)' \
                    " values (?, ?, ?, ?)".format(self.naam),
                    (max_id, value[0], value[key][1], key))
        if rtn:
            con.rollback()
            con.close()
            raise DataError(rtn)
        namen = []
        max_id = 0
        _cats = getsql(con, "select * from {0}_soort" \
            " order by value".format(self.naam))
        for item in _cats:
            if item["id"] > max_id:
                max_id = item["id"]
            ix = item["value"]
            if ix not in self.cat.keys():
                rtn = doesql(con, "delete from {0}_soort" \
                    " where value = ?".format(self.naam),
                    (ix,))
            else:
                namen.append(ix)
                if self.cat[ix] != (item["title"], item["order"]):
                    rtn = doesql(con, 'update {0}_soort set title = ?, "order" = ?' \
                        " where value = ?".format(self.naam),
                        (self.cat[ix][0], self.cat[ix][1], ix))
        pp.pprint(self.cat.items())
        for key, value in self.cat.items():
            if key not in namen:
                max_id += 1
                rtn = doesql(con, 'insert into {0}_soort (id, title, "order", value)' \
                    " values (?, ?, ?, ?)".format(self.naam),
                    (max_id, value[0], value[1], key))
        if rtn:
            con.rollback()
            con.close()
            raise DataError(rtn)
        con.commit()
        con.close()

def get_acties(naam, select=None, arch=""):
    """selecteer acties; geef het resultaat terug of throw an exception

    selectie mogelijk op id (groter dan / kleiner dan), soort, status, (deel van) titel
    een selecteer-key mag een van de volgejde waarden zijn:
    "idlt" - in dat geval moet de waarde een string zijn waarmee vergeleken wordt,
    "idgt" - in dat geval moet de waarde een string zijn waarmee vergeleken wordt,
    "soort" - in dat geval moet de waarde een list zijn van mogelijke soorten,
    "status" - in dat geval moet de waarde een list zijn van mogelijke statussen,
    "titel" - in dat geval moet de waarde een string zijn die in de titel moet voorkomen
    eventueel wildcards:
        als de string niet begint met een * dan moet de titel ermee beginnen
        als de string niet eindigt met een * dan moet de titel ermee eindigen
        als er een * in zit moet wat ervoor zit en erna komt in de titel zitten
    """
    if select is None:
        select = {}
    if "id" in select:
        if "idlt" not in select or "idgt" not in select:
            raise DataError("Foutieve combinatie van selectie-argumenten opgegeven")
    sel = [""]
    args = []
    item = select.pop("idlt","")
    if item:
        sel[0] += "nummer < ?"
        args.append(item)
    enof = select.pop("id","")
    if enof:
        sel[0] = sel[0].join(("(", " {0} ".format(enof)))
    item = select.pop("idgt","")
    if item:
        sel[0] += "nummer > ?"
        if enof:
            sel[0] += ")"
        args.append(item)
    if sel == [""]:
        sel = []
    item = select.pop("soort","")
    if item:
        sel.append("soort_id = ?")
        args.append(item)
    item = select.pop("status" ,"")
    if item:
        sel.append("status_id = ?")
        args.append(item)
    item = select.pop("titel" ,"")
    if item:
        sel.append("(about like ? or {0}_actie.title like ?)".format(naam))
        args.append("%{0}%".format(item))
        args.append("%{0}%".format(item))
    if select:
        raise DataError("Foutief selectie-argument opgegeven")
    if arch == "":
        sel.append("arch = 0")
    elif arch == "arch":
        sel.append("arch = 1")
    elif arch != "alles":
        raise DataError("Foutieve waarde voor archief opgegeven " \
            "(moet niks, 'arch'  of 'alles' zijn)")
    con = sql.connect(DBLOC)
    ## print "dml_sql.get_acties.sel:",sel
    ## print "dml_sql.get_acties.args:",args
    cmd = "select nummer, start, {0}_status.title, {0}_status.value, {0}_soort.title, " \
        "{0}_soort.value, about, {0}_actie.title, gewijzigd from {0}_actie " \
        "join {0}_soort on {0}_soort.id = {0}_actie.soort_id " \
        "join {0}_status on {0}_status.id = {0}_actie.status_id ".format(naam)
    if sel:
        cmd += "where {0}".format(" and ".join(sel))
    data = getsql(con, cmd, args)
    if data:
        return data
    else:
        raise DataError(naam + " bestaat niet")

class Actie:
    """lijst alle gegevens van een bepaald item"""
    def __init__(self, naam, id_):
        self.meld = ''
        self.naam = naam
        self.id = id_
        self.new_data = [0, '', '', '', '', '0', '', False, '', '', '', '']
        nummer, self.datum, self.over, self.titel, \
            gewijzigd, self.status, self.soort, self.arch, \
            self.melding, self.oorzaak, self.oplossing, self.vervolg = self.new_data
        self.events = []
        self.exists = False
        self.con = sql.connect(DBLOC)
        self.con.row_factory = sql.Row
        if self.id in (0, "0"):
            self.nieuw()
        else:
            self.read()

    def nieuw(self):
        "nieuwe actie initialiseren"
        acties = getsql(self.con,
            "select id, nummer from {0}".format("{0}_actie".format(self.naam)))
        if not acties:
            raise DataError("datafile bestaat niet")
        nw_date = dt.datetime.now()
        for item in acties:
            last = item
            print(item)
        self.nieuw_id = last["id"] + 1
        ## print(self.nieuw_id)
        jaar, volgnr = last["nummer"].split("-", 1)
        nieuwnummer = int(volgnr) if int(jaar) == nw_date.year else 0
        nieuwnummer += 1
        self.id = "{0}-{1:04}".format(nw_date.year, nieuwnummer)
        self.datum = dt.datetime.today().isoformat(' ')[:19]

    def read(self):
        "gegevens lezen van een bepaalde actie"
        data = getsql(self.con,
            "select {0}_actie.id, nummer, start, about, {0}_actie.title, gewijzigd, " \
            "{0}_status.value, {0}_soort.value, arch, " \
            "melding, oorzaak, oplossing, vervolg from {0}_actie " \
            "join {0}_soort on {0}_soort.id = {0}_actie.soort_id " \
            "join {0}_status on {0}_status.id = {0}_actie.status_id " \
            "where nummer = ?".format(self.naam), (self.id,))
        ## for item in data:
            ## print(item)
        ## return
        if data:
            for item in data:
                actie, self.id, self.datum, self.over, self.titel, self.updated, \
                    self.status, self.soort, self.arch, self.melding, self.oorzaak, \
                    self.oplossing, self.vervolg = item
            self.titel = " - ".join((self.over, self.titel))
            print(self.status, self.soort, sep=" ")
        else:
            raise DataError(self.naam + " bestaat niet")
        data = getsql(self.con, "select id, start, starter_id, text from {0}_event " \
            "where actie_id = ?".format(self.naam), (actie,))
        for item in data:
            self.events.append((item[1],item[3]))
        self.exists = True

    def getStatusText(self, waarde):
        "geef tekst bij statuscode"
        if str(waarde) in statdict:
            return statdict[str(waarde)][0]
        else:
            raise DataError("Geen tekst gevonden bij statuscode")

    def getSoortText(self, waarde):
        "geef tekst bij soortcode"
        if waarde in catdict:
            return catdict[waarde][0]
        else:
            raise DataError("Geen tekst gevonden bij soortcode")

    def setStatus(self, waarde):
        "stel status in (code of tekst)"
        if type(waarde) is int:
            if str(waarde) in statdict:
                self.status = waarde
            else:
                raise DataError("Foutieve numerieke waarde voor status")
        elif type(waarde) is str:
            found = False
            for x, y in list(statdict.values()):
                if x == waarde:
                    found = True
                    self.status = x
                    break
            if not found:
                raise DataError("Foutieve tekstwaarde voor status")
        else:
            raise DataError("Foutief datatype voor status")

    def setSoort(self, waarde):
        "stel soort in (code of tekst)"
        if type(waarde) is str:
            if waarde in catdict:
                self.soort = waarde
            else:
                for x, y in list(catdict.items()):
                    if y[0] == waarde:
                        found = True
                        self.soort = x
                        break
                if not found:
                    raise DataError("Foutieve tekstwaarde voor categorie")
        else:
            raise DataError("Foutief datatype voor categorie")

    def setArch(self, waarde):
        "stel archiefstatus in"
        if type(waarde) is bool:
            self.arch = waarde
        else:
            raise DataError("Foutief datatype voor archiveren")

    def write(self):
        "actiegegevens (terug)schrijven"
        if self.exists:
            print("write: update actie {0}".format(self.id))
            data = getsql(self.con,
                "select nummer, start, about, title, gewijzigd, status_id, soort_id, " \
                "arch, melding, oorzaak, oplossing, vervolg, id from {0}_actie " \
                "where nummer = ?".format(self.naam), (self.id,))
            if data:
                for item in data:
                    print("write: item", item, sep=" ")
                    data = [x for x in item]
                    actie_id = data.pop()
                print("write: data", data, sep=" ")
            else:
                raise DataError("Current record not found")
        else:
            print("write: nieuwe actie {0}".format(self.id))
            actie_id = self.nieuw_id
            data = self.new_data
        update = []
        insert = []
        items = []
        self.over, self.titel = self.titel.split(" - ", 1)
        if not self.exists or self.over != data[2]:
            insert.append("about")
            update.append("about = ?")
            items.append(self.over)
        if not self.exists or self.titel != data[3]:
            insert.append("title")
            update.append("title = ?")
            items.append(self.titel)
        if not self.exists or self.status != data[5]:
            insert.append("status_id")
            update.append("status_id = ?")
            items.append(self.status)
        if not self.exists or self.soort != data[6]:
            insert.append("soort_id")
            update.append("soort_id = ?")
            items.append(self.soort)
        if not self.exists or self.arch != data[7]:
            insert.append("arch")
            update.append("arch = ?")
            items.append(self.arch)
        if not self.exists or self.melding != data[8]:
            insert.append("melding")
            update.append("melding = ?")
            items.append(self.melding)
        if not self.exists or self.oorzaak != data[9]:
            insert.append("oorzaak")
            update.append("oorzaak = ?")
            items.append(self.oorzaak)
        if not self.exists or self.oplossing != data[10]:
            insert.append("oplossing")
            update.append("oplossing = ?")
            items.append(self.oplossing)
        if not self.exists or self.vervolg != data[11]:
            insert.append("vervolg")
            update.append("vervolg = ?")
            items.append(self.vervolg)
        insert.append("gewijzigd")
        update.append("gewijzigd = ?")
        items.append(dt.datetime.today().isoformat(' ')[:10])
        if self.exists:
            items.append(self.id)
            print("write update:", insert, sep=" ")
            print("write update:", items, sep=" ")
            rtn = doesql(self.con, "update {0}_actie set {1} " \
                "where nummer = ?".format(self.naam, ", ".join(update)), items)
        else:
            insert = ["id", "nummer", "start", "starter_id", "lasteditor_id", \
                "behandelaar_id"] + insert
            mask = ", ".join(["?" for x in insert])
            items = [actie_id, self.id, self.datum, USER, USER, USER] + items
            print("write nieuw:", insert, sep=" ")
            print("write nieuw:", items, sep=" ")
            rtn = doesql(self.con, "insert into {0}_actie ({1}) " \
                "values ({2})".format(self.naam, ", ".join(insert), mask), items)
        if rtn:
            self.con.rollback()
            raise DataError(rtn)
        data = getsql(self.con, "select id, start, starter_id, text from {0}_event " \
                "where actie_id = ?".format(self.naam), (actie_id,))
        if not data:
            self.con.rollback()
            raise DataError("Problem getting events")
        current_events = [x for x in data]
        last_id = 0
        data = getsql(self.con, "select id from {0}_event ".format(self.naam))
        for item in data:
            last_id = item[0]
        for ix, item in enumerate(self.events):
            start, text = item
            if ix >= len(current_events):
                last_id = last_id + 1
                rtn = doesql(self.con, "insert into {0}_event (id, start, starter_id, " \
                    " text, actie_id) values(?, ?, ?, ?, ?)".format(self.naam),
                    (last_id, start, USER, text, actie_id))
            elif (start, text) != (current_events[ix][1], current_events[ix][3]):
                rtn = doesql(self.con, "update {0}_event set text = ? " \
                    "where start = ? and actie_id = ?".format(self.naam),(text, start, actie_id))
        if rtn:
            self.con.rollback()
            raise DataError(rtn)
        self.con.commit()
        self.exists = True

    def list(self):
        "actiegegevens uitlijsten naar print"
        print("%s %s gemeld op %s status %s %s" % (
            self.getSoortText(self.soort),
            self.id,
            self.datum,
            self.status,
            self.getStatusText(self.status)
            ))
        print("Titel:", self.titel, sep=" ")
        print("Melding:", self.melding, sep=" ")
        print("Oorzaak:", self.oorzaak, sep=" ")
        print("Oplossing:", self.oplossing, sep=" ")
        print("Vervolg:", self.vervolg, sep=" ")
        print("Verslag:")
        for x, y in self.events:
            print("\t {0} - {1}".format(x, y))
        if self.arch:
            print("Actie is gearchiveerd.")


def test_checkfile(fnaam):
    "test routine"
    h = checkfile(fnaam, False)
    print('checkfile "{0}", False: {1}'.format(fnaam, h))
    h = checkfile("gnarfl", False)
    print('checkfile "{0}", False: {1}'.format("gnarfl", h))
    h = checkfile(fnaam, True)
    print('checkfile "{0}", True: {1}'.format(fnaam, h))

def test_get_acties(fnaam):
    "test routine"
    ## h = get_acties(fnaam,{})
    ## h = get_acties(fnaam,{"idlt": "2010", })
    ## h = get_acties(fnaam,{"idlt": "2010",  "id": "and",  "idgt": "2007-0003"})
    ## h = get_acties(fnaam,{"idgt": "2010",  "id": "or",  "idlt": "2007-0003"})
    ## h = get_acties(fnaam,{"idgt": "2007-0003",})
    ## h = get_acties(fnaam,{"status": "1",  "soort" : "2",})
    h = get_acties(fnaam, {"titel": "en"})
    ## h = get_acties(fnaam,{}, "arch")
    ## h = get_acties(fnaam,{}, "alles")
    i = 0
    for item in h:
        i += 1
        print(item[0])
        pp.pprint(item)
    print("{0} records".format(i))

def test_Actie(fnaam):
    "test routine"
    ## p = Actie(fnaam, 0)
    p = Actie(fnaam, "2010-0002")
    p.status = 2
    p.setArch(True)
    p.melding = "Het is niet gebeurd"
    p.oorzaak = "Het leek maar alsof"
    p.oplossing = "Dus hebben we teruggedraaid wat we er aan gedaan hebben"
    p.vervolg = ""
    ## p.events.append((dt.datetime.today().isoformat(' ')[:19], "Actie opgevoerd"))
    ## p.events.append((dt.datetime.today().isoformat(' ')[:19], "Meldingtekst aangepast"))
    p.events.append((dt.datetime.today().isoformat(' ')[:19], "Actie gearchiveerd"))
    ## p.events.append((dt.datetime.today().isoformat(' ')[:19], "Actie heropend"))
    ## p.list()
    p.write()

def test_Settings(fnaam):
    "test routine"
    h = Settings(fnaam)
    ## h.stat['7'] = ("Gloekgloekgloe", 15)
    ## h.cat["X"] = ("Willen we niet weten", 6)
    ## h.kop['4'] = "Gargl"
    ## h.stat['7'] = ("Gloekgloekgloe", 7)
    ## h.cat["X"] = ("Ahum ahum", 7)
    ## h.kop['4'] = "Oplossing/SvZ"
    h.stat.pop('7')
    h.cat.pop("X")
    h.write()
    h = Settings(fnaam)
    pp.pprint(h.kop)
    pp.pprint(h.stat)
    pp.pprint(h.cat)

if __name__ == "__main__":
    fnm = "_basic"
    ## test_getsql()
    ## test_doesql()
    ## test_checkfile(fnm)
    ## test_get_acties(fnm)
    test_Actie(fnm)
    ## test_Settings(fnm)
