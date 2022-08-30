import sys
import os
import types
import pytest

sys.path.append("/home/albert/projects/actiereg")  # location of actiereg project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "actiereg.settings")

import django
django.setup()

import probreg.dml_django as dml

def test_get_projnames(monkeypatch, capsys):
    testfilename = '/tmp/actieregtestapps.dat'
    with open(testfilename, 'w') as f:
        print('X;bep1;app1;testapp #1', file=f)
        print(';app2;app2;testapp #2', file=f)
        print('X;app3;app3;testapp #3', file=f)
    monkeypatch.setattr(dml, 'APPS', dml.pathlib.Path(testfilename))
    assert dml.get_projnames() == [('app3', 'App3', 'testapp #3'), ('bep1', 'App1', 'testapp #1')]


@pytest.mark.django_db
def test_get_user():
    me = django.contrib.auth.models.User(username='testuser')
    me.save()
    assert dml.get_user('me') is None
    assert dml.get_user('testuser') == me


@pytest.mark.django_db
def test_validate_user(monkeypatch):
    monkeypatch.setattr(dml, 'get_user', lambda x: None)
    assert dml.validate_user('naam', 'passw', 'project') is None
    me = django.contrib.auth.models.User(username='testuser')
    me.save()
    monkeypatch.setattr(dml, 'get_user', lambda x: me)
    monkeypatch.setattr(dml.django.contrib.auth.hashers, 'check_password', lambda *x: False)
    assert dml.validate_user('naam', 'passw', 'project') is None
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
        return [types.SimpleNamespace(), types.SimpleNamespace()]
    monkeypatch.setattr(dml, 'MY', {'test': 'stuff'})
    with pytest.raises(dml.DataError) as exc:
        data = dml.get_acties('not_test')
    assert str(exc.value) == 'not_test bestaat niet'
    monkeypatch.setattr(dml.core, 'get_acties', mock_get_no_acties)
    assert dml.get_acties('test') == []
    assert capsys.readouterr().out == "called core.get_acties() with args ('stuff', 0)\n"
