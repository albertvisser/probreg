# -*- coding: UTF-8 -*-
"data managenent statements"
from __future__ import print_function

import sys
import os
import pprint
import datetime as dt
from shutil import copyfile
from xml.etree.ElementTree import ElementTree, Element, SubElement
from config_xml import kopdict, statdict, catdict

datapad = os.getcwd()

class DataError(Exception):
    "Eigen all-purpose exception - maakt resultaat testen eenvoudiger"
    pass

def checkfile(fn, new=False):
    "controleer of projectbestand bestaat, maak indien aangegeven nieuwe aan"
    r = ''
    if new:
        root = Element("acties")
        s = SubElement(root,"settings")
        t = SubElement(s,"stats")
        for x, y in list(statdict.items()):
            u = SubElement(t, "stat", order=str(y[1]), value=x)
            u.text = y[0]
        t = SubElement(s,"cats")
        for x, y in list(catdict.items()):
            u = SubElement(t, "cat", order=str(y[1]), value=x)
            u.text = y[0]
        t = SubElement(s,"koppen")
        for x, y in list(kopdict.items()):
            u = SubElement(t, "kop", value=x)
            u.text = y
        ElementTree(root).write(fn)
    else:
        if not os.path.exists(fn):
            r = fn + " bestaat niet"
        else:
            tree = ElementTree(file=fn)
            if tree.getroot().tag != "acties":
                r = fn + " is geen bruikbaar xml bestand"
    return r

def get_nieuwetitel(fnaam, jaar=None):
    "bepaal nieuw uit te geven actienummer"
    if os.path.exists(fnaam):
        dnaam = fnaam
    elif os.path.exists(os.path.join(datapad, fnaam)):
        dnaam = os.path.join(datapad, fnaam)
    else:
        raise DataError("datafile bestaat niet")
    if jaar is None:
        jaar = str(dt.date.today().year)
    tree = ElementTree(file=dnaam)
    nummer = 0
    rt = tree.getroot()
    for x in rt.findall("actie"):
        t = x.get("id").split("-")
        if t[0] != jaar:
            continue
        if int(t[1]) > nummer:
            nummer = int(t[1])
    return "%s-%04i" % (jaar, nummer + 1)

def get_acties(fnaam, select=None, arch=""):
    """
    lijst alle items van een bepaald soort
    selectie meegeven mogelijk maken
    zoeken mogelijk op id (groter dan / kleiner dan), soort, status, (deel van) titel
    een selecteer-key mag een van de volgejde waarden zijn:
    "idlt" - in dat geval moet de waarde een string zijn waarmee vergeleken wordt,
    "idgt" - in dat geval moet de waarde een string zijn waarmee vergeleken wordt,
    "soort" - in dat geval moet de waarde een list zijn van mogelijke soorten,
    "status" - in dat geval moet de waarde een list zijn van mogelijke statussen,
    "titel" - in dat geval moet de waarde een string zijn die in de titel moet voorkomen
    eventueel wildcards:
        als de string niet begint met een * dan moet de titel ermee beginnen
        als de string niet eindigt met een * dan moet de titel ermee eindigen
        als er een * in zitmoet wat ervoor zit en erna komt in de titel zitten
     """
    if select is None:
        select = {}
        if not arch:
            return []
    lijst = []
    if len(select) > 0:
        keyfout = False
        for x in list(select.keys()):
            if x not in ("idlt", "id", "idgt", "soort", "status", "titel"):
                keyfout = True
                break
        if keyfout:
            raise DataError("Foutief selectie-argument opgegeven")
        if "id" in select:
            if "idlt" not in select and "idgt" not in select:
                raise DataError("Foutieve combinatie van selectie-argumenten opgegeven")
    if arch not in ("", "arch", "alles"):
        raise DataError("Foutieve waarde voor archief opgegeven " \
            "(moet niks, 'arch'  of 'alles' zijn)")
    sett = Settings(fnaam)
    if os.path.exists(fnaam):
        dnaam = fnaam
    elif os.path.exists(os.path.join(datapad, fnaam)):
        dnaam = os.path.join(datapad, fnaam)
    else:
        raise DataError("datafile bestaat niet")
    tree = ElementTree(file=dnaam)
    rt = tree.getroot()
    for x in rt.findall("actie"):
        a = x.get("arch")
        if a is None:
            if arch == "arch":
                continue
        else:
            if (a == "arch" and arch == "") or (a != "arch" and arch == "arch"):
                continue
        nr = x.get("id")
        if "id" in select and select["id"] == "or":
            if nr <= select["idgt"] and nr >= select["idlt"]:
                continue
        else:
            if ("idgt" in select and nr <= select["idgt"]) \
                or ("idlt" in select and nr >= select["idlt"]):
                continue
        ## alternatief en meer overeenkomend met de sql versie
        ## if 'id' in select:
            ## select_gt = select_lt = True
            ## if 'idgt' in select and nr <= select['idgt']:
                ## select_gt = False
            ## if 'idlt' in select and nr >= select['idlt']:
                ## select_lt = False
            ## if select['id'] == 'and' and (select_gt == False or select_lt == False):
                ## continue
            ## if select['id'] == 'or' and select_gt == False and select_lt == False:
                ## continue
        dd = x.get("datum")
        if dd is None:
            dd = ''
        lu = x.get("updated")
        if lu is None:
            lu = ""
        h = x.get("status")
        if "status" in select and h not in select["status"]:
            continue
        st = ''
        if h in list(sett.stat.keys()):
            st = sett.stat[h]
        h = x.get("soort")
        if h is None:
            h = ""
        if "soort" in select and h not in select["soort"]:
            continue
        ct = ''
        if h in list(sett.cat.keys()):
            ct = sett.cat[h]
        tl = x.find("titel").text
        if tl == None:
            tl = ""
        if "titel" in select and select["titel"].upper() not in tl.upper():
            continue
        lijst.append((nr, dd, st, ct, tl, lu))
    return lijst

class Settings:
    """
        argument = filenaam
        mag leeg zijn, moet eindingen op ".xml" (anders: DataError exception)
        de soorten hebben een numeriek id en alfanumerieke code
        de categorieen hebben een numeriek id en een numerieke code
        de id's bepalen de volgorde in de listboxen en de codes worden in de xml opgeslagen
    """
    def __init__(self, fnaam=""):
        self.kop = kopdict
        self.stat = statdict
        self.cat = catdict
        self.meld = ''
        if fnaam == "":
            self.meld = "Standaard waarden opgehaald"
            return
        if os.path.splitext(fnaam)[1] != ".xml":
            #~ print os.path.splitext(fnaam)[1]
            self.meld = "Geen xml-bestand opgegeven: " + fnaam
            raise DataError(self.meld)
        fn = os.path.split(fnaam)
        if fn[0] != "":
            self.fn = fnaam
            self.fnaam = fn[1]
        else:
            self.fn = os.path.join(datapad, fnaam) # naam van het xml bestand
            self.fnaam = fnaam
        self.fno = self.fn + ".old"     # naam van de backup van het xml bestand
        self.exists = False
        if os.path.exists(self.fn):
            self.exists = True
            self.read()

    def read(self):
        "settings lezen"
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()
        found = False # wordt niet gebruikt
        x = rt.find("settings")
        if x is not None:
            h = x.find("stats")
            if h is not None:
                self.stat = {}
                for y in h.findall("stat"):
                    self.stat[y.get("value")] = (y.text, y.get("order"))
            h = x.find("cats")
            if h is not None:
                self.cat = {}
                for y in h.findall("cat"):
                    self.cat[y.get("value")] = (y.text, y.get("order"))
            h = x.find("koppen")
            if h is not None:
                self.kop = {}
                for y in h.findall("kop"):
                    self.kop[y.get("value")] = y.text

    def write(self, srt=None): # extra argument ivm compat sql-versie
        "settings terugschrijven"
        if not self.exists:
            f = open(self.fn, "w")
            f.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<acties>\n</acties>\n')
            f.close()
            self.exists = True
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()
        el = rt.find("settings")
        if el is None:
            el = SubElement(rt,"settings")
        for x in list(el):
            if x.tag == "stats":
                el.remove(x)
            elif x.tag == "cats":
                el.remove(x)
            elif x.tag == "koppen":
                el.remove(x)
        h = SubElement(el,"stats")
        #~ print self.stat
        for x in list(self.stat.keys()):
            if x is int:
                x = str(x)
            j = SubElement(h, "stat", value=x)
            j.set("order", str(self.stat[x][1]))
            j.text = self.stat[x][0]
        h = SubElement(el,"cats")
        #~ print self.cat
        for x in list(self.cat.keys()):
            j = SubElement(h, "cat", value=x)
            j.set("order", str(self.cat[x][1]))
            j.text = self.cat[x][0]
        h = SubElement(el,"koppen")
        #~ print self.kop
        for x in list(self.kop.keys()):
            if x is int:
                x = str(x)
            j = SubElement(h, "kop", value=x)
            j.text = self.kop[x]
        copyfile(self.fn, self.fno)
        tree.write(self.fn)

    def set(self, naam, key=None, waarde=None):
        "settings warde instellen"
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
            if type(waarde) is not tuple:
                self.meld = 'Sleutelwaarde moet bestaan uit tekst en sortvolgnummer'
                raise DataError(self.meld)
            self.stat[key] = waarde
        elif naam == "cat":
            if type(waarde) is not tuple:
                self.meld = 'Sleutelwaarde moet bestaan uit tekst en sortvolgnummer'
                raise DataError(self.meld)
            self.cat[key] = waarde
        elif naam == "kop":
            if type(waarde) is not str:
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
                if type(key) is int:
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
                if type(key) is int:
                    key = str(key)
                if key not in self.kop:
                    self.meld = 'Sleutel bestaat niet voor kop'
                    raise DataError(self.meld)
                return self.kop[key]

class Actie:
    """lijst alle gegevens van een bepaald item"""
    def __init__(self, fnaam, _id):
        self.meld = ''
        if os.path.splitext(fnaam)[1] != ".xml":
            #~ print os.path.splitext(fnaam)[1]
            self.meld = "Geen xml-bestand opgegeven: " + fnaam
            raise DataError(self.meld)
        fn = os.path.split(fnaam)
        if fn[0] != "":
            self.fn = fnaam
            self.fnaam = fn[1]
        else:
            self.fn = os.path.join(datapad, fnaam) # naam van het xml bestand
            self.fnaam = fnaam
        self.settings = Settings(fnaam)
        self.id = _id
        self.datum = ''
        self.status = '0'
        self.soort = ''
        self.arch = False
        self.titel = ''
        self.melding = ''
        self.oorzaak = ''
        self.oplossing  = ''
        self.vervolg = ''
        self.stand = ''
        self.events = []
        self.fno = self.fn + ".old"     # naam van de backup van het xml bestand
        self.exists = False
        if os.path.exists(self.fn):
            pass
        elif _id == 0 or _id == "0":
            self.nieuwfile()
        if _id == 0 or _id == "0":
            self.nieuw()
        else:
            self.read()

    def nieuw(self):
        "nieuwe actie initialiseren"
        self.id = get_nieuwetitel(self.fn)
        self.datum = dt.datetime.today().isoformat(' ')[:19]

    def nieuwfile(self):
        "nieuw projectbestand aanmaken"
        f = open(self.fn, "w")
        f.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<acties>\n</acties>\n')
        f.close()

    def read(self):
        "gegevens lezen van een bepaalde actie"
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()
        found = False
        for x in rt.findall("actie"):
            if x.get("id") == self.id:
                found = True
                break
        if found:
            h = x.get("datum")
            if h is not None:
                self.datum = h
            self.status = x.get("status")
            try:
                self.soort = x.get("soort")
            except:
                pass
            h = x.get("arch")
            if h is not None:
                if h == "arch":
                    self.arch = True
            h = x.get("updated")
            if h is not None:
                self.updated = h
            else:
                self.updated = dt.datetime.today().isoformat(' ')[:19]
            for y in list(x):
                if y.tag == "titel":
                    if y.text is not None:
                        self.titel = y.text
                elif y.tag == "melding":
                    if y.text is not None:
                        self.melding = y.text
                elif y.tag == "oorzaak":
                    if y.text is not None:
                        self.oorzaak = y.text
                elif y.tag == "oplossing":
                    if y.text is not None:
                        self.oplossing = y.text
                elif y.tag == "vervolg":
                    if y.text is not None:
                        self.vervolg = y.text
                elif y.tag == "stand":
                    if y.text is not None:
                        self.stand = y.text
                elif y.tag == "events":
                    self.events = []
                    for z in list(y):
                        self.events.append((z.get("id"), z.text))
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

    def set_soort(self, waarde):
        "stel soort in (code of tekst)"
        print(waarde)
        if type(waarde) is str:
            if waarde in catdict:
                self.soort = waarde
            else:
                found = False
                for x, y in list(catdict.items()):
                    print(y)
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
        if type(waarde) is bool:
            self.arch = waarde
        else:
            raise DataError("Foutief datatype voor archiveren")

    def write(self):
        "actiegegevens terugschrijven"
        if os.path.exists(self.fn):
            tree = ElementTree(file=self.fn)
            rt = tree.getroot()
        else:
            rt = Element("acties")
        if not self.exists:
            x = SubElement(rt, "actie")
            x.set("id", self.id)
            x.set("datum", self.datum)
            found = True
        else:
            for x in rt.findall("actie"):
                if x.get("id") == self.id:
                    found = True
                    break
        if found:
            x.set("updated", dt.datetime.today().isoformat(' ')[:10])
            h = self.soort
            if h is None:
                self.soort = ""
            x.set("soort", self.soort)
            x.set("status", self.status)
            if self.arch:
                x.set("arch", "arch")
            else:
                h = x.get("arch")
                if h is not None:
                    x.set("arch", "herl")
            h = x.find("titel")
            if h is None:
                h = SubElement(x, "titel")
            h.text = self.titel
            h = x.find("melding")
            if h is None:
                h = SubElement(x, "melding")
            h.text = self.melding
            h = x.find("oorzaak")
            if h is None:
                h = SubElement(x, "oorzaak")
            h.text = self.oorzaak
            h = x.find("oplossing")
            if h is None:
                h = SubElement(x, "oplossing")
            h.text = self.oplossing
            h = x.find("vervolg")
            if h is None:
                h = SubElement(x, "vervolg")
            h.text = self.vervolg
            h = x.find("stand")
            if h is None:
                h = SubElement(x, "stand")
            h.text = self.stand
            h = x.find("events")
            if h is not None:
                x.remove(h)
            h = SubElement(x, "events") # maakt dit een bestaande "leeg" ?
            for y, z in self.events:
                q = SubElement(h, "event", id=y)
                q.text = z
            tree = ElementTree(rt)
            copyfile(self.fn, self.fno)
            tree.write(self.fn)
            self.exists = True
        else:
            return False

    def list(self):
        "actie uitlijsten naar print"
        print("%s %s gemeld op %s status %s %s" % (
            self.get_soorttext(),
            self.id,
            self.datum,
            self.status,
            self.get_statustext()
            ))
        print("Titel:", self.titel, sep=" ")
        print("Melding:", self.melding, sep=" ")
        print("Oorzaak:", self.oorzaak, sep=" ")
        print("Oplossing:", self.oplossing, sep=" ")
        print("Vervolg:", self.vervolg, sep=" ")
        print("Stand:", self.stand, sep=" ")
        print("Verslag:")
        for x, y in self.events:
            print("   {0} - {1}".format(x, y))
        if self.arch:
            print("Actie is gearchiveerd.")
