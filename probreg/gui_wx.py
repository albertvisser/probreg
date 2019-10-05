"""Actie (was: problemen) Registratie, wxPython versie
"""
import os
import sys
import pathlib
# import collections
import functools
import wx
import wx.html as html
import wx.lib.mixins.listctrl as listmix
import wx.adv
import wx.richtext as wxrt
# import wx.gizmos as gizmos
from mako.template import Template
import probreg.shared as shared
LIN = True if os.name == 'posix' else False
HERE = os.path.abspath(os.path.dirname(__file__))
xmlfilter = "XML files (*.xml)|*.xml|all files (*.*)|*.*"


def show_message(win, message):
    "present a message and wait for the user to confirm (having read it or whatever)"
    wx.MessageBox(message, shared.app_title, parent=win)


def get_open_filename(win, start=pathlib.Path.cwd()):
    "get the name of a file to open"
    what = shared.app_title + " - kies een gegevensbestand"
    return wx.LoadFileSelector(what, xmlfilter, default_name=str(start), parent=win)


def get_save_filename(win, start=pathlib.Path.cwd()):
    "get the name of a file to save"
    what = shared.app_title + " - nieuw gegevensbestand"
    return wx.SaveFileSelector(what, xmlfilter, default_name=str(start), parent=win)


def get_choice_item(win, caption, choices, current=0):
    "allow the user to choose one of a set of options and return it"
    text = ''
    with wx.SingleChoiceDialog(win, shared.app_title, caption, choices, wx.CHOICEDLG_STYLE) as dlg:
        dlg.SetSelection(current)
        ok = dlg.ShowModal()
        if ok == wx.ID_OK:
            text = dlg.GetStringSelection()
    return text


def ask_cancel_question(win, message):
    "ask the user a question with an option to cancel the process"
    with wx.MessageDialog(win, message, shared.app_title,
                          wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION) as dlg:
        ok = dlg.ShowModal()
    return ok == wx.ID_YES, ok == wx.ID_CANCEL


def show_dialog(win, cls, args=None):
    "show a dialog and return if the dialog was confirmed / accepted"
    if args is None:
        dlg = cls(win)
    else:
        dlg = cls(win, args)
    with dlg:
        send = True
        while send:
            ok = dlg.ShowModal()
            send = False
            if ok == wx.ID_OK and not dlg.accept():
                send = True
    return ok == wx.ID_OK


def setup_accels(win, accel_data, accel_list=None):
    "define keyboard shortcuts for a gui class"
    if accel_list is None:
        accel_list = []
    for text, callback, keyseq in accel_data:
        menuitem = wx.MenuItem(None, -1, text)
        win.Bind(wx.EVT_MENU, callback, menuitem)
        accel = wx.AcceleratorEntry(cmd=menuitem.GetId())
        ok = accel.FromString(keyseq)
        if ok:
            accel_list.append(accel)
    accel_table = wx.AcceleratorTable(accel_list)
    win.SetAcceleratorTable(accel_table)


class EditorPanel(wxrt.RichTextCtrl):
    "Rich text editor displaying the selected note"


class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    "list control mixed in with width adapter"
    def __init__(self, parent, id_, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, id_, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class PageGui(wx.Panel):
    "base class for notebook page"
    # def __init__(self, parent, id_, wants_chars=True):
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        super().__init__(parent)
        if not self.master.is_text_page:
            return
        # if wants_chars:
        #     wx.Panel.__init__(self, parent, id_, style=wx.WANTS_CHARS)
        # else:
        #     wx.Panel.__init__(self, parent, id_)
        #     return
        # self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        self.Bind(wx.EVT_TEXT, self.on_text, self.text1)
        self.save_button = wx.Button(self, -1, 'Sla wijzigingen op (Ctrl-S)')
        self.Bind(wx.EVT_BUTTON, self.savep, self.save_button)
        self.saveandgo_button = wx.Button(self, -1, 'Sla op en ga verder (Ctrl-G)')
        self.Bind(wx.EVT_BUTTON, self.savepgo, self.saveandgo_button)
        self.cancel_button = wx.Button(self, -1, 'Zet originele tekst terug (Ctrl-Z)')
        self.Bind(wx.EVT_BUTTON, self.restorep, self.cancel_button)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)

    def create_toolbar(self):
        """build toolbar wih buttons for changing text style
        """

    def create_text_field(self):
        """build rich text area with style changing properties
        """
        high = 330 if LIN else 430
        self.text1 = wx.TextCtrl(self, -1, size=(490, high), style=wx.TE_MULTILINE |
                                                                   wx.TE_PROCESS_TAB |
                                                                   wx.TE_RICH2 |
                                                                   wx.TE_WORDWRAP)
        self.text1.Bind(wx.EVT_KEY_DOWN, self.on_key)

    def doelayout(self):
        "layout page"
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.text1, 1, wx.ALL | wx.EXPAND, 4)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(sizer1, 1, wx.EXPAND)
        sizer2.Add(self.save_button, 0, wx.ALL, 3)
        sizer2.Add(self.saveandgo_button, 0, wx.ALL, 3)
        sizer2.Add(self.cancel_button, 0, wx.ALL, 3)
        sizer0.Add(sizer2, 0, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer0)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)
        return True

    def enable_buttons(self, state=True):
        "buttons wel of niet klikbaar maken"
        # if state:
        #     self.parent.checked_for_leaving = False
        self.save_button.Enable(state)
        if self.parent.current_tab < 6:
            self.saveandgo_button.Enable(state)
        self.cancel_button.Enable(state)

    def move_cursor_to_end(self):
        "position the cursor at the end of the text"
        self.text1.moveCursor(gui.QTextCursor.End, gui.QTextCursor.MoveAnchor)

    def set_textarea_contents(self, data):
        "set the page text"
        self.text1.set_contents(data)

    def get_textarea_contents(self):
        "get the page text"
        return self.text1.get_contents()

    def enable_toolbar(self, value):
        "make the toolbar accessible (or not)"
        self.toolbar.setEnabled(value)

    def set_text_readonly(self, value):
        "protect page text from updating (or not)"
        self.text1.setReadOnly(value)

    def can_saveandgo(self):
        "check if we are allowed/able to do this"
        return self.saveandgo_button.IsEnabled()

    def can_save(self):
        "check if we are allowed/able to do this"
        return self.save_button.IsEnabled()

    def build_newbuf(self):
        """read widget contents into the compare buffer
        """
        return self.get_textarea_contents()


class Page0Gui(PageGui, listmix.ColumnSorterMixin):
    "pagina 0: overzicht acties"
    def __init__(self, parent, master, widths):
        self.parent = parent
        self.master = master
        super().__init__(parent, master)
        self.selection = 'excl. gearchiveerde'
        self.sel_args = {}
        # self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        self.imglist = wx.ImageList(16, 16)
        self.up_arrow = self.imglist.Add(wx.Bitmap(wx.Image(os.path.join(HERE, 'icons/up.png'),
                                                            wx.BITMAP_TYPE_PNG)))
        self.down_arrow = self.imglist.Add(wx.Bitmap(wx.Image(os.path.join(HERE, 'icons/down.png'),
                                                              wx.BITMAP_TYPE_PNG)))
        self.p0list = MyListCtrl(self, -1, style=wx.LC_REPORT | wx.BORDER_SUNKEN |  # wx.LC_HRULES |
                                                 wx.LC_SINGLE_SEL)
        ## high = 400 if LIN else 444
        ## self.p0list.SetMinSize((440, high))
        self.p0list.SetImageList(self.imglist, wx.IMAGE_LIST_SMALL)

        # self.populate_list()

        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        self.itemDataMap = self.parent.data
        if self.parent.parent.datatype == shared.DataType.XML.name:
            aantcols = 6
        elif self.parent.parent.datatype == shared.DataType.SQL.name:
            aantcols = 7
        listmix.ColumnSorterMixin.__init__(self, aantcols)
        for indx, wid in enumerate(widths):
            self.p0list.InsertColumn(indx, self.parent.ctitels[indx])
            self.p0list.SetColumnWidth(indx, wid)
        self.SortListItems(0)  # , True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select_item, self.p0list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_activate_item, self.p0list)
        # self.Bind(wx.EVT_LIST_COL_CLICK, self.on_column_clicked, self.p0list)
        self.p0list.Bind(wx.EVT_LEFT_DCLICK, self.on_doubleclick)
        # self.p0list.Bind(wx.EVT_KEY_DOWN, self.on_key)
        # self.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.sort_button = wx.Button(self, label='S&Orteer')
        self.filter_button = wx.Button(self, label='F&Ilter')
        self.go_button = wx.Button(self, label='&Ga naar melding')
        self.archive_button = wx.Button(self, label='&Archiveer')
        self.new_button = wx.Button(self, label='Voer &Nieuwe melding op')
        self.Bind(wx.EVT_BUTTON, self.master.sort_items, self.sort_button)
        self.Bind(wx.EVT_BUTTON, self.master.select_items, self.filter_button)
        self.Bind(wx.EVT_BUTTON, self.master.goto_actie, self.go_button)
        self.Bind(wx.EVT_BUTTON, self.master.archiveer, self.archive_button)
        self.Bind(wx.EVT_BUTTON, self.master.nieuwp, self.new_button)

    def doelayout(self):
        "layout page"
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.p0list, 1, wx.EXPAND, 0)
        sizer0.Add(sizer1, 1, wx.EXPAND, 0)
        sizer2.Add(self.sort_button, 0, wx.ALL, 3)
        sizer2.Add(self.filter_button, 0, wx.ALL, 3)
        sizer2.Add(self.go_button, 0, wx.ALL, 3)
        sizer2.Add(self.archive_button, 0, wx.ALL, 3)
        sizer2.Add(self.new_button, 0, wx.ALL, 3)
        sizer0.Add(sizer2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer0)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)

    def enable_sorting(self, value):
        "stel in of sorteren mogelijk is"

    def enable_buttons(self):
        "buttons wel of niet bruikbaar maken"
        self.filter_button.Enable(bool(self.parent.parent.user))
        self.go_button.Enable(self.p0list.has_selection)
        self.new_button.Enable(self.parent.parent.is_user)
        if self.p0list.has_selection:
            self.sort_button.Enable(bool(self.parent.parent.user))
            self.archive_button.Enable(self.parent.parent.is_user)
        else:
            self.sort_button.Enable(False)
            self.archive_button.Enable(False)

    def GetListCtrl(self):
        "methode tbv correcte werking sorteer mixin"
        return self.p0list

    def GetSortImages(self):
        "methode tbv correcte werking sorteer mixin"
        return (self.down_arrow, self.up_arrow)

    def on_select_item(self, event):
        "callback voor selectie van item"
        print('in on_select_item')
        # self.parent.current_item = event.Index
        # seli = self.p0list.GetItemData(self.parent.current_item)
        # self.readp(self.parent.data[seli][0])
        # hlp = "&Herleef" if self.parent.pagedata.arch else "&Archiveer"
        # self.archive_button.SetLabel(hlp)
        self.master.change_selected(event.Index)
        # event.Skip()

    def on_activate_item(self, event):
        "callback voor activeren van item"
        print('in on_activate_item')
        # self.parent.current_item = event.Index
        self.master.activate_item()

    def on_doubleclick(self, event):
        "callback voor dubbelklikken op item"
        self.master.goto_actie()
        # event.Skip()

    def clear_list(self):
        "initialize the list"
        self.p0list.DeleteAllItems()
        self.p0list.has_selection = False

    def add_listitem(self, data):
        "add an item to the list"
        itemindex = self.p0list.InsertItem(self.p0list.GetItemCount(), data)
        self.p0list.SetItemData(itemindex, int(''.join(data.split('-'))))
        return itemindex

    def set_listitem_values(self, itemindex, data):
        "set column values for list entry"
        for col, value in enumerate(data):
            if col == 1:
                pos = value.index(".") + 1
                value = value[pos:pos + 1].upper()
            elif col == 2:
                pos = value.index(".") + 1
                value = value[pos:]
            self.p0list.SetItem(itemindex, col, value)
        self.p0list.has_selection = True

    def get_items(self):
        "retrieve all listitems"
        return [self.p0list.GetItem(i) for i in range(self.p0list.GetItemCount())]

    def get_item_text(self, item_or_index, column):
        "get the item's text for a specified column"
        print('in get_item_text; item_or_index is', item_or_index)
        try:
            test = int(item_or_index)
        except TypeError:
            item_or_index = item_or_index.GetId()
        return self.p0list.GetItemText(item_or_index, column)

    def set_item_text(self, item_or_index, column, text):
        "set the item's text for a specified column"
        self.p0list.SetItem(item_or_index, column, text)

    def get_first_item(self):
        "select the first item in the list"
        return 0  # self.p0list.GetItem(0)

    def has_selection(self):
        "return if list contains selection of data"
        return self.p0list.has_selection

    def set_selection(self):
        "set selected item if any"
        print('in set selection; current_item is', self.parent.current_item)
        if self.parent.current_item != -1:   # of komt hier kennelijk toch een item binnen?
            self.p0list.Select(self.parent.current_item)

    def get_selection(self):
        "get selected item"
        return self.p0list.GetFirstSelected()

    def ensure_visible(self, item):
        "make sure listitem is visible"
        if item:    # hier komt kennelijk toch een item binnen?
            self.p0list.EnsureVisible(item)

    def build_newbuf(self):
        """read widget contents into the compare buffer
        """
        return None

    def set_archive_button_text(self, txt):
        "set button text according to archive status"
        self.archive_button.SetLabel(txt)

    def get_selected_action(self):
        "return the key of the selected action"
        data = str(self.p0list.GetItemData(self.p0list.GetFirstSelected()))
        return '-'.join((data[:4], data[4:]))


class Page1Gui(PageGui):
    "pagina 1: startscherm actie"
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        super().__init__(parent, master)
        # self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        self.id_text = wx.TextCtrl(self, size=(120, -1))
        self.date_text = wx.TextCtrl(self, size=(150, -1))

        self.proc_entry = wx.TextCtrl(self, size=(150, -1))
        self.Bind(wx.EVT_TEXT, self.master.on_text, self.proc_entry)
        self.desc_entry = wx.TextCtrl(self, size=(360, -1))
        self.Bind(wx.EVT_TEXT, self.master.on_text, self.desc_entry)

        self.cat_choice = wx.ComboBox(self, size=(180, -1), style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.Bind(wx.EVT_TEXT, self.master.on_text, self.cat_choice)
        self.stat_choice = wx.ComboBox(self, size=(140, -1), style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.Bind(wx.EVT_TEXT, self.master.on_text, self.stat_choice)

        self.archive_text = wx.StaticText(self, label="")
        self.archive_button = wx.Button(self, label="Archiveren")
        self.Bind(wx.EVT_BUTTON, self.master.archiveer, self.archive_button)

        self.save_button = wx.Button(self, label='Sla wijzigingen op (Ctrl-S)')
        self.Bind(wx.EVT_BUTTON, self.master.savep, self.save_button)
        self.saveandgo_button = wx.Button(self, label='Sla op en ga verder (Ctrl-G)')
        self.Bind(wx.EVT_BUTTON, self.master.savepgo, self.saveandgo_button)
        self.cancel_button = wx.Button(self, label='Maak wijzigingen ongedaan (Alt-Ctrl-Z)')
        self.Bind(wx.EVT_BUTTON, self.master.restorep, self.cancel_button)

        accel_data = (('savep', self.master.savep, 'Ctrl+S'),
                      ('savepgo', self.master.savepgo, 'Ctrl+G'),
                      ('restorep', self.master.restorep, 'Alt+Ctrl+Z'),
                      ('nieuwp', self.master.nieuwp, 'Alt+N'))
        setup_accels(self, accel_data)

    def doelayout(self):
        "layout page"
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.GridBagSizer(3, 12)  # rows, cols, hgap, vgap
        sizer1.Add(wx.StaticText(self, label="Actie-id:"), (0, 0),
                   flag=wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_TOP, border=10)
        sizer1.Add(self.id_text, (0, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self, label="Datum/tijd:"), (1, 0),
                   flag=wx.ALL | wx.ALIGN_TOP, border=10)
        sizer1.Add(self.date_text, (1, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self, label="Job/\ntransactie:"), (2, 0),
                   flag=wx.ALL | wx.ALIGN_TOP, border=10)
        sizer1.Add(self.proc_entry, (2, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self, label="Melding/code/\nomschrijving:"), (3, 0),
                   flag=wx.ALL | wx.ALIGN_TOP, border=10)
        sizer1.Add(self.desc_entry, (3, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self, label="Categorie:"), (4, 0),
                   flag=wx.ALL | wx.ALIGN_TOP, border=10)
        sizer1.Add(self.cat_choice, (4, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self, label="Status:"), (5, 0),
                   flag=wx.ALL | wx.ALIGN_TOP, border=10)
        sizer1.Add(self.stat_choice, (5, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(self.archive_text, (6, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM,
                   border=10)
        sizer1.Add(self.archive_button, (7, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.TOP,
                   border=5)
        sizer1.Add((-1, 186), (9, 0))
        sizer1.AddGrowableRow(8)
        sizer1.AddGrowableCol(1)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(sizer1, 1, wx.EXPAND | wx.ALL, 8)
        sizer2.Add(self.save_button, 0, wx.ALL, 3)
        sizer2.Add(self.saveandgo_button, 0, wx.ALL, 3)
        sizer2.Add(self.cancel_button, 0, wx.ALL, 3)
        sizer0.Add(sizer2, 0, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer0)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)

    def init_fields(self):
        "initialize the fields on this screen"
        self.id_text.SetValue("")
        self.date_text.SetValue("")
        self.proc_entry.SetValue("")
        self.desc_entry.SetValue("")
        self.archive_text.SetLabel("")
        self.cat_choice.SetSelection(0)
        self.stat_choice.SetSelection(0)

    def set_text(self, fieldtype, value):
        "set textfield value"
        if fieldtype == 'id':
            self.id_text.SetValue(value)
        elif fieldtype == 'date':
            self.date_text.SetValue(value)
        elif fieldtype == 'proc':
            self.proc_entry.SetValue(value)
        elif fieldtype == 'desc':
            self.desc_entry.SetValue(value)
        elif fieldtype == 'arch':
            self.archive_text.SetLabel(value)

    def get_text(self, fieldtype):
        "get textfield value"
        if fieldtype == 'id':
            value = str(self.id_text.GetValue())
        elif fieldtype == 'date':
            value = str(self.date_text.GetValue())
        elif fieldtype == 'proc':
            value = str(self.proc_entry.GetValue())
        elif fieldtype == 'desc':
            value = str(self.desc_entry.GetValue())
        return value

    def set_choice(self, fieldtype, value):
        "set selected entry in a combobox"
        if fieldtype == 'stat':
            domain = self.parent.stats
            field = self.stat_choice
        elif fieldtype == 'cat':
            domain = self.parent.cats
            field = self.cat_choice
        for x in range(len(domain)):
            y = shared.data2str(field.GetClientData(x))
            if y == value:
                field.Select(x)
                break

    def get_choice_data(self, fieldtype):
        "get selected entry in a combobox"
        if fieldtype == 'stat':
            idx = self.stat_choice.GetSelection()
            code = shared.data2str(self.stat_choice.GetClientData(idx))
            text = self.stat_choice.GetStringSelection()
        elif fieldtype == 'cat':
            idx = self.cat_choice.GetSelection()
            code = shared.data2str(self.cat_choice.GetClientData(idx))
            text = str(self.cat_choice.GetStringSelection())
        return code, text

    def set_oldbuf(self):
        "get fieldvalues for comparison of entry was changed"
        self.oldbuf = (self.proc_entry.GetValue(), self.desc_entry.GetValue(),
                       self.stat_choice.GetSelection(), self.cat_choice.GetSelection())

    def get_field_text(self, entry_type):
        "return a screen field's value"
        test = ('actie', 'datum', 'oms', 'tekst', 'status', 'soort').index(entry_type)
        dest = ('id', 'date', 'proc', 'desc', 'stat', 'cat')[test]
        if test > 3:
            return self.get_choice_data(dest)[1]
        return self.get_text(dest)

    def set_archive_button_text(self, value):
        "set the text for the archive button"
        self.archive_button.SetLabel(value)

    def enable_fields(self, state):
        "make fields accessible, depending on user permissions"
        self.id_text.Enable(False)
        self.date_text.Enable(False)
        self.proc_entry.Enable(state)
        self.desc_entry.Enable(state)
        self.cat_choice.Enable(state)
        self.stat_choice.Enable(state)
        if self.parent.newitem or not self.master.parent.parent.is_user:
            self.archive_button.Enable(False)
        else:
            self.archive_button.Enable(True)

    def clear_stats(self):
        "initialize status choices"
        self.stat_choice.Clear()

    def clear_cats(self):
        "initialize category choices"
        self.cat_choice.Clear()

    def add_cat_choice(self, text, value):
        "add category choice"
        self.cat_choice.Append(text, value)

    def add_stat_choice(self, text, value):
        "add status choice"
        self.stat_choice.Append(text, value)

    def set_focus(self):
        "set the focus for this page to the proc field"
        self.proc_entry.SetFocus()

    def build_newbuf(self):
        """read widget contents into the compare buffer
        """
        return (str(self.proc_entry.GetValue()), str(self.desc_entry.GetValue()),
                int(self.stat_choice.GetSelection()), int(self.cat_choice.GetSelection()))


class Page6Gui(PageGui):
    "pagina 6: voortgang"
    def __init__(self, parent, id_):
        super().__init__(parent, id_, False)
        self.current_item = 0
        self.oldtext = ""
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        high = 200 if LIN else 280
        self.pnl = wx.SplitterWindow(self, -1, size=(500, 400), style=wx.SP_LIVE_UPDATE)

        self.progress_list = MyListCtrl(self.pnl, -1, size=(500, -1),  # high),
                                        style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES |
                                              wx.LC_SINGLE_SEL)
        self.progress_list.InsertColumn(0, 'Momenten')
        high = 100 if LIN else 110
        self.progress_text = wx.TextCtrl(self.pnl, -1, size=(500, -1),  # high),
                                         style=wx.TE_MULTILINE |        # wx.TE_PROCESS_TAB |
                                               wx.TE_RICH2 | wx.TE_WORDWRAP)
        self.progress_list.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.progress_list.Bind(wx.EVT_LEFT_UP, self.on_left_release)
        self.progress_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select_item)
        self.progress_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_deselect_item)
        self.progress_text.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.progress_text.Bind(wx.EVT_TEXT, self.on_text)
        self.pnl.SplitHorizontally(self.progress_list, self.progress_text)
        self.pnl.SetSashPosition(250)

        self.save_button = wx.Button(self, -1, 'Sla wijzigingen op (Ctrl-S)')
        self.Bind(wx.EVT_BUTTON, self.savep, self.save_button)
        self.saveandgo_button = wx.Button(self, -1, 'Sla op en ga verder (Ctrl-G)')
        self.Bind(wx.EVT_BUTTON, self.savepgo, self.saveandgo_button)
        self.cancel_button = wx.Button(self, -1, 'Maak wijzigingen ongedaan (Ctrl-Z)')
        self.Bind(wx.EVT_BUTTON, self.restorep, self.cancel_button)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)

    def doelayout(self):
        "layout page"
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.pnl, 1, wx.EXPAND | wx.ALL, 4)
        ## sizer1.Add(self.progress_list, 1, wx.EXPAND | wx.ALL, 4)
        ## sizer1.Add(self.progress_text, 1, wx.EXPAND | wx.ALL, 4)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(sizer1, 1, wx.EXPAND | wx.ALL, 8)
        sizer2.Add(self.save_button, 0, wx.ALL, 3)
        sizer2.Add(self.saveandgo_button, 0, wx.ALL, 3)
        sizer2.Add(self.cancel_button, 0, wx.ALL, 3)
        sizer0.Add(sizer2, 0, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer0)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)

    def vulp(self, evt=None):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        super().vulp()
        self.initializing = True
        self.event_list, self.event_data, self.old_list, self.old_data = [], [], [], []
        self.progress_text.Clear()
        self.progress_text.Enable(False)  # SetEditable(False)
        if self.parent.pagedata:  # and not self.parent.newitem:
            self.event_list = [x[0] for x in self.parent.pagedata.events]
            self.event_list.reverse()
            self.old_list = self.event_list[:]
            self.event_data = [x[1] for x in self.parent.pagedata.events]
            self.event_data.reverse()
            self.old_data = self.event_data[:]
            self.progress_list.DeleteAllItems()
            y = '-- (double)click to add new item --'
            index = self.progress_list.InsertItem(sys.maxsize, y)
            self.progress_list.SetItem(index, 0, y)
            self.progress_list.SetItemData(index, -1)
            for idx, datum in enumerate(self.event_list):
                index = self.progress_list.InsertItem(sys.maxsize, datum)
                try:
                    text = self.event_data[idx].split("\n")[0].strip()
                except AttributeError:
                    text = self.event_data[idx] or ""
                text = text if len(text) < 80 else text[:80] + "..."
                if self.parent.parent.datatype == shared.DataType.SQL.name:
                    datum = datum[:19]
                self.progress_list.SetItem(index, 0, "{} - {}".format(datum, text))
                        # datum, text.encode('latin-1')))
                self.progress_list.SetItemData(index, idx)
        self.oldbuf = (self.old_list, self.old_data)
        self.oldtext = ''
        self.initializing = False

    def savep(self, evt=None):
        "opslaan van de paginagegevens"
        super().savep()
        # voor het geval er na het aanpassen van een tekst direkt "sla op" gekozen is
        # nog even kijken of de tekst al in self.event_data is aangepast.
        idx = self.current_item
        hlp = self.progress_text.GetValue()
        if idx > 0:
            idx -= 1
        if self.event_data[idx] != hlp:
            self.event_data[idx] = hlp
            self.oldtext = hlp
            short_text = hlp.split("\n")[0]
            short_text = short_text if len(short_text) < 80 else short_text[:80] + "..."
            if self.parent.parent.datatype == shared.DataType.XML.name:
                short_text = short_text.encode('latin-1')
            self.progress_list.SetStringItem(idx + 1, 0, "{} - {}".format(
                self.event_list[idx], short_text))
            self.progress_list.SetItemData(idx + 1, idx)
        wijzig = False
        if self.event_list != self.old_list or self.event_data != self.old_data:
            wijzig = True
            hlp = len(self.event_list) - 1
            for idx, data in enumerate(self.parent.pagedata.events):
                if data != (self.event_list[hlp - idx], self.event_data[hlp - idx]):
                    self.parent.pagedata.events[idx] = (self.event_list[hlp - idx],
                                                        self.event_data[hlp - idx])
            for idx in range(len(self.parent.pagedata.events), hlp + 1):
                if self.event_data[hlp - idx]:
                    self.parent.pagedata.events.append((self.event_list[hlp - idx],
                                                        self.event_data[hlp - idx]))
        if wijzig:
            self.update_actie()
            ## try:
            self.parent.page0.p0list.SetItem(self.parent.current_item, 4,
                                             self.parent.pagedata.updated)  # bijwerken in panel 0
            ## except wx._core.PyAssertionError:
                ## pass
            self.old_list = self.event_list[:]
            self.old_data = self.event_data[:]
            self.oldbuf = (self.old_list, self.old_data)
        else:
            print("Leuk hoor, er was niks gewijzigd ! @#%&*Grrr")
        return True

    def on_left_release(self, event):
        """releasing the lmb (on an item)
        """
        x = event.GetX()
        y = event.GetY()
        item, flags = self.progress_list.HitTest((x, y))
        tekst = self.progress_list.GetItemText(item)  # niet gebruikt
        print("on left release:", item, tekst)
        if item == 0:
            hlp = shared.get_dts()
            self.progress_list.InsertStringItem(1, hlp)
            self.event_list.insert(0, hlp)
            self.event_data.insert(0, "")
            self.progress_list.Select(1)
            self.oldtext = ""
            self.progress_text.SetValue(self.oldtext)
            self.progress_text.Enable(True)
            self.progress_text.SetFocus()

    def on_select_item(self, event):
        """callback voor het selecteren van een item

        selecteren van (klikken op) een regel in de listbox doet de inhoud van de textctrl
        ook veranderen. eerst controleren of de tekst veranderd is
        dat vragen moet ook in de situatie dat je op een geactiveerde knop klikt,
        het panel wilt verlaten of afsluiten
        de knoppen onderaan doen de hele lijst bijwerken in self.parent.book.p"""
        self.current_item = event.Index  # - 1
        tekst = self.progress_list.GetItemText(self.current_item)  # niet gebruikt
        self.progress_text.SetEditable(False)
        if not self.parent.pagedata.arch:
            self.progress_text.SetEditable(True)
        if self.current_item == 0:
            self.oldtext = ""
        else:
            self.oldtext = self.event_data[self.current_item - 1]
        self.progress_text.SetValue(self.oldtext)
        self.progress_text.Enable(True)
        ## self.progress_text.SetFocus()
        ## event.Skip()

    def on_deselect_item(self, evt):
        "callback voor het niet meer geselecteerd zijn van een item"
        item = evt.GetItem()  # niet gebruikt
        idx = evt.Index
        tekst = self.progress_text.GetValue()  # self.progress_list.GetItemText(idx)
        if tekst != self.oldtext:
            self.event_data[idx - 1] = tekst
            self.oldtext = tekst
            short_text = tekst.split("\n")[0]
            short_text = short_text if len(short_text) < 80 else short_text[:80] + "..."
            self.progress_list.SetItem(idx, 0, "{} - {}".format(self.event_list[idx - 1],
                                                                short_text))
            self.progress_list.SetItemData(idx, idx - 1)
        evt.Skip()

    def on_text(self, evt):
        """callback voor EVT_TEXT

        de initializing flag wordt uitgevraagd omdat deze event ook tijdens vulp()
        plaatsvindt"""
        if not self.initializing:
            ## idx = self.current_item # self.progress_list.Selection # niet gebruikt
            tekst = self.progress_text.GetValue()  # self.progress_list.GetItemText(ix)
            if tekst != self.oldtext:
                self.enable_buttons()
                if self.current_item > 0:
                    self.event_data[self.current_item - 1] = tekst
            evt.Skip()


class EasyPrinter(html.HtmlEasyPrinting):
    "class om printen via html layout mogelijk te maken"
    def __init__(self):
        html.HtmlEasyPrinting.__init__(self)

    def print_(self, text, doc_name):
        "het daadwerkelijke printen"
        self.SetHeader(doc_name)
        self.PreviewText(text)


class SortOptionsDialog(wx.Dialog):
    "dialoog om de sorteer opties in te stellen"
    def __init__(self, parent, args):
        self.parent = parent
        wx.Dialog.__init__(self, parent, -1, title="Sorteren op meer dan 1 kolom",
                           pos=wx.DefaultPosition,
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.sortopts, lijst = args
        sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.GridBagSizer(2, 2)
        row = 0
        tekst = 'Multi-sorteren mogelijk maken'
        self.on_off = wx.CheckBox(self, label=tekst)
        self.on_off.Bind(wx.EVT_CHECKBOX, self.enable_fields)
        grid.Add(self.on_off, (row, 0), (1, 4))
        self._widgets = []
        row += 1
        while row < len(lijst):
            lbl = wx.StaticText(self, label=" {}.".format(row))
            grid.Add(lbl, (row, 0), flag=wx.ALIGN_CENTER_VERTICAL)
            cmb = wx.ComboBox(self, size=(90, -1), choices=lijst, style=wx.CB_DROPDOWN)
            cmb.SetSelection(0)
            grid.Add(cmb, (row, 1))
            rba = wx.RadioButton(self, label=" Asc ", style=wx.RB_GROUP)
            grid.Add(rba, (row, 2), flag=wx.ALIGN_CENTER_VERTICAL)
            rbd = wx.RadioButton(self, label=" Desc ")
            grid.Add(rbd, (row, 3), flag=wx.ALIGN_CENTER_VERTICAL)
            self._widgets.append((lbl, cmb, rba, rbd))
            row += 1

        grid.AddGrowableCol(1)
        sizer.Add(grid, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.set_defaults()

    def set_defaults(self):
        """set start values for dialog
        """
        self.enable_fields(False)
        self.on_off.SetValue(self.parent.master.sort_via_options)
        for ix, line in enumerate(self._widgets):
            _, combobox, rbasc, rbdesc = line
            if ix in sorted(self.sortopts):
                fieldname, orient = self.sortopts[ix]
                combobox.SetValue(fieldname)
                if orient == 'desc':
                    rbdesc.SetValue(True)
                else:
                    rbasc.SetValue(True)

    def enable_fields(self, event):
        "enable/disable widgets"
        state = self.on_off.GetValue()
        for lbl, cmb, rba, rbd in self._widgets:
            lbl.Enable(state)
            cmb.Enable(state)
            rba.Enable(state)
            rbd.Enable(state)

    def accept(self):
        """sorteerkolommen en -volgordes teruggeven aan hoofdscherm
        """
        if self.parent.parent.parent.datatype == shared.DataType.XML.name:
            show_message(self.parent, 'Sorry, werkt nog niet')
            return False
        new_sortopts = {}
        for ix, line in enumerate(self._widgets):
            _, combobox, rbgroup = line
            fieldname = combobox.currentText()
            checked_id = rbgroup.checkedId()
            if fieldname and fieldname != '(geen)':
                if checked_id == self._asc_id:
                    orient = 'asc'
                elif checked_id == self._desc_id:
                    orient = 'desc'
                new_sortopts[ix] = (fieldname, orient)
        via_options = self.on_off.isChecked()
        if via_options == self.parent.master.sort_via_options and new_sortopts == self.sortopts:
            show_message(self, 'U heeft niets gewijzigd')
            return False
        self.parent.master.sort_via_options = via_options
        if via_options:
            if self.parent.saved_sortopts:      # alleen SQL versie
                self.parent.saved_sortopts.save_options(new_sortopts)
        return True


class SelectOptionsDialog(wx.Dialog):
    """dialoog om de selectie op te geven

    sel_args is de dictionary waarin de filterwaarden zitten, bv:
    {'status': ['probleem'], 'idlt': '2006-0009', 'titel': 'x', 'soort': ['gemeld'],
    'id': 'and', 'idgt': '2005-0019'}"""
    def __init__(self, parent, args):
        self.parent = parent
        self.datatype = self.parent.parent.parent.datatype
        sel_args, self._data = args
        wx.Dialog.__init__(self, parent, -1, title="Selecteren",
                           ## size=(250,  250),  pos=wx.DefaultPosition,
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.cb_actie = wx.CheckBox(self, label=parent.parent.ctitels[0].join((" ", " -")))
        self.text_gt = wx.TextCtrl(self, value="", size=(153, -1))
        self.Bind(wx.EVT_TEXT, self.on_text, self.text_gt)
        self.rb_and = wx.RadioButton(self, label="en", style=wx.RB_GROUP)
        self.rb_or = wx.RadioButton(self, label="of")
        self.text_lt = wx.TextCtrl(self, value="", size=(153, -1))
        self.Bind(wx.EVT_TEXT, self.on_text, self.text_lt)

        self.cb_soort = wx.CheckBox(self, label=" soort -")
        self.clb_soort = wx.CheckListBox(self, size=(-1, 120),
            choices=[x[0] for x in [self.parent.parent.cats[y]
                                    for y in sorted(self.parent.parent.cats.keys())]])
        self.Bind(wx.EVT_CHECKLISTBOX, self.on_checked, self.clb_soort)

        self.cb_stat = wx.CheckBox(self, label=parent.parent.ctitels[2].join((" ", " -")))
        self.clb_stat = wx.CheckListBox(self, size=(-1, 120),
            choices=[x[0] for x in [self.parent.parent.stats[y]
                                    for y in sorted(self.parent.parent.stats.keys())]])
        self.Bind(wx.EVT_CHECKLISTBOX, self.on_checked, self.clb_stat)

        self.cb_text = wx.CheckBox(self, label=parent.parent.ctitels[4].join((" ", " -")))
        self.t_text = wx.TextCtrl(self, value="", size=(153, -1))
        self.Bind(wx.EVT_TEXT, self.on_text, self.t_text)

        self.cb_arch = wx.CheckBox(self, label="Archief")
        self.rb_aonly = wx.RadioButton(self, label="Alleen gearchiveerd", style=wx.RB_GROUP)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_rightclick, self.rb_aonly)
        self.rb_aboth = wx.RadioButton(self, label="gearchiveerd en lopend")
        self.Bind(wx.EVT_RADIOBUTTON, self.on_rightclick, self.rb_aboth)

        self.set_default_values(sel_args)
        self.doelayout()

    def doelayout(self):
        """realize the dialog layout
        """
        sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.FlexGridSizer(5, 2, 2, 2)  # rows, cols, hgap, vgap
        box_actie = wx.FlexGridSizer(3, 2, 2, 2)
        lbl_gt = wx.StaticText(self, label="groter dan:", size=(90, -1))  # was 70
        lbl_lt = wx.StaticText(self, label="kleiner dan:", size=(90, -1))  # was 70
        spacer = wx.StaticText(self, label="", size=(70, -1))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.rb_and, 0, wx.ALIGN_CENTER_HORIZONTAL)
        hbox.Add(self.rb_or, 0, wx.ALIGN_CENTER_HORIZONTAL)
        box_actie.AddMany([(lbl_gt, 0, wx.TOP, 10), (self.text_gt, 0, wx.TOP, 5),
                           (hbox, 0), (spacer, 0),
                           (lbl_lt, 0, wx.TOP | wx.BOTTOM, 5), (self.text_lt, 0, wx.BOTTOM, 5)])
        box_soort = wx.BoxSizer(wx.HORIZONTAL)
        box_soort.Add(wx.StaticText(self, label="selecteer\neen of meer:", size=(70, -1)), 0,
                      wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 5)
        box_soort.Add(self.clb_soort, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 5)
        box_stat = wx.BoxSizer(wx.HORIZONTAL)
        box_stat.Add(wx.StaticText(self, label="selecteer\neen of meer:", size=(70, -1)), 0,
                     wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 5)
        box_stat.Add(self.clb_stat, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 5)
        box_text = wx.BoxSizer(wx.HORIZONTAL)
        box_text.Add(wx.StaticText(self, label="zoek naar:", size=(70, -1)), 0,
                     wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 10)
        box_text.Add(self.t_text, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 5)
        box_arch = wx.BoxSizer(wx.HORIZONTAL)
        box_arch.Add(self.rb_aboth, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)
        box_arch.Add(self.rb_aonly, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)
        grid.AddMany([(self.cb_actie, 0, wx.TOP, 10), (box_actie, 0, wx.EXPAND | wx.TOP, 3),
                      (self.cb_soort, 0, wx.TOP, 5), (box_soort, 0, wx.EXPAND | wx.TOP, 3),
                      (self.cb_stat, 0, wx.TOP, 5), (box_stat, 0, wx.EXPAND | wx.TOP, 3),
                      (self.cb_text, 0, wx.TOP, 10), (box_text, 0, wx.EXPAND | wx.TOP, 3),
                      (self.cb_arch, 0, wx.TOP, 10), (box_arch, 0, wx.EXPAND)])
        grid.AddGrowableCol(1)
        sizer.Add(grid, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)

    def set_default_values(self, sel_args):
        """get search settings and present them in the dialog
        """
        if self.parent.parent.parent.datatype == shared.DataType.XML.name:
            self.getpos = 1
        elif self.parent.parent.parent.datatype == shared.DataType.SQL.name:
            self.getpos = 2
        if "idgt" in sel_args:
            self.text_gt.SetValue(sel_args["idgt"])
        if "id" in sel_args:
            if sel_args["id"] == "and":
                self.rb_and.SetValue(True)
            else:
                self.rb_or.SetValue(True)
        if "idlt" in sel_args:
            self.text_lt.SetValue(sel_args["idlt"])
        if "soort" in sel_args:
            for x in self.parent.parent.cats.keys():
                if self.parent.parent.cats[x][self.getpos] in sel_args["soort"]:
                    self.clb_soort.Check(int(x))
            self.cb_soort.SetValue(True)
        if "status" in sel_args:
            for x in self.parent.parent.stats.keys():
                if self.parent.parent.stats[x][self.getpos] in sel_args["status"]:
                    self.clb_stat.Check(int(x))
            self.cb_stat.SetValue(True)
        if "titel" in sel_args:
            self.t_text.SetValue(sel_args["titel"])
            self.cb_text.SetValue(True)
        if "arch" in sel_args:
            self.cb_arch.SetValue(True)
            if sel_args["arch"] == "arch":
                self.rb_aonly.SetValue(True)
            if sel_args["arch"] == "alles":
                self.rb_aboth.SetValue(True)

    def on_text(self, evt=None):
        "callback voor EVT_TEXT"
        obj = evt.GetEventObject()
        if obj in (self.text_gt, self.text_lt):
            target = self.cb_actie
        elif obj == self.t_text:
            target = self.cb_text
        if evt.GetString() == "":
            target.SetValue(False)
        else:
            target.SetValue(True)

    def on_checked(self, evt=None):
        "callback voor EVT_CHECK"
        index = evt.GetSelection()
        obj = evt.GetEventObject()
        obj.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
        if obj == self.clb.soort:
            target = self.cb_soort
        elif obj == self.clb_stat:
            target = self.cb_stat
        oneormore = False
        for i in range(obj.GetCount()):
            if obj.IsChecked(i):
                oneormore = True
                break
        if oneormore:
            target.SetValue(True)
        else:
            target.SetValue(False)

    def on_rightclick(self, evt=None):
        "callback voor EVT_RADIO"
        obj = evt.GetEventObject()
        if obj in (self.rb_aonly, self.rb_aboth):
            self.cb_arch.SetValue(True)

    def accept(self):  # set_options(self, evt=None):
        "aangegeven opties verwerken in sel_args dictionary"
        selection = 'excl.gearchiveerde'
        sel_args = {}
        if self.cb_actie.IsChecked():  # checkbox voor "id"
            selection = '(gefilterd)'
            id_gt, id_lt = self.text_gt.GetValue(), self.text_lt.GetValue()
            if id_gt:
                sel_args["idgt"] = id_gt
            if id_lt:
                sel_args["idlt"] = id_lt
            if self.rb_and.GetValue():
                sel_args["id"] = "and"
            if self.rb_or.GetValue():
                sel_args["id"] = "or"
        if self.cb_soort.IsChecked():  # checkbox voor "soort"
            selection = '(gefilterd)'
            lst = [self.parent.parent.cats[x][self.getpos] for x in range(
                   len(self.parent.parent.cats.keys())) if self.clb_soort.IsChecked(x)]
            if lst:
                sel_args["soort"] = lst
        if self.cb_stat.IsChecked():  # checkbox voor "status"
            selection = '(gefilterd)'
            lst = [self.parent.parent.stats[x][self.getpos] for x in range(
                   len(self.parent.parent.stats.keys())) if self.clb_stat.IsChecked(x)]
            if lst:
                sel_args["status"] = lst
        if self.cb_text.IsChecked():  # checkbox voor "titel bevat"
            selection = '(gefilterd)'
            txt = self.t_text.GetValue()
            sel_args["titel"] = txt
        if self.cb_arch.IsChecked():  # checkbox voor "archiefstatus"
            if self.rb_aonly.GetValue():
                sel_args["arch"] = "arch"
                if selection != '(gefilterd)':
                    selection = '(gearchiveerd)'
            if self.rb_aboth.GetValue():
                sel_args["arch"] = "alles"
                if selection != '(gefilterd)':
                    selection = ''
        self.parent.master.selection = selection
        self.parent.master.sel_args = sel_args

        if self._data:
            self._data.save_options(sel_args)
        return True


class SettOptionsDialog(wx.Dialog):
    "base class voor de opties dialogen"
    def __init__(self, parent, args):
        self.parent = parent
        cls = None
        if len(args) == 1:
            title = args[0]
        elif len(args) > 1:
            try:
                cls = args[0]
                title = args[1]
                size = args[2]
            except IndexError:
                pass    # wat er niet is is er niet
        self.cls = cls
        super().__init__(parent, title=shared.app_title, size=(300, 300))
        self.initstuff(parent)
        options = wx.adv.EL_ALLOW_EDIT
        if self.editable:
            options |= wx.adv.EL_ALLOW_NEW | wx.adv.EL_ALLOW_DELETE
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.elb = wx.adv.EditableListBox(self, label=self.titel, pos=(50, 50),
                                          size=(250, 250), style=options)
        self.elb.SetStrings(self.data)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.elb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "\n".join(self.tekst))
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL | wx.GROW | wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.ALIGN_CENTER_VERTICAL | wx.GROW | wx.RIGHT | wx.TOP, 5)

        setup_accels(self, (('edit', self.edit, 'F2'),), [])

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)

    def initstuff(self, parent):
        "placeholder voor aanvullende initialisatie methode"
        if self.cls is not None:
            self.cls.initstuff(self, parent)
            return
        self.titel = ""
        self.data = []
        self.tekst = ["", ""]
        # self.options = wx.adv.EL_ALLOW_EDIT
        self.editable = False

    def edit(self, event):
        "edit a line"
        # hopefully simulating pressing the edit button works
        # btn = self.elb.GetEditButton()
        # btn.Command(wx.CommandEvent(wx.EVT_BUTTON)) nou dit werkt in elk geval niet

    def accept(self):
        """Confirm changes to parent window

        call method on the helper class if provided
        """
        if self.cls is not None:
            self.cls.leesuit(self, self.parent, self.elb.GetStrings())
            return True
        raise NotImplementedError


class LoginBox(wx.Dialog):
    """Sign in with userid & password
    """


class MainGui(wx.Frame):
    """Hoofdscherm met menu, statusbalk, notebook en een "quit" button"""
    def __init__(self, master):
        self.master = master
        self.app = wx.App()  # redirect=True, filename="probreg.log")
        # self.title = 'Actieregistratie'
        self.printer = EasyPrinter()

        if LIN:
            wide, high, left, top = 764, 720, 2, 2
        else:
            wide, high, left, top = 588, 594, 20, 32
        wx.Frame.__init__(self, parent=None, title=self.master.title, pos=(left, top),
                          size=(wide, high),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        sbar = self.CreateStatusBar()
        sbar.SetFieldsCount(2)
        self.SetStatusBar(sbar)
        self.create_menu()
        self.create_actions()
        # self.helptext = self.get_helptext()
        # self.SetTitle(self.title)
        self.SetIcon(wx.Icon(os.path.join(HERE, "task.ico"), wx.BITMAP_TYPE_ICO))
        self.toolbar = None
        self.create_book()

    def create_menu(self):
        """menu opbouwen
        """
        def add_to_menu(menu, menuitem):
            "parse line and create menu item"
            if len(menuitem) == 1:
                menu.AppendSeparator()
            elif len(menuitem) == 4:
                caption, callback, keys, tip = menuitem
                if keys:  # altijd maar eén
                    caption = '\t'.join((caption, keys))
                action = menu.Append(-1, caption, tip)
                # self.Connect(action.GetId(), -1, wx.wxEVT_COMMAND_MENU_SELECTED, callback)
                self.Bind(wx.EVT_MENU, callback, action)
            elif len(menuitem) == 2:
                title, items = menuitem
                sub = wx.Menu()
                if title == '&Data':
                    subid = wx.NewId()
                    self.settingsmenu = (menu, subid)
                else:
                    subid = -1
                for subitem in items:
                    add_to_menu(sub, subitem)
                menu.Append(subid, title, sub)
        menu_bar = wx.MenuBar()
        for title, items in self.master.get_menu_data():
            menu = wx.Menu()
            for menuitem in items:
                add_to_menu(menu, menuitem)
            menu_bar.Append(menu, title)
        self.SetMenuBar(menu_bar)

    def create_actions(self):
        """Create additional application actions
        """
        accel_data = (('print', self.print_, 'Ctrl+P'),
                      ('prev', self.go_prev, 'Alt+Left'),
                      ('next', self.go_next, 'Alt+Right'))
        accel_list = []
        for char in '0123456':
            menuitem = wx.MenuItem(None, -1, 'goto-{}'.format(char))
            self.Bind(wx.EVT_MENU, functools.partial(self.go_to, int(char)), menuitem)
            accel = wx.AcceleratorEntry(cmd=menuitem.GetId())
            ok = accel.FromString('Alt+{}'.format(char))
            if ok:
                accel_list.append(accel)
        setup_accels(self, accel_data, accel_list)

    def create_book(self):
        "build the tabbed widget"
        self.pnl = wx.Panel(self, -1)
        self.bookwidget = wx.Notebook(self.pnl, size=(580, 570))
        self.bookwidget.sorter = None
        # self.book.Bind(wx.EVT_KEY_DOWN, self.on_key)
        # self.Bind(wx.EVT_KEY_DOWN, self.on_key)
        ## self.Bind(wx.EVT_CLOSE, self.exit_app)
        self.bookwidget.Bind(wx.EVT_LEFT_UP, self.on_left_release)
        self.bookwidget.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changed)
        self.bookwidget.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.on_page_changing)
        self.master.create_book(self.bookwidget)

    def go(self):
        "show screen and start application"
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.bookwidget, 1, wx.EXPAND)  # | wx.ALL, 8)
        sizer0.Add(sizer1, 1, wx.EXPAND)  # | wx.ALL, 8)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        self.exit_button = wx.Button(self.pnl, id=wx.ID_EXIT)
        self.Bind(wx.EVT_BUTTON, self.master.exit_app, self.exit_button)
        sizer2.Add(self.exit_button, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer0.Add(sizer2, 0, wx.EXPAND | wx.ALIGN_BOTTOM)
        self.pnl.SetSizer(sizer0)
        self.pnl.SetAutoLayout(True)
        sizer0.Fit(self.pnl)
        sizer0.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.Show(True)
        # self.set_tabfocus(0)  # book.page0.SetFocus()
        # self.select_first_tab()
        self.app.MainLoop()

    def on_page_changing(self, event):
        """deze methode is bedoeld om wanneer er van pagina gewisseld gaat worden
        te controleren of dat wel mogelijk is en zo niet, te melden waarom
        en de paginawissel tegen te houden.
        """
        # print('in maingui.on_page_changing')
        old = event.GetOldSelection()
        # new = event.GetSelection() # unused
        # sel = self.book.GetSelection() # unused
        self.mag_weg = True
        msg = ""
        # print('  old selection is', old)
        # print('  book data is', self.master.book.data)
        # print('  new item is', self.master.book.newitem)
        # print('  current item is', self.master.book.current_item)
        if old == -1:
            pass
        elif self.master.book.fnaam == "":
            if self.datatype == shared.DataType.XML.name:
                wat = 'bestand'
            elif self.datatype == shared.DataType.SQL.name:
                wat = 'project'
            msg = "Kies eerst een {} om mee te werken".format(wat)
            self.mag_weg = False
        elif not self.master.book.data and not self.master.book.newitem:
            msg = "Voer eerst één of meer acties op"
            self.mag_weg = False
        elif self.master.book.current_item == -1 and not self.master.book.newitem:
            msg = "Selecteer eerst een actie"
            self.mag_weg = False
        # print('  checked for leaving is', self.master.book.checked_for_leaving)
        if self.mag_weg and not self.master.book.checked_for_leaving:
            self.mag_weg = self.master.book.pages[self.master.book.current_tab].leavep()
        # print('  mag weg:', self.mag_weg)
        if not self.mag_weg:
            if msg != "":
                wx.MessageBox(msg, "Navigatie niet toegestaan", wx.ICON_ERROR)
            self.master.book.SetSelection(self.master.book.current_tab)
            event.Veto()
        else:
            event.Skip()

    def on_page_changed(self, event):
        """deze methode is bedoeld om na het wisselen van pagina het veld / de velden
        van de nieuwe pagina een waarde te geven met behulp van de vulp methode
        """
        # print('in maingui.on_page_changed')
        old = event.GetOldSelection()
        new = self.master.book.current_tab = event.GetSelection()
        # sel = self.master.book.GetSelection() # unused
        # print('  old selection is', old)
        if LIN and old == -1:  # bij initialisatie en bij afsluiten - op Windows is deze altijd -1?
            return
        self.master.book.pages[new].vulp()
        self.set_tabfocus(self.master.book.current_tab)
        event.Skip()

    def enable_all_book_tabs(self, state):
        "make all tabs (in)accessible"
        # don't know if we need this
        # for i in range(1, self.master.book.count()):
        #     self.bookwidget.setTabEnabled(i, state)

    def enable_book_tabs(self, state, tabfrom=0, tabto=-1):
        "make specified tabs (in)accessible"
        # don't know if we need this
        # if tabto == -1:
        #     tabto = self.master.book.count()
        # for i in range(tabfrom, tabto):
        #     self.bookwidget.setTabEnabled(i, state)

    def enable_all_other_tabs(self):
        "make all tabs accessible except the current one"
        # don't know if we need this
        # for i in range(self.master.book.count()):
        #     if i != self.master.book.current_tab:
        #         self.bookwidget.setTabEnabled(i, True)

    def add_book_tab(self, tab, title):
        "add a new tab to the widget"
        self.bookwidget.AddPage(tab.gui, title)
        tab.gui.doelayout()

    def exit(self):
        "Menukeuze: exit applicatie"
        self.Close(True)

    def set_page(self, num):
        "set the selected page to this index"
        # self.bookwidget.setCurrentIndex(num)
        self.bookwidget.SetSelection(num)
        # print('end of set_page')

    def get_page(self):
        "return index g=for the selected page"
        # return self.bookwidget.currentIndex()
        return self.bookwidget.GetSelection()

    def set_tabfocus(self, tabno):
        "focus geven aan de gekozen tab"
        widgets = [self.master.book.pages[0].gui.p0list,
                   self.master.book.pages[1].gui.proc_entry,
                   # self.master.book.pages[2].gui.text1,
                   # self.master.book.pages[3].gui.text1,
                   # self.master.book.pages[4].gui.text1,
                   # self.master.book.pages[5].gui.text1,
                   # self.master.book.pages[6].gui.progress_list
                  ]
        widgets[tabno].SetFocus()

    def go_next(self, *args):
        """redirect to the method of the current page
        """
        self.master.goto_next()

    def go_prev(self, *args):
        """redirect to the method of the current page
        """
        self.master.goto_prev()

    def go_to(self, page, event):
        """redirect to the method of the current page
        """
        self.master.goto_page(page)

    def print_(self):
        """callback voor ctrl-P(rint)

        vraag om printen scherm of actie, bv. met een InputDialog
        """
        choices = ['huidig scherm', 'huidige actie']
        choice = get_choice_item(self, 'Wat wil je afdrukken?', choices)
        if choice == choices[0]:
            self.master.print_scherm()
        elif choice == choices[1]:
            self.master.print_actie()

    def preview(self):
        """wordt aangeroepen door de menuprint methodes

        preview wordt afgehandeld door de printer class (dit is nog de oude wx methode,
        ik meen gezien te hebben dat wxPhoenix hier anders mee omgaat
        """
        self.css = ""
        if self.css != "":
            self.css = self.css.join(("<style>", "</style>"))
            self.master.printdict['css'] = self.css
        self.master.printdict['hdr'] = self.master.hdr
        html = Template(filename='probreg/actie.tpl').render(**self.master.printdict)
        self.printer.print_(html, self.master.hdr)

    def enable_settingsmenu(self):
        "instellen of gebruik van settingsmenu mogelijk is"
        menu, subid = self.settingsmenu
        menu.Enable(subid, self.master.is_admin)

    def set_statusmessage(self, msg=''):
        """stel tekst in statusbar in
        """
        self.GetStatusBar().SetStatusText(msg)

    def set_window_title(self, text):
        "build title for window"
        self.SetTitle(text)

    def show_username(self, msg):
        "show if/which user is logged in"
        self.GetStatusBar().SetStatusText(msg, 1)

    def set_tab_titles(self, tabs):
        "(re)build the titles on the tabs"
        old, tabs = tabs, {}
        for x, y in tabs.items():
            self.bookwidget.SetPageText(x, y)
        tabs = old

    def select_first_tab(self):
        "set selection to first page"
        self.bookwidget.SetSelection(0)

    def on_left_release(self, evt=None):
        """releasing the lmb (on a tab)
        """
        self.set_tabfocus(self.master.book.current_tab)
        evt.Skip()
