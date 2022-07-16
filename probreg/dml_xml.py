"data managenent voor ProbReg XML versie"
## import sys
import os
import pathlib
import base64  # gzip
import datetime as dt
from shutil import copyfile
from xml.etree.ElementTree import ElementTree, Element, SubElement
import logging
# ingekopieerd vanwege circular import:
# from probreg.shared import DataError, kopdict, statdict, catdict

datapad = os.getcwd()
dtformat = '%d-%m-%Y %H:%I:%S'  # zelfde als in shared.get_dts()


kopdict = {
    "0": ("Lijst", 'index'),
    "1": ("Titel/Status", 'detail'),
    "2": ("Probleem/Wens", 'meld'),
    "3": ("Oorzaak/Analyse", 'oorz'),
    "4": ("Oplossing/SvZ", 'opl'),
    "5": ("Vervolgactie", 'verv'),
    "6": ("Voortgang", 'voortg')
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
    meld = ''
    if not fnaam:
        return None, '', False, 'Please provide a filename'
    if fnaam.suffix != ".xml":
        meld = "Filename incorrect (must end in .xml)"
    if fnaam.parent != "":
        fn, fnaam = fnaam, fnaam.name
    else:
        fn = pathlib.Path('') / fnaam
    return fn, fnaam, fn.exists(), meld


def checkfile(fn, new=False):
    "controleer of projectbestand bestaat, maak indien aangegeven nieuwe aan"
    r = ''
    fnaam = str(fn)
    if new:
        root = Element("acties")
        s = SubElement(root, "settings", imagecount="0")
        t = SubElement(s, "stats")
        for x, y in list(statdict.items()):
            u = SubElement(t, "stat", order=str(y[1]), value=x)
            u.text = y[0]
        t = SubElement(s, "cats")
        for x, y in list(catdict.items()):
            u = SubElement(t, "cat", order=str(y[1]), value=x)
            u.text = y[0]
        t = SubElement(s, "koppen")
        for x, y in list(kopdict.items()):
            u = SubElement(t, "kop", value=x)
            u.text = y[0]
        ElementTree(root).write(fnaam, encoding='utf-8', xml_declaration=True)
    else:
        if not fn.exists():
            r = fnaam + " bestaat niet"
        else:
            tree = ElementTree(file=fnaam)
            if tree.getroot().tag != "acties":
                r = fnaam + " is geen bruikbaar xml bestand"
    return r


def get_nieuwetitel(fnaam, jaar=None):
    "bepaal nieuw uit te geven actienummer"
    if fnaam.exists():
        dnaam = str(fnaam)
    else:
        test = pathlib.Path('') / str(fnaam)
        if test.exists():
            dnaam = str(test)
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


def get_acties(fnaam, select=None, arch="", user=None):
    """ lijst alle items van een bepaald soort

    fnaam is a pathlib.Path object

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
        als er een * in zit moet wat ervoor zit en erna komt in de titel zitten
    het laatste argument `user` wordt hier niet gebruikt maar is voor compatibiliteit
    met de django versie
    """
    if select is None:
        select = {}
        if not arch:
            return []
    lijst = []
    if select:
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
        raise DataError("Foutieve waarde voor archief opgegeven "
                        "(moet niks, 'arch'  of 'alles' zijn)")
    sett = Settings(fnaam)
    if fnaam.exists():
        dnaam = str(fnaam)
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
        if tl is None:
            tl = ""
        if "titel" in select and select["titel"].upper() not in tl.upper():
            continue
        lijst.append((nr, dd, st, ct, tl, lu, a))
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
        self.kop = {x: y[0] for x, y in kopdict.items()}
        self.stat = {x: (y[0], y[1]) for x, y in statdict.items()}
        self.cat = {x: (y[0], y[1]) for x, y in catdict.items()}
        self.imagecount = 0
        self.startitem = ''
        self.meld = ''
        if fnaam == "":
            self.meld = "Standaard waarden opgehaald"
            return
        self.fn, self.fnaam, self.exists, self.meld = check_filename(fnaam)
        if self.meld:
            raise DataError(self.meld)
        if self.exists:
            self.read()

    def read(self):
        "settings lezen"
        tree = ElementTree(file=str(self.fn))
        rt = tree.getroot()
        ## found = False  # wordt niet gebruikt
        x = rt.find("settings")
        if x is not None:
            self.imagecount = x.get('imagecount') or '0'
            self.imagecount = int(self.imagecount)
            self.startitem = x.get('startitem') or ''
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
                    self.kop[y.get("value")] = (y.text,)

    def write(self, srt=None):  # extra argument ivm compat sql-versie
        "settings terugschrijven"
        fnaam = str(self.fn)
        if not self.exists:
            rt = Element('acties')
            tree = ElementTree(rt)
        else:
            tree = ElementTree(file=fnaam)
            rt = tree.getroot()
        el = rt.find("settings")
        if el is None:
            el = SubElement(rt, "settings")
        el.set('imagecount', str(self.imagecount))
        el.set('startitem', str(self.startitem))
        for x in list(el):
            if x.tag == "stats":
                el.remove(x)
            elif x.tag == "cats":
                el.remove(x)
            elif x.tag == "koppen":
                el.remove(x)
        h = SubElement(el, "stats")
        for x in list(self.stat.keys()):
            if x is int:
                x = str(x)
            j = SubElement(h, "stat", value=x)
            j.set("order", str(self.stat[x][1]))
            j.text = self.stat[x][0]
        h = SubElement(el, "cats")
        for x in list(self.cat.keys()):
            j = SubElement(h, "cat", value=x)
            j.set("order", str(self.cat[x][1]))
            j.text = self.cat[x][0]
        h = SubElement(el, "koppen")
        for x in list(self.kop.keys()):
            if x is int:
                x = str(x)
            j = SubElement(h, "kop", value=x)
            j.text = self.kop[x][0]
        copyfile(fnaam, fnaam + ".old")
        tree.write(fnaam, encoding='utf-8', xml_declaration=True)
        self.exists = True

    # def set(self, naam, key=None, waarde=None):
    #     "settings waarde instellen"
    #     if naam not in ("stat", "cat", "kop"):
    #         self.meld = 'Foutieve soort opgegeven'
    #         raise DataError(self.meld)
    #     elif key is None:
    #         self.meld = 'Geen sleutel opgegeven'
    #         raise DataError(self.meld)
    #     elif waarde is None:
    #         self.meld = 'Geen waarde voor sleutel opgegeven'
    #         raise DataError(self.meld)
    #     elif naam == "stat":
    #         if not isinstance(waarde, tuple):
    #             self.meld = 'Sleutelwaarde moet bestaan uit tekst en sortvolgnummer'
    #             raise DataError(self.meld)
    #         self.stat[key] = waarde
    #     elif naam == "cat":
    #         if not isinstance(waarde, tuple):
    #             self.meld = 'Sleutelwaarde moet bestaan uit tekst en sortvolgnummer'
    #             raise DataError(self.meld)
    #         self.cat[key] = waarde
    #     elif naam == "kop":
    #         if not isinstance(waarde, str):
    #             self.meld = 'Sleutelwaarde moet bestaan uit alleen tekst'
    #             raise DataError(self.meld)
    #         self.kop[key] = waarde

    # def get(self, naam, key=None):
    #     "settings waarde lezen"
    #     if naam not in ("stat", "cat", "kop"):
    #         self.meld = 'Foutieve soort opgegeven'
    #         raise DataError(self.meld)
    #     elif naam == "stat":
    #         if key is None:
    #             return self.stat
    #         else:
    #             if isinstance(key, int):
    #                 key = str(key)
    #             if key not in self.stat:
    #                 self.meld = 'Sleutel bestaat niet voor status'
    #                 raise DataError(self.meld)
    #             return self.stat[key]
    #     elif naam == "cat":
    #         if key is None:
    #             return self.cat
    #         else:
    #             if key not in self.cat:
    #                 self.meld = 'Sleutel bestaat niet voor soort'
    #                 raise DataError(self.meld)
    #             return self.cat[key]
    #     elif naam == "kop":
    #         if key is None:
    #             return self.kop
    #         else:
    #             if isinstance(key, int):
    #                 key = str(key)
    #             if key not in self.kop:
    #                 self.meld = 'Sleutel bestaat niet voor kop'
    #                 raise DataError(self.meld)
    #             return self.kop[key]


class Actie:
    """lijst alle gegevens van een bepaald item

    fnaam is a pathlib.Path object
    user is only for compatibilty with the Django version
    """
    def __init__(self, fnaam, _id, user=None):
        self.fn, self.fnaam, self.file_exists, self.meld = check_filename(fnaam)
        if self.meld:
            raise DataError(self.meld)
        self.settings = Settings(fnaam)
        self.imagecount = int(self.settings.imagecount)
        self.imagelist = []
        self.id, self.exists = _id, False
        self.datum = self.soort = self.titel = ''
        self.status, self.arch = '0', False
        self.melding = self.oorzaak = self.oplossing = self.vervolg = self.stand = ''
        self.events = []
        ## self.fno = str(self.fn) + ".old"     # naam van de backup van het xml bestand
        new_item = _id == 0 or _id == "0"
        if self.file_exists:
            if new_item:
                self.nieuw()
            else:
                self.read()
        else:
            if new_item:
                self.nieuwfile()
                self.nieuw()
            else:
                raise DataError("Can't pass non-empty id for nonexistant file")

    def nieuwfile(self):
        "nieuw projectbestand aanmaken"
        f = self.fn.open("w")
        with f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n<acties>\n</acties>\n')

    def nieuw(self):
        "nieuwe actie initialiseren"
        self.id = get_nieuwetitel(self.fn)
        self.datum = dt.datetime.today().isoformat(' ')[:19]

    def read(self):
        "gegevens lezen van een bepaalde actie"
        tree = ElementTree(file=str(self.fn))
        rt = tree.getroot()
        found = False
        log('%s %s', self.id, type(self.id))
        for x in rt.findall("actie"):
            if x.get("id") == self.id:
                found = True
                break
        if found:
            h = x.get("datum")
            if h is not None:
                self.datum = h
            self.status = x.get("status")
            self.soort = x.get("soort")
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
                elif y.tag == 'images':
                    self.imagelist = []
                    for z in list(y):
                        fname = z.get("filename")
                        self.imagelist.append(fname)
                        with open(fname, 'wb') as _out:
                            log('length of text:', len(z.text))
                            data = base64.b64decode(eval(z.text))  # eval is nodig omdat anders
                            # de quotes eromheen meegecodeerd worden
                            _out.write(data)
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

    # def set_status(self, waarde):
    #     "stel status in (code of tekst)"
    #     if isinstance(waarde, int):
    #         if str(waarde) in statdict:
    #             self.status = waarde
    #         else:
    #             raise DataError("Foutieve numerieke waarde voor status")
    #     elif isinstance(waarde, str):
    #         found = False
    #         for x, y in list(statdict.values()):
    #             log('%s %s %s', waarde, x, y)
    #             # if x == waarde:  # FIXME: moet dit soms y zijn?
    #             if y == waarde:
    #                 found = True
    #                 self.status = x
    #                 break
    #         if not found:
    #             raise DataError("Foutieve tekstwaarde voor status")
    #     else:
    #         raise DataError("Foutief datatype voor status")

    # def set_soort(self, waarde):
    #     "stel soort in (code of tekst)"
    #     log(waarde)
    #     if isinstance(waarde, str):
    #         if waarde in catdict:
    #             self.soort = waarde
    #         else:
    #             found = False
    #             for x, y in list(catdict.items()):
    #                 log(y)
    #                 if y[0] == waarde:
    #                     found = True
    #                     self.soort = x
    #                     break
    #             if not found:
    #                 raise DataError("Foutieve tekstwaarde voor categorie")
    #     else:
    #         raise DataError("Foutief datatype voor categorie")

    # def set_arch(self, waarde):
    #     "stel archiefstatus in"
    #     if not isinstance(waarde, bool):
    #         raise DataError("Foutief datatype voor archiveren")
    #     self.arch = waarde

    def add_event(self, txt):
        "voeg tekstregel toe aan events"
        now = dt.datetime.today()
        self.events.append((now.strftime(dtformat), txt))

    def write(self):
        "actiegegevens terugschrijven"
        if self.file_exists:     # os.path.exists(self.fn):
            tree = ElementTree(file=str(self.fn))
            rt = tree.getroot()
            sett = rt.find('settings')
        else:
            rt = Element("acties")
            sett = SubElement(rt, 'settings')
        # terugschrijven imagecount
        sett.set('imagecount', str(self.imagecount))  # moet dit niet parent.parent.imagecount zijn?
        if self.startitem:
            sett.set('startitem', str(self.startitem))

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
            print(self.soort)
            h = self.soort
            if h is None or h == '':
                self.soort = " "
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
            h = SubElement(x, "events")
            for y, z in self.events:
                q = SubElement(h, "event", id=y)
                q.text = z
            h = x.find("images")
            if h is not None:
                x.remove(h)
            h = SubElement(x, "images")
            for fname in self.imagelist:
                q = SubElement(h, 'image', filename=fname)
                with open(fname, 'rb') as _in:
                    data = _in.read()
                log('length of data:', len(data))
                q.text = str(base64.b64encode(data))
                log('length of text:', len(q.text))
                ## q.text = str(base64.encodebytes(data))
                ## q.text = str(gzip.compress(data)) # let op: bdata, geen cdata !
            tree = ElementTree(rt)
            copyfile(str(self.fn), str(self.fn) + ".old")
            tree.write(str(self.fn), encoding='utf-8', xml_declaration=True)
            self.exists = True
        ## else:
            ## return False
        return found

    def cleanup(self):
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
