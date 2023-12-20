"""Unit tests for XML dml
"""
import os
import types
import datetime
import pathlib
import pytest
import probreg.dml_xml as dml
from unittests.dml_xml_fixtures import (get_acties_fixture, settings_fixture, settings_output,
        actie_fixture, actie_output)

FIXDATE = datetime.datetime(2020, 1, 1)

class MockDate:
    def today():
        return types.SimpleNamespace(year=2022)


class MockSettings:
    def __init__(self, fnaam=''):
        self.imagecount = 1
        self.startitem = 0
    def write(self):
        print('called Settings.write()')


class MockDatetime:
    def utcnow(*args):
        return 'now'
    def today(*args):
        return FIXDATE
    def now():
        return FIXDATE


class MockTree(dml.ElementTree):
    def __init__(self, *args, **kwargs):
        print('called ElementTree.__init__()')


class MockElement:
    def __init__(self, *args, **kwargs):
        print('called Element() with args', args)
        self.tag = args[0] if len(args) > 0 else ''
        self.attrs = args[1] if len(args) > 1 else {}
        self.attrs.update(kwargs)
    def __iter__(self, *args):
        return (x for x in [])
    def __setattr__(self, *args):
        print('called Element.__setattr__() with args', args)
        super().__setattr__(*args)
    def findall(self, *args):
        pass
    def find(self, *args):
        print('called Element.find() with args', args)
    def get(self, *args):
        pass
    def set(self, *args):
        if args[0] == 'updated':
            print('called Element.set() with first arg', args[0])
        else:
            print('called Element.set() with args', args)
    def remove(self, *args):
        print('called Element.remove() for subelement', args[0].tag)


def test_check_filename(monkeypatch, capsys):
    monkeypatch.setattr(pathlib.Path, 'exists', lambda x: True)
    assert dml.check_filename('') == (None, '', False, 'Please provide a filename')
    assert dml.check_filename(pathlib.Path('test')) == (
            pathlib.Path('./test'), 'test', True, 'Filename incorrect (must end in .xml)')
    assert dml.check_filename(pathlib.Path('test.xml')) == (
            pathlib.Path('test.xml'), 'test.xml', True, '')
    assert dml.check_filename(pathlib.Path('here/test.xml')) == (
            pathlib.Path('here/test.xml'), 'test.xml', True, '')


def test_checkfile(monkeypatch, capsys):
    filename = pathlib.Path('/tmp/name')
    if filename.exists():
        filename.unlink()
    assert dml.checkfile(filename) == '/tmp/name bestaat niet'
    filename.write_text('<root><element/></root>')
    assert dml.checkfile(pathlib.Path('/tmp/name')) == '/tmp/name is geen bruikbaar xml bestand'
    filename.write_text('<acties><actie/></acties>')
    assert dml.checkfile(pathlib.Path('/tmp/name')) == ''
    data = filename.read_text()
    assert data == '<acties><actie/></acties>'
    assert dml.checkfile(pathlib.Path('/tmp/name'), new=True) == ''
    data = filename.read_text()
    assert data == ("<?xml version='1.0' encoding='utf-8'?>\n"
            '<acties><settings imagecount="0"><stats><stat order="0" value="0">gemeld</stat>'
            '<stat order="1" value="1">in behandeling</stat><stat order="2" value="2">oplossing'
            ' controleren</stat><stat order="3" value="3">nog niet opgelost</stat><stat order="4"'
            ' value="4">afgehandeld</stat><stat order="5" value="5">afgehandeld - vervolg</stat>'
            '</stats><cats><cat order="1" value="P">probleem</cat><cat order="2" value="W">wens'
            '</cat><cat order="0" value=" ">onbekend</cat><cat order="3" value="V">vraag</cat>'
            '<cat order="4" value="I">idee</cat><cat order="5" value="F">div. informatie</cat>'
            '</cats><koppen><kop value="0">Lijst</kop><kop value="1">Titel/Status</kop><kop'
            ' value="2">Probleem/Wens</kop><kop value="3">Oorzaak/Analyse</kop><kop value="4">'
            'Oplossing/SvZ</kop><kop value="5">Vervolgactie</kop><kop value="6">Voortgang</kop>'
            '</koppen></settings></acties>')


def test_get_nieuwetitel(monkeypatch, capsys):
    def mock_init(*args, **kwargs):
        print("called ElementTree.__init__() with kwargs", kwargs)
    def mock_getroot(*args):
        root = dml.Element('acties')
        return root
    def mock_getroot_2(*args):
        root = dml.Element('acties')
        dml.SubElement(root, 'actie', id='2020-0001')
        dml.SubElement(root, 'actie', id='2021-0001')
        return root
    def mock_getroot_3(*args):
        root = dml.Element('acties')
        dml.SubElement(root, 'actie', id='2020-0001')
        dml.SubElement(root, 'actie', id='2021-0001')
        dml.SubElement(root, 'actie', id='2022-0001')
        return root
    monkeypatch.setattr(dml.dt, 'date', MockDate)
    monkeypatch.setattr(pathlib.Path, 'exists', lambda x: False)
    with pytest.raises(dml.DataError) as exc:
        dml.get_nieuwetitel(pathlib.Path(''))
    assert str(exc.value) == 'Datafile bestaat niet'
    monkeypatch.setattr(pathlib.Path, 'exists', lambda x: True)
    monkeypatch.setattr(MockTree, '__init__', mock_init)
    monkeypatch.setattr(MockTree, 'getroot', mock_getroot)
    monkeypatch.setattr(dml, 'ElementTree', MockTree)
    assert dml.get_nieuwetitel(pathlib.Path('')) == '2022-0001'
    assert capsys.readouterr().out == "called ElementTree.__init__() with kwargs {'file': '.'}\n"
    assert dml.get_nieuwetitel(pathlib.Path(''), 2020) == '2020-0001'
    assert capsys.readouterr().out == "called ElementTree.__init__() with kwargs {'file': '.'}\n"
    monkeypatch.setattr(dml.ElementTree, 'getroot', mock_getroot_2)
    assert dml.get_nieuwetitel(pathlib.Path('')) == '2022-0001'
    assert capsys.readouterr().out == "called ElementTree.__init__() with kwargs {'file': '.'}\n"
    assert dml.get_nieuwetitel(pathlib.Path(''), 2020) == '2020-0002'
    assert capsys.readouterr().out == "called ElementTree.__init__() with kwargs {'file': '.'}\n"
    monkeypatch.setattr(dml.ElementTree, 'getroot', mock_getroot_3)
    assert dml.get_nieuwetitel(pathlib.Path('')) == '2022-0002'
    assert capsys.readouterr().out == "called ElementTree.__init__() with kwargs {'file': '.'}\n"
    assert dml.get_nieuwetitel(pathlib.Path(''), 2020) == '2020-0002'
    assert capsys.readouterr().out == "called ElementTree.__init__() with kwargs {'file': '.'}\n"


def test_get_acties(monkeypatch, capsys, get_acties_fixture):
    class MockSettings:
        def __init__(self, *args):
            self.stat = {'0': 'Gemeld', '1': 'In behandeling'}
            self.cat = {'P': 'Probleem', 'W': 'Wens'}
    monkeypatch.setattr(dml, 'Settings', MockSettings)
    with pytest.raises(dml.DataError) as exc:
        lijst = dml.get_acties(pathlib.Path('x'))
    # assert str(exc.value) == 'Filename incorrect (must end in .xml)'
    # with pytest.raises(dml.DataError) as exc:
    #     lijst = dml.get_acties(pathlib.Path('x.xml'))
    assert str(exc.value) == 'Datafile bestaat niet'
    with pytest.raises(dml.DataError) as exc:
        lijst = dml.get_acties('x', {'foute': 'waarde'})
    assert str(exc.value) == 'Foutief selectie-argument opgegeven'
    with pytest.raises(dml.DataError) as exc:
        lijst = dml.get_acties('x', {'id': 'x'})
    assert str(exc.value) == 'Foutieve combinatie van selectie-argumenten opgegeven'
    with pytest.raises(dml.DataError) as exc:
        lijst = dml.get_acties('x', {'id': 'x', 'idlt': 'y'})
    assert str(exc.value) == 'Foutieve combinatie van selectie-argumenten opgegeven'
    with pytest.raises(dml.DataError) as exc:
        lijst = dml.get_acties('x', {'id': 'x', 'idgt': 'y'})
    assert str(exc.value) == 'Foutieve combinatie van selectie-argumenten opgegeven'
    with pytest.raises(dml.DataError) as exc:
        lijst = dml.get_acties('x', arch='y')
    assert str(exc.value) == ('Foutieve waarde voor archief opgegeven'
                              " (moet leeg, 'arch' of 'alles' zijn)")
    testfile = get_acties_fixture
    lijst = dml.get_acties(testfile)    # niet geachiveerde
    assert [x[0] for x in lijst] == ['1', '3', '4', '6']
    lijst = dml.get_acties(testfile, arch='arch')
    assert [x[0] for x in lijst] == ['2', '5']
    lijst = dml.get_acties(testfile, arch='alles')
    assert [x[0] for x in lijst] == ['1', '2', '3', '4', '5', '6']
    lijst = dml.get_acties(testfile, select={'idlt': '4'}, arch='alles')
    assert [x[0] for x in lijst] == ['1', '2', '3']
    lijst = dml.get_acties(testfile, select={'idgt': '4'}, arch='alles')
    assert [x[0] for x in lijst] == ['5', '6']
    lijst = dml.get_acties(testfile, select={'idlt': '5', 'id': 'and', 'idgt': '2'}, arch='alles')
    assert [x[0] for x in lijst] == ['3', '4']
    lijst = dml.get_acties(testfile, select={'idlt': '3', 'id': 'or', 'idgt': '4'}, arch='alles')
    assert [x[0] for x in lijst] == ['1', '2', '5', '6']
    lijst = dml.get_acties(testfile, select={'soort': 'P'}, arch='alles')
    assert [x[0] for x in lijst] == ['1', '2', '4']
    lijst = dml.get_acties(testfile, select={'status': '1'}, arch='alles')
    assert [x[0] for x in lijst] == ['2', '4', '6']
    lijst = dml.get_acties(testfile, select={'titel': 'een act'}, arch='alles')
    assert [x[0] for x in lijst] == ['1', '2', '4', '5']


def test_settings_init(monkeypatch, capsys):
    def mock_read(self):
        print('called Settings.read()')
    monkeypatch.setattr(dml.Settings, 'read', mock_read)
    testobj = dml.Settings()
    assert testobj.kop == {x: (y[0],) for x, y in dml.kopdict.items()}
    assert testobj.stat == {x: (y[0], y[1]) for x, y in dml.statdict.items()}
    assert testobj.cat == {x: (y[0], y[1]) for x, y in dml.catdict.items()}
    assert testobj.imagecount == 0
    assert testobj.startitem == ''
    assert testobj.meld == "Standaard waarden opgehaald"
    monkeypatch.setattr(dml, 'check_filename', lambda x: ('x', 'y', False, "Something's not right"))
    with pytest.raises(dml.DataError) as exc:
        testobj = dml.Settings('name`')
    assert str(exc.value) == "Something's not right"
    monkeypatch.setattr(dml, 'check_filename', lambda x: ('x', 'y', True, "xxxx"))
    with pytest.raises(dml.DataError) as exc:
        testobj = dml.Settings('name`')
    assert str(exc.value) == "xxxx"
    monkeypatch.setattr(dml, 'check_filename', lambda x: ('x', 'y', False, ""))
    testobj = dml.Settings('name`')
    assert testobj.fn == 'x'
    assert testobj.fnaam == 'y'
    assert testobj.meld == "Datafile bestaat nog niet, Standaard waarden opgehaald"
    monkeypatch.setattr(dml, 'check_filename', lambda x: ('x', 'y', True, ""))
    testobj = dml.Settings('name`')
    assert testobj.fn == 'x'
    assert testobj.fnaam == 'y'
    assert testobj.meld == ""
    assert capsys.readouterr().out == 'called Settings.read()\n'


def test_settings_read(monkeypatch, capsys, tmp_path, settings_fixture):
    testpath = tmp_path / 'testprobregdml.xml'
    testobj = dml.Settings(settings_fixture.nosett())
    assert testobj.fn == testpath
    assert testobj.fnaam == testpath.name
    assert testobj.kop == {}
    assert testobj.stat == {}
    assert testobj.cat == {}
    assert testobj.imagecount == 0
    assert testobj.startitem == ''

    testobj = dml.Settings(settings_fixture.justsett())
    assert testobj.fn == testpath
    assert testobj.fnaam == testpath.name
    assert testobj.kop == {}
    assert testobj.stat == {}
    assert testobj.cat == {}
    assert testobj.imagecount == 0
    assert testobj.startitem == ''

    testobj = dml.Settings(settings_fixture.toplevels())
    assert testobj.fn == testpath
    assert testobj.fnaam == testpath.name
    assert testobj.kop == {}
    assert testobj.stat == {}
    assert testobj.cat == {}
    assert testobj.imagecount == 5
    assert testobj.startitem == '15'

    testobj = dml.Settings(settings_fixture.all_levels())
    assert testobj.fn == testpath
    assert testobj.fnaam == testpath.name
    assert testobj.kop == {'0': ('Overzicht',), '1': ('Details',)}
    assert testobj.stat == {'0': ('gemeld', '0'), '1': ('In behandeling', '1')}
    assert testobj.cat == {'P': ('Probleem', '1'), 'W': ('Wens', '2')}
    assert testobj.imagecount == 5
    assert testobj.startitem == '15'


def test_settings_write(monkeypatch, capsys, settings_output):
    def mock_getroot(self):
        print('called ElementTree.getroot()')
        return MockElement()
    def mock_write(self, *args, **kwargs):
        print('called ElementTree.write() with args', args, kwargs)
    def mock_subelement(*args, **kwargs):
        args_ = list(args)
        args_[0] = 'parent'
        print('called SubElement() with args ', args_, kwargs)
        return MockElement(args[1])
    def mock_copyfile(*args):
        print('called shutil.copyfile with args', args)
    def mock_init(self, *args):
        self.fn = pathlib.Path('anything_goes')
        print('called Settings()')
    def mock_iter(self, *args):
        return (x for x in [MockElement('stats'), MockElement('cats'), MockElement('koppen')])
    monkeypatch.setattr(dml, 'Element', MockElement)
    monkeypatch.setattr(dml.ElementTree, 'getroot', mock_getroot)
    monkeypatch.setattr(dml.ElementTree, 'write', mock_write)
    monkeypatch.setattr(dml, 'ElementTree', MockTree)
    monkeypatch.setattr(dml, 'SubElement', mock_subelement)
    monkeypatch.setattr(dml, 'copyfile', mock_copyfile)
    monkeypatch.setattr(dml.Settings, '__init__', mock_init)
    testobj = dml.Settings()
    testobj.exists = False
    testobj.imagecount = 5
    testobj.startitem = 15
    testobj.stat = {}
    testobj.cat = {}
    testobj.kop = {}
    testobj.write()
    assert testobj.exists
    assert capsys.readouterr().out == settings_output['new']

    monkeypatch.setattr(MockElement, '__iter__', mock_iter)
    monkeypatch.setattr(dml, 'Element', MockElement)
    monkeypatch.setattr(dml.ElementTree, 'getroot', mock_getroot)
    monkeypatch.setattr(dml.ElementTree, 'write', mock_write)
    monkeypatch.setattr(dml, 'ElementTree', MockTree)
    monkeypatch.setattr(dml, 'SubElement', mock_subelement)
    testobj = dml.Settings()
    testobj.exists = True
    testobj.imagecount = 5
    testobj.startitem = 15
    testobj.stat = {'0': ('this', '0'), 1: ('that', '1')}
    testobj.cat = {'a': ('something', '0'), 'b': ('anything', '1')}
    testobj.kop = {'1': ('ook',), 2: ('eek',)}
    testobj.write()
    assert testobj.exists
    assert capsys.readouterr().out == settings_output['existing']


def test_actie_init(monkeypatch, capsys):
    def mock_nieuw(self):
        print('called Actie.nieuw()')
    def mock_nieuwfile(self):
        print('called Actie.nieuwfile()')
    def mock_read(self):
        print('called Actie.read()')
    monkeypatch.setattr(dml, 'check_filename', lambda x: ('x', 'y', False, "Something's not right"))
    with pytest.raises(dml.DataError) as exc:
        testobj = dml.Actie('name`', 'x')
    assert str(exc.value) == "Something's not right"
    monkeypatch.setattr(dml, 'check_filename', lambda x: ('x', 'y', True, "xxxx"))
    with pytest.raises(dml.DataError) as exc:
        testobj = dml.Actie('name`', 'x')
    assert str(exc.value) == "xxxx"
    monkeypatch.setattr(dml, 'Settings', MockSettings)
    monkeypatch.setattr(dml.Actie, 'nieuw', mock_nieuw)
    monkeypatch.setattr(dml.Actie, 'nieuwfile', mock_nieuwfile)
    monkeypatch.setattr(dml.Actie, 'read', mock_read)
    monkeypatch.setattr(dml, 'check_filename', lambda x: ('x', 'y', False, ""))
    with pytest.raises(dml.DataError) as exc:
        testobj = dml.Actie('x', 1)
    assert str(exc.value) == "Can't pass non-empty id for nonexistant file"
    testobj = dml.Actie('x', 0)
    assert capsys.readouterr().out == 'called Actie.nieuwfile()\ncalled Actie.nieuw()\n'
    testobj = dml.Actie('x', '0')
    assert capsys.readouterr().out == 'called Actie.nieuwfile()\ncalled Actie.nieuw()\n'
    monkeypatch.setattr(dml, 'check_filename', lambda x: ('x', 'y', True, ""))
    testobj = dml.Actie('x', 1)
    assert capsys.readouterr().out == 'called Actie.read()\n'
    testobj = dml.Actie('x', 0)
    assert capsys.readouterr().out == 'called Actie.nieuw()\n'
    testobj = dml.Actie('x', '0')
    assert capsys.readouterr().out == 'called Actie.nieuw()\n'


def test_actie_nieuwfile(monkeypatch, capsys):
    testfilename = '/tmp/testactie.xml'
    def mock_init(self, *args):
        self.fn = pathlib.Path(testfilename)
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    testobj = dml.Actie()
    testobj.nieuwfile()
    assert os.path.exists(testfilename)
    with open(testfilename) as f:
        data = f.read()
    assert data == '<?xml version="1.0" encoding="utf-8"?>\n<acties>\n</acties>\n'


def test_actie_nieuw(monkeypatch, capsys):
    testfilename = '/tmp/testactie.xml'
    def mock_init(self, *args):
        self.fn = pathlib.Path(testfilename)
    monkeypatch.setattr(dml, 'get_nieuwetitel', lambda *x: f'nieuw item voor {x[0]}')
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    monkeypatch.setattr(dml.dt, 'datetime', MockDatetime)
    testobj = dml.Actie()
    testobj.nieuw()
    assert testobj.id == 'nieuw item voor /tmp/testactie.xml'
    assert testobj.datum == '2020-01-01 00:00:00'


def test_actie_read(monkeypatch, capsys, actie_fixture):
    # testfilename = '/tmp/testactie.xml'
    # testpath = pathlib.Path(testfilename)
    monkeypatch.setattr(dml.dt, 'datetime', MockDatetime)
    testobj = dml.Actie(actie_fixture.justaroot(), '1')
    testobj.read()
    assert not testobj.exists
    testobj = dml.Actie(actie_fixture.wrongaction(), '1')
    testobj.read()
    assert not testobj.exists
    testobj = dml.Actie(actie_fixture.incomplete(), '1')
    testobj.read()
    assert testobj.exists
    assert testobj.datum ==''
    assert testobj.status == '1'
    assert testobj.soort == 'P'
    assert not testobj.arch
    assert testobj.updated == '2020-01-01 00:00:00'
    assert testobj.titel == ''
    assert testobj.melding == ''
    assert testobj.oorzaak == ''
    assert testobj.oplossing == ''
    assert testobj.vervolg == ''
    assert testobj.events == []
    assert testobj.imagelist == []
    testobj = dml.Actie(actie_fixture.complete(), '1')
    testobj.read()
    assert testobj.exists
    assert testobj.datum =='x'
    assert testobj.status == '1'
    assert testobj.soort == 'P'
    assert testobj.arch
    assert testobj.updated == 'y'
    assert testobj.titel == 'Dit'
    assert testobj.melding == 'Dat'
    assert testobj.oorzaak == 'Iets'
    assert testobj.oplossing == 'Iets anders'
    assert testobj.vervolg == 'Nog iets'
    assert testobj.events == [('now', 'hello'), ('then', 'sailor')]
    assert testobj.imagelist == ['/tmp/x.img']
    assert os.path.exists('/tmp/x.img')


def test_actie_get_statustext(monkeypatch, capsys):
    testfilename = '/tmp/testactie.xml'
    def mock_init(self, *args):
        self.fn = pathlib.Path(testfilename)
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    testobj = dml.Actie()
    testobj.status = (1, '1')
    testobj.settings = types.SimpleNamespace(stat={'1': ('active', 1)})
    assert testobj.get_statustext() == 'active'
    testobj.status = (0, 1)
    with pytest.raises(dml.DataError) as exc:
        testobj.get_statustext()
    assert str(exc.value) == 'Geen tekst gevonden bij statuscode 0'


def test_actie_get_soorttext(monkeypatch, capsys):
    testfilename = '/tmp/testactie.xml'
    def mock_init(self, *args):
        self.fn = pathlib.Path(testfilename)
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    testobj = dml.Actie()
    testobj.soort = 'P'
    testobj.settings = types.SimpleNamespace(cat={'P': ('probleem', 1)})
    assert testobj.get_soorttext() == 'probleem'
    testobj.soort = '0'
    with pytest.raises(dml.DataError) as exc:
        testobj.get_soorttext()
    assert str(exc.value) == 'Geen tekst gevonden bij soortcode 0'


def test_actie_add_event(monkeypatch, capsys):
    testfilename = '/tmp/testactie.xml'
    def mock_init(self, *args):
        self.fn = pathlib.Path(testfilename)
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    monkeypatch.setattr(dml.dt, 'datetime', MockDatetime)
    testobj = dml.Actie()
    testobj.events = []
    testobj.add_event('new event')
    assert testobj.events == [('01-01-2020 00:12:00', 'new event')]


def test_actie_write(monkeypatch, capsys, actie_output):
    def mock_getroot(self):
        print('called ElementTree.getroot()')
        return MockElement()
    def mock_write(self, *args, **kwargs):
        print('called ElementTree.write() with args', args, kwargs)
    def mock_subelement(*args, **kwargs):
        args_ = list(args)
        args_[0] = 'parent'
        print('called SubElement() with args ', args_, kwargs)
        return MockElement(args[1])
    def mock_copyfile(*args):
        print('called shutil.copyfile with args', args)
    def mock_findall(self, *args):
        print('called Element.findall() with args', args)
        return [MockElement('actie', id='1'), MockElement('actie', id='2')]
    def mock_get(self, *args):
        print('called Element.get() with args', args)
    def mock_get_2(self, *args):
        print('called Element.get() with args', args)
        return self.attrs.get('id')
    def mock_find(self, *args):
        print('called Element.find() with args', args)
        return MockElement(args[0])
    monkeypatch.setattr(MockElement, 'findall', mock_findall)
    monkeypatch.setattr(MockElement, 'get', mock_get)
    monkeypatch.setattr(dml, 'Element', MockElement)
    monkeypatch.setattr(dml.ElementTree, 'getroot', mock_getroot)
    monkeypatch.setattr(dml.ElementTree, 'write', mock_write)
    monkeypatch.setattr(dml, 'ElementTree', MockTree)
    monkeypatch.setattr(dml, 'SubElement', mock_subelement)
    monkeypatch.setattr(dml, 'copyfile', mock_copyfile)

    testfilename = '/tmp/testactie.xml'
    def mock_init(self, *args):
        self.fn = pathlib.Path(testfilename)
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    testobj = dml.Actie()
    testobj.file_exists = False
    testobj.exists = False
    testobj.imagecount = 0
    testobj.id = '1'
    testobj.datum = 'now'
    testobj.soort = 'P'
    testobj.status = '0'
    testobj.arch = False
    testobj.titel = 'Paniek in de biertent'
    testobj.melding = 'Er is iets gebeurd'
    testobj.oorzaak = 'Het kwam hierdoor'
    testobj.oplossing = 'Dit hebben we eraan gedaan'
    testobj.vervolg = 'Dit moet ook nog'
    testobj.events = [('ooit', 'deden we dit'), ('later', 'deden we dit')]
    testobj.imagelist = []
    assert testobj.write()
    assert capsys.readouterr().out == actie_output['new']

    # testobj.file_exists = False
    # testobj.exists = True  # kan dit?
    # testobj.id = '1'
    # testobj.datum='now'
    # testobj.write()

    # testobj.file_exists = True
    # testobj.exists = False
    # testobj.id = '1'
    # testobj.datum='now'
    # testobj.write()

    monkeypatch.setattr(MockElement, 'findall', mock_findall)
    monkeypatch.setattr(MockElement, 'find', mock_find)
    monkeypatch.setattr(MockElement, 'get', mock_get_2)
    monkeypatch.setattr(dml, 'Element', MockElement)
    monkeypatch.setattr(dml.ElementTree, 'getroot', mock_getroot)
    monkeypatch.setattr(dml.ElementTree, 'write', mock_write)
    monkeypatch.setattr(dml, 'ElementTree', MockTree)
    monkeypatch.setattr(dml, 'SubElement', mock_subelement)
    monkeypatch.setattr(dml, 'copyfile', mock_copyfile)
    testobj.file_exists = True
    testobj.exists = True
    testobj.id = '1'
    testobj.datum='now'
    testobj.soort = ''
    testobj.status = '0'
    testobj.arch = True
    testobj.titel = 'Paniek in de biertent'
    testobj.melding = 'Er is iets gebeurd'
    testobj.oorzaak = 'Het kwam hierdoor'
    testobj.oplossing = 'Dit hebben we eraan gedaan'
    testobj.vervolg = 'Dit moet ook nog'
    testobj.events = [('ooit', 'deden we dit'), ('later', 'deden we dit')]
    testobj.imagelist = []
    assert testobj.write()
    assert capsys.readouterr().out == actie_output['old']


def test_actie_cleanup(monkeypatch, capsys):
    def mock_remove(fname):
        print(f'called os.remove on file {fname}')
    testfilename = '/tmp/testactie.xml'
    def mock_init(self, *args):
        self.fn = pathlib.Path(testfilename)
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    monkeypatch.setattr(dml.os, 'remove', mock_remove)
    testobj = dml.Actie()
    testobj.imagelist = ['image1.png', 'image2.png']
    testobj.cleanup()
    assert capsys.readouterr().out == ('called os.remove on file image1.png\n'
                                       'called os.remove on file image2.png\n')


def test_actie_list(monkeypatch, capsys):
    testfilename = '/tmp/testactie.xml'
    def mock_init(self, *args):
        self.fn = pathlib.Path(testfilename)
    def mock_get_soorttext(self, *args):
        return 'Probleem'
    def mock_get_soorttext_err(self, *args):
        raise dml.DataError
    def mock_get_statustext(self, *args):
        return 'In behandeling'
    def mock_get_statustext_err(self, *args):
        raise dml.DataError
    monkeypatch.setattr(dml.Actie, '__init__', mock_init)
    monkeypatch.setattr(dml.Actie, 'get_soorttext', mock_get_soorttext)
    monkeypatch.setattr(dml.Actie, 'get_statustext', mock_get_statustext)
    testobj = dml.Actie()
    testobj.id = '2020-0001'
    testobj.soort = 'P'
    testobj.status = '1'
    testobj.datum = '2020-01-01'
    testobj.titel = 'Something happened'
    testobj.melding = 'A strange phenomenon occurred'
    testobj.oorzaak = 'This caused it'
    testobj.oplossing = 'This resolved it'
    testobj.vervolg = "But wait... there's more"
    testobj.events = [('first', 'it broke'), ('then', 'we fixed it')]
    testobj.arch = ''
    assert testobj.list() == ['Probleem 2020-0001 gemeld op 2020-01-01 status 1 In behandeling',
            'Titel: Something happened',
            'Melding: A strange phenomenon occurred',
            'Oorzaak: This caused it',
            'Oplossing: This resolved it',
            "Vervolg: But wait... there's more",
            'Verslag:',
            '\tfirst - it broke',
            '\tthen - we fixed it']
    monkeypatch.setattr(dml.Actie, 'get_soorttext', mock_get_soorttext_err)
    monkeypatch.setattr(dml.Actie, 'get_statustext', mock_get_statustext_err)
    testobj = dml.Actie()
    testobj.id = '2020-0001'
    testobj.soort = 'P'
    testobj.status = '1'
    testobj.datum = '2020-01-01'
    testobj.titel = 'Something happened'
    testobj.melding = 'A strange phenomenon occurred'
    testobj.oorzaak = 'This caused it'
    testobj.oplossing = 'This resolved it'
    testobj.vervolg = "But wait... there's more"
    testobj.events = [('first', 'it broke'), ('then', 'we fixed it')]
    testobj.arch = 'arch'
    assert testobj.list() == ['P 2020-0001 gemeld op 2020-01-01 status 1',
            'Titel: Something happened',
            'Melding: A strange phenomenon occurred',
            'Oorzaak: This caused it',
            'Oplossing: This resolved it',
            "Vervolg: But wait... there's more",
            'Verslag:',
            '\tfirst - it broke',
            '\tthen - we fixed it',
            'Actie is gearchiveerd.']

