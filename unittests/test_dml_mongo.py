import types
import pytest
import probreg.dml_mongo as dmlm

class MockDate:
    def today():
        return types.SimpleNamespace(year=2022)

class MockDatetime:
    def utcnow(*args):
        return 'now'

class MockColl:
    def find(self, *args, **kwargs):
        pass  # in testmethode patchen met gewenst resultaat

    def find_one(self, *args, **kwargs):
        pass  # in testmethode patchen met gewenst resultaat

def test_get_nieuwetitel(monkeypatch, capsys):
    def mock_find(self, *args, **kwargs):
        return [{'nummer': 1}, {'nummer': 17}, {'nummer': 5}]
    monkeypatch.setattr(dmlm.dt, 'date', MockDate)
    monkeypatch.setattr(MockColl, 'find', mock_find)
    monkeypatch.setattr(dmlm, 'coll', MockColl())
    assert dmlm.get_nieuwetitel('') == '2022-0018'
    assert dmlm.get_nieuwetitel('', 2020) == '2020-0018'

def test_get_acties(monkeypatch, capsys):
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

    assert dmlm.get_acties('', select={'idlt': 'x'}) == '{"nummer": {"lt": "x"}}'
    assert dmlm.get_acties('', select={'idgt': 'y'}) == '{"nummer": {"gt": "y"}}'
    assert dmlm.get_acties('', select={'idlt': 'x', 'id': 'en', 'idgt': 'y'}) == ('{"nummer":'
            ' {"lt": "x", "gt": "y"}}')
    assert dmlm.get_acties('', select={'idlt': 'x', 'id': 'of', 'idgt': 'y'}) == ('{"nummer":'
            ' {"or": {"lt": "x", "gt": "y"}}}')

    # bij zoeklogica doorgeven aan momgodb heeft uitkomst testen niet zoveel zin, kijken naar
    # output van gesimuleerd database commando wel
    result = [('2022-0001', 'vandaag', 'nieuw', 'idee', 'iets', 'vandaag', ''),
              ('2022-0002', 'vandaag', 'nieuw', 'idee', 'iets', 'vandaag', '')]
    # alles dat er is
    assert dmlm.get_acties('') == result
    assert dmlm.get_acties('', select={}) == result
    # alles dat niet gearchiveerd is
    assert dmlm.get_acties('', arch='') == result
    assert dmlm.get_acties('', select={}, arch='') == result
    # alles dat gearchiveerd is
    assert dmlm.get_acties('', arch='arch') == result
    # alles
    assert dmlm.get_acties('', arch='alles') == result

