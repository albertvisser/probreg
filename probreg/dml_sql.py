"""dml voor probreg met sql om dezelfde data te gebruiken die de Django versie
gebruikt

vervallen omdat we nu de versie gebruiken die met het Django ORM werkt
"""
from __future__ import print_function

## import sys
import os
import datetime as dt
import sqlite3 as sql
from contextlib import closing
import logging
from probreg.shared import DataError, DBLOC, USER, kopdict, statdict, catdict


def log(msg, *args, **kwargs):
    "write message to log depending on DEBUG setting"
    if 'DEBUG' in os.environ and os.environ['DEBUG']:
        logging.info(msg, *args, **kwargs)


def getsql(con, cmd, item=None):
    """retrieval sql uitvoeren en resultaat teruggeven

    resultaat = []: query mislukt
    """
    log("getsql tweede argument: {0}".format(cmd))
    log("getsql derde  argument: {0}".format(item))
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
    log("doesql tweede argument: {0}".format(cmd))
    log("doesql derde  argument: {0}".format(item))
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


def get_acties(naam, select=None, arch="", user=None):
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
    het laatste argument `user` wordt niet gebruikt maar is voor compatibiliteit met de django versie
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
    item_lt = select.pop("idlt", "")
    enof = select.pop("id", "")
    item_gt = select.pop("idgt", "")
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
    item = select.pop("soort", "")
    if item:
        log(item)
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
    item = select.pop("status", "")
    if item:
        log(item)
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
    item = select.pop("titel", "")
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
        raise DataError("Foutieve waarde voor archief opgegeven "
                        "(moet niks, 'arch'  of 'alles' zijn)")
    con = sql.connect(DBLOC)
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
        self.imagecount = 0   # compatability with dml_xml.py
        self.meld = ''
        if fnaam == "":
            self.meld = "Standaard waarden opgehaald"
            return
        self.naam = fnaam
        self.read()

    def read(self):
        "settings lezen"
        with closing(sql.connect(DBLOC)) as con:
            meld = self._read(con)
            self.exists = meld == ''

    def _read(self, con):
        "get settings from database"
        con.row_factory = sql.Row
        try:
            data = getsql(con,
                          'select * from {0}_page order by "order"'.format(self.naam))
        except DataError as err:
            self.meld = "{} bestaat niet ({})".format(self.naam, err)
            return
        self.kop = {}
        for row in data:
            self.kop[str(row["order"])] = (row["title"], row["link"])

        try:
            data = getsql(con, "select * from {0}_status".format(self.naam))
        except DataError as err:
            self.meld = "Er is iets misgegaan ({})".format(err)
            return
        self.stat = {}
        for row in data:
            self.stat[str(row["value"])] = (row["title"], row["order"], row["id"])

        try:
            data = getsql(con, "select * from {0}_soort".format(self.naam))
        except DataError as err:
            self.meld = "Er is iets misgegaan ({})".format(err)
            return
        self.cat = {}
        for row in data:
            self.cat[row["value"]] = (row["title"], row["order"], row["id"])

    def write(self, srt):
        "settings terugschrijven"
        with closing(sql.connect(DBLOC)) as con:
            if self.exists:
                rtn = self._write_existing(con, srt)
            else:
                rtn = self._write_new(con, srt)
            if rtn:
                con.rollback()
                raise DataError(rtn)
            else:
                con.commit()

    def _write_existing(self, con, srt):
        "modify existing settings in datadase"
        con.row_factory = sql.Row
        if srt == 'kop':
            _pages = getsql(con,
                            'select * from {0}_page order by "order"'.format(self.naam))
            rtn = 0
            for item in _pages:
                idx = str(item["order"])
                if self.kop[idx] != (item["title"], item["link"]):
                    rtn = doesql(con, "update {}_page set title = ?,"
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
                    if rtn:
                        break
        return rtn

    def _write_new(self, con, srt):
        "initialize new settings in database"
        if srt == 'kop':
            for order, item in self.kop:
                rtn = doesql(con, "insert into {0}_page values"
                             ' (?,?,?,?)'.format(self.naam),
                             (order + 1, item[0], item[1], order))
                if rtn:
                    break
        return rtn

    def get_statusid(self, waarde):
        "geef id bij statuscode of -tekst"
        log(waarde, type(waarde), sep=" ")
        for code, value in self.stat.items():
            log(code, type(code), value, sep=" ")
            text, sortkey, row_id = value
            ## if int(waarde) == key or str(waarde) == key or waarde == value[0]:
            if waarde == code or waarde == text:
                return row_id
        raise DataError("geen status bij code of omschrijving '{}' gevonden".format(
            waarde))

    def get_soortid(self, waarde):
        "geef id bij soortcode of -tekst"
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

# connection als context manager
# def connect_db():
#     return sql.connect(DATABASE)

    ## with closing(connect_db()) as db:
        ## db.row_factory = sql.Row
        ## cur = db.cursor()


class Actie:
    """lijst alle gegevens van een bepaald item"""
    def __init__(self, naam, id_):
        self.meld = ''
        self.naam = naam
        ## if naam == 'Demo':
            ## naam = '_basic'
        self.settings = Settings(naam)
        self.id = id_
        self.over = self.titel = self.gewijzigd = ''
        self.status, self.soort, self.arch = 1, 1, False
        self.melding = self.oorzaak = self.oplossing = self.vervolg = ''
        self.exists = False
        self.imagelist = []                     # compatibility
        self.con = sql.connect(DBLOC)
        self.con.row_factory = sql.Row
        if self.id in (0, "0"):
            self.nieuw()
        else:
            self.read()

    def nieuw(self):
        "nieuwe actie initialiseren"
        try:
            acties = getsql(self.con, "select id, "
                            "nummer from {0}".format("{0}_actie".format(self.naam)))
        except DataError as err:
            raise DataError("datafile bestaat niet ({})".format(str(err)))
        nw_date = dt.datetime.now()
        ## for item in acties:
            ## last = item
        last = acties[-1]
        self.nieuw_id = last["id"] + 1
        ## log(self.nieuw_id)
        jaar, volgnr = last["nummer"].split("-", 1)
        nieuwnummer = int(volgnr) + 1 if int(jaar) == nw_date.year else 1
        self.id = "{0}-{1:04}".format(nw_date.year, nieuwnummer)
        self.status = self.soort = 1
        self.datum = dt.datetime.today().isoformat(' ')  # [:19]
        self.events = [(self.datum, "Actie opgevoerd")]

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
            ## log(item)
        ## return
        if len(data) == 0:
            self.exists = False
            return
        elif not data:
            raise DataError(self.naam + " bestaat niet")
        for item in data:
            ## log(item)
            (actie, self.id, self.datum, self.over, self.titel, self.updated,
             self.status, self.soort, self.arch, self.melding, self.oorzaak,
             self.oplossing, self.vervolg) = item
            # string van maken omdat het door sqlite  blijkbaar als int wordt geretourneerd:
            self.status = str(self.status)
            ## self.titel = " - ".join((self.over, self.titel))
        data = getsql(self.con, "select id, start, starter_id, text from"
                      " {0}_event where actie_id = ?".format(self.naam), (actie,))
        self.events = [(item[1], item[3]) for item in data]
        self.exists = True

    def get_statustext(self):
        "geef tekst bij statuscode"
        log(self.status)
        return self.settings.get_statustext(self.status)

    def get_soorttext(self):
        "geef tekst bij soortcode"
        return self.settings.get_soorttext(self.soort)

    def set_status(self, waarde):
        "stel status in (code of tekst) met controle a.h.v. project settings"
        self.status = self.settings.get_statusid(waarde)
        ## log(waarde, self.status, sep = " ")
        self.events.append((dt.datetime.today().isoformat(' '),  # [:19],
                            'status gewijzigd in "{0}"'.format(self.get_statustext())))

    def set_soort(self, waarde):
        "stel soort in (code of tekst) met controle a.h.v. project settings"
        self.soort = self.settings.get_soortid(waarde)
        ## log(waarde, self.soort, sep = " ")
        self.events.append((dt.datetime.today().isoformat(' '),  # [:19],
                            'soort gewijzigd in "{0}"'.format(self.get_soorttext())))

    def set_arch(self, waarde):
        "stel archiefstatus in - garandeert dat dat een boolean waarde wordt"
        if waarde:
            self.arch = True
            self.events.append((dt.datetime.today().isoformat(' '),  # [:19],
                                "Actie gearchiveerd"))
        else:
            self.arch = False
            self.events.append((dt.datetime.today().isoformat(' '),  # [:19],
                                "Actie herleefd"))

    def write(self):
        "actiegegevens (terug)schrijven"
        if self.exists:
            log("write: update actie {0}".format(self.id))
            data = getsql(self.con,
                          "select nummer, start, about, title, gewijzigd, status_id, "
                          "soort_id, arch, melding, oorzaak, oplossing, vervolg, id "
                          "from {0}_actie where nummer = ?".format(self.naam), (self.id,))
            if data:
                for item in data:
                    log("write: item", item, sep=" ")
                    data = [x for x in item]
                    actie_id = data.pop()
                log("write: data", data, sep=" ")
            else:
                raise DataError("Current record not found")
        else:
            # FIXME: dit wordt niet altijd aangeroepen volgend op self.nieuw() waarin nieuw_id wordt ingesteld
            log("write: nieuwe actie {0}".format(self.nieuw_id))
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
        items.append(dt.datetime.today().isoformat(' '))  # [:19])
        if self.exists:
            items.append(self.id)
            log("write update:", insert, sep=" ")
            log("write update:", items, sep=" ")
            rtn = doesql(self.con, "update {}_actie set {} where nummer = ?".format(
                self.naam, ", ".join(update)), items)
        else:
            insert = ["id", "nummer", "start", "starter_id", "lasteditor_id",
                      "behandelaar_id"] + insert
            mask = ", ".join(["?" for x in insert])
            items = [self.nieuw_id, self.id, self.datum, USER, USER, USER] + items
            log("write nieuw:", insert, sep=" ")
            log("write nieuw:", items, sep=" ")
            rtn = doesql(self.con, "insert into {0}_actie ({1}) values ({2})".format(
                self.naam, ", ".join(insert), mask), items)
        if rtn:
            self.con.rollback()
            raise DataError(str(rtn))
        data = getsql(self.con, "select id, start, starter_id, text from {0}_event "
                      "where actie_id = ?".format(self.naam), (actie_id,))
        ## if not data:
            ## self.con.rollback()
            ## raise DataError("Problem getting events")
        current_events = [x for x in data] if data else []
        last_id = 0
        data = getsql(self.con, "select id from {0}_event order by id desc".format(
            self.naam))
        for item in data:
            last_id = item[0]
            break
            ## log(last_id, end=",")
        ## last_id = data[0][1]
        for idx, item in enumerate(self.events):
            start, text = item
            if idx >= len(current_events):
                last_id = last_id + 1
                rtn = doesql(self.con, "insert into {0}_event (id, start, starter_id,"
                             " text, actie_id) values(?, ?, ?, ?, ?)".format(self.naam),
                             (last_id, start, USER, text, actie_id))
            elif (start, text) != (current_events[idx][1], current_events[idx][3]):
                rtn = doesql(self.con, "update {0}_event set text = ? "
                             "where start = ? and actie_id = ?".format(self.naam),
                             (text, start, actie_id))
        if rtn:
            self.con.rollback()
            raise DataError(rtn)
        self.con.commit()
        self.exists = True

    def clear(self):                            # compatibility with dml_xml.py
        "images opruimen"
        pass

    def list(self):
        "actiegegevens uitlijsten"
        result = ["%s %s gemeld op %s status %s %s" % (self.get_soorttext(),
                                                       self.id,
                                                       self.datum,
                                                       self.status,
                                                       self.get_statustext())]
        result.append("Titel: {}".format(self.titel))
        result.append("Melding: {}".format(self.melding))
        result.append("Oorzaak: {}".format(self.oorzaak))
        result.append("Oplossing: {}".format(self.oplossing))
        result.append("Vervolg: {}".format(self.vervolg))
        result.append("Verslag:")
        for date, text in self.events:
            result.append("\t {} - {}".format(date, text))
        if self.arch:
            result.append("Actie is gearchiveerd.")
        # for now
        return result
