# -*- coding: utf-8 -*-
"""dml voor probreg va de ORM van de Django versie

importeer settings uit top package omdat Django het wil
lees apps.dat uit package dir voor alle huidige projecten
importeer core uit top package voor basis dml routines
importeer models uit alle subdirectories/packages voor benaderen gewenste data
"""
from __future__ import print_function

import sys
import os
## import pprint as pp
import datetime as dt
import collections

import pathlib
ROOT = pathlib.Path("/home/albert/projects/actiereg")
sys.path.append(str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "actiereg.settings")


def get_projnames():
    data = []
    with APPS.open() as f_in:
        for line in f_in:
            sel, naam, titel, oms = line.strip().split(";")
            if sel == "X":
                data.append((naam, titel.capitalize(), oms))
    data = data
    return sorted(data)

import importlib
APPS = ROOT / 'actiereg' / "apps.dat"
MY = {}
for proj in get_projnames():
    name = proj[0]
    if name == 'basic':
        name = '_basic'
    MY[name] = importlib.import_module('actiereg.{}.models'.format(name))


import django
django.setup()

from django.core.exceptions import ObjectDoesNotExist
import django.contrib.auth.models as aut
USER = aut.User.objects.get(pk=2)

import actiereg.core as core
from actiereg._basic.sample_data import soort_list, stat_list, page_list
from actiereg._basic.models import ORIENTS, SORTFIELDS, CHOICES, OP_CHOICES

import logging
def log(msg, *args, **kwargs):
    if 'DEBUG' in os.environ and os.environ['DEBUG']:
        logging.info(msg, *args, **kwargs)

from probreg.shared import DataError


def get_acties(naam, select=None, arch=""):
    """
    core.get_acties verwacht twee argumenten: my (de models module uit het actieve
    project) en user (de aangelogde gebruiker).
    eigenijk zijn deze argumenten overbodig doordat de selectie in de database
    opgeslagen wordt en tijdens de aangeroepen functie vanzelf toegepast wordt
    """
    my = MY[naam]

    data = core.get_acties(my, USER.id)
    print([x.nummer for x in data])
    if data:
        actiedata = []
        for actie in data:
            gewijzigd = actie.gewijzigd.strftime('%x %X') if actie.gewijzigd else ''
            linedata = (actie.nummer, actie.start,
                        actie.status.title, actie.status.value,
                        actie.soort.title, actie.soort.value,
                        actie.about, actie.title, gewijzigd)  # .isoformat())
            actiedata.append(linedata)
        return actiedata
    elif len(data) == 0:
        return data
    else:
        raise DataError(naam + " bestaat niet")

class SortOptions:
    """instellingen voor user m.b.t. sortering
    in de django database gerealiseerd d.m.v.
    SortOrder   user volgnr veldnm richting (CHOICES)
    CHOICES = (('asc', 'oplopend'),
               ('desc', 'aflopend'))


    zie methodes core.order/setorder
    """
    def __init__(self, fnaam):
        self.fnaam = fnaam
        self.my = MY[fnaam]
        self.user = USER.id
        self.olddata = {}

    def load_options(self):
        data = {}
        for sorter in self.my.SortOrder.objects.filter(user=self.user):
            data[sorter.volgnr] = (sorter.veldnm, sorter.richting)
        self.olddata = collections.OrderedDict({x: y for x, y in data.items()})
        return data

    def save_options(self, data):
        print('in save_options')
        newdata = collections.OrderedDict({ix: sorter for ix, sorter in data.items()})
        print([(x, y[0], y[1]) for x, y in self.olddata.items()])
        print([(x, y[0], y[1]) for x, y in newdata.items()])
        if newdata == self.olddata:
            return "no changes"
        print('saving new options')
        self.my.SortOrder.objects.filter(user=self.user).delete()
        if newdata:
            for ix, sorter in newdata.items():
                field, orient = sorter
                self.my.SortOrder.objects.create(user=self.user,
                                                 volgnr=ix,
                                                 veldnm=field,
                                                 richting=orient)


class SelectOptions:
    """instellingen voor user m.b.t. selectie
    in de django database gerealiseerd d.m.v.
    Selection   user veldnm operator (OP_CHOICES) extra (CHOICES) value
    CHOICES = (('  ', '  '),
               ('EN', 'en'),
               ('OF', 'of'))
    OP_CHOICES = (('LT', 'kleiner dan'),
                  ('GT', 'groter dan'),
                  ('EQ', 'gelijk aan'),
                  ('NE', 'ongelijk aan'),
                  ('INCL', 'bevat'),
                  ('EXCL', 'bevat niet'))

    zie methodes core.select/setsel
    """

    def __init__(self, fnaam):
        self.fnaam = fnaam
        self.my = MY[fnaam]
        self.user = USER.id

    def load_options(self):
        data = {"arch": 0, "gewijzigd": [], "nummer": [],
                "soort": [], "status": [], "titel": []}
        for sel in self.my.Selection.objects.filter(user=self.user):
            if sel.veldnm == "soort":
                data[sel.veldnm].append(sel.value)
            elif sel.veldnm == "status":
                data[sel.veldnm].append(sel.value)
            elif sel.veldnm == "arch":
                data[sel.veldnm] += 1
            elif sel.veldnm == "nummer":
                if sel.extra.strip():
                    data["nummer"].append(sel.extra.lower())
                data["nummer"].append((sel.value, sel.operator))
            elif sel.veldnm in ("about", "title"):
                if not data['titel']:
                    data["titel"].append((sel.value, sel.operator))
        self.olddata = collections.OrderedDict({x: y for x, y in sorted(data.items())})
        return data

    def save_options(self, data):
        newdata = collections.OrderedDict({"arch": 0, "gewijzigd": [], "nummer": [],
                                         "soort": [], "status": [], "titel": []})

        value = []
        min_value = data.get("idgt", '')
        if min_value:
            value.append((min_value, 'GT'))
        oper = data.get("id", '') # waarde "and" of "or"
        if oper:
            value.append(oper.lower())
        max_value = data.get("idlt", '')
        if max_value:
            value.append((max_value, 'LT'))
        sel_id = min_value or max_value
        newdata['nummer'] = value

        name = 'soort'
        soorten = data.get(name, [])
        newdata[name] = soorten
        name = 'status'
        stats = data.get(name, [])
        newdata[name] = stats

        name = 'titel'
        about = data.get(name, [])
        newdata[name] = about

        # django view
        name = 'arch'
        arch = data.get(name, 0)  # "arch" of "alles"
        newdata[name] = arch

        if newdata and newdata == self.olddata:
            return "no changes"

        self.my.Selection.objects.filter(user=self.user).delete()
        no_extra = "  "
        if sel_id:
            if min_value:
                ok = self.my.Selection.objects.create(user=self.user,
                                                      veldnm="nummer", operator="GT",
                                                      extra=no_extra,
                                                      value=min_value)
            if max_value:
                ok = self.my.Selection.objects.create(user=self.user,
                                                      veldnm="nummer", operator="LT",
                                                      extra=oper.upper(),
                                                      value=max_value)
        if soorten:
            extra = no_extra
            for srt in soorten:
                ok = self.my.Selection.objects.create(user=self.user,
                                                      veldnm="soort", operator="EQ",
                                                      extra=extra, value=srt)
                extra = "OR"
        if stats:
            extra = no_extra
            for stat in stats:
                ok = self.my.Selection.objects.create(user=self.user,
                                                      veldnm="status", operator="EQ",
                                                      extra=extra, value=stat)
                extra = "OR"
        if about:
                ok = self.my.Selection.objects.create(user=self.user, veldnm="about",
                                                      operator="INCL",
                                                      extra=no_extra, value=about)
                ok = self.my.Selection.objects.create(user=self.user,
                                                      veldnm="title", operator="INCL",
                                                      extra='OF', value=about)
        if arch:
            ok = self.my.Selection.objects.create(user=self.user,
                                                  veldnm="arch", operator="EQ",
                                                  extra=no_extra, value=False)
            if arch == "alles":
                ok = self.my.Selection.objects.create(user=self.user,
                                                      veldnm="arch", operator="EQ",
                                                      extra=no_extra, value=True)


class Settings:
    """instellingen voor project

    buffer tussen programma en database
    self.kop is een dict met volgnummer als key en titel en link als waarde
    self.stat is een dict met code als key en titel, volgorde en record-id
        als waarde
    self.cat idem
    de get methoden zijn voor het gemak
    wijzigen doe je maar direct in de attributen (properties van maken?)

    is in django als volgt gedefinieerd:
    Status      title value order
    Soort       title value order
    Page        title link order
    zou anders bijgewerkt kunnen worden maar zo werkt deze applicatie niet
    """
    def __init__(self, fnaam=""):
        self.imagecount = 0   # compatibility with dml_xml.py
        self.exists = self.meld = ''
        self.kop, self.stat, self.cat = {}, {}, {}
        if fnaam == "":
            self.my = MY['_basic']
            self.meld = "Standaard waarden opgehaald"
        else:
            try:
                self.my = MY[fnaam]
            except KeyError as err:
                raise DataError("{} bestaat niet ({})".format(fnaam, err))
        for page in self.my.Page.objects.all().order_by('order'):
            self.kop[str(page.order)] = (page.title, page.link)
        for stat in self.my.Status.objects.all().order_by('order'):
            self.stat[str(stat.value)] = (stat.title, stat.order, stat.value)
        for cat in self.my.Soort.objects.all().order_by('order'):
            self.cat[cat.value] = (cat.title, cat.order, cat.value)
        self.naam = fnaam

    def write(self, srt, sett_id):
        # als ik ze stuk voor stuk ga schrijven hier moet k verwijderen mogelijk maken
        if srt == 'kop':
            item = self.my.Page.objects.all.filter(order='{}'.format(sett_id))
            item.order = int(sett_id)
            item.title, item.link = self.page[sett_id]
            item.save()
        elif srt == 'stat':
            item = self.my.Status.objects.all.filter(value='{}'.format(sett_id))
            item.value = int(sett_id)
            item.title, item.order, _ = self.stat[sett_id]
            item.save()
        elif srt == 'cat':
            item = self.my.Soort.objects.all.filter(value='{}'.format(sett_id))
            item.order = sett_id
            item.title, item.order, _ = self.cat[sett_id]
            item.save()

    def get_statusid(self, waarde):
        "geef id bij statuscode of -tekst"
        log(waarde, type(waarde), sep=" ")
        for code, value in self.stat.items():
            log(code, type(code), value, sep=" ")
            text, sortkey, row_id = value
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

    def get_statuscode(self, waarde):
        "geef code bij statusid"
        ## try:
            ## return self.stat[waarde][0]
        ## except KeyError:
            ## pass
        for text, sortkey, row_id in self.stat.values():
            if waarde == sortkey:   #  or waarde == row_id:
                return row_id   # text
        raise DataError("Geen omschrijving gevonden bij statuscode of -id '{}'".format(
            waarde))

    def get_soortcode(self, waarde):
        "geef code bij soortid"
        ## try:
            ## return self.cat[waarde][0]
        ## except KeyError:
            ## pass
        for text, sortkey, row_id in self.cat.values():
            if waarde == sortkey:   #  or waarde == row_id:
                return row_id   # text
        raise DataError("Geen omschrijving gevonden bij soortcode of -id '{}'".format(
            waarde))


class Actie:
    """lijst alle gegevens van een bepaald item

    is in django als volgt gedefinieerd:
    Actie       nummer start starter (User) about title gewijzigd lasteditor (User)
                soort ('Soort') status ('Status') behandelaar (User) arch
                melding oorzaak oplossing vervolg
    Event       actie ('Actie') start starter (User) text
    """
    def __init__(self, naam, id_):
        # self.my is gerelateerd aan naam
        self.my = MY[naam]
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
        if self.id in (0, "0"):
            self.nieuw()
        else:
            self._actie = self.my.Actie.objects.filter(nummer='{}'.format(self.id))
            if self._actie:
                self._actie = self._actie[0]
        self.read()

    def nieuw(self):
        "nieuwe actie initialiseren"
        self._actie = self.my.Actie()
        nw_date = dt.datetime.now()
        volgnr = 0
        # replaced by code from core.py -
        aant = self.my.Actie.objects.count()
        nw_date = dt.datetime.now()
        if aant:
            last = self.my.Actie.objects.all()[aant - 1]
            jaar, volgnr = last.nummer.split("-")
            volgnr = int(volgnr) if int(jaar) == nw_date.year else 0
        volgnr += 1
        #end replace
        self._actie.nummer = "{0}-{1:04}".format(nw_date.year, volgnr)
        try:
            self._actie.soort = self.my.Soort.objects.get(value="")
        except ObjectDoesNotExist:
            self._actie.soort = self.my.Soort.objects.get(value=" ")
        self._actie.status = self.my.Status.objects.get(value="0")
        self._actie.datum = nw_date.strftime('%x %X')  # .isoformat(' ')  # [:19]
        self._actie.starter = self._actie.behandelaar = USER
        self._actie.lasteditor = USER
        self._actie.save()
        self.events = [(self._actie.datum, "Actie opgevoerd")]

    def read(self):
        "gegevens lezen van een bepaalde actie"
        if not self._actie:
            self.exists = False
            return
        actie = self._actie.id
        self.id = self._actie.nummer # verandert niet
        self.datum = self._actie.start.strftime('%x %X')  # .isoformat(' ') # verandert niet
        self.over = self.over_oud = self._actie.about
        self.titel = self.titel_oud = self._actie.title
        if self._actie.gewijzigd:
            self.updated = self._actie.gewijzigd.strftime('%x %X')  # .isoformat()[:19]
        else:
            self.updated = ''
        self.status = self.status_oud = self._actie.status.value
        self.soort = self.soort_oud = self._actie.soort.value
        self.arch = self.arch_oud = self._actie.arch
        self.melding = self.melding_oud = self._actie.melding
        self.oorzaak = self.oorzaak_oud = self._actie.oorzaak
        self.oplossing = self.oplossing_oud = self._actie.oplossing
        self.vervolg = self.vervolg_oud = self._actie.vervolg
        ## self.events = [(x.start, x.text) for x in self._actie.events.all()]
        self.events = []
        for x in self._actie.events.all():
            start = x.start.strftime('%x %X') if x.start else '(data/time unknown)'
            self.events.append((start, x.text))
        self.events_oud = self.events
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
        self.store_event('status gewijzigd in "{}"'.format(self.get_statustext()))

    def set_soort(self, waarde):
        "stel soort in (code of tekst) met controle a.h.v. project settings"
        self.soort = self.settings.get_soortid(waarde)
        self.store_event('status gewijzigd in "{}"'.format(self.get_soorttext()))

    def set_arch(self, waarde):
        "stel archiefstatus in - garandeert dat dat een boolean waarde wordt"
        if waarde:
            self.arch = True
            txt = "Actie gearchiveerd"
        else:
            self.arch = False
            txt = "Actie herleefd"
        self.store_event(txt)

    def store_gewijzigd(self, msg, txt):
        self.events.append((dt.datetime.today().isoformat(' '),  # [:19],
                            '{} gewijzigd in "{}"'.format(msg, txt)))

    def store_event(self, txt):
        self.events.append((dt.datetime.today().isoformat(' '), txt)) # [:19],

    def write(self):
        "actiegegevens (terug)schrijven"
        mld = []
        if self.over != self.over_oud:
            self.store_gewijzigd('onderwerp', self.over)
        if self.titel != self.titel_oud:
            self.store_gewijzigd(my, 'titel', self.title)
        if self.status != self.status_oud:
            self.store_gewijzigd(my, 'status', self.status)
        if self.soort != self.soort_oud:
            self.store_gewijzigd(my, 'soort', self.soort)
        if self.arch != self.arch_oud:
            self.store_gewijzigd(my, 'onderwerp', self.over)
        if self.melding != self.melding_oud:
            self.store_event("Meldingtekst aangepast")
        if self.oorzaak != self.oorzaak_oud:
            msg = self.store_event("Beschrijving oorzaak aangepast")
        if self.oplossing != self.oplossing_oud:
            self.store_event("Beschrijving oplossing aangepast")
        if self.vervolg != self.vervolg_oud:
            self.store_event("Beschrijving vervolgactie aangepast")
        self._actie.save()
        for item in self.events:
            if item in self.events_oud:
                continue
            date, msg = item
            core.store_event_with_date(self.my, msg, self._actie, date, USER)
        self.read()

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
        for item in self.events.all():
            result.append("\t {} - {}".format(x.start, x.text))
        if self.arch:
            result.append("Actie is gearchiveerd.")
        # for now
        return result
