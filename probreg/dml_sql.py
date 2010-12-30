#! usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
import datetime as dt
from sqlite3 import dbapi2 as sql

dbnaam = os.getcwd() + "/probreg.db"
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

def do_sql(con,statement,parms="",commit=True):
    try:
        if parms:
            items = con.execute(statement, parms)
        else:
            items = con.execute(statement)
    except sql.OperationalError,msg:
        return False, msg
    except sql.ProgrammingError,msg:
        return False, msg
    if commit:
        con.commit()
    return True, items

## def checkfile(fn,new=False):
def checkfile(projnaam,new=False):
    con = sql.connect(dbnaam)
    r = ''
    if new:
        insert_stmt = projnaam.join(('insert into ','_status values(?,?,?,?)'))
        for ix, stat in enumerate(statdict):
            titel, volgorde = statdict[stat]
            ok, doe = do_sql(con,insert_stmt,parms=(ix+1,titel,int(stat),volgorde),
                commit=False)
            if not ok:
                return doe
            ## con.commit()
        insert_stmt = projnaam.join(('insert into ','_soort values(?,?,?,?)'))
        for ix, cat in enumerate(catdict):
            titel, volgorde = catdict[cat]
            ok, doe = do_sql(con,insert_stmt,parms=(ix+1,titel,int(cat),volgorde),
                commit=False)
            if not ok:
                return doe
            ## con.commit()
        insert_stmt = projnaam.join(('insert into ','_page values(?,?,?,?)'))
        for ix, kop in enumerate(kopdict):
            titel, volgorde = kopdict[kop]
            link = ['index','detail','meld','oorz','opl','verv','voortg'][volgorde]
            ok, doe = do_sql(con,insert_stmt,parms=(ix+1,titel,link,volgorde),
                commit=False)
            if not ok:
                return doe
        con.commit()
    else:
        check_stmt = "SELECT * FROM sqlite_master WHERE type='table' AND name='{0}_acties'"
        ok, doe = do_sql(con,check_stmt)
        if not ok:
            return doe
        if not doe:
            return "project {0} bestaat (nog) niet".format(projnaam)
    return r

class DataError(Exception):
    pass

class LaatsteActie:
    def __init__(self,projnaam,jaar=None):
        if jaar == None:
            jaar = str(dt.date.today().year)
        self.con = sql.connect(dbnaam)
        select = projnaam.join(
                ("select nummer from ","_acties where nummer like ? order by nummer"))
        ok, result = do_sql(self.con,select,jaar + "%")
        if ok:
            ok = [x for x in result][-1]
            nummer = ok[0]
            self.nieuwnummer = nummer + 1
            self.nieuwetitel = ("%s-%04i" % (jaar,self.nieuwnummer))
        else:
            raise dataError(result)

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
            for x in select.keys():
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
        self.meld = ''
        self.lijst = []
        parms = []
        select_stmt = "SELECT nummer,start,gewijzigd,{0}_status.title,{0}_soort.title,"
            "{0}_acties.title FROM {0}_acties,{0}_status,{0}_soort WHERE",
            "soort_id = {0}_soort_id AND status_id == {0}_status.id".format(projnaam)
        if arch == "arch":
            select_stmt += " AND arch = 1"
        elif arch != "alles":
            select_stmt += " AND arch = 0"
        if "id" in select:
            select_stmt += " AND ("
            if "idgt" in select:
                select_stmt = "nummer > ?"
                parms.append(select["idgt"])
            if "idlt" in select:
                select_stmt += " {0} ".format(select["id"])
                select_stmt += "nummer < ?"
                parms.append(select["idlt"])
            select_stmt += ")"
        if "status" in select:
            select_stmt += " AND {0}_status.value IN ?".format(projnaam)
            parms.append(select["status"])
        if "soort" in select:
            select_stmt += " AND {0}_soort.value IN ?".format(projnaam)
            parms.append(select["soort"])
        if "titel" in select:
            select_stmt += "AND titel LIKE ?"
            parms.append("*{0}*".format(select["titel"]))
        ok, doe = do_sql(self.con,select_stmt,parms=parms)
        if ok:
            self.lijst = doe
        else:
            raise DataError(doe)

class Settings:
    """
        de soorten hebben een numeriek id en alfanumerieke code
        de categorieen hebben een numeriek id en een numerieke code
        de id's bepalen de volgorde in de listboxen en de codes worden in de xml opgeslagen
    """
    def __init__(self,projnaam=""):
        self.con = sql.connect(dbnaam)
        self.kop = kopdict
        self.stat = statdict
        self.cat = catdict
        self.meld = ''
        if projnaam == "":
            self.meld = "Standaard waarden opgehaald"
            return
        self.exists = False
        check_stmt = "SELECT * FROM sqlite_master WHERE type='table' AND name='{0}_acties'"
        ok, doe = do_sql(con,check_stmt)
        if not ok:
            raise dataError(doe)
        if doe:
            self.exists = True
            self.read()

    def read(self):
        select_stmt = projnaam.join(('select title,value,order from ','_status'))
        ok,doe = do_sql(self.con,select_stmt)
        if ok and doe:
            for title, value, order in doe:
                self.stat[value] = (title, order)
        select_stmt = projnaam.join(('select title,value,order from ','_soort'))
        ok,doe = do_sql(self.con,select_stmt)
        if ok and doe:
            for title, value, order in doe:
                self.cat[value] = (title, order)
        select_stmt = projnaam.join(('select title,order from ','_page'))
        ok,doe = do_sql(self.con,select_stmt)
        if ok and doe:
            for title, order in doe:
                self.stat[order] = title

    def write(self):
        ok,doe = do_sql(self.con,'delete from {0}_status'.format(projnaam))
        insert_stmt = 'insert into {0}_status values(?,?,?,?)'.format(projnaam)
        for ix, stat in enumerate(statdict):
            titel, volgorde = statdict[stat]
            ok, doe = do_sql(self.con,insert_stmt,parms=(ix+1,titel,int(stat),volgorde),
                commit=False)
            if not ok:
                return doe
            ## con.commit()
        ok,doe = do_sql(self.con,'delete from {0}_soort'.format(projnaam))
        insert_stmt = 'insert into {0}_soort values(?,?,?,?)'.format(projnaam)
        for ix, cat in enumerate(catdict):
            titel, volgorde = catdict[cat]
            ok, doe = do_sql(self.con,insert_stmt,parms=(ix+1,titel,int(cat),volgorde),
                commit=False)
            if not ok:
                return doe
            ## con.commit()
        ok,doe = do_sql(self.con,'delete from {0}_page'.format(projnaam))
        insert_stmt = 'insert into {0}_page values(?,?,?,?)'.format(projnaam)
        for ix, kop in enumerate(kopdict):
            titel, volgorde = kopdict[kop]
            link = ['index','detail','meld','oorz','opl','verv','voortg'][volgorde]
            ok, doe = do_sql(self.con,insert_stmt,parms=(ix+1,titel,link,volgorde),
                commit=False)
            if not ok:
                return doe
        self.con.commit()

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
                if not self.stat.has_key(key):
                    self.meld = 'Sleutel bestaat niet voor status'
                    raise DataError(self.meld)
                return self.stat[key]
        elif naam == "cat":
            if key is None:
                return self.cat
            else:
                if not self.cat.has_key(key):
                    self.meld = 'Sleutel bestaat niet voor soort'
                    raise DataError(self.meld)
                return self.cat[key]
        elif naam == "kop":
            if key is None:
                return self.kop
            else:
                if type(key) is int:
                    key = str(key)
                if not self.kop.has_key(key):
                    self.meld = 'Sleutel bestaat niet voor kop'
                    raise DataError(self.meld)
                return self.kop[key]

class Actie:
    """lijst alle gegevens van een bepaald item"""
    def __init__(self,projnaam,id):
        self.meld = ''
        self.nummer = id
        self.projnaam = projnaam
        self.start = ''
        self.starter_id = 0
        self.about = ''
        self.title = ''
        self.gewijzigd = ''
        self.lasteditor_id = 0
        self.status_id = 0
        self.soort_id = 0
        self.behandelaar_id = 0
        self.arch = False
        self.melding = ''
        self.oorzaak = ''
        self.oplossing  = ''
        self.vervolg = ''
        self.stand = ''
        self.events = []
        self.exists = False
        if id == 0 or id == "0":
            check_stmt = "SELECT * FROM sqlite_master WHERE type='table' AND name='{0}_acties'"
            ok, doe = do_sql(con,check_stmt)
            if not ok:
                return doe
            if not doe:
                self.nieuwfile()
            self.nieuw()
        else:
            self.read()

    def nieuw(self):
        insert_stmt = "insert into {0}_acties ()".format(self.projnaam)
        self.id = LaatsteActie(self.fn).nieuwetitel
        self.datum= dt.datetime.today().isoformat(' ')[:19]

    def nieuwfile(self):
        # tabellen creeren
        pass

    def read(self):
        select_stmt = projnaam.join(
            "select * from ",
            "_acties where nummer = ?")

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
            for x,y in statdict.values():
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
                for x,y in catdict.items():
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
        if os.path.exists(self.fn):
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
            x.set("updated",dt.datetime.today().isoformat(' ')[:10])
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
            shutil.copyfile(self.fn,self.fno)
            tree.write(self.fn)
            self.exists = True
        else:
            return False

    def list(self):
        print "%s %s gemeld op %s status %s %s" % (
            self.getSoortText(self.soort),
            self.id,
            self.datum,
            self.status,
            self.getStatusText(self.status)
            )
        print "Titel:",self.titel
        print "Melding:",self.melding
        print "Oorzaak:",self.oorzaak
        print "Oplossing:",self.oplossing
        print "Vervolg:",self.vervolg
        print "Stand:",self.stand
        print "Verslag:"
        for x,y in self.events:
            print "\t",x,"-",y
        if self.arch:
            print "Actie is gearchiveerd."

def test(i):
    #~ fn = "pythoneer.xml"
    #~ fn = "magiokis.xml"
    ## fn = "_probreg.xml"
    fn = 'Project.xml'
    if i == "Laatste":
        try:
            h = LaatsteActie(fn)
        except DataError, meld:
            print meld
        else:
            print h.nieuwetitel
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
        except DataError, meld:
            print meld
            return
        if len(h.lijst) == 0:
            print "(nog) geen acties gemeld"
        else:
            for x in h.lijst:
                print x
    elif i == "Actie":
        ## h = Actie(fn,"2007-0001")
        h = Actie(fn,"1")
        print h.meld
        if h.exists:
            h.list()
        else:
            print "geen probleem met deze sleutel bekend"
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
            print "na init"
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
        print "-- na init ----------------"
        for x in h.__dict__.items():
            print x
        print "stat: "
        for x in h.stat:
                print "\t",x,h.stat[x]
        print "cat: "
        for x in h.cat:
                print "\t",x,h.cat[x]
        print "kop: "
        for x in h.kop:
                print "\t",x,h.kop[x]
        return
        stats = {}
        cats = {}
        tabs = {}
        for x in h.stat.keys():
            stats[h.stat[x][1]] = (x,h.stat[x][0])
        for x in h.cat.keys():
            cats[h.cat[x][1]] = (x,h.cat[x][0])
        for x in h.kop.keys():
            tabs[x] = h.kop[x]
        print stats
        print cats
        print tabs
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
        for x in h.stat.keys():
            h.set("stat",x,(h.stat[x][0],x))
        i = 0
        for x in h.cat.keys():
            h.set("cat",x,(h.cat[x][0],str(i)))
            i += 1
        print "-- na bijwerken -----------"
        print "stat: ",h.stat
        print "cat:",h.cat
        h.set("cat","V",("vraag","5"))
        h.set("stat","4",("onoplosbaar","7"))
        h.set("kop","7","bonuspagina")
        h.set("cat","",("o niks","8"))
        h.set("stat","3",("opgelost","15"))
        h.set("kop","2","opmerking")
        print "-- na sets -----------------"
        print "stat: ",h.stat
        print "cat:",h.cat
        print "kop:",h.kop
        h.write()
    elif i == "Archiveren":
        h = Actie(fn,"2006-0001")
        print h.meld
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
    print "Wat voor test:"
    for x in watten.items():
        print "    %s. %s" % x
    wat = -1
    while wat:
        try:
            wat = int(raw_input("Kies 1-5 of 0: "))
        except:
            wat = -1
        if wat in watten:
            test(watten[wat])

