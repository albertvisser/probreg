"""unittests for ./probreg/dml_mongo.py
"""
import types
import datetime
import pytest
import probreg.dml_mongo as dmlm

FIXDATE = datetime.datetime(2020, 1, 1)

class MockDate:
    """stub for datatime.Date object
    """
    @staticmethod
    def today():
        """stub
        """
        return types.SimpleNamespace(year=2022)

class MockSettings:
    """stub for dml_mongo.Settings object
    """
    def __init__(self, fnaam=''):
        self.imagecount = 1
        self.startitem = 0
    def write(self):
        """stub
        """
        print('called Settings.write()')

class MockDatetime:
    """stub for datetime.datetime object
    """
    def utcnow(*args):
        """stub
        """
        return 'now'
    def today(*args):
        """stub
        """
        return FIXDATE
    @staticmethod
    def now():
        """stub
        """
        return FIXDATE

class MockColl:
    """stub for pymongo.collection.Collection object
    """
    def find(self, *args, **kwargs):
        """stub - in testmethode patchen met gewenst resultaat
        """

    def find_one(self, *args, **kwargs):
        """stub - in testmethode patchen met gewenst resultaat
        """

    def insert_one(self, *args, **kwargs):
        """stub - in testmethode patchen met gewenst resultaat
        """

    def update_one(self, *args, **kwargs):
        """stub - in testmethode patchen met gewenst resultaat
        """

def test_get_nieuwetitel(monkeypatch):
    """unittest for dml_mongo.get_nieuwetitel
    """
    def mock_find(self, *args, **kwargs):
        """stub
        """
        return [{'nummer': 1}, {'nummer': 17}, {'nummer': 5}]
    def mock_find_none(self, *args, **kwargs):
        """stub
        """
        return []
    monkeypatch.setattr(dmlm.dt, 'date', MockDate)
    monkeypatch.setattr(MockColl, 'find', mock_find)
    monkeypatch.setattr(dmlm, 'coll', MockColl())
    assert dmlm.get_nieuwetitel('') == '2022-0018'
    assert dmlm.get_nieuwetitel('', 2020) == '2020-0018'
    monkeypatch.setattr(MockColl, 'find', mock_find_none)
    monkeypatch.setattr(dmlm, 'coll', MockColl())
    assert dmlm.get_nieuwetitel('') == '2022-0001'
    assert dmlm.get_nieuwetitel('', 2020) == '2020-0001'

def test_get_acties(monkeypatch, capsys):
    """unittest for dml_mongo.get_acties
    """
    def mock_find(self, *args, **kwargs):
        """stub
        """
        print('called collection.find() for selection', args[0])
        return []
    monkeypatch.setattr(MockColl, 'find', mock_find)
    monkeypatch.setattr(dmlm, 'coll', MockColl())
    with pytest.raises(dmlm.DataError) as excinfo:
        dmlm.get_acties('', arch='x')
    assert str(excinfo.value) == ("Foutieve waarde voor archief opgegeven "
                                  "(moet niks, 'arch'  of 'alles' zijn)")
    # with pytest.raises(dmlm.DataError) as excinfo:
    #     dmlm.get_acties('', select={'x': 'y'})
    # assert str(excinfo.value) == "Foutief selectie-argument opgegeven"
    with pytest.raises(dmlm.DataError) as excinfo:
        dmlm.get_acties('', select={'id': 'x'})
    assert str(excinfo.value) == "Foutieve waarde voor id-operator opgegeven"
    with pytest.raises(dmlm.DataError) as excinfo:
        dmlm.get_acties('', select={'idlt': 'x', 'idgt': 'y'})
    assert str(excinfo.value) == "Geen operator opgegeven bij twee grenswaarden voor id"
    with pytest.raises(dmlm.DataError) as excinfo:
        dmlm.get_acties('', select={'idlt': 'y', 'id': 'en'})
    assert str(excinfo.value) == "Operator alleen opgeven bij twee grenswaarden voor id"
    with pytest.raises(dmlm.DataError) as excinfo:
        dmlm.get_acties('', select={'idgt': 'y', 'id': 'of'})
    assert str(excinfo.value) == "Operator alleen opgeven bij twee grenswaarden voor id"

    # niet geïnteresseerd in het resultaat, wel in het vertalen van de zoekargumenten
    dmlm.get_acties('', select={'idlt': 'x'})
    assert capsys.readouterr().out == ('called collection.find() for selection'
            " {'nummer': {'lt': 'x'}, 'archived': False}\n")
    dmlm.get_acties("", select={'idgt': 'y'})
    assert capsys.readouterr().out == ('called collection.find() for selection'
            " {'nummer': {'gt': 'y'}, 'archived': False}\n")
    dmlm.get_acties("", select={'idlt': 'x', 'id': 'en', 'idgt': 'y'})
    assert capsys.readouterr().out == ('called collection.find() for selection'
            " {'nummer': {'lt': 'x', 'gt': 'y'}, 'archived': False}\n")
    dmlm.get_acties("", select={'idlt': 'x', 'id': 'of', 'idgt': 'y'})
    assert capsys.readouterr().out == ('called collection.find() for selection'
            " {'nummer': {'or': {'lt': 'x', 'gt': 'y'}}, 'archived': False}\n")

    dmlm.get_acties("", select={'soort': '1'})
    assert capsys.readouterr().out == ('called collection.find() for selection'
            " {'soort': '1', 'archived': False}\n")
    dmlm.get_acties("", select={'status': '1'})
    assert capsys.readouterr().out == ('called collection.find() for selection'
            " {'status': '1', 'archived': False}\n")
    dmlm.get_acties("", select={'titel': 'x'})
    assert capsys.readouterr().out == ('called collection.find() for selection'
            " {'titel': {'regex': '\\\\.*x\\\\.*'}, 'archived': False}\n")
    dmlm.get_acties("", select={'onderwerp': 'x'})
    assert capsys.readouterr().out == ('called collection.find() for selection'
            " {'onderwerp': {'regex': '\\\\.*x\\\\.*'}, 'archived': False}\n")
    with pytest.raises(dmlm.DataError) as excinfo:
        dmlm.get_acties('', select={'x': 'y'})
    assert str(excinfo.value) == "Foutief selectie-argument opgegeven"

    # alles dat er is
    dmlm.get_acties('', arch='alles')
    assert capsys.readouterr().out == ("called collection.find() for selection"
                                       " {'archived': {'$in': [True, False]}}\n")
    dmlm.get_acties('', select={}, arch='alles')
    assert capsys.readouterr().out == ("called collection.find() for selection"
                                       " {'archived': {'$in': [True, False]}}\n")
    # alles dat niet gearchiveerd is
    dmlm.get_acties('', arch='')
    assert capsys.readouterr().out == "called collection.find() for selection {'archived': False}\n"
    dmlm.get_acties('', select={}, arch='')
    assert capsys.readouterr().out == "called collection.find() for selection {'archived': False}\n"
    # alles dat gearchiveerd is
    dmlm.get_acties('', arch='arch')
    assert capsys.readouterr().out == "called collection.find() for selection {'archived': True}\n"
    dmlm.get_acties('', select={}, arch='arch')
    assert capsys.readouterr().out == "called collection.find() for selection {'archived': True}\n"

def test_settings(monkeypatch):
    """unittest for dml_mongo.Settings(.__init__)
    """
    monkeypatch.setattr(dmlm.Settings, 'read', lambda x: False)
    testobj = dmlm.Settings()
    assert not testobj.exists
    assert testobj.kop == {x: (y[0],) for x, y in dmlm.kopdict.items()}
    assert testobj.stat == {x: (y[0], y[1]) for x, y in dmlm.statdict.items()}
    assert testobj.cat == {x: (y[0], y[1]) for x, y in dmlm.catdict.items()}
    assert testobj.imagecount == 0
    assert testobj.startitem == ''
    monkeypatch.setattr(dmlm.Settings, 'read', lambda x: True)
    testobj = dmlm.Settings()
    assert testobj.exists

def test_settings_read(monkeypatch):
    """unittest for dml_mongo.Settings.read
    """
    id_number = 100
    start_number = 15
    def mock_find_none(self, *args, **kwargs):
        """stub
        """
        return None
    def mock_find_one(self, *args, **kwargs):
        """stub
        """
        return {'_id': id_number, 'headings': {0: ('Begin',)}, 'statuses': {0: ('Started', 1)},
                'categories': {'U': ('Unknown', 1)}, 'imagecount': 1, 'startitem': start_number}
    monkeypatch.setattr(MockColl, 'find_one', mock_find_none)
    monkeypatch.setattr(dmlm, 'coll', MockColl())
    testobj = dmlm.Settings()  # read wordt uitgevoerd tijdens __init__
    assert not testobj.exists
    assert testobj.kop == {x: (y[0],) for x, y in dmlm.kopdict.items()}
    assert testobj.stat == {x: (y[0], y[1]) for x, y in dmlm.statdict.items()}
    assert testobj.cat == {x: (y[0], y[1]) for x, y in dmlm.catdict.items()}
    assert testobj.imagecount == 0
    assert testobj.startitem == ''

    monkeypatch.setattr(MockColl, 'find_one', mock_find_one)
    monkeypatch.setattr(dmlm, 'coll', MockColl())
    testobj = dmlm.Settings()  # read wordt uitgevoerd tijdens __init__
    assert testobj.exists
    assert testobj.settings_id == id_number
    assert testobj.kop == {0: ('Begin',)}
    assert testobj.stat == {0: ('Started', 1)}
    assert testobj.cat == {'U': ('Unknown', 1)}
    assert testobj.imagecount == 1
    assert testobj.startitem == start_number

def test_settings_write(monkeypatch, capsys):
    """unittest for dml_mongo.Settings.write
    """
    def mock_insert_one(self, *args):
        """stub
        """
        print('called coll.insert_one() with args', args)
        return types.SimpleNamespace(inserted_id=5)
    def mock_update_one(self, *args):
        """stub
        """
        print('called coll.update_one() with args', args)
    monkeypatch.setattr(MockColl, 'insert_one', mock_insert_one)
    monkeypatch.setattr(MockColl, 'update_one', mock_update_one)
    monkeypatch.setattr(dmlm, 'coll', MockColl())

    # nog geen settings aanwezig
    monkeypatch.setattr(dmlm.Settings, 'read', lambda x: False)
    testobj = dmlm.Settings()
    assert not testobj.exists
    testobj.kop = {0: 'head'}
    testobj.stat = {0: 'stat'}
    testobj.cat = {0: 'cat'}
    testobj.imagecount = 1
    testobj.startitem = 1
    testobj.write()
    assert testobj.exists
    assert capsys.readouterr().out == (
        "called coll.insert_one() with args ({'name': 'settings'},)\n"
        "called coll.update_one() with args ({'_id': 5}, {'$set': {'headings': {0: 'head'}}})\n"
        "called coll.update_one() with args ({'_id': 5}, {'$set': {'statuses': {0: 'stat'}}})\n"
        "called coll.update_one() with args ({'_id': 5}, {'$set': {'categories': {0: 'cat'}}})\n"
        "called coll.update_one() with args ({'_id': 5}, {'$set': {'imagecount': 1}})\n"
        "called coll.update_one() with args ({'_id': 5}, {'$set': {'startitem': 1}})\n")

    # settings aanwezig
    monkeypatch.setattr(dmlm.Settings, 'read', lambda x: True)
    testobj = dmlm.Settings()
    assert testobj.exists
    testobj.settings_id = 10
    testobj.kop = {0: 'head'}
    testobj.stat = {0: 'stat'}
    testobj.cat = {0: 'cat'}
    testobj.imagecount = 2
    testobj.startitem = 9
    testobj.write()
    assert testobj.exists
    assert capsys.readouterr().out == (
        "called coll.update_one() with args ({'_id': 10}, {'$set': {'headings': {0: 'head'}}})\n"
        "called coll.update_one() with args ({'_id': 10}, {'$set': {'statuses': {0: 'stat'}}})\n"
        "called coll.update_one() with args ({'_id': 10}, {'$set': {'categories': {0: 'cat'}}})\n"
        "called coll.update_one() with args ({'_id': 10}, {'$set': {'imagecount': 2}})\n"
        "called coll.update_one() with args ({'_id': 10}, {'$set': {'startitem': 9}})\n")

def test_actie(monkeypatch, capsys):
    """unittest for dml_mongo.actie
    """
    def mock_nieuw(*args):
        """stub
        """
        print('called Actie.nieuw()')
    def mock_read(*args):
        """stub
        """
        print('called Actie.read()')
    monkeypatch.setattr(dmlm, 'Settings', MockSettings)
    monkeypatch.setattr(dmlm.Actie, 'read', mock_read)
    monkeypatch.setattr(dmlm.Actie, 'nieuw', mock_nieuw)
    testobj = dmlm.Actie('', '0')
    assert testobj.imagecount == 1
    assert testobj.id == '0'
    assert (testobj.imagelist, testobj.events) == ([], [])
    assert (testobj.datum, testobj.updated, testobj.soort, testobj.titel) == ('', '', '', '')
    assert (testobj.status, testobj.arch) == ('0', False)
    assert testobj.melding == ''
    assert capsys.readouterr().out == 'called Actie.nieuw()\n'
    testobj = dmlm.Actie('', 'x')
    assert testobj.imagecount == 1
    assert testobj.id == 'x'
    assert (testobj.imagelist, testobj.events) == ([], [])
    assert (testobj.datum, testobj.updated, testobj.soort, testobj.titel) == ('', '', '', '')
    assert (testobj.status, testobj.arch) == ('0', False)
    assert testobj.melding == ''
    assert capsys.readouterr().out == 'called Actie.read()\n'

def test_actie_nieuw(monkeypatch):
    """unittest for dml_mongo.Actie.nieuw
    """
    monkeypatch.setattr(dmlm.dt, 'datetime', MockDatetime)
    monkeypatch.setattr(dmlm, 'Settings', MockSettings)
    monkeypatch.setattr(dmlm, 'get_nieuwetitel', lambda y, x: str(x) + '-0001')
    testobj = dmlm.Actie('', '0')  # gaat nieuw() uitvoeren
    assert testobj.id == '2020-0001'
    assert testobj.datum == '2020-01-01 00:00:00'
    assert not testobj.arch

def test_actie_read(monkeypatch):
    """unittest for dml_mongo.Actie.read
    """
    def mock_find_one(self, *args, **kwargs):
        """stub
        """
        return {'_id': 100, 'jaar': '2020', 'nummer': '0001', 'gemeld': 'vandaag', 'status': 0,
                'soort': 'A', 'bijgewerkt': 'ook vandaag', 'onderwerp': 'it', 'titel': 'whatever',
                'melding': 'dit', 'archived': True,
                'events': [('zonet', 'iets'), ('straks', 'nog iets')]}
    def mock_find_none(self, *args, **kwargs):
        """stub
        """
        return None
    monkeypatch.setattr(dmlm, 'Settings', MockSettings)
    monkeypatch.setattr(MockColl, 'find_one', mock_find_one)
    monkeypatch.setattr(dmlm, 'coll', MockColl())
    testobj = dmlm.Actie('', '2020-0001')  # read is executed during __init__
    assert testobj.exists
    assert testobj.id == '2020-0001'
    assert testobj.datum == 'vandaag'
    assert testobj.status == 0
    assert testobj.soort == 'A'
    assert testobj.updated == 'ook vandaag'
    assert testobj.titel == 'whatever'
    assert testobj.melding == 'dit'
    assert testobj.arch
    assert testobj.events == [('zonet', 'iets'), ('straks', 'nog iets')]
    monkeypatch.setattr(MockColl, 'find_one', mock_find_none)
    monkeypatch.setattr(dmlm, 'coll', MockColl())
    with pytest.raises(dmlm.DataError) as excinfo:
        testobj = dmlm.Actie('', '1-1')  # read is executed during __init__
    assert str(excinfo.value) == 'Actie object does not exist'

def test_actie_write(monkeypatch, capsys):
    """unittest for dml_mongo.Actie.write
    """
    def mock_nieuw(*args):
        """stub
        """
        print('called Actie.nieuw()')
    def mock_read(*args):
        """stub
        """
        print('called Actie.read()')
    def mock_insert_one(self, *args):
        """stub
        """
        print('called coll.insert_one() with args', args)
        return types.SimpleNamespace(inserted_id='5')
    def mock_update_one(self, *args):
        """stub
        """
        print('called coll.update_one() with args', args)
    monkeypatch.setattr(dmlm.dt, 'datetime', MockDatetime)
    monkeypatch.setattr(dmlm, 'Settings', MockSettings)
    monkeypatch.setattr(dmlm.Actie, 'nieuw', mock_nieuw)
    monkeypatch.setattr(dmlm.Actie, 'read', mock_read)
    monkeypatch.setattr(MockColl, 'insert_one', mock_insert_one)
    monkeypatch.setattr(MockColl, 'update_one', mock_update_one)
    monkeypatch.setattr(dmlm, 'coll', MockColl())
    testobj = dmlm.Actie('', '0')
    testobj.exists = False
    testobj.id = '2020-0001'
    testobj.datum = 'vandaag'
    testobj.status = 0
    testobj.soort = 'A'
    # testobj.updated = 'ook vandaag'
    testobj.over = 'it'
    testobj.titel = 'whatever'
    testobj.melding = 'dit'
    testobj.arch = False
    testobj.events = [('zonet', 'iets'), ('straks', 'nog iets')]
    testobj.write()
    assert testobj.settings.startitem == '5'
    assert capsys.readouterr().out == ('called Actie.nieuw()\n'
        "called coll.insert_one() with args ({'jaar': 2020, 'nummer': 1},)\n"
        'called Settings.write()\n'
        "called coll.update_one() with args ({'_id': '5'}, {'$set': {'gemeld': 'vandaag',"
        " 'status': 0, 'soort': 'A', 'bijgewerkt': '2020-01-01 00:00:00',"
        " 'onderwerp': 'it', 'titel': 'whatever', 'melding': 'dit', 'archived': False,"
        " 'events': [('zonet', 'iets'), ('straks', 'nog iets')]}})\n")
    testobj = dmlm.Actie('', '1')
    testobj.actie_id = '10'
    testobj.exists = True
    testobj.id = '2020-0001'
    testobj.datum = 'vandaag'
    testobj.status = 0
    testobj.soort = 'A'
    # testobj.updated = 'ook vandaag'
    testobj.over = 'it'
    testobj.titel = 'whatever'
    testobj.melding = 'dit'
    testobj.arch = True
    testobj.events = [('zonet', 'iets'), ('straks', 'nog iets')]
    testobj.write()
    assert testobj.settings.startitem == '10'
    assert capsys.readouterr().out == ('called Actie.read()\n'
        'called Settings.write()\n'
        "called coll.update_one() with args ({'_id': '10'}, {'$set': {'gemeld': 'vandaag',"
        " 'status': 0, 'soort': 'A', 'bijgewerkt': '2020-01-01 00:00:00',"
        " 'onderwerp': 'it', 'titel': 'whatever', 'melding': 'dit', 'archived': True,"
        " 'events': [('zonet', 'iets'), ('straks', 'nog iets')]}})\n")

def test_actie_get_statustext(monkeypatch, capsys):
    """unittest for dml_mongo.Actie.get_statustext
    """
    def mock_read(*args):
        """stub
        """
        print('called Actie.read()')
    monkeypatch.setattr(dmlm, 'Settings', MockSettings)
    monkeypatch.setattr(dmlm.Actie, 'read', mock_read)
    testobj = dmlm.Actie('', '1')
    testobj.settings.stat = {'0': ('nieuw', 0)}
    testobj.status = 0
    assert testobj.get_statustext() == 'nieuw'
    assert capsys.readouterr().out == 'called Actie.read()\n'
    testobj.status = 1
    with pytest.raises(dmlm.DataError) as excinfo:
        testobj.get_statustext()
    assert str(excinfo.value) == 'Geen tekst gevonden bij statuscode 1'

def test_actie_get_soorttext(monkeypatch, capsys):
    """unittest for dml_mongo.Actie.get_soorttext
    """
    def mock_read(*args):
        """stub
        """
        print('called Actie.read()')
    monkeypatch.setattr(dmlm, 'Settings', MockSettings)
    monkeypatch.setattr(dmlm.Actie, 'read', mock_read)
    testobj = dmlm.Actie('', '1')
    testobj.settings.cat = {'N': ('nieuw', 0)}
    testobj.soort = 'N'
    assert testobj.get_soorttext() == 'nieuw'
    assert capsys.readouterr().out == 'called Actie.read()\n'
    testobj.soort = 'Q'
    with pytest.raises(dmlm.DataError) as excinfo:
        testobj.get_soorttext()
    assert str(excinfo.value) == 'Geen tekst gevonden bij soortcode Q'

def test_actie_add_event(monkeypatch, capsys):
    """unittest for dml_mongo.Actie.add_event
    """
    def mock_read(*args):
        """stub
        """
        print('called Actie.read()')
    monkeypatch.setattr(dmlm.dt, 'datetime', MockDatetime)
    monkeypatch.setattr(dmlm, 'Settings', MockSettings)
    monkeypatch.setattr(dmlm.Actie, 'read', mock_read)
    testobj = dmlm.Actie('', 'x')
    assert testobj.events == []
    testobj.add_event('some text')
    assert testobj.events == [('01-01-2020 00:12:00', 'some text')]
    assert capsys.readouterr().out == 'called Actie.read()\n'

def test_actie_cleanup(monkeypatch, capsys):
    """unittest for dml_mongo.Actie.cleanup
    """
    def mock_read(*args):
        """stub
        """
        print('called Actie.read()')
    def mock_remove(*args):
        """stub
        """
        print('called os.remove() with args', args)
    monkeypatch.setattr(dmlm.os, 'remove', mock_remove)
    monkeypatch.setattr(dmlm, 'Settings', MockSettings)
    monkeypatch.setattr(dmlm.Actie, 'read', mock_read)
    testobj = dmlm.Actie('', '1')
    testobj.imagelist = ['image1', 'image2']
    testobj.cleanup()
    assert capsys.readouterr().out == ('called Actie.read()\n'
                                       "called os.remove() with args ('image1',)\n"
                                       "called os.remove() with args ('image2',)\n")
