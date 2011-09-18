# -*- coding: utf-8 -*-
"""dml voor probreg met sql om dezelfde data te gebruiken die de Django versie
gebruikt
"""

from __future__ import print_function
## import sys
## import os
import pprint as pp
import datetime as dt
import sqlite3 as sql
from config import DBLOC, USER, kopdict, statdict, catdict

def getsql(con, cmd, item=None):
    """retrieval sql uitvoeren en resultaat teruggeven

    resultaat = []: query mislukt
    """
    print("getsql tweede argument: {0}".format(cmd))
    print("getsql derde  argument: {0}".format(item))
    if item is None:
        item = ()
    try:
        result = [x for x in con.execute(cmd, item)]
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

def complete_ids(dic):
    """ids genereren voor items met id = -1

    input is een dictionary van 3-tuples (naam, volgorde, id)
    elementen met een id van -1 krijgen in plaats van deze een passende waarde
    (eerstvolgend hogere id)
    """
    l1, l2 = [], []
    for key, value in dic.items():
        if value[2] == -1:
            l2.append(key)
        else:
            l1.append((value[2],key))
    l1.sort()
    last_id = int(l1[-1][0])
    for key in l2:
        last_id += 1
        dic[key] = (dic[key][0], dic[key][1], last_id)

class DataError(Exception):
    """Eigen all-purpose exception - met de nieuwe dml misschien helemaal niet nodig"""
    pass

class Settings:
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
        self.kop = {}
        for y in h:
            self.kop[str(y["order"])] = (y["title"], y["link"])

        h = getsql(con, "select * from {0}_status".format(self.naam))
        self.stat = {}
        for y in h:
            self.stat[str(y["value"])] = (y["title"], y["order"], y["id"])

        h = getsql(con, "select * from {0}_soort".format(self.naam))
        self.cat = {}
        for y in h:
            self.cat[y["value"]] = (y["title"], y["order"], y["id"])

        con.close()

    def write(self):
        "settings terugschrijven"
        con = sql.connect(DBLOC)
        con.row_factory = sql.Row

        if self.exists:
            _pages = getsql(con,
                'select * from {0}_page order by "order"'.format(self.naam))
            rtn = 0
            for item in _pages:
                ix = str(item["order"])
                if self.kop[ix] != (item["title"], item["link"]):
                    rtn = doesql(con, "update {0}_page set title = ?,"
                        ' link = ? where "order" = ?'.format(self.naam),
                        (self.kop[ix][0], self.kop[ix][1], ix))
                    if rtn:
                        break
        else:
            for order, item in self.kop:
                rtn = doesql(con, "insert into {0}_page values"
                    ' (?,?,?,?)'.format(naam), (order +  1, item[0], item[1],
                    order))
                if rtn:
                    break

        if rtn:
            con.rollback()
            con.close()
            raise DataError(rtn)

        if self.exists:
            rtn = doesql(con, 'delete from {0}_status'.format(self.naam), None)
        if not rtn:
            complete_ids(self.stat)
            for key, value in self.stat.items():
                rtn = doesql(con, 'insert into {0}_status (id, value, title,'
                    ' "order") values (?, ?, ?, ?)'.format(self.naam),
                    (value[2], key, value[0], value[1]))
                if rtn:
                    break
        if rtn:
            con.rollback()
            con.close()
            raise DataError(rtn)

        if self.exists:
            rtn = doesql(con, "delete from {0}_soort".format(self.naam), None)
        if not rtn:
            complete_ids(self.cat)
            for key, value in self.cat.items():
                rtn = doesql(con, 'insert into {0}_soort (id, value, title,'
                    ' "order") values (?, ?, ?, ?)'.format(self.naam),
                    (value[2], key, value[0], value[1]))
        if rtn:
            con.rollback()
            con.close()
            raise DataError(rtn)
        con.commit()
        con.close()

    def get_statusid(self, waarde):
        for key, value in self.stat.items():
            if waarde == key or waarde == value[0]:
                return value[2]
        raise DataError("geen status bij code of omschrijving gevonden")


    def get_soortid(self, waarde):
        for key, value in self.cat.items():
            if waarde == key or waarde == value[0]:
                return value[2]
        raise DataError("geen soort bij code of omschrijving gevonden")

    def get_statustext(self, waarde):
        "geef tekst bij statuscode of -id"
        try:
            return self.stat[waarde][0]
        except KeyError:
            pass
        for key, value in self.stat.items():
            if waarde == value[2]:
                return value[0]
        raise DataError("Geen omschrijving gevonden bij statuscode of -id")

    def get_soorttext(self, waarde):
        "geef tekst bij soortcode of -id"
        try:
            return self.cat[waarde][0]
        except KeyError:
            pass
        for key, value in self.cat.items():
            if waarde == value[2]:
                return value[0]
        raise DataError("Geen omschrijving gevonden bij soortcode of -id")


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
    if data or len(data) == 0:
        return data
    else:
        raise DataError(naam + " bestaat niet")

class Actie:
    """lijst alle gegevens van een bepaald item"""
    def __init__(self, naam, id_):
        self.meld = ''
        self.naam = naam
        self.settings = Settings(naam)
        self.id = id_
        self.new_data = [0, '', '', '', '', '0', '0', False, '', '', '', '']
        (nummer, self.datum, self.over, self.titel, gewijzigd,
            self.status, self.soort, self.arch, self.melding,
            self.oorzaak, self.oplossing, self.vervolg) = self.new_data
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
        nieuwnummer = int(volgnr) + 1 if int(jaar) == nw_date.year else 1
        self.id = "{0}-{1:04}".format(nw_date.year, nieuwnummer)
        self.datum = dt.datetime.today().isoformat(' ')[:19]
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
            (actie, self.id, self.datum, self.over, self.titel, self.updated,
                self.status, self.soort, self.arch, self.melding, self.oorzaak,
                self.oplossing, self.vervolg) = item
            self.titel = " - ".join((self.over, self.titel))
            print(self.status, self.soort, sep=" ")
        data = getsql(self.con, "select id, start, starter_id, text from"
            " {0}_event where actie_id = ?".format(self.naam), (actie,))
        for item in data:
            self.events.append((item[1],item[3]))
        self.exists = True

    def get_statustext(self):
        "geef tekst bij statuscode"
        return self.settings.get_statustext(self.status)

    def get_soorttext(self):
        "geef tekst bij soortcode"
        return self.settings.get_soorttext(self.soort)

    def set_status(self, waarde):
        "stel status in (code of tekst) met controle a.h.v. project settings"
        self.status = self.settings.get_statusid(waarde)
        print(waarde, self.status, sep = " ")
        self.events.append((dt.datetime.today().isoformat(' ')[:19],
            'status gewijzigd in "{0}"'.format(self.get_statustext())))

    def set_soort(self, waarde):
        "stel soort in (code of tekst) met controle a.h.v. project settings"
        self.soort = self.settings.get_soortid(waarde)
        print(waarde, self.soort, sep = " ")
        self.events.append((dt.datetime.today().isoformat(' ')[:19],
            'soort gewijzigd in "{0}"'.format(self.get_soorttext())))

    def set_arch(self, waarde):
        "stel archiefstatus in - garandeert dat dat een boolean waarde wordt"
        if waarde:
            self.arch = True
            self.events.append((dt.datetime.today().isoformat(' ')[:19],
                "Actie gearchiveerd"))
        else:
            self.arch = False
            self.events.append((dt.datetime.today().isoformat(' ')[:19],
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
            print("write: nieuwe actie {0}".format(self.id))
            actie_id = self.nieuw_id
            data = self.new_data
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
        items.append(dt.datetime.today().isoformat(' ')[:19])
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
        ## if not data:
            ## self.con.rollback()
            ## raise DataError("Problem getting events")
        current_events = [x for x in data] if data else []
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
            self.get_soorttext(),
            self.id,
            self.datum,
            self.status,
            self.get_statustext()
            ))
        print("Titel", self.over, self.titel, sep=": ")
        print("Melding:", self.melding, sep=" ")
        print("Oorzaak:", self.oorzaak, sep=" ")
        print("Oplossing:", self.oplossing, sep=" ")
        print("Vervolg:", self.vervolg, sep=" ")
        print("Verslag:")
        for x, y in self.events:
            print("\t {0} - {1}".format(x, y))
        if self.arch:
            print("Actie is gearchiveerd.")


def test_get_acties(fnaam):
    "test routine"
    for op1, op2 in (
            ({}, ""),
            ({"idlt": "2010", }, ""),
            ({"idlt": "2010",  "id": "and",  "idgt": "2007-0003"}, ""),
            ({"idgt": "2010",  "id": "or",  "idlt": "2007-0003"}, ""),
            ({"idgt": "2007-0003",}, ""),
            ({"status": "1",  "soort" : "2",}, ""),
            ({"titel": "en"}, ""),
            ({}, "arch"),
            ({}, "alles"),):
        h = get_acties(fnaam, op1, op2)
        i = 0
        for item in h:
            i += 1
            print(item[0])
            pp.pprint(item)
        print("{0} records".format(i))

def test_Settings(fnaam):
    "test routine"
    h = Settings(fnaam)
    pp.pprint(h.kop)
    pp.pprint(h.stat)
    pp.pprint(h.cat)
    h.stat['7'] = ("Gloekgloekgloe", 15, -1)
    h.cat["X"] = ("Willen we niet weten", 6, -1)
    h.kop['4'] = ("Gargl", "opl")
    print("\nNa toevoegen waarden:")
    pp.pprint(h.kop)
    pp.pprint(h.stat)
    pp.pprint(h.cat)
    h.stat['7'] = ("Gloekgloekgloe", 7, -1)
    h.cat["X"] = ("Ahum ahum", 7, -1)
    h.kop['4'] = ("Oplossing/SvZ", "opl")
    print("\nNa wijzigen waarden:")
    pp.pprint(h.kop)
    pp.pprint(h.stat)
    pp.pprint(h.cat)
    ## h.stat.pop('7')
    ## h.cat.pop("X")
    h.write()
    h = Settings(fnaam)
    print("\nNa schrijven en opnieuw lezen:")
    pp.pprint(h.kop)
    pp.pprint(h.stat)
    pp.pprint(h.cat)

def test_Actie(fnaam):
    "test routine"
    p = Actie(fnaam, "2009-0002")
    pp.pprint(p.__dict__)
    p = Actie(fnaam, "2011-0002")
    if not p.exists:
        p = Actie(fnaam, "0")
        p.over = "test"
        p.titel = "nieuwe actie"
        p.events.append((dt.datetime.today().isoformat(' ')[:19],
            'titel gewijzigd in "{0}: {1}"'.format(p.over, p.titel)))
        p.set_soort("probleem")
        p.set_status("in behandeling")
        pp.pprint(p.__dict__)
    else:
        p.list()
        return
    p.list()
    p.melding = "Het is niet gebeurd"
    p.events.append((dt.datetime.today().isoformat(' ')[:19],
        "Meldingtekst aangepast"))
    p.oorzaak = "Het leek maar alsof"
    p.events.append((dt.datetime.today().isoformat(' ')[:19],
        "Beschrijving oorzaak aangepast"))
    p.oplossing = "Dus hebben we teruggedraaid wat we er aan gedaan hebben"
    p.events.append((dt.datetime.today().isoformat(' ')[:19],
        "Beschrijving oplossing aangepast"))
    ## p.vervolg = ""
    p.status = 2
    p.set_arch(True)
    ## p.events.append((dt.datetime.today().isoformat(' ')[:19], "Actie heropend"))
    p.list()
    ## return
    p.write()

if __name__ == "__main__":
    fnm = "_basic"
    ## test_getsql()
    ## test_doesql()
    ## test_get_acties(fnm)
    ## test_Settings(fnm)
    test_Actie(fnm)
