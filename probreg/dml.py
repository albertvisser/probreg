# -*- coding: UTF-8 -*-
"""data managenent statements
bevat dml voor werken met xml files en dml voor werken met sql
in het laatste geval wordt dezelfde data gebruikt die de Django versie gebruikt

het aanroepende programma (probreg_qt.py in dit geval) is hier nog niet op aangepast
en ik weet ook niet of het slim is om dat te doen omdat je dan overal verschil
moet gaan maken in plaats van klassen te gebruiken met dezelfde namen maar
verschillend gedrag
of misschien was dit wel de versie waar alles in stond voordat ik besloot om het
op een slimmere manier apart neer te zetten?
"""
from __future__ import print_function

import sys
import os
import pprint
import datetime as dt
import shutil
from xml.etree.ElementTree import ElementTree, Element, SubElement
import sqlite3 as sql
import config

datapad = os.getcwd()


class DataError(Exception):
    "Eigen all-purpose exception - maakt resultaat testen eenvoudiger"
    pass


def getsql(con, cmd, item=None):
    """retrieval sql uitvoeren en resultaat teruggeven

    resultaat = []: query mislukt
    """
    ## print("getsql tweede argument: {0}".format(cmd))
    ## print("getsql derde  argument: {0}".format(item))
    if item is None:
        item = ()
    try:
        result = [x for x in con.execute(cmd, item)]
    except (sql.ProgrammingError, sql.OperationalError) as err:
        raise DataError(str(err))
    return result


def doesql(con, cmd, item=None):
    """update sql uitvoeren en resultaat terugmelden

    resultaat == "" : alles ok - anders foutmelding
    """
    ## print("doesql tweede argument: {0}".format(cmd))
    ## print("doesql derde  argument: {0}".format(item))
    if item is None:
        item = ()
    err = ""
    try:
        con.execute(cmd, item)
    except (TypeError, ValueError, sql.IntegrityError,
            sql.ProgrammingError, sql.OperationalError) as msg:
        err = str(msg)
    return err


def complete_ids(dic):
    """ids genereren voor items met id = -1

    input is een dictionary van 3-tuples (naam, volgorde, id)
    elementen met een id van -1 krijgen in plaats van deze een passende waarde
    (eerstvolgend hogere id)
    """
    oldkeys, newkeys = [], []
    for key, value in dic.items():
        if len(value) < 3 or value[2] == -1:
            newkeys.append(key)
        else:
            oldkeys.append((value[2], key))
    if oldkeys:
        oldkeys.sort()
        last_id = int(oldkeys[-1][0])
    else:
        last_id = 0
    for key in newkeys:
        last_id += 1
        dic[key] = (dic[key][0], dic[key][1], last_id)


def checkfile(fn, new=False):
    "controleer of projectbestand bestaat, maak indien aangegeven nieuwe aan"
    message = ''
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
            message = fn + " bestaat niet"
        else:
            tree = ElementTree(file=fn)
            if tree.getroot().tag != "acties":
                message = fn + " is geen bruikbaar xml bestand"
    return message


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


def get_acties_xml(fnaam, select=None, arch=""):
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
                raise DataError("Foutieve combinatie van selectie-argumenten "
                    "opgegeven")
    if arch not in ("", "arch", "alles"):
        raise DataError("Foutieve waarde voor archief opgegeven "
            "(moet niks, 'arch'  of 'alles' zijn)")
    sett = XmlSettings(fnaam)
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
        if select.get("id", '') == "or":
            if nr <= select["idgt"] and nr >= select["idlt"]:
                continue
        else:
            if ("idgt" in select and nr <= select["idgt"]) \
                or ("idlt" in select and nr >= select["idlt"]):
                continue
        dd = x.get("datum")
        if dd is None:
            dd = ''
        lu = x.get("updated")
        if lu is None:
            lu = ""
        h = x.get("status")
        if h not in select.get("status", [h]):
            continue
        st = ''
        if h in list(sett.stat.keys()):
            st = sett.stat[h]
        h = x.get("soort")
        if h is None:
            h = ""
        if h not in select.get("soort", [h]):
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


class XmlSettings:
    """
        argument = filenaam
        mag leeg zijn, moet eindingen op ".xml" (anders: DataError exception)
        de soorten hebben een numeriek id en alfanumerieke code
        de categorieen hebben een numeriek id en een numerieke code
        de id's bepalen de volgorde in de listboxen en de codes worden in de xml opgeslagen
    """
    def __init__(self, fnaam=""):
        self.kop = config.kopdict_xml
        self.stat = config.statdict_xml
        self.cat = config.catdict_xml
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
        for x in self.stat.keys():
            if x is int:
                x = str(x)
            j = SubElement(h, "stat", value=x)
            j.set("order", str(self.stat[x][1]))
            j.text = self.stat[x][0]
        h = SubElement(el,"cats")
        #~ print self.cat
        for x in self.cat.keys():
            j = SubElement(h, "cat", value=x)
            j.set("order", str(self.cat[x][1]))
            j.text = self.cat[x][0]
        h = SubElement(el,"koppen")
        #~ print self.kop
        for x in self.kop.keys():
            if x is int:
                x = str(x)
            j = SubElement(h, "kop", value=x)
            j.text = self.kop[x]
        shutil.copyfile(self.fn, self.fno)
        tree.write(self.fn)

    def set(self, naam, key=None, waarde=None):
        "settings waarde instellen"
        meld = ''
        if naam not in ("stat", "cat", "kop"):
            meld = 'Foutieve soort opgegeven'
        elif key is None:
            meld = 'Geen sleutel opgegeven'
        elif waarde is None:
            meld = 'Geen waarde voor sleutel opgegeven'
        elif naam == "stat":
            if isinstance(waarde, tuple) and len(waarde) == 2:
                self.stat[key] = waarde
            else:
                meld = 'Sleutelwaarde moet bestaan uit tekst en sortvolgnummer'
        elif naam == "cat":
            if isinstance(waarde, tuple) and len(waarde) == 2:
                self.cat[key] = waarde
            else:
                meld = 'Sleutelwaarde moet bestaan uit tekst en sortvolgnummer'
        elif naam == "kop":
            if isinstance(waarde, str):
                self.kop[key] = waarde
            else:
                meld = 'Sleutelwaarde moet bestaan uit alleen tekst'
        if meld:
            raise DataError(meld)

    def get(self, naam, key=None):
        "settings waarde lezen"
        meld = ''
        if naam not in ("stat", "cat", "kop"):
            meld = 'Foutieve soort opgegeven'
        elif naam == "stat":
            if key is None:
                retval = self.stat
            else:
                if isinstance(key, int):
                    key = str(key)
                if key in self.stat:
                    retval = self.stat[key]
                meld = 'Sleutel bestaat niet voor status'
        elif naam == "cat":
            if key is None:
                retval = self.cat
            else:
                if key in self.cat:
                    retval = self.cat[key]
                meld = 'Sleutel bestaat niet voor soort'
        elif naam == "kop":
            if key is None:
                retval = self.kop
            else:
                if isinstance(key, int):
                    key = str(key)
                if key in self.kop:
                    retval = self.kop[key]
                meld = 'Sleutel bestaat niet voor kop'
        if meld:
            raise DataError(meld)
        return retval


class XmlActie:
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
        self.settings = XmlSettings(fnaam)
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

    def get_statustext(self, waarde=None):
        "geef tekst bij statuscode"
        if waarde is None:
            waarde = self.status[0]
        ## if str(waarde) in statdict:
        try:
            return self.settings.stat[str(waarde)][0]
        ## else:
        except KeyError:
            raise DataError("Geen tekst gevonden bij statuscode {}".format(waarde))

    def get_soorttext(self, waarde=None):
        "geef tekst bij soortcode"
        if waarde is None:
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
            if str(waarde) in config.statdict_xml:
                self.status = waarde
            else:
                raise DataError("Foutieve numerieke waarde voor status")
        elif isinstance(waarde, str):
            found = False
            for x, y in list(config.statdict_xml.values()):
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
        if isinstance(waarde, str):
            if waarde in config.catdict_xml:
                self.soort = waarde
            else:
                found = False
                for x, y in list(config.catdict_xml.items()):
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
        if isinstance(waarde, bool):
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
            shutil.copyfile(self.fn, self.fno)
            tree.write(self.fn)
            self.exists = True
        else:
            return False

    def list(self, _out=sys.stdout):
        "actie uitlijsten naar stream"
        print("%s %s gemeld op %s status %s %s" % (
            self.get_soorttext(self.soort),
            self.id,
            self.datum,
            self.status,
            self.get_statustext(self.status)
            ), file=_out)
        print("Titel:", self.titel, sep=" ", file=_out)
        print("Melding:", self.melding, sep=" ", file=_out)
        print("Oorzaak:", self.oorzaak, sep=" ", file=_out)
        print("Oplossing:", self.oplossing, sep=" ", file=_out)
        print("Vervolg:", self.vervolg, sep=" ", file=_out)
        print("Stand:", self.stand, sep=" ", file=_out)
        print("Verslag:", file=_out)
        for x, y in self.events:
            print("   {0} - {1}".format(x, y), file=_out)
        if self.arch:
            print("Actie is gearchiveerd.", file=_out)


def get_acties_sql(naam, select=None, arch=""):
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
        if not arch:
            return
    if "id" in select:
        if "idlt" not in select and "idgt" not in select:
            raise DataError("Foutieve combinatie van selectie-argumenten opgegeven")
    sel = [""]
    args = []
    item_lt = select.pop("idlt","")
    enof = select.pop("id","")
    item_gt = select.pop("idgt","")
    if item_gt:
        sel[0] += "nummer > ?"
        if item_lt:
            sel[0] = "({} {} ".format(sel[0], enof)
        args.append(item_gt)
    if item_lt:
        sel[0] += "nummer < ?"
        args.append(item_lt)
        if item_gt:
            sel[0] += ")"
    if sel == [""]:
        sel = []
    item = select.pop("soort","")
    if item:
        print(item)
        if len(item) == 1:
            sel.append("soort_id = ?")
            args.append(item[0])
        else:
            append_to_sel = "soort_id in ("
            for value in item[:-1]:
                append_to_sel += "?,"
                args.append(value)
            sel.append(append_to_sel + '?)')
            args.append(item[-1])
    item = select.pop("status" ,"")
    if item:
        print(item)
        if len(item) == 1:
            sel.append("status_id = ?")
            args.append(item[0])
        else:
            append_to_sel = "status_id in ("
            for value in item[:-1]:
                append_to_sel += "?,"
                args.append(value)
            sel.append(append_to_sel + '?)')
            args.append(item[-1])
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
    con = sql.connect(config.DBLOC)
    ## print "dml_sql.get_acties.sel:",sel
    ## print "dml_sql.get_acties.args:",args
    cmd = "select nummer, start, {0}_status.title, {0}_status.value, {0}_soort.title, " \
        "{0}_soort.value, about, {0}_actie.title, gewijzigd from {0}_actie " \
        "join {0}_soort on {0}_soort.id = {0}_actie.soort_id " \
        "join {0}_status on {0}_status.id = {0}_actie.status_id ".format(naam)
    if sel:
        cmd += "where {0}".format(" and ".join(sel))
    data = getsql(con, cmd, args)
    if data or len(data) == 0:
        return data
    else:
        raise DataError(naam + " bestaat niet")


class SqlSettings:
    """instellingen voor project

    buffer tussen programma en database
    self.kop is een dict met volgnummer als key en titel en link als waarde
    self.stat is een dict met code als key en titel, volgorde en record-id
        als waarde
    self.cat idem
    de get methoden zijn voor het gemak
    wijzigen doe je maar direct in de attributen (properties van maken?)
    """
    def __init__(self, fnaam=""):
        self.kop = config.kopdict_sql
        self.stat = config.statdict_sql
        self.cat = config.catdict_sql
        self.meld = ''
        if fnaam == "":
            self.meld = "Standaard waarden opgehaald"
            return
        self.naam = fnaam
        self.read()

# connection als context manager
## def connect_db():
    ## return sql.connect(DATABASE)

    ## with closing(connect_db()) as db:
        ## db.row_factory = sql.Row
        ## cur = db.cursor()

    def read(self):
        "settings lezen"
        con = sql.connect(config.DBLOC)
        con.row_factory = sql.Row
        try:
            data = getsql(con,
                'select * from {0}_page order by "order"'.format(self.naam))
        except DataError as err:
            self.meld = "{} bestaat niet ({})".format(self.naam, err)
            self.exists = False
            con.close()
            return
        self.exists = True
        self.kop = {}
        for row in data:
            self.kop[str(row["order"])] = (row["title"], row["link"])

        try:
            data = getsql(con, "select * from {0}_status".format(self.naam))
        except DataError as err:
            self.meld = "Er is iets misgegaan ({})".format(self.naam, err)
            con.close()
            return
        self.stat = {}
        for row in data:
            self.stat[str(row["value"])] = (row["title"], row["order"], row["id"])

        try:
            data = getsql(con, "select * from {0}_soort".format(self.naam))
        except DataError as err:
            self.meld = "Er is iets misgegaan ({})".format(self.naam, err)
            con.close()
            return
        self.cat = {}
        for row in data:
            self.cat[row["value"]] = (row["title"], row["order"], row["id"])

        con.close()

    def write(self, srt):
        "settings terugschrijven"
        con = sql.connect(config.DBLOC)
        con.row_factory = sql.Row

        if self.exists:
            if srt == 'kop':
                _pages = getsql(con,
                    'select * from {0}_page order by "order"'.format(self.naam))
                rtn = 0
                for item in _pages:
                    idx = str(item["order"])
                    if self.kop[idx] != (item["title"], item["link"]):
                        rtn = doesql(con, "update {0}_page set title = ?,"
                            ' link = ? where "order" = ?'.format(self.naam),
                            (self.kop[idx], item['link'], idx))
                        if rtn:
                            break
            elif srt == 'stat':
                rtn = doesql(con, 'delete from {0}_status'.format(self.naam), None)
                if not rtn:
                    complete_ids(self.stat)
                    for key, value in self.stat.items():
                        rtn = doesql(con, 'insert into {0}_status (id, value, '
                            'title, "order") values (?, ?, ?, ?)'.format(self.naam),
                            (value[2], key, value[0], value[1]))
                        if rtn:
                            break
            elif srt == 'cat':
                rtn = doesql(con, "delete from {0}_soort".format(self.naam), None)
                if not rtn:
                    complete_ids(self.cat)
                    for key, value in self.cat.items():
                        rtn = doesql(con, 'insert into {0}_soort (id, value, '
                            'title, "order") values (?, ?, ?, ?)'.format(self.naam),
                            (value[2], key, value[0], value[1]))
        else:
            if srt == 'kop':
                for order, item in self.kop:
                    rtn = doesql(con, "insert into {0}_page values"
                        ' (?,?,?,?)'.format(self.naam), (order +  1, item[0], item[1],
                        order))
                    if rtn:
                        break

        if rtn:
            con.rollback()
            con.close()
            raise DataError(rtn)

        con.commit()
        con.close()

    def get_statusid(self, waarde):
        print(waarde, type(waarde), sep=" ")
        for code, value in self.stat.items():
            print(code, type(code), value, sep=" ")
            text, sortkey, row_id = value
            ## if int(waarde) == key or str(waarde) == key or waarde == value[0]:
            if waarde == code or waarde == text:
                return row_id
        raise DataError("geen status bij code of omschrijving '{}' gevonden".format(
            waarde))


    def get_soortid(self, waarde):
        for code, value in self.cat.items():
            text, sortkey, row_id = value
            if waarde == code or waarde == text:
                return row_id
        raise DataError("geen soort bij code of omschrijving '{}' gevonden".format(
            waarde))

    def get_statustext(self, waarde):
        "geef tekst bij statuscode of -id"
        try:
            return self.stat[waarde][0]
        except KeyError:
            pass
        for text, sortkey, row_id in self.stat.values():
            if waarde == sortkey or waarde == row_id:
                return text
        raise DataError("Geen omschrijving gevonden bij statuscode of -id '{}'".format(
            waarde))

    def get_soorttext(self, waarde):
        "geef tekst bij soortcode of -id"
        try:
            return self.cat[waarde][0]
        except KeyError:
            pass
        for text, sortkey, row_id in self.cat.values():
            if waarde == sortkey or waarde == row_id:
                return text
        raise DataError("Geen omschrijving gevonden bij soortcode of -id '{}'".format(
            waarde))


class SqlActie:
    """lijst alle gegevens van een bepaald item"""
    def __init__(self, naam, id_):
        self.meld = ''
        self.naam = naam
        self.settings = SqlSettings(naam)
        self.id = id_
        new_data = ['', '', '', 1, 1, False, '', '', '', '']
        (self.over, self.titel, self.gewijzigd, self.status, self.soort, self.arch,
            self.melding, self.oorzaak, self.oplossing, self.vervolg) = new_data
        self.events = []
        self.exists = False
        self.con = sql.connect(config.DBLOC)
        self.con.row_factory = sql.Row
        if self.id in (0, "0"):
            self.nieuw()
        else:
            self.read()

    def nieuw(self):
        "nieuwe actie initialiseren"
        try:
            acties = getsql(self.con,
                "select id, nummer from {0}".format("{0}_actie".format(self.naam)))
        except DataError as err:
            raise DataError("datafile bestaat niet ({})".format(str(err)))
        nw_date = dt.datetime.now()
        ## for item in acties:
            ## last = item
        last = acties[-1]
        self.nieuw_id = last["id"] + 1
        ## print(self.nieuw_id)
        jaar, volgnr = last["nummer"].split("-", 1)
        nieuwnummer = int(volgnr) + 1 if int(jaar) == nw_date.year else 1
        self.id = "{0}-{1:04}".format(nw_date.year, nieuwnummer)
        self.status = self.soort = 1
        self.datum = dt.datetime.today().isoformat(' ') # [:19]
        self.events.append((self.datum, "Actie opgevoerd"))

    def read(self):
        "gegevens lezen van een bepaalde actie"
        data = getsql(self.con,
            "select {0}_actie.id, nummer, start, about, {0}_actie.title,"
            " gewijzigd, {0}_status.value, {0}_soort.value, arch,"
            " melding, oorzaak, oplossing, vervolg from {0}_actie"
            " join {0}_soort on {0}_soort.id = {0}_actie.soort_id"
            " join {0}_status on {0}_status.id = {0}_actie.status_id"
            " where nummer = ?".format(self.naam), (self.id,))
        ## for item in data:
            ## print(item)
        ## return
        if len(data) == 0:
            self.exists = False
            return
        elif not data:
            raise DataError(self.naam + " bestaat niet")
        for item in data:
            print(item)
            (actie, self.id, self.datum, self.over, self.titel, self.updated,
                self.status, self.soort, self.arch, self.melding, self.oorzaak,
                self.oplossing, self.vervolg) = item
            # string van maken omdat het door sqlite  blijkbaar als int wordet geretourneerd:
            self.status = str(self.status)
            ## self.titel = " - ".join((self.over, self.titel))
        data = getsql(self.con, "select id, start, starter_id, text from"
            " {0}_event where actie_id = ?".format(self.naam), (actie,))
        for item in data:
            self.events.append((item[1], item[3]))
        self.exists = True

    def get_statustext(self):
        "geef tekst bij statuscode"
        print(self.status)
        return self.settings.get_statustext(self.status)

    def get_soorttext(self):
        "geef tekst bij soortcode"
        return self.settings.get_soorttext(self.soort)

    def set_status(self, waarde):
        "stel status in (code of tekst) met controle a.h.v. project settings"
        self.status = self.settings.get_statusid(waarde)
        print(waarde, self.status, sep = " ")
        self.events.append((dt.datetime.today().isoformat(' '), # [:19],
            'status gewijzigd in "{0}"'.format(self.get_statustext())))

    def set_soort(self, waarde):
        "stel soort in (code of tekst) met controle a.h.v. project settings"
        self.soort = self.settings.get_soortid(waarde)
        print(waarde, self.soort, sep = " ")
        self.events.append((dt.datetime.today().isoformat(' '), # [:19],
            'soort gewijzigd in "{0}"'.format(self.get_soorttext())))

    def set_arch(self, waarde):
        "stel archiefstatus in - garandeert dat dat een boolean waarde wordt"
        if waarde:
            self.arch = True
            self.events.append((dt.datetime.today().isoformat(' '), # [:19],
                "Actie gearchiveerd"))
        else:
            self.arch = False
            self.events.append((dt.datetime.today().isoformat(' '), # [:19],
                "Actie herleefd"))

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
            # FIXME: dit wordt niet altijd aangeroepen volgend op self.nieuw() waarin nieuw_id wordt ingesteld
            print("write: nieuwe actie {0}".format(self.nieuw_id))
            actie_id = self.nieuw_id
            ## data = self.new_data
        update = []
        insert = []
        items = []
        ## self.over, self.titel = self.titel.split(" - ", 1)
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
            items.append(self.settings.get_statusid(self.status))
        if not self.exists or self.soort != data[6]:
            insert.append("soort_id")
            update.append("soort_id = ?")
            items.append(self.settings.get_soortid(self.soort))
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
        items.append(dt.datetime.today().isoformat(' ')) # [:19])
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
            items = [self.nieuw_id, self.id, self.datum, USER, USER, USER] + items
            print("write nieuw:", insert, sep=" ")
            print("write nieuw:", items, sep=" ")
            rtn = doesql(self.con, "insert into {0}_actie ({1}) " \
                "values ({2})".format(self.naam, ", ".join(insert), mask), items)
        if rtn:
            self.con.rollback()
            raise DataError(str(rtn))
        data = getsql(self.con, "select id, start, starter_id, text from {0}_event " \
                "where actie_id = ?".format(self.naam), (actie_id,))
        ## if not data:
            ## self.con.rollback()
            ## raise DataError("Problem getting events")
        current_events = [x for x in data] if data else []
        last_id = 0
        data = getsql(self.con, "select id from {0}_event ".format(self.naam))
        for item in data:
            last_id = item[0]
        for idx, item in enumerate(self.events):
            start, text = item
            if idx >= len(current_events):
                last_id = last_id + 1
                rtn = doesql(self.con, "insert into {0}_event (id, start, starter_id,"
                    " text, actie_id) values(?, ?, ?, ?, ?)".format(self.naam),
                    (last_id, start, USER, text, actie_id))
            elif (start, text) != (current_events[idx][1], current_events[idx][3]):
                rtn = doesql(self.con, "update {0}_event set text = ? " \
                    "where start = ? and actie_id = ?".format(self.naam),(text, start, actie_id))
        if rtn:
            self.con.rollback()
            raise DataError(rtn)
        self.con.commit()
        self.exists = True

    def list(self, _out=sys.stdout):
        "actiegegevens uitlijsten naar print"
        print("%s %s gemeld op %s status %s %s" % (
            self.get_soorttext(),
            self.id,
            self.datum,
            self.status,
            self.get_statustext()
            ), file=_out)
        print("Titel: {} - {}".format(self.over, self.titel), file=_out)
        print("Melding:", self.melding, sep=" ", file=_out)
        print("Oorzaak:", self.oorzaak, sep=" ", file=_out)
        print("Oplossing:", self.oplossing, sep=" ", file=_out)
        print("Vervolg:", self.vervolg, sep=" ", file=_out)
        print("Verslag:", file=_out)
        for date, text in self.events:
            print("\t {0} - {1}".format(date, text), file=_out)
        if self.arch:
            print("Actie is gearchiveerd.", file=_out)


def get_config_objects(sql=True):
    """geef de voor sql dan wel xml mode toepasselijke symbolen terug
    als dictionary waarden zodat deze makkelijk aan globals() kunnen worden
    toegevoegd.
    """
    retval = {"DataError": DataError}
    if sql:
        retval["get_acties"] = get_acties_sql
        retval["Settings"] = SqlSettings
        retval["Actie"] = SqlActie
        retval["APPS"] = config.APPS
    else:
        retval["get_acties"] = get_acties_xml
        retval["Settings"] = XmlSettings
        retval["Actie"] = XmlActie
        retval["checkfile"] = checkfile
    return retval
