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
