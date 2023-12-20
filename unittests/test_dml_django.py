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

FIXDATE = datetime.datetime(2020, 1, 1)


class MockDatetime:
    ""
    def utcnow(self, *args):
        return 'now'
    def today(self, *args):
        return FIXDATE
    def now():
        return FIXDATE


@pytest.mark.django_db
def test_get_projnames(monkeypatch, capsys):
    ""
    dml.my.Project.objects.create(name='bep1', description='testapp #1')
    dml.my.Project.objects.create(name='app1', description='testapp #2')
    assert dml.get_projnames() == [('app1', 'app1', 'testapp #2'), ('bep1', 'bep1', 'testapp #1')]


@pytest.mark.django_db
def test_get_user():
    ""
    me = dml.my.User.objects.create(username='testuser')
    assert dml.get_user('me') is None
    assert dml.get_user('testuser') == me


@pytest.mark.django_db
def test_validate_user(monkeypatch):
    ""
    monkeypatch.setattr(dml, 'get_user', lambda x: None)
    assert dml.validate_user('naam', 'passw', 'project') == ('', False, False)
    me = dml.my.User.objects.create(username='testuser')
    monkeypatch.setattr(dml, 'get_user', lambda x: me)
    monkeypatch.setattr(dml.hashers, 'check_password', lambda *x: False)
    assert dml.validate_user('naam', 'passw', 'project') == ('', False, False)
    monkeypatch.setattr(dml.hashers, 'check_password', lambda *x: True)
    monkeypatch.setattr(dml.core, 'is_user', lambda *x: True)
    monkeypatch.setattr(dml.core, 'is_admin', lambda *x: True)
    assert dml.validate_user('naam', 'passw', 'project') == (me, True, True)


@pytest.mark.django_db
def test_get_acties(monkeypatch, capsys):
    ""
    def mock_get_no_acties(*args):
        print('called core.get_acties() with args', args)
        return []
    def mock_get_acties(*args):
        print('called core.get_acties() with args', args)
        fixdate = dml.dt.datetime(2020, 1, 1)
        return [types.SimpleNamespace(nummer='1', start='once', about='me', title='a giant',
                                      status=types.SimpleNamespace(title='A', value='1'),
                                      soort=types.SimpleNamespace(title='X', value='x'),
                                      gewijzigd='', arch=''),
                types.SimpleNamespace(nummer='2', start='twice', about='me', title='still a giant',
                                      status=types.SimpleNamespace(title='B', value='2'),
                                      soort=types.SimpleNamespace(title='Y', value='y'),
                                      gewijzigd=fixdate, arch='arch')]
    myproj = dml.my.Project.objects.create(name='test', description='testapp #1')
    monkeypatch.setattr(dml.core, 'get_acties', mock_get_no_acties)
    assert dml.get_acties('test') == []
    assert capsys.readouterr().out == f"called core.get_acties() with args ({repr(myproj)}, 0)\n"
    monkeypatch.setattr(dml.core, 'get_acties', mock_get_acties)
    myuser = dml.my.User.objects.create(username='testuser')
    assert dml.get_acties('test', myuser) == [('1', 'once', 'A', '1', 'X', 'x', 'me', 'a giant',
                                               '', ''),
                                              ('2', 'twice', 'B', '2', 'Y', 'y', 'me',
                                               'still a giant', '01-01-2020 00:12:00', 'arch')]


@pytest.mark.django_db
def test_sortoptions(monkeypatch, capsys):
    ""
    myuser = dml.my.User.objects.create(username='testuser')
    project_name = 'testfile'
    myproject = dml.my.Project.objects.create(name=project_name)
    testobj = dml.SortOptions(project_name)
    assert testobj.project == myproject
    assert testobj.user == 0
    assert testobj.olddata == {}
    testobj = dml.SortOptions(project_name, myuser)
    assert testobj.project == myproject
    assert testobj.user == myuser.id
    assert testobj.olddata == {}


@pytest.mark.django_db
def test_sortoptions_load(monkeypatch, capsys):
    ""
    myuser = dml.my.User.objects.create(username='testuser')
    myuser2 = dml.my.User.objects.create(username='testuser2')
    project_name = 'testfile'
    myproject = dml.my.Project.objects.create(name=project_name)
    dml.my.SortOrder.objects.create(project=myproject, user=myuser.id, volgnr=1, veldnm='x',
                                    richting='asc')
    dml.my.SortOrder.objects.create(project=myproject, user=myuser.id, volgnr=2, veldnm='y',
                                    richting='asc')
    dml.my.SortOrder.objects.create(project=myproject, user=myuser.id, volgnr=3, veldnm='z',
                                    richting='desc')
    dml.my.SortOrder.objects.create(project=myproject, user=myuser2.id, volgnr=4, veldnm='a',
                                    richting='asc')
    dml.my.SortOrder.objects.create(project=myproject, user=myuser2.id, volgnr=5, veldnm='b',
                                    richting='asc')
    dml.my.SortOrder.objects.create(project=myproject, user=myuser2.id, volgnr=6, veldnm='c',
                                    richting='desc')
    testobj = dml.SortOptions(project_name, myuser)
    assert testobj.load_options() == {1: ('x', 'asc'), 2: ('y', 'asc'), 3: ('z', 'desc')}
    assert testobj.olddata == {1: ('x', 'asc'), 2: ('y', 'asc'), 3: ('z', 'desc')}


@pytest.mark.django_db
def test_sortoptions_save(monkeypatch, capsys):
    ""
    myuser = dml.my.User.objects.create(username='testuser')
    project_name = 'testfile'
    dml.my.Project.objects.create(name=project_name)
    testobj = dml.SortOptions(project_name, myuser)
    testobj.olddata = {1: ('x', 'asc'), 2: ('y', 'asc'), 3: ('z', 'desc')}
    assert testobj.save_options({1: ('x', 'asc'), 2: ('y', 'asc'), 3: ('z', 'desc')}) == 'no changes'
    testobj.save_options({1: ('x', 'desc'), 2: ('z', 'desc')})
    data = dml.my.SortOrder.objects.all()
    # assert len(data) ==len([1, 2])
    assert (data[0].volgnr, data[0].veldnm, data[0].richting) == (1, 'x', 'desc')
    assert (data[1].volgnr, data[1].veldnm, data[1].richting) == (2, 'z', 'desc')
    with pytest.raises(IndexError):
        data[2]

@pytest.mark.django_db
def test_selectoptions(monkeypatch, capsys):
    ""
    myuser = dml.my.User.objects.create(username='testuser')
    project_name = 'testfile'
    myproject = dml.my.Project.objects.create(name=project_name)
    testobj = dml.SelectOptions(project_name)
    assert testobj.project == myproject
    assert testobj.user == 0
    # assert testobj.olddata == {}
    testobj = dml.SelectOptions(project_name, myuser)
    assert testobj.project == myproject
    assert testobj.user == myuser.id
    # assert testobj.olddata == {}


@pytest.mark.django_db
def test_selectoptions_load(monkeypatch, capsys):
    ""
    myuser = dml.my.User.objects.create(username='testuser')
    myuser2 = dml.my.User.objects.create(username='testuser2')
    project_name = 'testfile'
    myproject = dml.my.Project.objects.create(name=project_name)
    testobj = dml.SelectOptions(project_name, myuser)
    assert testobj.load_options() == {"arch": '', "gewijzigd": [], "nummer": [], "soort": [],
                                      "status": [], "titel": []}
    assert testobj.olddata == {"arch": '', "gewijzigd": [], "nummer": [], "soort": [], "status": [],
                               "titel": []}
    dml.my.Selection.objects.create(project=myproject, user=myuser.id, veldnm='soort', value='x',
                                    extra='asc')
    dml.my.Selection.objects.create(project=myproject, user=myuser.id, veldnm='status', value='y',
                                    extra='asc')
    dml.my.Selection.objects.create(project=myproject, user=myuser.id, veldnm='arch', value='z',
                                    extra='desc')
    dml.my.Selection.objects.create(project=myproject, user=myuser.id, veldnm='nummer', value='a',
                                    operator='gt')
    dml.my.Selection.objects.create(project=myproject, user=myuser.id, veldnm='nummer', value='d',
                                    extra='or', operator='lt')
    dml.my.Selection.objects.create(project=myproject, user=myuser.id, veldnm='about', value='b')
    dml.my.Selection.objects.create(project=myproject, user=myuser.id, veldnm='title', value='c',
                                    extra='+')
    dml.my.Selection.objects.create(project=myproject, user=myuser2.id, veldnm='title', value='c',
                                    extra='+')
    dml.my.Selection.objects.create(project=myproject, user=myuser.id, veldnm='oink', value='c',
                                    extra='+')
    testobj = dml.SelectOptions(project_name, myuser)
    assert testobj.load_options() == {"arch": 'arch', "gewijzigd": [], "nummer": [('a', 'gt'),
                                      ('or',), ('d', 'lt')], "soort": ['x'], "status": ['y'],
                                      "titel": [('about', 'b'), ('+',), ('title', 'c')]}
    assert testobj.olddata == {"arch": 'arch', "gewijzigd": [], "nummer": [('a', 'gt'), ('or',),
                               ('d', 'lt')], "soort": ['x'], "status": ['y'],
                               "titel": [('about', 'b'), ('+',), ('title', 'c')]}


@pytest.mark.django_db
def test_selections_save(monkeypatch, capsys):
    ""
    myuser = dml.my.User.objects.create(username='testuser')
    myuser2 = dml.my.User.objects.create(username='testuser2')
    project_name = 'testfile'
    myproject = dml.my.Project.objects.create(name=project_name)
    testobj = dml.SelectOptions(project_name, myuser)
    testobj.olddata = {"arch": '', "gewijzigd": [], "nummer": [], "soort": [], "status": [],
                       "titel": []}
    assert testobj.save_options({}) == 'no changes'
    testobj = dml.SelectOptions(project_name, myuser)
    testobj.olddata = {"arch": 'arch', "gewijzigd": [], "nummer": [('1', 'GT'), 'or',
                       ('5', 'LT')], "soort": ['P'], "status": ['1'], "titel": ['Oeps']}
    assert testobj.save_options({"arch": 'arch', "gewijzigd": [], "idgt": '1', 'id': 'or',
                                 'idlt': '5', "soort": ['P'], "status": ['1'],
                                 "titel": ['Oeps']}) == 'no changes'
    dml.my.Selection.objects.create(project=myproject, user=myuser2.id, veldnm='title', value='c',
                                    extra='+')
    assert len(myproject.selections.all()) == 1
    testobj = dml.SelectOptions(project_name, myuser)
    testobj.olddata = {}
    assert testobj.save_options({"arch": 'alles', "gewijzigd": [], "idgt": '1', 'id': 'or',
                                 'idlt': '5', "soort": ['P'], "status": ['1'],
                                 "titel": [('over', 'Oeps'), ('or',), ('titel', 'mis')]}) == ''
    data = myproject.selections.filter(user=myuser.id)
    assert len(data) == len(['nummer', 'ummer', 'soort', 'status', 'over', 'titel', 'arch', 'arch'])
    assert (data[0].veldnm, data[0].operator, data[0].value, data[0].extra) == ('nummer', 'GT',
                                                                                '1', '  ')
    assert (data[1].veldnm, data[1].operator, data[1].value, data[1].extra) == ('nummer', 'LT',
                                                                                '5', 'OR')
    assert (data[2].veldnm, data[2].operator, data[2].value, data[2].extra) == ('soort', 'EQ',
                                                                                'P', '  ')
    assert (data[3].veldnm, data[3].operator, data[3].value, data[3].extra) == ('status', 'EQ',
                                                                                '1', '  ')
    assert (data[4].veldnm, data[4].operator, data[4].value, data[4].extra) == ('over', 'INCL',
                                                                                'Oeps', '  ')
    assert (data[5].veldnm, data[5].operator, data[5].value, data[5].extra) == ('titel', 'INCL',
                                                                                'mis', 'OR')
    assert (data[6].veldnm, data[6].operator, data[6].value, data[6].extra) == ('arch', 'EQ',
                                                                                'False', '  ')
    assert (data[7].veldnm, data[7].operator, data[7].value, data[7].extra) == ('arch', 'EQ',
                                                                                'True', '  ')


@pytest.mark.django_db
def test_settings(monkeypatch, capsys):
    ""
    projectnaam = 'test'
    myproject = dml.my.Project.objects.create(name=projectnaam)
    dml.my.Page.objects.create(order=1, title='page1', link='/there')
    dml.my.Soort.objects.create(project=myproject, order=1, value='P', title='Problem')
    dml.my.Status.objects.create(project=myproject, order=1, value=0, title='started')
    testobj = dml.Settings()
    assert testobj.meld == 'Standaard waarden opgehaald'
    assert testobj.kop == {'1': ('page1', '/there')}
    assert testobj.cat == {}  # 'P': ('Problem', 1)}
    assert testobj.stat == {}  # 0: ('started', 1)}
    testobj = dml.Settings(projectnaam)
    assert testobj.meld == ''
    assert testobj.kop == {'1': ('page1', '/there')}
    assert testobj.cat == {'P': ('Problem', 1)}
    assert testobj.stat == {0: ('started', 1)}


@pytest.mark.django_db
def test_settings_write(monkeypatch):
    ""
    projectnaam = 'test'
    myproject = dml.my.Project.objects.create(name=projectnaam)
    dml.my.Page.objects.create(order=0, title='page0', link='/here')
    dml.my.Page.objects.create(order=1, title='page1', link='/there')
    dml.my.Soort.objects.create(project=myproject, order=0, value='P', title='Problem')
    cat_to_keep = dml.my.Soort.objects.create(project=myproject, order=1, value='R',
                                              title='Request')
    cat_to_remove = dml.my.Soort.objects.create(project=myproject, order=2, value='D',
                                                title='Discussion')
    stat_to_keep = dml.my.Status.objects.create(project=myproject, order=0, value=0,
                                                title='started')
    stat_to_remove = dml.my.Status.objects.create(project=myproject, order=1, value=1,
                                                  title='continued')
    dml.my.Status.objects.create(project=myproject, order=2, value=2, title='finished')
    testobj = dml.Settings(projectnaam)
    testobj.kop['0'] = ('start', '/here')     # waarom heeft de kop dict string keys?
    testobj.kop['1'] = ('page1', '/nowhere')
    testobj.cat['P'] = ('Defect', 0)
    testobj.cat['R'] = ('Request', 2)
    testobj.cat['B'] = ('Brainstorm', 1)
    testobj.cat.pop('D')
    testobj.stat[0] = ('created', 0)
    testobj.stat.pop(1)
    testobj.stat[2] = ('done', 1)
    testobj.stat[3] = ('reopened', 2)
    user = dml.my.User.objects.create(username='me')
    actie = dml.my.Actie.objects.create(project=myproject, nummer='xx', starter=user,
                                        lasteditor=user, soort=cat_to_remove,
                                        status=stat_to_remove, behandelaar=user)
    assert testobj.write() == ('status', 1)
    actie.status = stat_to_keep
    actie.save()
    assert testobj.write() == ('soort', 'D')
    actie.soort = cat_to_keep
    actie.save()
    testobj.write()
    pages = dml.my.Page.objects.all()
    assert len(pages) == len(['start', 'page1'])
    assert [pages[0].order, pages[0].title, pages[0].link] == [0, 'start', '/here']
    assert [pages[1].order, pages[1].title, pages[1].link] == [1, 'page1', '/nowhere']
    cats = myproject.soort.all()
    assert len(cats) == len(['defect', 'request', 'brainstorm'])
    assert [cats[0].value, cats[0].title, cats[0].order] == ['P', 'Defect', 0]
    assert [cats[1].value, cats[1].title, cats[1].order] == ['R', 'Request', 2]
    assert [cats[2].value, cats[2].title, cats[2].order] == ['B', 'Brainstorm', 1]
    stats = myproject.status.all()
    assert len(stats) == len(['created', 'done', 'reopened'])
    assert [stats[0].value, stats[0].title, stats[0].order] == [0, 'created', 0]
    assert [stats[1].value, stats[1].title, stats[1].order] == [2, 'done', 1]
    assert [stats[2].value, stats[2].title, stats[2].order] == [3, 'reopened', 2]


# dit was de test als je een argument 'settingtype' mee kon geven
# @pytest.mark.django_db
# def _test_settings_write(monkeypatch, capsys):
#     dml.my.Page.objects.create(order='1', title='page1', link='/there')
#     dml.my.Soort.objects.create(order='1', value='P', title='Problem')
#     dml.my.Status.objects.create(order='1', value='0', title='started')
#
#     testobj = dml.Settings()
#     testobj.kop[1] = ('page0', '/here')
#     testobj.write('kop', '1')
#     data = dml.my.Page.objects.all().filter(order='1')
#     assert len(data) == 1
#     assert data[0].title, data[0].link == ('page0', '/here')
#
#     testobj.cat['P'] = ('Wish', '2', 'P')
#     testobj.write('cat', 'P')
#     data = dml.my.Soort.objects.all().filter(value='P')
#     assert len(data) == 1
#     assert data[0].title, data[0].order == ('Wish', '2')
#
#     testobj.stat[0] = ('In process', '2', 0)
#     testobj.write('stat', '0')
#     data = dml.my.Status.objects.all().filter(value='0')
#     assert len(data) == 1
#     assert data[0].title, data[0].order == ('In process', '2')


@pytest.mark.django_db
def test_actie(monkeypatch, capsys):
    ""
    def mock_settings(*args):
        print('called Settings() with args', args)
    def mock_nieuw(self, *args):
        print('called Actie.nieuw() with args', args)
    def mock_read(self):
        print('called Actie.read()')
    projectnaam = 'test'
    myproject = dml.my.Project.objects.create(name=projectnaam)
    monkeypatch.setattr(dml, 'Settings', mock_settings)
    monkeypatch.setattr(dml.Actie, 'nieuw', mock_nieuw)
    monkeypatch.setattr(dml.Actie, 'read', mock_read)
    myuser = dml.my.User.objects.create(username='test')
    mysoort = dml.my.Soort.objects.create(project=myproject, order=1, value='P', title='Problem')
    mystatus = dml.my.Status.objects.create(project=myproject, order=1, value=0, title='started')
    testobj = dml.Actie(projectnaam, 0, myuser)
    assert testobj.id == 0
    assert not testobj.exists
    assert capsys.readouterr().out == (f"called Settings() with args ('{projectnaam}',)\n"
                                       f'called Actie.nieuw() with args ({repr(myuser)},)\n'
                                       'called Actie.read()\n')
    myactie = dml.my.Actie.objects.create(project=myproject, nummer='x', starter_id=myuser.id,
                                          lasteditor_id=myuser.id, soort_id=mysoort.id,
                                          status_id=mystatus.id, behandelaar_id=myuser.id)
    testobj = dml.Actie(projectnaam, 'x', myuser)
    assert testobj.id == 'x'
    assert testobj._actie == myactie
    assert capsys.readouterr().out == (f"called Settings() with args ('{projectnaam}',)\n"
                                       'called Actie.read()\n')


@pytest.mark.django_db
def test_actie_nieuw(monkeypatch, capsys):
    ""
    def mock_init(self, *args):
        print('called Actie() with args', args)
    actiecount = 0
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    yr = datetime.datetime.today().year
    mo = datetime.datetime.today().month
    dy = datetime.datetime.today().day
    myuser = dml.my.User.objects.create(username='me')
    projectnaam = 'naam'
    myproject = dml.my.Project.objects.create(name=projectnaam)
    mysoort = dml.my.Soort.objects.create(project=myproject, order='1', value='', title='onbekend')
    mystatus = dml.my.Status.objects.create(project=myproject, order='1', value='0', title='started')
    testobj = dml.Actie('naam', 'x', myuser)
    testobj.project = myproject
    testobj.nieuw(myuser)
    actiecount += 1
    assert dml.my.Actie.objects.count() == actiecount
    myactie = dml.my.Actie.objects.all()[0]
    assert testobj._actie == myactie
    assert testobj._actie.nummer == f'{yr}-0001'
    assert testobj._actie.soort == mysoort
    assert testobj._actie.status == mystatus
    assert testobj._actie.start.year == yr
    assert testobj._actie.start.month == mo
    assert testobj._actie.start.day == dy
    assert testobj._actie.starter == myuser
    assert testobj._actie.behandelaar == myuser
    assert testobj._actie.lasteditor == myuser
    assert len(testobj.events) == 1
    assert testobj.events[0][0].year == yr
    assert testobj.events[0][0].month == mo
    assert testobj.events[0][0].day == dy
    assert testobj.events[0][1] == 'Actie opgevoerd'
    assert capsys.readouterr().out == "called Actie() with args ('naam', 'x', <User: me>)\n"

    dml.my.Soort.objects.filter(value='').update(value=' ')
    testobj.nieuw(myuser)
    actiecount += 1
    assert dml.my.Actie.objects.count() == actiecount
    myactie = dml.my.Actie.objects.all()[1]
    assert testobj._actie == myactie
    assert testobj._actie.nummer == f'{yr}-0002'
    assert testobj._actie.soort == mysoort
    assert testobj._actie.status == mystatus
    assert testobj._actie.start.year == yr
    assert testobj._actie.start.month == mo
    assert testobj._actie.start.day == dy
    assert testobj._actie.starter == myuser
    assert testobj._actie.behandelaar == myuser
    assert testobj._actie.lasteditor == myuser
    assert len(testobj.events) == 1
    assert testobj.events[0][0].year == yr
    assert testobj.events[0][0].month == mo
    assert testobj.events[0][0].day == dy
    assert testobj.events[0][1] == 'Actie opgevoerd'
    assert capsys.readouterr().out == ''


@pytest.mark.django_db
def test_actie_read(monkeypatch, capsys):
    ""
    def mock_init(self, *args):
        print('called Actie() with args', args)
    projectnaam = 'naam'
    myproject = dml.my.Project.objects.create(name=projectnaam)
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    testobj = dml.Actie('naam', 'x', 'testuser')
    testobj._actie = None
    testobj.read()
    assert not testobj.exists
    assert capsys.readouterr().out == "called Actie() with args ('naam', 'x', 'testuser')\n"
    user = dml.my.User.objects.create(username='testuser')
    testobj._actie = dml.my.Actie.objects.create(project=myproject, nummer='x',  # start=FIXDATE,
                                                 starter=user, about='me', title='yes, me',
                                                 # gewijzigd=FIXDATE,
                                                 status=dml.my.Status.objects.create(
                                                     project=myproject, value='1', order=1),
                                                 behandelaar=user,
                                                 soort=dml.my.Soort.objects.create(
                                                     project=myproject, value='P', order=1),
                                                 lasteditor=user,
                                                 arch=False, melding='iets', oorzaak='dit',
                                                 oplossing='dat', vervolg='')
    ev1 = dml.my.Event.objects.create(actie=testobj._actie, start=FIXDATE, starter=user,
                                      text='event 1')
    testobj._actie.events.add(ev1)
    ev2 = dml.my.Event.objects.create(actie=testobj._actie, start=FIXDATE, starter=user,
                                      text='event 2')
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
    assert len(testobj.events) == len([ev1, ev2])
    assert testobj.events[0][0].startswith(today_string)
    assert testobj.events[1][0].startswith(today_string)
    assert (testobj.events[0][1], testobj.events[1][1]) == ('event 1', 'event 2')
    assert (testobj.over_oud, testobj.titel_oud) == ('me', 'yes, me')
    assert (testobj.status_oud, testobj.soort_oud, testobj.arch_oud) == ('1', 'P', False)
    assert (testobj.melding_oud, testobj.oorzaak_oud, testobj.oplossing_oud) == ('iets', 'dit',
                                                                                 'dat')
    assert testobj.vervolg_oud == ''
    assert testobj.events_oud == testobj.events


def test_actie_statustext(monkeypatch, capsys):
    ""
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
    ""
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
    ""
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
    ""
    def mock_init(self, *args):
        print('called Actie() with args', args)
    def mock_store_event(*args):
        # print('called core.store_event_with_date() with args', args[1:])
        print('called core.store_event() with args', args)
    projectnaam = 'naam'
    myproject = dml.my.Project.objects.create(name=projectnaam)
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    # monkeypatch.setattr(dml, 'MY', {'naam': dml.my.)
    # monkeypatch.setattr(dml.core, 'store_event_with_date', mock_store_event)
    monkeypatch.setattr(dml.core, 'store_event', mock_store_event)
    testobj = dml.Actie('naam', 'x', 'testuser')
    testobj.project = myproject
    testobj.over_oud = testobj.titel_oud = testobj.status_oud = testobj.soort_oud = ''
    testobj.arch_oud = False
    testobj.melding_oud = testobj.oorzaak_oud = testobj.oplossing_oud = testobj.vervolg_oud = ''
    testobj.events_oud = [('x', 'y')]
    user_o = dml.my.User.objects.create(username='me')
    testobj._actie = dml.my.Actie.objects.create(project=myproject, nummer='x', starter=user_o,
                                                 status=dml.my.Status.objects.create(
                                                     project=myproject, value='0', order=0),
                                                 behandelaar=user_o,
                                                 soort=dml.my.Soort.objects.create(
                                                     project=myproject, value='W', order=0),
                                                 lasteditor=user_o,
                                                 arch=False)
    testobj.over, testobj.titel, testobj.status, testobj.soort = 'hee', 'jijdaar', '1', 'P'
    testobj.arch = True
    testobj.melding, testobj.oorzaak, testobj.oplossing, testobj.vervolg = 'x', 'y', 'z', 'c'
    testobj.events = [('x', 'y'), ('date', 'msg')]
    myuser = dml.my.User.objects.create(username='testuser')
    new_status = dml.my.Status.objects.create(project=myproject, value='1', order=1)
    new_soort = dml.my.Soort.objects.create(project=myproject, value='P', order=1)
    testobj.write(myuser)
    written = dml.my.Actie.objects.get(nummer='x')
    assert (written.about, written.title, written.status) == ('hee', 'jijdaar', new_status)
    assert (written.soort, written.arch, written.melding) == (new_soort, True, 'x')
    assert (written.oorzaak, written.oplossing, written.vervolg) == ('y', 'z', 'c')
    assert written.lasteditor == myuser
    assert capsys.readouterr().out == ("called Actie() with args ('naam', 'x', 'testuser')\n"
                                       "called core.store_event() with args ('msg',"
                                       f" {repr(testobj._actie)}, {repr(myuser)})\n")
            # "called core.store_event() with args ('msg', <Actie: x>, 'date',"
            # " <User: testuser>)\n")


def test_actie_cleanup(monkeypatch, capsys):
    ""
    def mock_init(self, *args):
        pass
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    testobj = dml.Actie('naam', 'x', 'testuser')
    testobj.cleanup()  # leeg, deze aanroep is alleen t.b.v. coverage
