#! C:/python24
# -*- coding: UTF-8 -*-
# aangepast python 2.5: xml.etree ipv elementtree

import sys
if sys.version[:3] >= '2.5':
    from xml.etree.ElementTree import ElementTree, Element, SubElement
else:
    from elementtree.ElementTree import ElementTree, Element, SubElement

from os import getcwd
from os.path import exists,split,splitext
from shutil import copyfile
from datetime import datetime

# 18-11-2007: statdict en catdict uit Settings class overgenomen, aanmaken nieuw bestand toegevoegd
# 18-06-2008: rename i.p.v. copyfile

datapad = getcwd() + "\\"
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

def checkfile(fn,new=False):
    r = ''
    if new:
        root = Element("acties")
        s = SubElement(root,"settings")
        t = SubElement(s,"stats")
        for x,y in list(statdict.items()):
            u = SubElement(t,"stat",order=str(y[1]),value=x)
            u.text = y[0]
        t = SubElement(s,"cats")
        for x,y in list(catdict.items()):
            u = SubElement(t,"cat",order=str(y[1]),value=x)
            u.text = y[0]
        t = SubElement(s,"koppen")
        for x,y in list(kopdict.items()):
            u = SubElement(t,"kop",value=x)
            u.text = y
        ElementTree(root).write(fn)
    else:
        if not exists(fn):
            r = fn + " bestaat niet"
        else:
            tree = ElementTree(file=fn)
            if tree.getroot().tag != "acties":
                r = fn + " is geen bruikbaar xml bestand"
    return r

class DataError(Exception):
    pass

class LaatsteActie:
    def __init__(self,fnaam,jaar=None):
        if exists(fnaam):
            dnaam = fnaam
        elif exists(datapad + fnaam):
            dnaam = datapad + fnaam
        else:
            raise DataError("datafile bestaat niet")
        if jaar == None:
            from datetime import date
            jaar = str(date.today().year)
        tree = ElementTree(file=dnaam)
        nummer = 0
        rt = tree.getroot()
        for x in rt.findall("actie"):
            t = x.get("id").split("-")
            if t[0] != jaar: continue
            if int(t[1]) > nummer: nummer = int(t[1])
        self.nieuwnummer = nummer + 1
        self.nieuwetitel = ("%s-%04i" % (jaar,self.nieuwnummer))

class Acties:
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
    def __init__(self,fnaam,select={},arch=""):
        if len(select) > 0:
            keyfout = False
            for x in list(select.keys()):
                if x not in ("idlt","id","idgt","soort","status","titel"):
                    keyfout = True
                    break
            if keyfout:
                raise DataError("Foutief selectie-argument opgegeven")
            if "id" in select:
                if "idlt" not in select or "idgt" not in select:
                    raise DataError("Foutieve combinatie van selectie-argumenten opgegeven")
        if arch not in ("","arch","alles"):
            raise DataError("Foutieve waarde voor archief opgegeven (moet niks, 'arch'  of 'alles' zijn)")
        sett = Settings(fnaam)
        self.meld = ''
        self.lijst = []
        if exists(fnaam):
            dnaam = fnaam
        elif exists(datapad + fnaam):
            dnaam = datapad + fnaam
        else:
            raise DataError("datafile bestaat niet")
        tree = ElementTree(file=dnaam)
        rt = tree.getroot()
        for x in rt.findall("actie"):
            a = x.get("arch")
            if a is None:
                if arch == "arch": continue
            else:
                if (a == "arch" and arch == "") or (a != "arch" and arch == "arch"):
                    continue
            nr = x.get("id")
            if "id" in select and select["id"] == "or":
                if nr <= select["idgt"] and nr >= select["idlt"]:
                    continue
            else:
                if ("idgt" in select and nr <= select["idgt"]) or ("idlt" in select and nr >= select["idlt"]):
                    continue
            dd = x.get("datum")
            if dd is None:
                dd = ''
            lu = x.get("updated")
            if lu is None: lu = ""
            h = x.get("status")
            if "status" in select and h not in select["status"]:
                continue
            st = ''
            if h in list(sett.stat.keys()):
                st = sett.stat[h]
            h = x.get("soort")
            if h is None: h = ""
            if "soort" in select and h not in select["soort"]:
                continue
            ct = ''
            if h in list(sett.cat.keys()):
                ct = sett.cat[h]
            tl = x.find("titel").text
            if tl == None: tl = ""
            if "titel" in select and select["titel"] not in tl:
                continue
            self.lijst.append((nr,dd,st,ct,tl,lu))

class Settings:
    """
        de soorten hebben een numeriek id en alfanumerieke code
        de categorieen hebben een numeriek id en een numerieke code
        de id's bepalen de volgorde in de listboxen en de codes worden in de xml opgeslagen
    """
    def __init__(self,fnaam=""):
        self.kop = kopdict
        self.stat = statdict
        self.cat = catdict
        self.meld = ''
        if fnaam == "":
            self.meld = "Standaard waarden opgehaald"
            return
        if splitext(fnaam)[1] != ".xml":
            #~ print splitext(fnaam)[1]
            self.meld = "Geen xml-bestand opgegeven: " + fnaam
            raise DataError(self.meld)
        fn = split(fnaam)
        if fn[0] != "":
            self.fn = fnaam
            self.fnaam = fn[1]
        else:
            self.fn = datapad + fnaam # naam van het xml bestand
            self.fnaam = fnaam
        self.fno = self.fn + ".old"     # naam van de backup van het xml bestand
        self.exists = False
        if exists(self.fn):
            self.exists = True
            self.read()

    def read(self):
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()
        found = False
        x = rt.find("settings")
        if x is not None:
            h = x.find("stats")
            if h is not None:
                self.stat = {}
                for y in h.findall("stat"):
                    self.stat[y.get("value")] = (y.text,y.get("order"))
                    h = x.find("cats")
            if h is not None:
                self.cat = {}
                for y in h.findall("cat"):
                    self.cat[y.get("value")] = (y.text,y.get("order"))
                    h = x.find("koppen")
            if h is not None:
                self.kop = {}
                for y in h.findall("kop"):
                    self.kop[y.get("value")] = y.text

    def write(self):
        if not self.exists:
            f = open(self.fn,"w")
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
            if x is int: x = str(x)
            j = SubElement(h,"stat",value=x)
            j.set("order",str(self.stat[x][1]))
            j.text = self.stat[x][0]
        h = SubElement(el,"cats")
        #~ print self.cat
        for x in list(self.cat.keys()):
            j = SubElement(h,"cat",value=x)
            j.set("order",str(self.cat[x][1]))
            j.text = self.cat[x][0]
        h = SubElement(el,"koppen")
        #~ print self.kop
        for x in list(self.kop.keys()):
            if x is int: x = str(x)
            j = SubElement(h,"kop",value=x)
            j.text = self.kop[x]
        copyfile(self.fn,self.fno)
        tree.write(self.fn)

    def set(self,naam,key=None,waarde=None):
        if naam not in ("stat","cat","kop"):
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

    def get(self,naam,key=None):
        if naam not in ("stat","cat","kop"):
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
    def __init__(self,fnaam,id):
        self.meld = ''
        if splitext(fnaam)[1] != ".xml":
            #~ print splitext(fnaam)[1]
            self.meld = "Geen xml-bestand opgegeven: " + fnaam
            raise DataError(self.meld)
        fn = split(fnaam)
        if fn[0] != "":
            self.fn = fnaam
            self.fnaam = fn[1]
        else:
            self.fn = datapad + fnaam # naam van het xml bestand
            self.fnaam = fnaam
        self.id = id
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
        if exists(self.fn):
            pass
        elif id == 0 or id == "0":
            self.nieuwfile()
        if id == 0 or id == "0":
            self.nieuw()
        else:
            self.read()

    def nieuw(self):
        self.id = LaatsteActie(self.fn).nieuwetitel
        self.datum= datetime.today().isoformat(' ')[:19]

    def nieuwfile(self):
        f = open(self.fn,"w")
        f.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<acties>\n</acties>\n')
        f.close()

    def read(self):
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
                    for z in list(y):
                        self.events.append((z.get("id"),z.text))
            self.exists = True

    def getStatusText(self,waarde):
        if str(waarde) in statdict:
            return statdict[str(waarde)]
        else:
            raise DataError("Geen tekst gevonden bij statuscode")

    def getSoortText(self,waarde):
        if waarde in catdict:
            return catdict[waarde]
        else:
            raise DataError("Geen tekst gevonden bij soortcode")

    def setStatus(self,waarde):
        if type(waarde) is int:
            if str(waarde) in statdict:
                self.status = waarde
            else:
                raise DataError("Foutieve numerieke waarde voor status")
        elif type(waarde) is str:
            found = False
            for x,y in list(statdict.values()):
                if x == waarde:
                    found = True
                    self.status = x
                    break
            if not found:
                raise DataError("Foutieve tekstwaarde voor status")
        else:
            raise DataError("Foutief datatype voor status")

    def setSoort(self,waarde):
        if type(waarde) is str:
            if waarde in catdict:
                self.soort = waarde
            else:
                for x,y in list(catdict.items()):
                    if y[0] == waarde:
                        self.soort = x
                    else:
                        raise DataError("Foutieve tekstwaarde voor categorie")
        else:
            raise DataError("Foutief datatype voor categorie")

    def setArch(self,waarde):
        if type(waarde) is bool:
            self.arch = waarde
        else:
            raise DataError("Foutief datatype voor archiveren")

    def write(self):
        if exists(self.fn):
            tree = ElementTree(file=self.fn)
            rt = tree.getroot()
        else:
            rt = Element("acties")
        if not self.exists:
            x = SubElement(rt,"actie")
            x.set("id",self.id)
            x.set("datum",self.datum)
            found = True
        else:
            for x in rt.findall("actie"):
                if x.get("id") == self.id:
                    found = True
                    break
        if found:
            x.set("updated",datetime.today().isoformat(' ')[:10])
            h = self.soort
            if h is None:
                self.soort = ""
            x.set("soort",self.soort)
            x.set("status",self.status)
            if self.arch:
                x.set("arch","arch")
            else:
                h = x.get("arch")
                if h is not None:
                    x.set("arch","herl")
            h = x.find("titel")
            if h is None:
                h = SubElement(x,"titel")
            h.text = self.titel
            h = x.find("melding")
            if h is None:
                h = SubElement(x,"melding")
            h.text = self.melding
            h = x.find("oorzaak")
            if h is None:
                h = SubElement(x,"oorzaak")
            h.text = self.oorzaak
            h = x.find("oplossing")
            if h is None:
                h = SubElement(x,"oplossing")
            h.text = self.oplossing
            h = x.find("vervolg")
            if h is None:
                h = SubElement(x,"vervolg")
            h.text = self.vervolg
            h = x.find("stand")
            if h is None:
                h = SubElement(x,"stand")
            h.text = self.stand
            h = x.find("events")
            if h is not None:
                x.remove(h)
            h = SubElement(x,"events") # maakt dit een bestaande "leeg" ?
            for y,z in self.events:
                q = SubElement(h,"event",id=y)
                q.text = z
            tree = ElementTree(rt)
            copyfile(self.fn,self.fno)
            tree.write(self.fn)
            self.exists = True
        else:
            return False

    def list(self):
        print("%s %s gemeld op %s status %s %s" % (
            self.getSoortText(self.soort),
            self.id,
            self.datum,
            self.status,
            self.getStatusText(self.status)
            ))
        print("Titel:",self.titel)
        print("Melding:",self.melding)
        print("Oorzaak:",self.oorzaak)
        print("Oplossing:",self.oplossing)
        print("Vervolg:",self.vervolg)
        print("Stand:",self.stand)
        print("Verslag:")
        for x,y in self.events:
            print("\t",x,"-",y)
        if self.arch:
            print("Actie is gearchiveerd.")

def test(i):
    #~ fn = "pythoneer.xml"
    #~ fn = "magiokis.xml"
    ## fn = "_probreg.xml"
    fn = 'Project.xml'
    if i == "Laatste":
        try:
            h = LaatsteActie(fn)
        except DataError as meld:
            print(meld)
        else:
            print(h.nieuwetitel)
    elif i == "Acties":
        try:
            h = Acties(fn,arch="")
            ## h = Acties(fn,select={"idgt": "2006-0010"})
            ## h = Acties(fn,{"idlt": "2005-0019"})
            ## h = Acties(fn,{"idgt": "2005-0019" ,"idlt": "2006-0010"})
            ## h = Acties(fn,{"idgt": "2005-0019" ,"idlt": "2006-0010", "id": "and" })
            ## h = Acties(fn,{"idgt": "2006-0010" ,"idlt": "2005-0019", "id": "or" })
            ## h = Acties(fn,{"status": ("0","1","3")})
            ## h = Acties(fn,{"soort": ("W","P")})
            ## h = Acties(fn,{"titel": ("tekst")})
        except DataError as meld:
            print(meld)
            return
        if len(h.lijst) == 0:
            print("(nog) geen acties gemeld")
        else:
            for x in h.lijst:
                print(x)
    elif i == "Actie":
        ## h = Actie(fn,"2007-0001")
        h = Actie(fn,"1")
        print(h.meld)
        if h.exists:
            h.list()
        else:
            print("geen probleem met deze sleutel bekend")
            #~ h = Actie(fn,0)
            #~ print "na init"
            #~ h.list()
            #~ h.setStatus(2)
            h.setStatus("in behandeling")
            #~ h.setSoort("P")
            h.setSoort("wens")
            #~ h.titel = "er ging iets mis"
            #~ h.probleem = "dit is het probleem"
            #~ h.oorzaak = "het kwam hierdoor"
            #~ h.oplossing  = "we hebben het zo opgelost"
            #~ h.vervolg = "maar er moet nog een vervolg komen"
            #~ h.list()
            #~ h.write()
            h = Actie(fn,0)
            print("na init")
            h.list()
            h.titel = "er ging nog iets mis"
            h.probleem = "dit is dit keer het probleem"
            h.oorzaak = "het kwam ditmaal hierdoor"
            h.oplossing  = "we hebben het weer zo opgelost"
            h.vervolg = "uitzoeken of er een verband is"
            h.stand = "net begonnen"
            h.events = [("eerste","hallo"),("tweede","daar")]
            h.list()
            h.write()
    elif i == "Settings":
        h = Settings(fn)
        print("-- na init ----------------")
        for x in list(h.__dict__.items()):
            print(x)
        print("stat: ")
        for x in h.stat:
                print("\t",x,h.stat[x])
        print("cat: ")
        for x in h.cat:
                print("\t",x,h.cat[x])
        print("kop: ")
        for x in h.kop:
                print("\t",x,h.kop[x])
        return
        stats = {}
        cats = {}
        tabs = {}
        for x in list(h.stat.keys()):
            stats[h.stat[x][1]] = (x,h.stat[x][0])
        for x in list(h.cat.keys()):
            cats[h.cat[x][1]] = (x,h.cat[x][0])
        for x in list(h.kop.keys()):
            tabs[x] = h.kop[x]
        print(stats)
        print(cats)
        print(tabs)
        return
        #~ try:
            #~ h.set("test")
            #~ h.set("cat")
            #~ h.set("stat")
            #~ h.set("cat","test")
            #~ h.set("stat","test")
            #~ h.set("cat","V","vraag")
            #~ h.set("stat","4","onoplosbaar")
            #~ h.set("cat","","o niks")
            #~ h.set("stat","3","opgelost")
            #~ print h.get("test")
            #~ print h.get("cat")
            #~ print h.get("stat","x")
            #~ print h.get("cat","x")
            #~ print h.get("stat","1")
            #~ print h.get("cat","")
            #~ print h.get("kop","1")
            #~ print h.get("stat",3)
            #~ print h.get("cat",3)
            #~ print h.get("kop",1)
        #~ except DataError,meld:
            #~ print meld
            #~ return
        #~ print "-- na set -----------------"
        #~ for x in h.__dict__.items():
            #~ print x
        for x in list(h.stat.keys()):
            h.set("stat",x,(h.stat[x][0],x))
        i = 0
        for x in list(h.cat.keys()):
            h.set("cat",x,(h.cat[x][0],str(i)))
            i += 1
        print("-- na bijwerken -----------")
        print("stat: ",h.stat)
        print("cat:",h.cat)
        h.set("cat","V",("vraag","5"))
        h.set("stat","4",("onoplosbaar","7"))
        h.set("kop","7","bonuspagina")
        h.set("cat","",("o niks","8"))
        h.set("stat","3",("opgelost","15"))
        h.set("kop","2","opmerking")
        print("-- na sets -----------------")
        print("stat: ",h.stat)
        print("cat:",h.cat)
        print("kop:",h.kop)
        h.write()
    elif i == "Archiveren":
        h = Actie(fn,"2006-0001")
        print(h.meld)
        if h.exists:
            h.list()
            h.setArch(True)
            h.write()
            h.read()
            h.list()

if __name__ == "__main__":
    watten = {
        1: "Laatste",
        2: "Acties",
        3: "Actie",
        4: "Settings",
        5: "Archiveren",
        0: "Geen test, afbreken"
        }
    print("Wat voor test:")
    for x in list(watten.items()):
        print("    %s. %s" % x)
    wat = -1
    while wat:
        try:
            wat = int(input("Kies 1-5 of 0: "))
        except:
            wat = -1
        if wat in watten:
            test(watten[wat])

