"""unittests for ./probreg/gui_qt.py
"""
from mockgui import mockqtwidgets as mockqtw
from probreg import gui_qt as testee


class MockGui:
    def __init__(self, *args):
        print('called Gui.__init__ with args', args)

def test_show_message(monkeypatch, capsys):
    """unittest for gui_qt.show_message
    """
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    win = MockGui()
    assert capsys.readouterr().out == "called Gui.__init__ with args ()\n"
    testee.shared.app_title = 'xxx'
    testee.show_message(win, 'Message')
    assert capsys.readouterr().out == (
            f"called MessageBox.information with args `{win}` `xxx` `Message`\n")
    testee.show_message(win, 'Message', 'yyy')
    assert capsys.readouterr().out == (
            f"called MessageBox.information with args `{win}` `yyy` `Message`\n")


def test_get_open_filename(monkeypatch, capsys):
    """unittest for gui_qt.get_open_filename
    """
    monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
    monkeypatch.setattr(testee.pathlib.Path, 'cwd', testee.pathlib.Path.home)
    win = MockGui()
    assert capsys.readouterr().out == "called Gui.__init__ with args ()\n"
    testee.shared.app_title = 'xxx'
    assert testee.get_open_filename(win) == ''
    assert capsys.readouterr().out == (
            f"called FileDialog.getOpenFilename with args {win} ('xxx - kies een gegevensbestand',"
            f" '{testee.pathlib.Path.home()}', 'XML files (*.xml);;all files (*.*)') {{}}\n")
    assert testee.get_open_filename(win, start='qqq') == ""
    assert capsys.readouterr().out == (
            f"called FileDialog.getOpenFilename with args {win} ('xxx - kies een gegevensbestand',"
            f" 'qqq', 'XML files (*.xml);;all files (*.*)') {{}}\n")


def test_get_save_filename(monkeypatch, capsys):
    """unittest for gui_qt.get_save_filename
    """
    monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
    monkeypatch.setattr(testee.pathlib.Path, 'cwd', testee.pathlib.Path.home)
    win = MockGui()
    assert capsys.readouterr().out == "called Gui.__init__ with args ()\n"
    testee.shared.app_title = 'xxx'
    assert testee.get_save_filename(win) == ''
    assert capsys.readouterr().out == (
            f"called FileDialog.getSaveFilename with args {win} ('xxx - nieuw gegevensbestand',"
            f" '{testee.pathlib.Path.home()}', 'XML files (*.xml);;all files (*.*)') {{}}\n")
    assert testee.get_save_filename(win, start='qqq') == ""
    assert capsys.readouterr().out == (
            f"called FileDialog.getSaveFilename with args {win} ('xxx - nieuw gegevensbestand',"
            f" 'qqq', 'XML files (*.xml);;all files (*.*)') {{}}\n")


def test_get_choice_item(monkeypatch, capsys):
    """unittest for gui_qt.get_choice_item
    """
    def mock_get(*args, **kwargs):
        print('called InputDialog.getItem with args', args, kwargs)
        return 'aaa', True
    monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
    win = MockGui()
    assert capsys.readouterr().out == "called Gui.__init__ with args ()\n"
    assert testee.get_choice_item(win, 'caption', ['choices']) == ""
    assert capsys.readouterr().out == (
            f"called InputDialog.getItem with args {win} ('xxx', 'caption', ['choices'])"
            " {'current': 0, 'editable': False}\n")
    monkeypatch.setattr(mockqtw.MockInputDialog, 'getItem', mock_get)
    assert testee.get_choice_item(win, 'caption', ['choices'], current=1) == "aaa"
    assert capsys.readouterr().out == (
            f"called InputDialog.getItem with args ({win}, 'xxx', 'caption', ['choices'])"
            " {'current': 1, 'editable': False}\n")


def test_ask_cancel_question(monkeypatch, capsys):
    """unittest for gui_qt.ask_cancel_question
    """
    def mock_ask(parent, caption, message, buttons):
        print(f'called MessageBox.question with args `{parent}` `{caption}` `{message}` `{buttons}`')
        return mockqtw.MockMessageBox.Yes
    def mock_ask_2(parent, caption, message, buttons):
        print(f'called MessageBox.question with args `{parent}` `{caption}` `{message}` `{buttons}`')
        return mockqtw.MockMessageBox.Cancel
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    win = MockGui()
    assert capsys.readouterr().out == "called Gui.__init__ with args ()\n"
    testee.shared.app_title = 'xxx'
    assert testee.ask_cancel_question(win, 'question') == (False, False)
    assert capsys.readouterr().out == ("called MessageBox.question with args"
                                       f" `{win}` `xxx` `question` `14`\n")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question',mock_ask)
    assert testee.ask_cancel_question(win, 'question') == (True, False)
    assert capsys.readouterr().out == ("called MessageBox.question with args"
                                       f" `{win}` `xxx` `question` `14`\n")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question',mock_ask_2)
    assert testee.ask_cancel_question(win, 'question') == (False, True)
    assert capsys.readouterr().out == ("called MessageBox.question with args"
                                       f" `{win}` `xxx` `question` `14`\n")


def test_show_dialog(monkeypatch, capsys):
    """unittest for gui_qt.show_dialog
    """
    def mock_exec(self):
        print('called Dialog.exec_')
        return testee.qtw.QDialog.Accepted
    cls = mockqtw.MockDialog
    win = mockqtw.MockWidget()
    assert capsys.readouterr().out == 'called Widget.__init__\n'
    assert not testee.show_dialog(win, cls)
    assert capsys.readouterr().out == (f"called Dialog.__init__ with args {win} () {{}}\n"
                                       "called Dialog.exec_\n")
    monkeypatch.setattr(mockqtw.MockDialog, 'exec_', mock_exec)
    assert testee.show_dialog(win, cls, 'args')
    assert capsys.readouterr().out == (f"called Dialog.__init__ with args {win} ('args',) {{}}\n"
                                       "called Dialog.exec_\n")


class TestEditorPanel:
    """unittest for gui_qt.EditorPanel
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.EditorPanel object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EditorPanel.__init__ with args', args)
        testobj = testee.EditorPanel()
        assert capsys.readouterr().out == 'called EditorPanel.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for EditorPanel.__init__
        """
        testobj = testee.EditorPanel(parent)
        assert capsys.readouterr().out == ("")

    def _test_canInsertFromMimeData(self, monkeypatch, capsys):
        """unittest for EditorPanel.canInsertFromMimeData
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.canInsertFromMimeData(source) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_insertFromMimeData(self, monkeypatch, capsys):
        """unittest for EditorPanel.insertFromMimeData
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.insertFromMimeData(source) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_contents(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_contents(data) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_contents(self, monkeypatch, capsys):
        """unittest for EditorPanel.get_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_contents() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_bold(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_bold
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_bold() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_italic(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_italic
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_italic() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_underline(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_underline
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_underline() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_strikethrough(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_strikethrough
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_strikethrough() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_case_lower(self, monkeypatch, capsys):
        """unittest for EditorPanel.case_lower
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.case_lower() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_case_upper(self, monkeypatch, capsys):
        """unittest for EditorPanel.case_upper
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.case_upper() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_indent_more(self, monkeypatch, capsys):
        """unittest for EditorPanel.indent_more
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.indent_more() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_indent_less(self, monkeypatch, capsys):
        """unittest for EditorPanel.indent_less
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.indent_less() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_change_indent(self, monkeypatch, capsys):
        """unittest for EditorPanel.change_indent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.change_indent(amount) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_font(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_font
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_font() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_family(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_family
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_family(family) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enlarge_text(self, monkeypatch, capsys):
        """unittest for EditorPanel.enlarge_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enlarge_text() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_shrink_text(self, monkeypatch, capsys):
        """unittest for EditorPanel.shrink_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.shrink_text() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_linespacing_1(self, monkeypatch, capsys):
        """unittest for EditorPanel.linespacing_1
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.linespacing_1() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_linespacing_15(self, monkeypatch, capsys):
        """unittest for EditorPanel.linespacing_15
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.linespacing_15() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_linespacing_2(self, monkeypatch, capsys):
        """unittest for EditorPanel.linespacing_2
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.linespacing_2() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_linespacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_linespacing
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_linespacing(amount) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_increase_paragraph_spacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.increase_paragraph_spacing
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.increase_paragraph_spacing() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_decrease_paragraph_spacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.decrease_paragraph_spacing
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.decrease_paragraph_spacing() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_paragraph_spacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_paragraph_spacing
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_paragraph_spacing(more=False, less=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_size(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_size
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_size(size) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_charformat_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.charformat_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.charformat_changed(format) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_cursorposition_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.cursorposition_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.cursorposition_changed() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_font_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.font_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.font_changed(font) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_mergeCurrentCharFormat(self, monkeypatch, capsys):
        """unittest for EditorPanel.mergeCurrentCharFormat
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.mergeCurrentCharFormat(format) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_update_bold(self, monkeypatch, capsys):
        """unittest for EditorPanel.update_bold
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.update_bold() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_update_italic(self, monkeypatch, capsys):
        """unittest for EditorPanel.update_italic
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.update_italic() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_update_underline(self, monkeypatch, capsys):
        """unittest for EditorPanel.update_underline
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.update_underline() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test__check_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanel._check_dirty
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj._check_dirty() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test__mark_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanel._mark_dirty
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj._mark_dirty(value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test__openup(self, monkeypatch, capsys):
        """unittest for EditorPanel._openup
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj._openup(value) == "expected_result"
        assert capsys.readouterr().out == ("")


class TestPageGui:
    """unittest for gui_qt.PageGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.PageGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called PageGui.__init__ with args', args)
        testobj = testee.PageGui()
        assert capsys.readouterr().out == 'called PageGui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for PageGui.__init__
        """
        testobj = testee.PageGui(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_create_text_field(self, monkeypatch, capsys):
        """unittest for PageGui.create_text_field
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_text_field() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_create_toolbar(self, monkeypatch, capsys):
        """unittest for PageGui.create_toolbar
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_toolbar(textfield=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_doelayout(self, monkeypatch, capsys):
        """unittest for PageGui.doelayout
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.doelayout() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_reset_font(self, monkeypatch, capsys):
        """unittest for PageGui.reset_font
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.reset_font() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_buttons(self, monkeypatch, capsys):
        """unittest for PageGui.enable_buttons
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_buttons(state=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_move_cursor_to_end(self, monkeypatch, capsys):
        """unittest for PageGui.move_cursor_to_end
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.move_cursor_to_end() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_textarea_contents(self, monkeypatch, capsys):
        """unittest for PageGui.set_textarea_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_textarea_contents(data) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_textarea_contents(self, monkeypatch, capsys):
        """unittest for PageGui.get_textarea_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textarea_contents() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_toolbar(self, monkeypatch, capsys):
        """unittest for PageGui.enable_toolbar
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_toolbar(value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_text_readonly(self, monkeypatch, capsys):
        """unittest for PageGui.set_text_readonly
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_text_readonly(value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_can_saveandgo(self, monkeypatch, capsys):
        """unittest for PageGui.can_saveandgo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.can_saveandgo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_can_save(self, monkeypatch, capsys):
        """unittest for PageGui.can_save
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.can_save() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_build_newbuf(self, monkeypatch, capsys):
        """unittest for PageGui.build_newbuf
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_newbuf() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestPage0Gui:
    """unittest for gui_qt.Page0Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.Page0Gui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page0Gui.__init__ with args', args)
        testobj = testee.Page0Gui()
        assert capsys.readouterr().out == 'called Page0Gui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for Page0Gui.__init__
        """
        testobj = testee.Page0Gui(parent, master, widths)
        assert capsys.readouterr().out == ("")

    def _test_doelayout(self, monkeypatch, capsys):
        """unittest for Page0Gui.doelayout
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.doelayout() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_sorting(self, monkeypatch, capsys):
        """unittest for Page0Gui.enable_sorting
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_sorting(value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_buttons(self, monkeypatch, capsys):
        """unittest for Page0Gui.enable_buttons
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_buttons() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_change_selected(self, monkeypatch, capsys):
        """unittest for Page0Gui.on_change_selected
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_change_selected(item_n, item_o) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_activate_item(self, monkeypatch, capsys):
        """unittest for Page0Gui.on_activate_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_activate_item(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_list(self, monkeypatch, capsys):
        """unittest for Page0Gui.clear_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_list() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_listitem(self, monkeypatch, capsys):
        """unittest for Page0Gui.add_listitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_listitem(data) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_listitem_values(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_listitem_values
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_listitem_values(item, data) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_items(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_items
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_items() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_item_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_item_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item_text(item_or_index, column) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_item_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_item_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_item_text(item_or_index, column, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_first_item(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_first_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_first_item() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_item_by_index(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_item_by_index
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item_by_index(item_n) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_item_by_id(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_item_by_id
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item_by_id(item_id) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_has_selection(self, monkeypatch, capsys):
        """unittest for Page0Gui.has_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.has_selection() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_selection(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_selection() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_selection(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selection() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_ensure_visible(self, monkeypatch, capsys):
        """unittest for Page0Gui.ensure_visible
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ensure_visible(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_archive_button_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_archive_button_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_archive_button_text(txt) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_selected_action(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_selected_action
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_action() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_list_row(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_list_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_list_row() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_list_row(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_list_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_list_row(num) == "expected_result"
        assert capsys.readouterr().out == ("")


class TestPage1Gui:
    """unittest for gui_qt.Page1Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.Page1Gui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page1Gui.__init__ with args', args)
        testobj = testee.Page1Gui()
        assert capsys.readouterr().out == 'called Page1Gui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for Page1Gui.__init__
        """
        testobj = testee.Page1Gui(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_doelayout(self, monkeypatch, capsys):
        """unittest for Page1Gui.doelayout
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.doelayout() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_fields(self, monkeypatch, capsys):
        """unittest for Page1Gui.init_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_fields() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_text(fieldtype, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_text(fieldtype) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_choice(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_choice
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_choice(domain, field, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_choice_data(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_choice_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_choice_data(field) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_oldbuf(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_oldbuf
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_oldbuf() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_field_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_field_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_field_text(entry_type) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_archive_button_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_archive_button_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_archive_button_text(value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_fields(self, monkeypatch, capsys):
        """unittest for Page1Gui.enable_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_fields(state) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_stats(self, monkeypatch, capsys):
        """unittest for Page1Gui.clear_stats
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_stats() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_cats(self, monkeypatch, capsys):
        """unittest for Page1Gui.clear_cats
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_cats() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_cat_choice(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_cat_choice
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_cat_choice(text, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_stat_choice(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_stat_choice
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_stat_choice(text, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_focus(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_focus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_focus() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_build_newbuf(self, monkeypatch, capsys):
        """unittest for Page1Gui.build_newbuf
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_newbuf() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_fieldvalues(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_fieldvalues
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_fieldvalues() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestPage6Gui:
    """unittest for gui_qt.Page6Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.Page6Gui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page6Gui.__init__ with args', args)
        testobj = testee.Page6Gui()
        assert capsys.readouterr().out == 'called Page6Gui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for Page6Gui.__init__
        """
        testobj = testee.Page6Gui(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_doelayout(self, monkeypatch, capsys):
        """unittest for Page6Gui.doelayout
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.doelayout() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_activate_item(self, monkeypatch, capsys):
        """unittest for Page6Gui.on_activate_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_activate_item(item=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_new_item_to_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.add_new_item_to_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_new_item_to_list(datum, oldtext) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_is_first_line(self, monkeypatch, capsys):
        """unittest for Page6Gui.is_first_line
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.is_first_line(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_select_item(self, monkeypatch, capsys):
        """unittest for Page6Gui.on_select_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_select_item(item_n, item_o) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.init_textfield
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_textfield() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.init_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_list(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_item_to_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.add_item_to_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_item_to_list(idx, datum) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_list_callback(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_list_callback
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_list_callback() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.clear_textfield
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_textfield() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_protect_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.protect_textfield
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.protect_textfield(value=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_textfield_contents(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_textfield_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textfield_contents() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_textfield_contents(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_textfield_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_textfield_contents(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_listitem_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_listitem_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_listitem_text(itemindex, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_listitem_data(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_listitem_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_listitem_data(itemindex) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_list_row(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_list_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_list_row() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_list_row(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_list_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_list_row(num) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_list_rowcount(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_list_rowcount
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_list_rowcount() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_move_cursor_to_end(self, monkeypatch, capsys):
        """unittest for Page6Gui.move_cursor_to_end
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.move_cursor_to_end() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_focus_to_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_focus_to_textfield
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_focus_to_textfield() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_convert_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.convert_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.convert_text(text, to) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_listitem_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_listitem_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_listitem_text(itemindex) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_build_newbuf(self, monkeypatch, capsys):
        """unittest for Page6Gui.build_newbuf
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_newbuf() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestSortOptionsDialog:
    """unittest for gui_qt.SortOptionsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.SortOptionsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SortOptionsDialog.__init__ with args', args)
        testobj = testee.SortOptionsDialog()
        assert capsys.readouterr().out == 'called SortOptionsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for SortOptionsDialog.__init__
        """
        testobj = testee.SortOptionsDialog(parent, args)
        assert capsys.readouterr().out == ("")

    def _test_set_defaults(self, monkeypatch, capsys):
        """unittest for SortOptionsDialog.set_defaults
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_defaults() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_fields(self, monkeypatch, capsys):
        """unittest for SortOptionsDialog.enable_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_fields(state) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for SortOptionsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestSelectOptionsDialog:
    """unittest for gui_qt.SelectOptionsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.SelectOptionsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SelectOptionsDialog.__init__ with args', args)
        testobj = testee.SelectOptionsDialog()
        assert capsys.readouterr().out == 'called SelectOptionsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.__init__
        """
        testobj = testee.SelectOptionsDialog(parent, args)
        assert capsys.readouterr().out == ("")

    def _test_doelayout(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.doelayout
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.doelayout() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_default_values(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.set_default_values
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_default_values(sel_args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_text(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.on_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_text(arg, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_checked(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.on_checked
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_checked(arg) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestSettOptionsDialog:
    """unittest for gui_qt.SettOptionsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.SettOptionsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SettOptionsDialog.__init__ with args', args)
        testobj = testee.SettOptionsDialog()
        assert capsys.readouterr().out == 'called SettOptionsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.__init__
        """
        testobj = testee.SettOptionsDialog(parent, args)
        assert capsys.readouterr().out == ("")

    def _test_initstuff(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.initstuff
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.initstuff(parent) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.keyReleaseEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.keyReleaseEvent(evt) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_edit_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.edit_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.edit_item() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_end_edit(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.end_edit
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.end_edit(item_n, item_o) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.add_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_item() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.remove_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_item() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_move_item_up(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.move_item_up
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.move_item_up() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_move_item_down(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.move_item_down
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.move_item_down() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_move_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.move_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.move_item(up=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestLoginBox:
    """unittest for gui_qt.LoginBox
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.LoginBox object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called LoginBox.__init__ with args', args)
        testobj = testee.LoginBox()
        assert capsys.readouterr().out == 'called LoginBox.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for LoginBox.__init__
        """
        testobj = testee.LoginBox(parent)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for LoginBox.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestMainGui:
    """unittest for gui_qt.MainGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.MainGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called MainGui.__init__ with args', args)
        testobj = testee.MainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for MainGui.__init__
        """
        testobj = testee.MainGui(master)
        assert capsys.readouterr().out == ("")

    def _test_create_menu(self, monkeypatch, capsys):
        """unittest for MainGui.create_menu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_menu() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_create_actions(self, monkeypatch, capsys):
        """unittest for MainGui.create_actions
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_actions() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_bookwidget(self, monkeypatch, capsys):
        """unittest for MainGui.get_bookwidget
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_bookwidget() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_go(self, monkeypatch, capsys):
        """unittest for MainGui.go
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_refresh_page(self, monkeypatch, capsys):
        """unittest for MainGui.refresh_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.refresh_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_page_changing(self, monkeypatch, capsys):
        """unittest for MainGui.on_page_changing
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_page_changing(newtabnum) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_book_tabs(self, monkeypatch, capsys):
        """unittest for MainGui.enable_book_tabs
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_book_tabs(state, tabfrom=0, tabto=-1) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_all_other_tabs(self, monkeypatch, capsys):
        """unittest for MainGui.enable_all_other_tabs
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_all_other_tabs(state) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_book_tab(self, monkeypatch, capsys):
        """unittest for MainGui.add_book_tab
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_book_tab(tab, title) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_exit(self, monkeypatch, capsys):
        """unittest for MainGui.exit
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.exit() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_close(self, monkeypatch, capsys):
        """unittest for MainGui.close
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.close() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_page(self, monkeypatch, capsys):
        """unittest for MainGui.set_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_page(num) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_page_title(self, monkeypatch, capsys):
        """unittest for MainGui.set_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_page_title(num, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_page(self, monkeypatch, capsys):
        """unittest for MainGui.get_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_tabfocus(self, monkeypatch, capsys):
        """unittest for MainGui.set_tabfocus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_tabfocus(tabno) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_go_next(self, monkeypatch, capsys):
        """unittest for MainGui.go_next
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go_next() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_go_prev(self, monkeypatch, capsys):
        """unittest for MainGui.go_prev
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go_prev() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_go_to(self, monkeypatch, capsys):
        """unittest for MainGui.go_to
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go_to(page) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_print_(self, monkeypatch, capsys):
        """unittest for MainGui.print_
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.print_() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_preview(self, monkeypatch, capsys):
        """unittest for MainGui.preview
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.preview() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_afdrukken(self, monkeypatch, capsys):
        """unittest for MainGui.afdrukken
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.afdrukken(printer) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_settingsmenu(self, monkeypatch, capsys):
        """unittest for MainGui.enable_settingsmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_settingsmenu() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_statusmessage(self, monkeypatch, capsys):
        """unittest for MainGui.set_statusmessage
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_statusmessage(msg='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_window_title(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_window_title(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_show_username(self, monkeypatch, capsys):
        """unittest for MainGui.show_username
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_username(msg) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_tab_titles(self, monkeypatch, capsys):
        """unittest for MainGui.set_tab_titles
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_tab_titles(tabs) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_select_first_tab(self, monkeypatch, capsys):
        """unittest for MainGui.select_first_tab
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.select_first_tab() == "expected_result"
        assert capsys.readouterr().out == ("")
