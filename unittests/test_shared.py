"""unittests for ./probreg/shared.py
"""
import datetime
from probreg import shared

FIXDATE = datetime.datetime(2020, 1, 1)


class MockDatetime:
    """stub
    """
    @staticmethod
    def now():
        """stub
        """
        return FIXDATE


def test_log(monkeypatch, capsys):
    """unittest for shared.log
    """
    def mock_log(*args):
        """stub
        """
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


def test_get_dts(monkeypatch):
    """unittest for shared.get_dts
    """
    monkeypatch.setattr(shared.datetime, 'datetime', MockDatetime)
    assert shared.get_dts() == '01-01-2020 00:00:00'


def test_tabsize():
    """unittest for shared.tabsize
    """
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
