"""dml voor probreg va de ORM van de Django versie

importeer settings uit top package omdat Django het wil
lees apps.dat uit package dir voor alle huidige projecten
importeer core uit top package voor basis dml routines
importeer models uit alle subdirectories/packages voor benaderen gewenste data
"""
import sys
import os
import datetime as dt
import collections
import importlib

import pathlib
ROOT = pathlib.Path("~/projects/actiereg").expanduser()   # location of actiereg project
sys.path.append(str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "actiereg.settings")
APPS = ROOT / 'actiereg' / "apps.dat"

import django
django.setup()

from django.core.exceptions import ObjectDoesNotExist
import django.contrib.auth.models as auth
from django.contrib.auth import hashers


def get_projnames():
    "return a list of registered projects"
    data = []
    with APPS.open() as f_in:
        for line in f_in:
            sel, naam, titel, oms = line.strip().split(";")
            if sel == "X":
                data.append((naam, titel, oms))
    return sorted(data)


MY = {}
for proj in get_projnames():
    name = proj[0]
    if name == 'basic':
        name = '_basic'
    MY[name] = importlib.import_module(f'actiereg.{name}.models')

from actiereg import core
from actiereg._basic.models import SORTFIELDS   # used in main.py
dtformat = '%d-%m-%Y %H:%I:%S'  # was '%x %X' en daarvoor .isoformat(' ')


def get_user(inp):
    """retrieve user by username
    """
    try:
        test = auth.User.objects.get(username=inp)
    except auth.User.DoesNotExist:
        test = None
    return test


def validate_user(naam, passw, project):
    """check username and password; if ok, return user and whether user is assigned to project
    and whether user has admin rights
    """
    user = get_user(naam)
    if not user:
        return '', False, False
    if not hashers.check_password(passw, user.password):
        return '', False, False
    return user, core.is_user(project, user), core.is_admin(project, user)


class DataError(ValueError):    # Exception):
    "Eigen all-purpose exception - maakt resultaat testen eenvoudiger"


def get_acties(naam, select=None, arch="", user=None):
    """lees acties voor een bepaald project
    de extra argumenten select en arch zijn alleen voor compatibiliteit met de xml versie.
    core.get_acties verwacht twee argumenten: my (de models module uit het actieve
    project) en user (de aangelogde gebruiker) en past zelf de in de selectie en
    sortering toe die in de database zijn opgeslagen voor de betreffende gebruiker.
    Om die reden is ook de `user` parameter _als laatste_ toegevoegd
    """
    try:
        my = MY[naam]
    except KeyError as exc:
        raise DataError(naam + " bestaat niet") from exc    # pylint W0707

    userid = user.id if user else 0
    data = core.get_acties(my, userid)
    if data:
        actiedata = []
        for actie in data:
            # gewijzigd = actie.gewijzigd.strftime('%x %X') if actie.gewijzigd else ''
            gewijzigd = actie.gewijzigd.strftime(dtformat) if actie.gewijzigd else ''
            linedata = (actie.nummer, actie.start,
                        actie.status.title, actie.status.value,
                        actie.soort.title, actie.soort.value,
                        actie.about, actie.title, gewijzigd, actie.arch)
            actiedata.append(linedata)
        return actiedata
    return []


class SortOptions:
    """instellingen voor user m.b.t. sortering
    in de django database gerealiseerd d.m.v.
    SortOrder   user volgnr veldnm richting (CHOICES)
    CHOICES = (('asc', 'oplopend'),
               ('desc', 'aflopend'))


    zie methodes core.order/setorder
    """
    def __init__(self, fnaam, user=None):
        self.fnaam = fnaam
        self.my = MY[fnaam]
        self.user = user.id if user else 0
        self.olddata = {}

    def load_options(self):
        "lees opties"
        data = {}
        for sorter in self.my.SortOrder.objects.filter(user=self.user):
            data[sorter.volgnr] = (sorter.veldnm, sorter.richting)
        self.olddata = dict(data.items())  # collections.OrderedDict({x: y for x, y in data.items()})
        return data

    def save_options(self, data):
        "schrijf opties terug"
        newdata = dict(data.items())  # collections.OrderedDict({ix: sorter for ix, sorter in data.items()})
        if newdata == self.olddata:
            return "no changes"
        self.my.SortOrder.objects.filter(user=self.user).delete()
        if newdata:
            for ix, sorter in newdata.items():
                field, orient = sorter
                self.my.SortOrder.objects.create(user=self.user,
                                                 volgnr=ix,
                                                 veldnm=field,
                                                 richting=orient)
        return ''


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

    def __init__(self, fnaam, user=None):
        self.fnaam = fnaam
        self.my = MY[fnaam]
        self.user = user.id if user else 0

    def load_options(self):
        "lees opties"
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
                    data["nummer"].append((sel.extra.lower(),))
                data["nummer"].append((sel.value, sel.operator))
            elif sel.veldnm in ("about", "title"):
                if sel.extra.strip():
                    data["titel"].append((sel.extra.lower(),))
                data["titel"].append((sel.veldnm, sel.value))
        data['arch'] = {0: '', 1: "arch", 2: "alles"}[data['arch']]
        self.olddata = dict(sorted(data.items()))
        return data

    def save_options(self, data):
        "schrijf opties terug"
        newdata = collections.OrderedDict({"arch": 0, "gewijzigd": [], "nummer": [],
                                           "soort": [], "status": [], "titel": []})

        value = []
        min_value = data.get("idgt", '')
        if min_value:
            value.append((min_value, 'GT'))
        oper = data.get("id", '')  # waarde "and" of "or"
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
        name = 'arch'
        arch = data.get(name, '')
        newdata[name] = arch
        # for name, default  in (('soort', []), ('status', []), ('titel', []), ('arch', '')):
        #     value = data.get(name, [])
        #     newdata[name] = value

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
            extra = no_extra
            for item in about:
                if len(item) == 1:
                    extra = item[0].upper()
                elif item:
                    ok = self.my.Selection.objects.create(user=self.user,
                                                          veldnm=item[0], operator="INCL",
                                                          extra=extra, value=item[1])
        if arch:
            ok = self.my.Selection.objects.create(user=self.user,
                                                  veldnm="arch", operator="EQ",
                                                  extra=no_extra, value=False)
            if arch == 'alles':
                ok = self.my.Selection.objects.create(user=self.user,
                                                      veldnm="arch", operator="EQ",
                                                      extra=no_extra, value=True)
        return ''


class Settings:
    """instellingen voor project

    buffer tussen programma en database
    self.kop is een dict met volgnummer als key en titel en link als waarde
    self.stat is een dict met code als key en titel, volgorde en record-id
        als waarde
    self.cat idem

    is in django als volgt gedefinieerd:
    Status      title value order
    Soort       title value order
    Page        title link order
    zou anders bijgewerkt kunnen worden maar zo werkt deze applicatie niet
    """
    def __init__(self, fnaam=""):
        self.imagecount = 0   # compatibility with dml_xml.py
        self.startitem = ''   # compatibility with dml_xml.py
        self.exists = self.meld = ''
        self.kop, self.stat, self.cat = {}, {}, {}
        if fnaam == "":
            self.my = MY['_basic']
            self.meld = "Standaard waarden opgehaald"
        else:
            self.my = MY[fnaam]
        for page in self.my.Page.objects.all().order_by('order'):
            self.kop[str(page.order)] = (page.title, page.link)
        for stat in self.my.Status.objects.all().order_by('order'):
            # self.stat[str(stat.value)] = (stat.title, stat.order, stat.value)
            # self.stat[str(stat.value)] = (stat.title, stat.order)
            self.stat[stat.value] = (stat.title, stat.order)
        for cat in self.my.Soort.objects.all().order_by('order'):
            # self.cat[cat.value] = (cat.title, cat.order, cat.value)
            self.cat[cat.value] = (cat.title, cat.order)
        self.naam = fnaam

    # def write(self, srt, sett_id):
    #     "schrijf alle settings terug"
    #     # als ik ze stuk voor stuk ga schrijven hier moet ik verwijderen mogelijk maken
    #     if srt == 'kop':
    #         item = self.my.Page.objects.get_or_create(order='{}'.format(sett_id))[0]
    #         item.title, item.link = self.kop[sett_id]
    #         item.save()
    #     elif srt == 'stat':
    #         item = self.my.Status.objects.get_or_create(value='{}'.format(sett_id))[0]
    #         item.title, item.order, _ = self.stat[sett_id]
    #         item.save()
    #     elif srt == 'cat':
    #         item = self.my.Soort.objects.get_or_create(value='{}'.format(sett_id))[0]
    #         item.title, item.order, _ = self.cat[sett_id]
    #         item.save()

    def write(self):
        "schrijf alle settings terug"
        # eerst controle of te verwijderen statussen / soorten nog gebruikt worden
        stats_to_delete = []
        for stat in self.my.Status.objects.all():
            if stat.value not in self.stat:  # .keys():
                data = self.my.Actie.objects.filter(status=stat)
                if data:
                    return 'status', stat.value  # status wordt nog gebruikt, afbreken
                stats_to_delete.append(stat.id)
        cats_to_delete = []
        for cat in self.my.Soort.objects.all():
            if cat.value not in self.cat:  # .keys():
                data = self.my.Actie.objects.filter(soort=cat)
                if data:
                    return 'soort', cat.value  # soort wordt nog gebruikt, afbreken
                cats_to_delete.append(cat.id)
        for order, heading in self.kop.items():
            page = self.my.Page.objects.get(order=order)
            page.title, page.link = heading
            page.save()
        self.my.Status.objects.filter(id__in=stats_to_delete).delete()
        for value, statdata in self.stat.items():
            name, row = statdata
            try:
                stat = self.my.Status.objects.get(value=value)
            except self.my.Status.DoesNotExist:
                self.my.Status.objects.create(value=value, title=name, order=row)
            else:
                stat.title, stat.order = name, row
                stat.save()
        self.my.Soort.objects.filter(id__in=cats_to_delete).delete()
        for value, catdata in self.cat.items():
            name, row = catdata
            try:
                cat = self.my.Soort.objects.get(value=value)
            except self.my.Soort.DoesNotExist:
                self.my.Soort.objects.create(value=value, title=name, order=row)
            else:
                cat.title, cat.order = name, row
                cat.save()
        return ''


class Actie:
    """lijst alle gegevens van een bepaald item

    is in django als volgt gedefinieerd:
    Actie       nummer start starter (User) about title gewijzigd lasteditor (User)
                soort ('Soort') status ('Status') behandelaar (User) arch
                melding oorzaak oplossing vervolg
    Event       actie ('Actie') start starter (User) text
    """
    def __init__(self, naam, actie_id, user):
        # self.my is gerelateerd aan naam
        self.my = MY[naam]
        self.meld = ''
        self.naam = naam
        ## if naam == 'Demo':
            ## naam = '_basic'
        self.settings = Settings(naam)
        self.id = actie_id
        self.over = self.titel = self.gewijzigd = ''
        self.status, self.soort, self.arch = 1, 1, False
        self.melding = self.oorzaak = self.oplossing = self.vervolg = ''
        self.exists = False
        self.imagelist = []                     # compatibility
        if self.id in (0, "0"):
            self.nieuw(user)
        else:
            self._actie = self.my.Actie.objects.get(nummer=f'{self.id}')
        self.read()

    def nieuw(self, user):
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
        # end replace
        self._actie.nummer = f"{nw_date.year}-{volgnr:04}"
        try:
            self._actie.soort = self.my.Soort.objects.get(value="")
        except ObjectDoesNotExist:
            self._actie.soort = self.my.Soort.objects.get(value=" ")
        self._actie.status = self.my.Status.objects.get(value="0")
        self._actie.start = nw_date.strftime('%x %X')  # .isoformat(' ')  # [:19]
        self._actie.starter = self._actie.behandelaar = user
        self._actie.lasteditor = user
        self._actie.save()
        self.events = [(self._actie.start, "Actie opgevoerd")]

    def read(self):
        "gegevens lezen van een bepaalde actie"
        if not self._actie:
            self.exists = False
            return
        ## actie = self._actie.id
        self.id = self._actie.nummer  # verandert niet
        self.datum = self._actie.start.strftime(dtformat)
        self.over = self.over_oud = self._actie.about
        self.titel = self.titel_oud = self._actie.title
        # if self._actie.gewijzigd:  # is net als start een auto_now_add veld
        self.updated = self._actie.gewijzigd.strftime(dtformat)
        # else:
        #    self.updated = ''
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
            start = x.start.strftime(dtformat) if x.start else '(data/time unknown)'
            self.events.append((start, x.text))
        self.events_oud = self.events[:]
        self.exists = True

    def get_statustext(self):
        "geef tekst bij statuscode"
        # log(self.status)
        # return self.settings.get_statustext(self.status)
        waarde = self.status
        try:
            return self.settings.stat[waarde][0]
        except KeyError:
            for text, sortkey, row_id in self.settings.stat.values():
                if waarde in (sortkey, row_id):
                    return text
        raise DataError(f"Geen omschrijving gevonden bij statuscode of -id '{waarde}'")

    def get_soorttext(self):
        "geef tekst bij soortcode"
        # return self.settings.get_soorttext(self.soort)
        waarde = self.soort
        try:
            return self.settings.cat[waarde][0]
        except KeyError:
            for text, sortkey, row_id in self.settings.cat.values():
                if waarde in (sortkey, row_id):
                    return text
        raise DataError(f"Geen omschrijving gevonden bij soortcode of -id '{waarde}'")

    def add_event(self, txt):
        "voeg tekstregel toe aan events"
        self.events.append((dt.datetime.today(), txt))

    def write(self, user):
        "actiegegevens (terug)schrijven"
        if self.over != self.over_oud:
            self._actie.about = self.over
        if self.titel != self.titel_oud:
            self._actie.title = self.titel
        if self.status != self.status_oud:
            self._actie.status = self.my.Status.objects.get(value=self.status)
        if self.soort != self.soort_oud:
            self._actie.soort = self.my.Soort.objects.get(value=self.soort)
        if self.arch != self.arch_oud:
            self._actie.arch = self.arch
        if self.melding != self.melding_oud:
            self._actie.melding = self.melding
        if self.oorzaak != self.oorzaak_oud:
            self._actie.oorzaak = self.oorzaak
        if self.oplossing != self.oplossing_oud:
            self._actie.oplossing = self.oplossing
        if self.vervolg != self.vervolg_oud:
            self._actie.vervolg = self.vervolg
        self._actie.lasteditor = user
        self._actie.save()
        for item in self.events:
            if item in self.events_oud:
                continue
            date, msg = item
            core.store_event_with_date(self.my, msg, self._actie, date, user)

    def cleanup(self):                            # compatibility with dml_xml.py
        "images opruimen"
