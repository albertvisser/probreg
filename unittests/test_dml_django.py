import sys
import os
import types
import datetime
import pytest

sys.path.append("/home/albert/projects/actiereg")  # location of actiereg project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "actiereg.settings")

import django
django.setup()

import probreg.dml_django as dml
import actiereg._basic.models as my

FIXDATE = datetime.datetime(2020, 1, 1)

class MockDatetime:
    def utcnow(*args):
        return 'now'
    def today(*args):
        return FIXDATE
    def now():
        return FIXDATE

def test_get_projnames(monkeypatch, capsys):
    testfilename = '/tmp/actieregtestapps.dat'
    with open(testfilename, 'w') as f:
        print('X;bep1;App1;testapp #1', file=f)
        print(';app2;App2;testapp #2', file=f)
        print('X;app3;app3;testapp #3', file=f)
    monkeypatch.setattr(dml, 'APPS', dml.pathlib.Path(testfilename))
    assert dml.get_projnames() == [('app3', 'app3', 'testapp #3'), ('bep1', 'App1', 'testapp #1')]


@pytest.mark.django_db
def test_get_user():
    me = django.contrib.auth.models.User(username='testuser')
    me.save()
    assert dml.get_user('me') is None
    assert dml.get_user('testuser') == me


@pytest.mark.django_db
def test_validate_user(monkeypatch):
    monkeypatch.setattr(dml, 'get_user', lambda x: None)
    assert dml.validate_user('naam', 'passw', 'project') == ('', False, False)
    me = django.contrib.auth.models.User.objects.create(username='testuser')
    # me = django.contrib.auth.models.User(username='testuser')
    # me.save()
    monkeypatch.setattr(dml, 'get_user', lambda x: me)
    monkeypatch.setattr(dml.django.contrib.auth.hashers, 'check_password', lambda *x: False)
    assert dml.validate_user('naam', 'passw', 'project') == ('', False, False)
    monkeypatch.setattr(dml.django.contrib.auth.hashers, 'check_password', lambda *x: True)
    monkeypatch.setattr(dml.core, 'is_user', lambda *x: True)
    monkeypatch.setattr(dml.core, 'is_admin', lambda *x: True)
    assert dml.validate_user('naam', 'passw', 'project') == (me , True, True)


def test_get_acties(monkeypatch, capsys):
    def mock_get_no_acties(*args):
        print('called core.get_acties() with args', args)
        return []
    def mock_get_acties(*args):
        print('called core.get_acties() with args', args)
        fixdate = dml.dt.datetime(2020,1,1)
        return [types.SimpleNamespace(nummer='1', start='once', about='me', title='a giant',
            status=types.SimpleNamespace(title='A', value='1'),
            soort=types.SimpleNamespace(title='X', value='x'), gewijzigd='', arch=''),
            types.SimpleNamespace(nummer='2', start='twice', about='me', title='still a giant',
            status=types.SimpleNamespace(title='B', value='2'),
            soort=types.SimpleNamespace(title='Y', value='y'), gewijzigd=fixdate, arch='arch')]
    monkeypatch.setattr(dml, 'MY', {'test': 'stuff'})
    with pytest.raises(dml.DataError) as exc:
        data = dml.get_acties('not_test')
    assert str(exc.value) == 'not_test bestaat niet'
    monkeypatch.setattr(dml.core, 'get_acties', mock_get_no_acties)
    assert dml.get_acties('test') == []
    assert capsys.readouterr().out == "called core.get_acties() with args ('stuff', 0)\n"
    monkeypatch.setattr(dml.core, 'get_acties', mock_get_acties)
    user_jan = types.SimpleNamespace(id=15)
    assert dml.get_acties('test', user_jan) == [
            ('1', 'once', 'A', '1', 'X', 'x', 'me', 'a giant', '', ''),
            ('2', 'twice', 'B', '2', 'Y', 'y', 'me', 'still a giant', '01-01-2020 00:12:00', 'arch')]


def test_sortoptions(monkeypatch, capsys):
    monkeypatch.setattr(dml, 'MY', {'testfile': 'stuff'})
    user_jan = types.SimpleNamespace(id=15)
    testobj = dml.SortOptions('testfile')
    assert testobj.fnaam == 'testfile'
    assert testobj.my == 'stuff'
    assert testobj.user == 0
    assert testobj.olddata == {}
    testobj = dml.SortOptions('testfile', user_jan)
    assert testobj.fnaam == 'testfile'
    assert testobj.my == 'stuff'
    assert testobj.user == 15
    assert testobj.olddata == {}


@pytest.mark.django_db
def test_sortoptions_load(monkeypatch, capsys):
    my.SortOrder.objects.create(user=15, volgnr=1, veldnm='x', richting='asc')
    my.SortOrder.objects.create(user=15, volgnr=2, veldnm='y', richting='asc')
    my.SortOrder.objects.create(user=15, volgnr=3, veldnm='z', richting='desc')
    my.SortOrder.objects.create(user=16, volgnr=4, veldnm='a', richting='asc')
    my.SortOrder.objects.create(user=16, volgnr=5, veldnm='b', richting='asc')
    my.SortOrder.objects.create(user=16, volgnr=6, veldnm='c', richting='desc')
    monkeypatch.setattr(dml, 'MY', {'naam': my})
    testobj = dml.SortOptions('naam', types.SimpleNamespace(id=15))
    assert testobj.load_options() == {1: ('x', 'asc'), 2: ('y', 'asc'), 3: ('z', 'desc')}
    assert testobj.olddata == {1: ('x', 'asc'), 2: ('y', 'asc'), 3: ('z', 'desc')}


@pytest.mark.django_db
def test_sortoptions_save(monkeypatch, capsys):
    monkeypatch.setattr(dml, 'MY', {'naam': my})
    testobj = dml.SortOptions('naam', types.SimpleNamespace(id=15))
    testobj.olddata = {1: ('x', 'asc'), 2: ('y', 'asc'), 3: ('z', 'desc')}
    assert testobj.save_options({1: ('x', 'asc'), 2: ('y', 'asc'), 3: ('z', 'desc')}) == 'no changes'
    testobj.save_options({1: ('x', 'desc'), 2: ('z', 'desc')})
    data = my.SortOrder.objects.all()
    assert len(data) == 2
    assert (data[0].volgnr, data[0].veldnm, data[0].richting) == (1, 'x', 'desc')
    assert (data[1].volgnr, data[1].veldnm, data[1].richting) == (2, 'z', 'desc')


def test_selectoptions(monkeypatch, capsys):
    monkeypatch.setattr(dml, 'MY', {'testfile': 'stuff'})
    user_jan = types.SimpleNamespace(id=15)
    testobj = dml.SelectOptions('testfile')
    assert testobj.fnaam == 'testfile'
    assert testobj.my == 'stuff'
    assert testobj.user == 0
    # assert testobj.olddata == {}
    testobj = dml.SelectOptions('testfile', user_jan)
    assert testobj.fnaam == 'testfile'
    assert testobj.my == 'stuff'
    assert testobj.user == 15
    # assert testobj.olddata == {}


@pytest.mark.django_db
def test_selectoptions_load(monkeypatch, capsys):
    monkeypatch.setattr(dml, 'MY', {'naam': my})
    user_jan = types.SimpleNamespace(id=15)
    testobj = dml.SelectOptions('naam', types.SimpleNamespace(id=15))
    assert testobj.load_options() == {"arch": '', "gewijzigd": [], "nummer": [], "soort": [],
                                      "status": [], "titel": []}
    assert testobj.olddata == {"arch": '', "gewijzigd": [], "nummer": [], "soort": [], "status": [],
                               "titel": []}
    my.Selection.objects.create(user=15, veldnm='soort', value='x', extra='asc')
    my.Selection.objects.create(user=15, veldnm='status', value='y', extra='asc')
    my.Selection.objects.create(user=15, veldnm='arch', value='z', extra='desc')
    my.Selection.objects.create(user=15, veldnm='nummer', value='a', operator='gt')
    my.Selection.objects.create(user=15, veldnm='nummer', value='d', extra='or', operator='lt')
    my.Selection.objects.create(user=15, veldnm='about', value='b')
    my.Selection.objects.create(user=15, veldnm='title', value='c', extra='+')
    my.Selection.objects.create(user=16, veldnm='title', value='c', extra='+')
    my.Selection.objects.create(user=15, veldnm='oink', value='c', extra='+')
    testobj = dml.SelectOptions('naam', types.SimpleNamespace(id=15))
    assert testobj.load_options() == {"arch": 'arch', "gewijzigd": [], "nummer": [('a', 'gt'),
                                      ('or',), ('d', 'lt')], "soort": ['x'], "status": ['y'],
                                      "titel": [('about', 'b'), ('+',), ('title', 'c')]}
    assert testobj.olddata == {"arch": 'arch', "gewijzigd": [], "nummer": [('a', 'gt'), ('or',),
                               ('d', 'lt')], "soort": ['x'], "status": ['y'],
                               "titel": [('about', 'b'), ('+',), ('title', 'c')]}


@pytest.mark.django_db
def test_selections_save(monkeypatch, capsys):
    monkeypatch.setattr(dml, 'MY', {'naam': my})
    user_jan = types.SimpleNamespace(id=15)
    testobj = dml.SelectOptions('naam', types.SimpleNamespace(id=15))
    testobj.olddata = {"arch": '', "gewijzigd": [], "nummer": [], "soort": [], "status": [],
                       "titel": []}
    assert testobj.save_options({}) == 'no changes'
    testobj = dml.SelectOptions('naam', types.SimpleNamespace(id=15))
    testobj.olddata = {"arch": 'arch', "gewijzigd": [], "nummer": [('1', 'GT'), 'or',
                       ('5', 'LT')], "soort": ['P'], "status": ['1'], "titel": ['Oeps']}
    assert testobj.save_options({"arch": 'arch', "gewijzigd": [], "idgt": '1', 'id': 'or',
                                 'idlt': '5', "soort": ['P'], "status": ['1'],
                                 "titel": ['Oeps']}) == 'no changes'
    my.Selection.objects.create(user=16, veldnm='title', value='c', extra='+')
    assert len(my.Selection.objects.all()) == 1
    testobj = dml.SelectOptions('naam', types.SimpleNamespace(id=15))
    testobj.olddata = {}
    # breakpoint()
    assert testobj.save_options({"arch": 'alles', "gewijzigd": [], "idgt": '1', 'id': 'or',
                                 'idlt': '5', "soort": ['P'], "status": ['1'],
                                 "titel": [('over', 'Oeps'), ('or',), ('titel', 'mis')]}) is None
    data = my.Selection.objects.all()
    assert len(data) == 9
    data = data.filter(user='15')
    assert (data[0].veldnm, data[0].operator, data[0].value, data[0].extra) == ('nummer', 'GT', '1',
                                                                                '  ')
    assert (data[1].veldnm, data[1].operator, data[1].value, data[1].extra) == ('nummer', 'LT', '5',
                                                                                'OR')
    assert (data[2].veldnm, data[2].operator, data[2].value, data[2].extra) == ('soort', 'EQ', 'P',
                                                                                '  ')
    assert (data[3].veldnm, data[3].operator, data[3].value, data[3].extra) == ('status', 'EQ', '1',
                                                                                '  ')
    assert (data[4].veldnm, data[4].operator, data[4].value, data[4].extra) == ('over', 'INCL',
            'Oeps', '  ')
    assert (data[5].veldnm, data[5].operator, data[5].value, data[5].extra) == ('titel', 'INCL',
            'mis', 'OR')
    assert (data[6].veldnm, data[6].operator, data[6].value, data[6].extra) == ('arch', 'EQ', 'False',
                                                                                '  ')
    assert (data[7].veldnm, data[7].operator, data[7].value, data[7].extra) == ('arch', 'EQ', 'True',
                                                                                '  ')


@pytest.mark.django_db
def test_settings(monkeypatch, capsys):
    monkeypatch.setattr(dml, 'MY', {'_basic': my, 'naam': my})
    my.Page.objects.create(order='1', title='page1', link='/there')
    my.Soort.objects.create(order='1', value='P', title='Problem')
    my.Status.objects.create(order='1', value='0', title='started')
    testobj = dml.Settings()
    assert testobj.meld == 'Standaard waarden opgehaald'
    assert testobj.kop == {'1': ('page1', '/there')}
    assert testobj.cat == {'P': ('Problem', 1, 'P')}
    assert testobj.stat == {'0': ('started', 1, 0)}
    testobj = dml.Settings('naam')
    assert testobj.meld == ''
    assert testobj.kop == {'1': ('page1', '/there')}
    assert testobj.cat == {'P': ('Problem', 1, 'P')}
    assert testobj.stat == {'0': ('started', 1, 0)}


@pytest.mark.django_db
def test_settings_write(monkeypatch, capsys):
    my.Page.objects.create(order='1', title='page1', link='/there')
    my.Soort.objects.create(order='1', value='P', title='Problem')
    my.Status.objects.create(order='1', value='0', title='started')

    testobj = dml.Settings()
    testobj.kop[1] = ('page0', '/here')
    testobj.write('kop', '1')
    data = my.Page.objects.all().filter(order='1')
    assert len(data) == 1
    assert data[0].title, data[0].link == ('page0', '/here')

    testobj.cat['P'] = ('Wish', '2', 'P')
    testobj.write('cat', 'P')
    data = my.Soort.objects.all().filter(value='P')
    assert len(data) == 1
    assert data[0].title, data[0].order == ('Wish', '2')

    testobj.stat[0] = ('In process', '2', 0)
    testobj.write('stat', '0')
    data = my.Status.objects.all().filter(value='0')
    assert len(data) == 1
    assert data[0].title, data[0].order == ('In process', '2')


@pytest.mark.django_db
def test_actie(monkeypatch, capsys):
    def mock_settings(*args):
        print('called Settings() with args', args)
    def mock_nieuw(self, args):
        print('called Actie.nieuw() with args', args)
    def mock_read(self):
        print('called Actie.read()')
    monkeypatch.setattr(dml, 'MY', {'naam': my})
    monkeypatch.setattr(dml, 'Settings', mock_settings)
    monkeypatch.setattr(dml.Actie, 'nieuw', mock_nieuw)
    monkeypatch.setattr(dml.Actie, 'read', mock_read)
    testuser = django.contrib.auth.models.User.objects.create(id=15)
    my.Soort.objects.create(id=1, order='1', value='P', title='Problem')
    my.Status.objects.create(id=1, order='1', value='0', title='started')
    testobj = dml.Actie('naam', 0, testuser)
    assert testobj.id == 0
    assert testobj.exists == False
    assert capsys.readouterr().out == ("called Settings() with args ('naam',)\n"
                                       'called Actie.nieuw() with args \n'
                                       'called Actie.read()\n')
    testactie = my.Actie.objects.create(nummer='x', starter_id=15, lasteditor_id=15, soort_id=1,
            status_id=1, behandelaar_id=15)
    testobj = dml.Actie('naam', 'x', testuser)
    assert testobj.id == 'x'
    assert testobj._actie == testactie
    assert capsys.readouterr().out == ("called Settings() with args ('naam',)\n"
                                       'called Actie.read()\n')


@pytest.mark.django_db
def test_actie_nieuw(monkeypatch, capsys):
    def mock_init(self, *args):
        print('called Actie() with args', args)
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    monkeypatch.setattr(dml, 'MY', {'naam': my})
    yr = datetime.datetime.today().year
    mo = datetime.datetime.today().month
    dy = datetime.datetime.today().day
    testuser = django.contrib.auth.models.User.objects.create(id=15, username='me')
    my.Soort.objects.create(id=1, order='1', value='', title='onbekend')
    my.Status.objects.create(id=1, order='1', value='0', title='started')
    testobj = dml.Actie('naam', 'x', testuser)
    testobj.my = my
    testobj.nieuw(testuser)
    assert my.Actie.objects.count() == 1
    testactie = my.Actie.objects.all()[0]
    assert testobj._actie == testactie
    assert testactie.nummer == f'{yr}-0001'
    assert testactie.soort == my.Soort.objects.get(pk=1)
    assert testactie.status == my.Status.objects.get(pk=1)
    assert testactie.start.year == yr
    assert testactie.start.month == mo
    assert testactie.start.day == dy
    assert testactie.starter == testuser
    assert testactie.behandelaar == testuser
    assert testactie.lasteditor == testuser
    assert len(testobj.events) == 1
    assert testobj.events[0][0].year == yr
    assert testobj.events[0][0].month == mo
    assert testobj.events[0][0].day == dy
    assert testobj.events[0][1] == 'Actie opgevoerd'
    assert capsys.readouterr().out == "called Actie() with args ('naam', 'x', <User: me>)\n"

    my.Soort.objects.filter(value='').update(value=' ')
    testobj.nieuw(testuser)
    assert my.Actie.objects.count() == 2
    testactie = my.Actie.objects.all()[1]
    assert testobj._actie == testactie
    assert testactie.nummer == f'{yr}-0002'
    assert testactie.soort == my.Soort.objects.get(pk=1)
    assert testactie.status == my.Status.objects.get(pk=1)
    assert testactie.start.year == yr
    assert testactie.start.month == mo
    assert testactie.start.day == dy
    assert testactie.starter == testuser
    assert testactie.behandelaar == testuser
    assert testactie.lasteditor == testuser
    assert len(testobj.events) == 1
    assert testobj.events[0][0].year == yr
    assert testobj.events[0][0].month == mo
    assert testobj.events[0][0].day == dy
    assert testobj.events[0][1] == 'Actie opgevoerd'
    assert capsys.readouterr().out == ''


@pytest.mark.django_db
def test_actie_read(monkeypatch, capsys):
    def mock_init(self, *args):
        print('called Actie() with args', args)
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    monkeypatch.setattr(dml, 'MY', {'naam': my})
    testobj = dml.Actie('naam', 'x', 'testuser')
    testobj._actie = None
    testobj.read()
    assert not testobj.exists
    assert capsys.readouterr().out == "called Actie() with args ('naam', 'x', 'testuser')\n"
    user = django.contrib.auth.models.User.objects.create(username='testuser')
    testobj._actie = my.Actie.objects.create(nummer='x',
            # start=FIXDATE,
            starter=user, about='me', title='yes, me',
            # gewijzigd=FIXDATE,
            status=my.Status.objects.create(value='1', order=1), behandelaar=user,
            soort=my.Soort.objects.create(value='P', order=1), lasteditor=user,
            arch=False, melding='iets', oorzaak='dit', oplossing='dat', vervolg='')
    ev1 = my.Event.objects.create(actie=testobj._actie, start=FIXDATE, starter=user, text='event 1')
    testobj._actie.events.add(ev1)
    ev2 = my.Event.objects.create(actie=testobj._actie, start=FIXDATE, starter=user, text='event 2')
    testobj._actie.events.add(ev2)
    testobj.read()
    todday = datetime.datetime.today()
    dd, mm, yy = todday.day, todday.month, todday.year
    today_string = f'{dd:02}-{mm:02}-{yy}'
    assert testobj.exists
    assert (testobj.id, testobj.over, testobj.titel) == ('x', 'me', 'yes, me')
    assert testobj.datum.startswith(today_string)
    assert testobj.updated.startswith(today_string)
    assert (testobj.status, testobj.soort, testobj.arch) == ('1', 'P', False)
    assert (testobj.melding, testobj.oorzaak, testobj.oplossing) == ('iets', 'dit', 'dat')
    assert testobj.vervolg == ''
    assert len(testobj.events) == 2
    assert testobj.events[0][0].startswith(today_string)
    assert testobj.events[1][0].startswith(today_string)
    assert (testobj.events[0][1], testobj.events[1][1]) == ('event 1', 'event 2')
    assert (testobj.over_oud, testobj.titel_oud) == ('me', 'yes, me')
    assert (testobj.status_oud, testobj.soort_oud, testobj.arch_oud) == ('1', 'P', False)
    assert (testobj.melding_oud, testobj.oorzaak_oud, testobj.oplossing_oud) == ('iets', 'dit', 'dat')
    assert testobj.vervolg_oud == ''
    assert testobj.events_oud == testobj.events


def test_actie_statustext(monkeypatch, capsys):
    def mock_init(self, *args):
        pass
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    testobj = dml.Actie('naam', 'x', 'testuser')
    testobj.settings = types.SimpleNamespace(stat={'0': ('gemeld', 0, '0'),
                                                   '1': ('in behandeling', 1, '1')})
    testobj.status = 0
    assert testobj.get_statustext() == 'gemeld'
    testobj.status = '0'
    assert testobj.get_statustext() == 'gemeld'
    testobj.status = '2'
    with pytest.raises(dml.DataError) as exc:
        testobj.get_statustext()
    assert str(exc.value) == "Geen omschrijving gevonden bij statuscode of -id '2'"


def test_actie_soorttext(monkeypatch, capsys):
    def mock_init(self, *args):
        pass
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    testobj = dml.Actie('naam', 'x', 'testuser')
    testobj.settings = types.SimpleNamespace(cat={'P': ('probleem', 0, 'P'),
                                                  'W': ('wens', 1, 'W')})
    testobj.soort = 0
    assert testobj.get_soorttext() == 'probleem'
    testobj.soort = 'P'
    assert testobj.get_soorttext() == 'probleem'
    testobj.soort = 'Q'
    with pytest.raises(dml.DataError) as exc:
        testobj.get_soorttext()
    assert str(exc.value) == "Geen omschrijving gevonden bij soortcode of -id 'Q'"


def test_actie_add_event(monkeypatch, capsys):
    def mock_init(self, *args):
        pass
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    testobj = dml.Actie('naam', 'x', 'testuser')
    testobj.events = []
    today = datetime.datetime.today()
    dd, mm, yyyy = today.day, today.month, today.year
    testobj.add_event('garglbargl')
    test = testobj.events
    assert len(test) == 1
    assert test[0][0].day == dd
    assert test[0][0].month == mm
    assert test[0][0].year == yyyy
    assert test[0][1] == 'garglbargl'


@pytest.mark.django_db
def test_actie_write(monkeypatch, capsys):
    def mock_init(self, *args):
        print('called Actie() with args', args)
    def mock_store_event(*args):
        print('called core.store_event_with_date() with args', args[1:])
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    # monkeypatch.setattr(dml, 'MY', {'naam': my})
    monkeypatch.setattr(dml.core, 'store_event_with_date', mock_store_event)
    testobj = dml.Actie('naam', 'x', 'testuser')
    testobj.my = my
    testobj.over_oud = testobj.titel_oud = testobj.status_oud = testobj.soort_oud = ''
    testobj.arch_oud = False
    testobj.melding_oud = testobj.oorzaak_oud = testobj.oplossing_oud = testobj.vervolg_oud = ''
    testobj.events_oud = [('x', 'y')]
    user_o = django.contrib.auth.models.User.objects.create(username='me')
    testobj._actie = my.Actie.objects.create(nummer='x',
            starter=user_o, #  about='me', title='yes, me',
            status=my.Status.objects.create(value='0', order=0), behandelaar=user_o,
            soort=my.Soort.objects.create(value='W', order=0), lasteditor=user_o,
            arch=False)  # , melding='iets', oorzaak='dit', oplossing='dat', vervolg='')
    testobj.over, testobj.titel, testobj.status, testobj.soort = 'hee', 'jijdaar', '1', 'P'
    testobj.arch = True
    testobj.melding, testobj.oorzaak, testobj.oplossing, testobj.vervolg = 'x', 'y', 'z', 'c'
    testobj.events = [('x', 'y'), ('date', 'msg')]
    user = django.contrib.auth.models.User.objects.create(username='testuser')
    new_status = my.Status.objects.create(value='1', order=1)
    new_soort = my.Soort.objects.create(value='P', order=1)
    testobj.write(user)
    written = my.Actie.objects.get(nummer='x')
    assert (written.about, written.title, written.status) == ('hee', 'jijdaar', new_status)
    assert (written.soort, written.arch, written.melding) == (new_soort, True, 'x')
    assert (written.oorzaak, written.oplossing, written.vervolg) == ('y', 'z', 'c')
    assert written.lasteditor == user
    assert capsys.readouterr().out == ("called Actie() with args ('naam', 'x', 'testuser')\n"
            "called core.store_event_with_date() with args ('msg', <Actie: x>, 'date',"
            " <User: testuser>)\n")


def test_actie_cleanup(monkeypatch, capsys):
    def mock_init(self, *args):
        pass
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    testobj = dml.Actie('naam', 'x', 'testuser')
    testobj.cleanup()  # leeg, deze aanroep is alleen t.b.v. coverage
