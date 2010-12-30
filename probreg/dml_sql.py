#! usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
import datetime as dt
from sqlite3 import dbapi2 as sql
from sqlite3 import Row
import pprint as pp

dbnaam = os.getcwd() + "/probreg.db"
kopdict = {
    "0": ("Lijst",'index'),
    "1": ("Titel/Status",'detail'),
    "2": ("Probleem/Wens",'meld'),
    "3": ("Oorzaak/Analyse",'oorz'),
    "4": ("Oplossing",'opl'),
    "5": ("Vervolgactie",'verv'),
    "6": ("Voortgang",'voortg')
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
    " ": ("onbekend",0),
    "V": ("vraag",3),
    "I": ("idee",4),
    "F": ("div. informatie",5)
}
class MethodError(Exception):
    pass

class DataError(Exception):
    pass

def do_sql(con,statement,parms="",commit=True):
    print(statement)
    print(parms)
    try:
        if parms:
            items = [x for x in con.execute(statement, parms)]
        else:
            items = [x for x in con.execute(statement)]
    except sql.OperationalError as msg:
        return False, msg
    except sql.ProgrammingError as msg:
        return False, msg
    if commit:
        con.commit()
    return True, items

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
        check_stmt = projnaam.join((
            "SELECT * FROM sqlite_master WHERE type='table' AND name='",
            "_actie'"))
        ok, doe = do_sql(con,check_stmt)
        if not ok:
            return doe
        if not doe:
            return "project {0} bestaat (nog) niet".format(projnaam)
    return r


def laatste_actie(projnaam,jaar=None):
    if jaar == None:
        jaar = str(dt.date.today().year)
    con = sql.connect(dbnaam)
    select = "select id from {0}_actie".format(projnaam)
    ok, result = do_sql(con,select)
    if ok:
        ok = [x for x in result][-1]
        new_id = ok[0] + 1
    select = projnaam.join(("select nummer from ",
        "_actie where nummer like ? order by nummer"))
    ok, result = do_sql(con,select,(jaar + "%",))
    if not ok:
        raise DataError(result)
    ok = [x for x in result][-1]
    jaar,nummer = ok[0].split("-")
    nieuwnummer = int(nummer) + 1
    nieuwetitel = "{0}-{1:04}".format(jaar,nieuwnummer)
    return new_id, nieuwetitel

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
    def __init__(self,projnaam,select={},arch=""):
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
        self.meld = ''
        self.lijst = []
        parms = []
        select_stmt = "".join((
            "SELECT nummer,start,gewijzigd,{0}_status.title,{0}_soort.title,",
            "{0}_actie.title FROM {0}_actie,{0}_status,{0}_soort WHERE ",
            "{0}_actie.soort_id = {0}_soort.id AND {0}_actie.status_id == {0}_status.id"))
        select_stmt = select_stmt.format(projnaam)
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
        con = sql.connect(dbnaam)
        ok, doe = do_sql(con,select_stmt,parms=parms)
        if ok:
            self.lijst = [x for x in doe]
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
        self.projnaam = projnaam
        self.exists = False
        check_stmt = self.projnaam.join((
            "SELECT * FROM sqlite_master WHERE type='table' AND name='",
            "_actie'"))
        ok, doe = do_sql(self.con,check_stmt)
        if not ok:
            raise DataError(doe)
        ## print doe
        if doe:
            self.exists = True
            self.read()

    def read(self):
        select_stmt = 'select * from {0}_status'.format(self.projnaam)
        ok,doe = do_sql(self.con,select_stmt)
        print(doe)
        if ok and doe:
            for id, title, value, order in doe:
                self.stat[str(value)] = (title, order)
        select_stmt = 'select * from {0}_soort'.format(self.projnaam)
        ok,doe = do_sql(self.con,select_stmt)
        print(doe)
        if ok and doe:
            for id, title, value, order in doe:
                self.cat[value] = (title, order)
        select_stmt = 'select * from {0}_page'.format(self.projnaam)
        ok,doe = do_sql(self.con,select_stmt)
        print(doe)
        if ok and doe:
            for id, title, link, order in doe:
                self.kop[str(order)] = (title,link)

    def write(self):
        ok,doe = do_sql(self.con,'delete from {0}_status'.format(self.projnaam))
        ix = 0
        insert_stmt = self.projnaam.join(("insert into ",
            "_status values(?,?,?,?)"))
        for waarde, stat in list(self.stat.items()):
            titel, volgorde = stat
            ix += 1
            ok, doe = do_sql(self.con,insert_stmt,
                parms=(ix,titel,waarde,volgorde),commit=False)
            if not ok:
                return doe
            ## con.commit()
        ok,doe = do_sql(self.con,'delete from {0}_soort'.format(self.projnaam))
        ix = 0
        insert_stmt = self.projnaam.join(('insert into ',
            '_soort values(?,?,?,?)'))
        for waarde, cat in list(self.cat.items()):
            titel, volgorde = cat
            ix += 1
            ok, doe = do_sql(self.con,insert_stmt,
                parms=(ix,titel,waarde,volgorde),commit=False)
            if not ok:
                return doe
            ## con.commit()
        ok,doe = do_sql(self.con,'delete from {0}_page'.format(self.projnaam))
        ix = 0
        insert_stmt = self.projnaam.join(('insert into ',
            '_page values(?,?,?,?)'))
        for volgorde, kop in list(self.kop.items()):
            titel, link = kop
            ## link = ['index','detail','meld','oorz','opl','verv','voortg'][volgorde]
            ix += 1
            ok, doe = do_sql(self.con,insert_stmt,
                parms=(ix,titel,link,volgorde),commit=False)
            if not ok:
                return doe
        self.con.commit()

    def set(self,naam,key=None,waarde=None):
        raise MethodError('Settings.set({0},key={1},waarde={2}) called'.format(
            naam,key,waarde))
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
        raise MethodError('Settings.get({0},key={1}) called'.format(
            naam,key))
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
    def __init__(self,projnaam,id):
        self.con = sql.connect(dbnaam)
        self.con.row_factory = Row
        self.meld = ''
        self.nummer = id
        self.projnaam = projnaam
        if id == 0 or id == "0":
            check_stmt = self.projnaam.join((
                "SELECT * FROM sqlite_master WHERE type='table' AND name='",
                "_actie'"))
            ok, doe = do_sql(self.con,check_stmt)
            if not ok:
                return doe
            if not doe:
                self.nieuwfile()
            self.nieuw()
        else:
            self.read()

    def nieuw(self):
        insert_stmt = "insert into {0}_acties ()".format(self.projnaam)
        self.id, self.nummer = laatste_actie(self.fn)
        self.datum= dt.datetime.today().isoformat(' ')[:19]
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
        self.events = []
        self.exists = False

    def nieuwfile(self):
        # tabellen creeren
        r = checkfile(self.projnaam,new=True)

    def read(self):
        select_stmt = "SELECT * FROM {0}_actie WHERE nummer = ?".format(self.projnaam)
        self.select_actie = select_stmt
        ok, doe = do_sql(self.con,select_stmt,parms=(self.nummer,))
        if not ok:
            raise DataError(doe)
        self.exists = False
        if not doe:
            raise DataError("Geen gegevens opgehaald!?")
        self.exists = True
        ## for x in doe[0]:
            ## print(x)
        self.id = doe[0]["id"]
        self.datum = doe[0]["start"]
        self.starter = doe[0]["starter_id"]
        self.about = doe[0]["about"]
        self.title = doe[0]["title"]
        self.titel = ": ".join((self.about,self.title))
        self.gewijzigd = doe[0]["gewijzigd"]
        self.lasteditor = doe[0]["lasteditor_id"]
        self.status = doe[0]["status_id"]
        self.soort = doe[0]["soort_id"]
        self.behandelaar = doe[0]["behandelaar_id"]
        self.arch = doe[0]["arch"]
        self.melding = doe[0]["melding"]
        self.oorzaak = doe[0]["oorzaak"]
        self.oplossing  = doe[0]["oplossing"]
        self.vervolg = doe[0]["vervolg"]
        self.events = []
        select_stmt = "SELECT * FROM {0}_event WHERE actie_id = ?".format(self.projnaam)
        self.select_events = select_stmt
        ok, doe = do_sql(self.con,select_stmt,parms=(self.id,))
        if not ok:
            raise DataError(doe)
        if doe:
            self.events = [(event["start"],event["text"],event["starter_id"]) for event in doe]

    def getStatusText(self,waarde):
        ## raise MethodError('Actie.getStatusText({0}) called'.format(
            ## waarde))
        select_stmt = "select title from {0}_status where id = ?".format(self.projnaam)
        ok, doe = do_sql(self.con,select_stmt,parms=(waarde,))
        if not ok:
            raise DataError(doe)
        if doe:
            return doe[0][0]

    def getSoortText(self,waarde):
        ## raise MethodError('Actie.getSoortText({0}) called'.format(
            ## waarde))
        select_stmt = "select title from {0}_soort where id = ?".format(self.projnaam)
        ok, doe = do_sql(self.con,select_stmt,parms=(waarde,))
        if not ok:
            raise DataError(doe)
        if doe:
            return doe[0][0]

    def getPersonName(self,waarde):
        ## raise MethodError('Actie.getPersonName({0}) called'.format(
            ## waarde))
        select_stmt = "select username from auth_user where id = ?"
        ok, doe = do_sql(self.con,select_stmt,parms=(waarde,))
        if not ok:
            raise DataError(doe)
        if doe:
            return doe[0][0]

    def setStatus(self,waarde):
        raise MethodError('Actie.setStatus({0}) called'.format(
            waarde))
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
        raise MethodError('Actie.setSoort({0}) called'.format(
            waarde))
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
        raise MethodError('Actie.setArch({0}) called'.format(
            waarde))
        if type(waarde) is bool:
            self.arch = waarde
        else:
            raise DataError("Foutief datatype voor archiveren")

    def write(self):
        self.gewijzigd = dt.datetime.today().isoformat(' ')[:10]
        if self.exists:
            update_stmt = "UPDATE {0}_actie SET ".format(self.projnaam)
            ok, doe = do_sql(self.con,self.select_actie,parms=(self.nummer,))
            parms = []
            if self.about == doe[0]["about"]:
                update_stmt += "about = ?, "
                parms.append(self.about)
            if self.title == doe[0]["title"]:
                update_stmt += "title = ?, "
                parms.append(self.title)
            if self.gewijzigd == doe[0]["gewijzigd"]:
                update_stmt += "gewijzigd = ?, "
                parms.append(self.gewijzigd)
            if self.lasteditor == doe[0]["lasteditor_id"]:
                update_stmt += "lasteditor_id = ?, "
                parms.append(self.lasteditor)
            if self.status == doe[0]["status_id"]:
                update_stmt += "status_id = ?, "
                parms.append(self.status)
            if self.soort == doe[0]["soort_id"]:
                update_stmt += "soort_id = ?, "
                parms.append(self.soort)
            if self.behandelaar == doe[0]["behandelaar_id"]:
                update_stmt += "behandelaar_id = ?, "
                parms.append(self.behandelaar)
            if self.arch == doe[0]["arch"]:
                update_stmt += "arch = ?, "
                parms.append(self.arch)
            if self.melding == doe[0]["melding"]:
                update_stmt += "melding = ?, "
                parms.append(self.melding)
            if self.oorzaak == doe[0]["oorzaak"]:
                update_stmt += "oorzaak = ?, "
                parms.append(self.oorzaak)
            if self.oplossing == doe[0]["oplossing"]:
                update_stmt += "oplossing = ?, "
                parms.append(self.oplossing)
            if self.vervolg == doe[0]["vervolg"]:
                update_stmt += "vervolg = ?, "
                parms.append(self.vervolg)
            update_stmt += "WHERE nummer = ?"
            parms.append(self.nummer)
            ok, doe = do_sql(self.con,update_stmt,parms=parms)

        else:
            self.exists = True
            insert_stmt = " ".join(("INSERT INTO {0}_actie",
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                )).format(self.projnaam)
            parms = (
                self.id,
                self.datum,
                self.starter,
                self.about,
                self.title,
                self.gewijzigd,
                self.lasteditor,
                self.status,
                self.soort,
                self.behandelaar,
                self.arch,
                self.melding,
                self.oorzaak,
                self.oplossing,
                self.vervolg
                )
            ok, doe = do_sql(self.con,insert_stmt,parms=parms)

        if self.exists:
            last_id = 0
            ok, doe = do_sql(self.con,"SELECT id FROM {0}_event".format(self.projnaam))
            if not ok:
                raise DataError(doe)
            if doe:
                last_id = doe[-1][0]
            event_dict = {}
            ok, doe = do_sql(self.con,self.select_events,parms=(self.id,))
            if doe:
                for event in doe:
                    event_dict[event["start"]] = (event["text"],event["starter_id"])
            for start,text,starter in self.events:
                if start in event_dict:
                    if (text,starter) != event_dict[start]:
                        update_stmt = " ".join(("UPDATE {0}_event",
                            "SET text = ?,",
                            "SET starter_id = ?",
                            "WHERE start = ?")).format(self.projnaam)
                        parms = (text, starter, start)
                        ok, doe = do_sql(self.con,update_stmt,parms=parms)
                else:
                    last_id += 1
                    insert_stmt = "INSERT INTO {0}_event VALUES (?,?,?,?)".format(self.projnaam)
                    parms =  (last_id, start, text, starter)
                    ok, doe = do_sql(self.con,insert_stmt,parms=parms)

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
        print("Verslag:")
        for x,y,z in self.events:
            print("\t",x,"-",y)
        if self.arch:
            print("Actie is gearchiveerd.")

def test(i):
    #~ fn = "pythoneer.xml"
    #~ fn = "magiokis.xml"
    ## fn = "_probreg.xml"
    ## fn = 'Project.xml'
    fn = "_basic"
    if i == "Laatste":
        try:
            i,h = laatste_actie(fn)
        except DataError as meld:
            print(meld)
        else:
            print(i,h)
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
        h = Actie(fn,"2009-0001")
        ## h = Actie(fn,"0")
        print(h.meld)
        if h.exists:
            h.list()
        else:
            print("geen actie met deze sleutel bekend")
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
        print("stat: ")
        pp.pprint(h.stat)
        print("cat: ")
        pp.pprint(h.cat)
        print("kop: ")
        pp.pprint(h.kop)
        ## return
        h.write()
        h.read()
        print("-- na terugschrijven en herlezen ----------------")
        print("stat: ")
        pp.pprint(h.stat)
        print("cat: ")
        pp.pprint(h.cat)
        print("kop: ")
        pp.pprint(h.kop)

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
    wat = -1
    while wat:
        print("\nWat voor test:")
        for x in list(watten.items()):
            print("    %s. %s" % x)
        try:
            ## wat = int(raw_input("Kies 1-5 of 0: "))
            wat = int(input("Kies 1-5 of 0: "))
        except TypeError:
            wat = -1
        if wat in watten:
            test(watten[wat])

