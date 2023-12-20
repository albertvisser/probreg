import pytest
import datetime
from probreg import shared

FIXDATE = datetime.datetime(2020, 1, 1)

class MockDatetime:
    def now():
        return FIXDATE

def test_log(monkeypatch, capsys):
    def mock_log(*args):
        print('called logging.info() with args', args)
    monkeypatch.setattr(shared.logging, 'info', mock_log)
    monkeypatch.setattr(shared.os, 'environ', {})
    shared.log('message')
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(shared.os, 'environ', {'DEBUG': False})
    shared.log('message')
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(shared.os, 'environ', {'DEBUG': True})
    shared.log('message')
    assert capsys.readouterr().out == "called logging.info() with args ('message',)\n"


def test_get_dts(monkeypatch, capsys):
    monkeypatch.setattr(shared.datetime, 'datetime', MockDatetime)
    assert shared.get_dts() == '01-01-2020 00:00:00'


def test_tabsize():
    assert shared.tabsize(0) == 0
    assert shared.tabsize(1) == 4
    assert shared.tabsize(2) == 8
    assert shared.tabsize(3) == 8
    assert shared.tabsize(4) == 12
    assert shared.tabsize(5) == 16
    assert shared.tabsize(6) == 20
    assert shared.tabsize(7) == 24
    assert shared.tabsize(8) == 24
    assert shared.tabsize(9) == 28
    assert shared.tabsize(10) == 32
