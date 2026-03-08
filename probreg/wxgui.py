"""Actie (was: problemen) Registratie, wxPython versie
"""
import os
import sys
import pathlib
import tempfile
# import functools
import wx
import wx.html
import wx.lib.mixins.listctrl as listmix
import wx.adv
import wx.richtext as wxrt
# import wx.gizmos as gizmos
from mako.template import Template
from probreg import shared
LIN = os.name == 'posix'
HERE = os.path.abspath(os.path.dirname(__file__))
xmlfilter = "XML files (*.xml)|*.xml|all files (*.*)|*.*"


def show_message(win, message, title=''):
    "present a message and wait for the user to confirm (having read it or whatever)"
    if not title:
        title = shared.app_title
    wx.MessageBox(message, title, wx.ICON_INFORMATION, parent=win)


def show_error(win, message, title=''):
    "present a message and wait for the user to confirm (having read it or whatever)"
    if not title:
        title = shared.app_title
    wx.MessageBox(message, title, wx.ICON_ERROR, parent=win)


def get_open_filename(win, start=None):
    "get the name of a file to open"
    start = start or pathlib.Path.cwd()
    what = shared.app_title + " - kies een gegevensbestand"
    return wx.LoadFileSelector(what, xmlfilter, default_name=str(start), parent=win)


def get_save_filename(win, start=None):
    "get the name of a file to save"
    start = start or pathlib.Path.cwd()
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


def ask_question(win, message):
    "ask the user a question with an option to cancel the process"
    with wx.MessageDialog(win, message, shared.app_title, wx.YES_NO | wx.ICON_QUESTION) as dlg:
        ok = dlg.ShowModal()
    return ok == wx.ID_YES


def ask_cancel_question(win, message):
    "ask the user a question with an option to cancel the process"
    with wx.MessageDialog(win, message, shared.app_title,
                          wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION) as dlg:
        ok = dlg.ShowModal()
    return ok == wx.ID_YES, ok == wx.ID_CANCEL


# def show_dialog(win, cls, args=None):
#     "show a dialog and return if the dialog was confirmed / accepted"
#     dlg = cls(win) if args is None else cls(win, args)
#     with dlg:
#         send = True
#         while send:
#             ok = dlg.ShowModal()
#             send = False
#             if ok == wx.ID_OK and not dlg.accept():
#                 send = True
#     return ok == wx.ID_OK


def show_dialog(dlg):
    "show a dialog and return if the dialog was confirmed / accepted"
    with dlg:
        send = True
        while send:
            ok = dlg.ShowModal()
            send = False
            if ok == wx.ID_OK and not dlg.accept():
                send = True
    return ok == wx.ID_OK


def setup_accels(win, accel_data):  # , accel_list=None):
    "define keyboard shortcuts for a gui class"
    menuitemlist = []
    # if accel_list is None:
    accel_list = []
    for text, callback, keyseq in accel_data:
        menuitem = wx.MenuItem(None, -1, text)
        menuitemlist.append(menuitem)
        win.Bind(wx.EVT_MENU, callback, menuitem)
        accel = wx.AcceleratorEntry(cmd=menuitem.GetId())
        ok = accel.FromString(keyseq)
        if ok:
            accel_list.append(accel)
    accel_table = wx.AcceleratorTable(accel_list)
    win.SetAcceleratorTable(accel_table)
    return menuitemlist  # just for unittest


class MainGui(wx.Frame):
    """Hoofdscherm met menu, statusbalk, notebook en een "quit" button"""
    def __init__(self, master):
        self.master = master
        self.app = wx.App()  # redirect=True, filename="probreg.log")
        # self.title = 'Actieregistratie'
        self.printer = EasyPrinter()

        if LIN:
            wide, high, left, top = 1000, 1000, 2, 2  # 764, 720, 2, 2
        else:
            wide, high, left, top = 588, 594, 20, 32
        wx.Frame.__init__(self, parent=None, title=self.master.title, pos=(left, top),
                          size=(wide, high),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        sbar = self.CreateStatusBar()
        sbar.SetFieldsCount(2)
        # self.SetStatusBar(sbar)  -- is dit nodig als je al CreateStatusBar hebt gedaan?
        # self.helptext = self.get_helptext()
        # self.SetTitle(self.title)
        self.SetIcon(wx.Icon(os.path.join(HERE, 'icons', "task.png"), wx.BITMAP_TYPE_PNG))
        self.pnl = wx.Panel(self, -1)
        self.toolbar = None

    def create_menu(self):
        """menu opbouwen
        """
        def add_to_menu(menu, menuitem):
            "parse line and create menu item"
            if len(menuitem) == 1:
                menu.AppendSeparator()
            elif len(menuitem) == len(['caption', 'callback', 'key', 'tip']):
                caption, callback, key, tip = menuitem
                if key:
                    caption = f'{caption}\t{key}'
                action = menu.Append(-1, caption, tip)
                # self.Connect(action.GetId(), -1, wx.wxEVT_COMMAND_MENU_SELECTED, callback)
                self.Bind(wx.EVT_MENU, callback, action)
            elif len(menuitem) == len(['title', 'items']):
                title, items = menuitem
                sub = wx.Menu()
                if title == '&Data':
                    subid = wx.NewId()
                    self.settingsmenu = (menu, subid)
                # else:
                #     subid = -1
                for subitem in items:
                    add_to_menu(sub, subitem)
                menu.AppendSubMenu(sub, title)
        menu_bar = wx.MenuBar()
        for title, items in self.master.get_menu_data():
            menu = wx.Menu()
            for menuitem in items:
                add_to_menu(menu, menuitem)
            menu_bar.Append(menu, title)
        self.SetMenuBar(menu_bar)

    def create_actions(self, actiondefs):
        """Create additional application actions
        """
        # accel_data = (('print', self.master.print_something, 'Ctrl+P'),
        #               ('prev', self.master.goto_prev, 'Alt+Left'),
        #               ('next', self.master.goto_next, 'Alt+Right'))
        # accel_list = []
        accel_data = []
        for text, callback in actiondefs:
            accel_data.append((text, callback, text))
        # for char in '0123456':
        #     menuitem = wx.MenuItem(None, -1, 'goto-{}'.format(char))
        #     self.Bind(wx.EVT_MENU, functools.partial(self.go_to, int(char)), menuitem)
        #     accel = wx.AcceleratorEntry(cmd=menuitem.GetId())
        #     ok = accel.FromString('Alt+{}'.format(char))
        #     if ok:
        #         accel_list.append(accel)
        setup_accels(self, accel_data)  # , accel_list)

    def get_bookwidget(self):
        "build the tabbed widget"
        bookwidget = wx.Notebook(self.pnl, size=(580, 570))
        bookwidget.sorter = None
        bookwidget.Bind(wx.EVT_LEFT_UP, self.on_left_release)
        bookwidget.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changed)
        bookwidget.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.on_page_changing)
        return bookwidget

    def go(self):
        "show screen and start application"
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.master.book, 1, wx.EXPAND)  # | wx.ALL, 8)
        sizer0.Add(sizer1, 1, wx.EXPAND)  # | wx.ALL, 8)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        self.exit_button = wx.Button(self.pnl, id=wx.ID_EXIT)
        self.Bind(wx.EVT_BUTTON, self.master.exit_app, self.exit_button)
        sizer2.Add(self.exit_button, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer0.Add(sizer2, 0, wx.EXPAND)
        self.pnl.SetSizer(sizer0)
        self.pnl.SetAutoLayout(True)
        sizer0.Fit(self.pnl)
        sizer0.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.Show(True)
        self.app.MainLoop()

    def refresh_page(self):
        """reload page while staying on it
        this method is called when a user signs in
        """
        self.on_page_changed(newtabnum=0)

    def on_page_changing(self, event):
        """deze methode is bedoeld om wanneer er van pagina gewisseld gaat worden
        te controleren of dat wel mogelijk is en zo niet, te melden waarom
        en de paginawissel tegen te houden.
        """
        if self.master.initializing:
            return
        old = event.GetOldSelection()
        # new = event.GetSelection() # unused
        # sel = self.book.GetSelection() # unused
        mag_weg = True
        # msg = ""
        if old == -1:
            pass
        # in de qt variant zitten de volgende controles in leavep
        # elif self.master.book.fnaam == "":
        #     if self.master.multiple_files:  # datatype == shared.DataType.XML.name:
        #         wat = 'bestand'
        #     elif self.master.multiple_projects:  # datatype == shared.DataType.SQL.name:
        #         wat = 'project'
        #     msg = f"Kies eerst een {wat} om mee te werken"
        #     mag_weg = False
        # elif not self.master.book.data and not self.master.book.newitem:
        #     # bestand bevat nog geen gegevens en we zijn nog niet bezig met de eerste opvoeren
        #     msg = "Voer eerst één of meer acties op"
        #     mag_weg = False
        # elif self.master.book.current_item == -1 and not self.master.book.newitem:
        #     # geen actie geselecteerd en we zijn niet bezig met een nieuwe
        #     msg = "Selecteer eerst een actie"
        #     mag_weg = False
        else:
            mag_weg = self.master.book.pages[self.master.book.current_tab].leavep(old)
        if not mag_weg:
            # if msg != "":
            #     wx.MessageBox(msg, "Navigatie niet toegestaan", wx.ICON_ERROR)
            self.master.book.SetSelection(self.master.book.current_tab)  # is dit nodig?
            event.Veto()
        else:
            event.Skip()

    def on_page_changed(self, event=None, newtabnum=None):
        """deze methode is bedoeld om na het wisselen van pagina het veld / de velden
        van de nieuwe pagina een waarde te geven met behulp van de vulp methode

        newtabnum is om een paginawissel te forceren zonder dat er een event is gestuurd
        (momenteel alleen voor een refresh van page 0)
        """
        if event:
            old = event.GetOldSelection()
            new = self.master.book.current_tab = event.GetSelection()
        elif newtabnum is not None:
            old = new = newtabnum
        else:
            return
        notab, firsttab, lasttab = -1, 0, 6
        # sel = self.master.book.GetSelection() # unused
        # print('  old selection is', old)
        if LIN and old == notab:  # bij initialisatie en bij afsluiten - op Windows is old altijd -1?
            return
        if firsttab < new < lasttab:
            self.master.book.pages[new].vulp()
        elif new in (firsttab, lasttab):
            if old == new:
                item = self.master.book.pages[new].gui.get_list_row()  # remember current item
            self.master.book.pages[new].vulp()
            if old == new:
                self.master.book.pages[new].gui.set_list_row(item)     # reselect item
        self.set_tabfocus(self.master.book.current_tab)
        if event:
            event.Skip()

    def add_book_tab(self, bookwidget, tab, title):
        "add a new tab to the widget"
        bookwidget.AddPage(tab.gui, title)

    def enable_tab(self, bookwidget, tabno, state):
        """make a tab accessible or not"

        is called from main, but not really needed here because I can block navigation in
        on_page_changing, but maybe worth implementing by way of ging a visual clue
        Although I can't find if this is at all possible (wx.ToolBook does have EnablePage)
        """

    def get_tab_count(self, bookwidget):
        "return the number of pages"
        return bookwidget.GetRowCount()

    def exit(self):
        "Menukeuze: exit applicatie"
        self.Close(True)

    def Close(self, *args):
        "redefined"
        self.master.save_startitem_on_exit()
        super().Close(*args)

    def set_page(self, bookwidget, num):
        "set the selected page to this index"
        if 0 <= num <= len(bookwidget.pages):
            bookwidget.SetSelection(num)

    def set_page_title(self, bookwidget, num, text):
        "change the tab title"
        bookwidget.SetPageText(num, text)

    def get_page(self, bookwidget):
        "return index for the selected page"
        return bookwidget.GetSelection()

    def set_tabfocus(self, tabno):
        "focus geven aan de gekozen tab"
        self.master.get_focus_widget_for_tab(tabno).SetFocus()

    # def go_to(self, page, event):
    #     """redirect to the method of the current page
    #     """
    #     print('in mainGui.go_to naar page', page, 'event', event)
    #     self.master.goto_page(page)

    def preview(self):
        """wordt aangeroepen door de menuprint methodes

        preview wordt afgehandeld door de printer class (dit is nog de oude wx methode,
        ik meen gezien te hebben dat wxPhoenix hier anders mee omgaat
        """
        # self.css = ""
        # if self.css:
        #     self.css = self.css.join(("<style>", "</style>"))
        #     self.master.printdict['css'] = self.css
        self.master.printdict['hdr'] = self.master.hdr
        html = Template(filename=os.path.join(os.path.dirname(__file__),
                                              'actie.tpl')).render(**self.master.printdict)
        self.printer.print(html, self.master.hdr)

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

    def on_left_release(self, evt=None):
        """releasing the lmb (on a tab)
        """
        self.set_tabfocus(self.master.book.current_tab)
        if evt:
            evt.Skip()


class PageGui(wx.Panel):
    "base class for notebook page"
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        self.appbase = self.parent.parent
        self.accel_data = []
        super().__init__(parent)

    def start_display(self):
        "begin building the screen"
        vsizer = wx.BoxSizer(wx.VERTICAL)
        # mogelijk moet dit aan het eind van het opbouwen van de display
        self.SetAutoLayout(True)
        self.SetSizer(vsizer)
        vsizer.Fit(self)
        vsizer.SetSizeHints(self)
        return vsizer

    def create_text_field(self, sizer, width, height, callback, parent=None):
        """build rich text area with style changing properties
        """
        parent = parent or self
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        # high = 330 if LIN else 430
        cls = EditorPanelRt if self.appbase.use_rt else EditorPanel
        textfield = cls(parent, size=wx.Size(width, height))
        self.Bind(wx.EVT_TEXT, callback, textfield)
        # textfield.Bind(wx.EVT_KEY_DOWN, self.on_key)
        # textfield.font_changed(textfield.font())
        hsizer.Add(textfield, 1, wx.ALL | wx.EXPAND, 10)  # 4)
        sizer.Add(hsizer, 1, wx.EXPAND)
        return textfield

    def create_toolbar(self, sizer, textfield, toolbardata, parent=None):
        """build toolbar with buttons for changing text style
        """
        parent = parent or self
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        toolbar = wx.ToolBar(parent)
        toolbar.SetToolBitmapSize((16, 16))
        fontbutton = wx.Button(toolbar, label="Font")
        fontbutton.Bind(wx.EVT_BUTTON, self.choose_font)
        toolbar.AddControl(fontbutton)

        # accel_data = []
        for menudef in toolbardata:
            if not menudef:
                toolbar.AddSeparator()
                continue
            label, shortcut, icon, info, *methods = menudef
            if icon:
                bmp = wx.Bitmap(wx.Image(os.path.join(HERE, icon + '.png'), wx.BITMAP_TYPE_PNG))
            else:
                bmp = wx.NullBitmap
            toolid = wx.NewId()
            if info.startswith("Toggle"):
                toolbar.AddCheckTool(toolid, label, bmp, shortHelp=info)
            else:
                toolbar.AddTool(toolid, label, bmp, shortHelp=info)
            try:
                callback, update_ui = methods
            except ValueError:
                callback, update_ui = methods[0], None
            self.Bind(wx.EVT_TOOL, callback, id=toolid)
            if shortcut:
                # accel_data.append((label, callback, shortcut))
                self.add_keybind(shortcut, callback, label)
            if update_ui:
                self.Bind(wx.EVT_UPDATE_UI, update_ui, id=toolid)
        # if accel_data:
        #     setup_accels(self, accel_data)

        # self.combo_font.activated[str].connect(textfield.text_family)
        # self.combo_size.activated[str].connect(textfield.text_size)
        toolbar.Realize()
        hsizer.Add(toolbar, 1, wx.ALL | wx.EXPAND, 4)
        sizer.Insert(0, hsizer, 0, wx.EXPAND)
        return toolbar

    def create_buttons(self, buttondefs, sizer=None):
        """add buttonbar
        """
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons = []
        for text, callback in buttondefs:
            btn = wx.Button(self, label=text)
            self.Bind(wx.EVT_BUTTON, callback, btn)
            if '(' in text:
                text, keydef = text.split('(', 1)
                keydef = keydef.split(')')[0].replace('-', '+')
                # self.actiondict.append((text, callback, keydef))
                self.add_keybind(keydef, callback, text.strip())
            hsizer.Add(btn)
            buttons.append(btn)
        if sizer:
            sizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        else:
            self.vsizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        return buttons

    def add_keybind(self, keydef, callback, text='', last=False):
        """set up additional keybindings (i.e. not embedded in buttonlabels, menuoptions etc.)
        """
        if not text:
            text = keydef
        self.accel_data.append((text, callback, keydef))
        if last:
            setup_accels(self, self.accel_data)

    def choose_font(self, event):
        """show font dialog
        """
        self.text1.text_font(event)

    def reset_font(self):
        """compatibility between versions, geen idee of ik dat hier echt nodig heb"""

    def enable_widget(self, widget, state):
        "make a field accessible or not"
        widget.Enable(state)

    def move_cursor_to_end(self, textfield):
        "position the cursor at the end of the text"
        try:
            textfield.MoveEnd()
        except AttributeError:
            textfield.SetInsertionPointEnd()

    def set_textarea_contents(self, textfield, data):
        "set the page text"
        textfield.set_contents(data)

    def get_textarea_contents(self, textfield):
        "get the page text"
        return textfield.get_contents()

    def enable_toolbar(self, toolbar, value):
        "make the toolbar accessible (or not)"
        toolbar.Enable(value)

    def set_text_readonly(self, textfield, value):
        "protect page text from updating (or not)"
        textfield.SetEditable(not value)

    def is_enabled(self, widget):
        "return if the widget is accessible"
        return widget.IsEnabled()

    def set_focus_to_field(self, field):
        "set the focus for this page to a specific field"
        field.SetFocus()


class EditorPanel(wx.TextCtrl):
    "Temporary (?) replacement for RichTextCtrl"
    # def __init__(self, parent=None, size=):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, size=(400, 200),
                         style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB | wx.TE_RICH2 | wx.TE_WORDWRAP)

    def set_contents(self, data):
        "load contents into editor"
        self.SetValue(data)

    def get_contents(self):
        "return contents from editor"
        return self.GetValue()

    def _check_dirty(self):
        "check for modifications"
        return self.IsModified()

    def _mark_dirty(self, value):
        "manually turn modified flag on/off (mainly intended for off)"
        self.SetModified(not value)

    def _openup(self, value):
        "make text accessible (or not)"
        self.Enable(value)


class EditorPanelRt(wxrt.RichTextCtrl):
    "Rich text editor displaying the selected comment"
    # def __init__(self, parent=None, size=(400, 200)):  # , _id):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, size=(400, 200), style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER)
        self.textAttr = wxrt.RichTextAttr()

    def set_contents(self, data):
        "load contents into editor"
        # if data.startswith('<'):  # only load as html if it looks like html
        #     self.setHtml(data)
        # else:
        #     self.setText(data)
        self.Clear()
        if data.startswith('<?xml'):
            handler = wxrt.RichTextXMLHandler()
            _buffer = self.GetBuffer()
            _buffer.AddHandler(handler)
            with tempfile.NamedTemporaryFile(mode='w+') as out:
            # with io.BytesIO() as stream:
                out.write(data)
                handler.LoadFile(_buffer, out.name)
                # handler.LoadFile(_buffer, stream)
        else:
            self.SetValue(data)
        self.Refresh()
        # self.oldtext = data
        if data.startswith('<?xml'):
            return handler, _buffer, out.name  # just for test method

    def get_contents(self):
        "return contents from editor"
        handler = wxrt.RichTextXMLHandler()
        _buffer = self.GetBuffer()
        _buffer.AddHandler(handler)
        with tempfile.NamedTemporaryFile(mode='w+') as out:
        # with io.BytesIO() as stream:
            handler.SaveFile(_buffer, out.name)
            # handler.SaveFile(_buffer, stream)
            content = out.read()
            # content = stream.getvalue()
        # return self.GetValue()
        self.teststuff = handler, _buffer, out.name  # just for test method
        return content

    def text_bold(self, event):
        "selectie vet maken"
        if self.HasFocus():
            self.ApplyBoldToSelection()

    def text_italic(self, event):
        "selectie schuin schrijven"
        if self.HasFocus():
            self.ApplyItalicToSelection()

    def text_underline(self, event):
        "selectie onderstrepen"
        if self.HasFocus():
            self.ApplyUnderlineToSelection()

    def text_strikethrough(self, event):
        "selectie doorstrepen"
        # niet ingebouwd in wx voor zover ik kan nagaan

    def case_lower(self, event):
        "change case not implemented"

    def case_upper(self, event):
        "change case not implemented"

    def indent_more(self, event):
        "alinea verder laten inspringen"
        self.change_indent(100)

    def indent_less(self, event):
        "alinea minder ver laten inspringen"
        self.change_indent(-100)

    def change_indent(self, amount):
        "alinea inspringing instellen"
        if not self.HasFocus():
            return
        attr = wxrt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            range = wxrt.RichTextRange(ip, ip)
            if self.HasSelection():
                range = self.GetSelectionRange()
            attr.SetLeftIndent(attr.GetLeftIndent() + amount)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.SetStyle(range, attr)

    def text_font(self, event):
        "lettertype en/of -grootte instellen"
        # if not self.HasFocus():
        #     return
        range = self.GetSelectionRange()
        fontData = wx.FontData()
        fontData.EnableEffects(False)
        # attr = wxrt.TextAttrEx()
        attr = wxrt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_FONT)
        if self.GetStyle(self.GetInsertionPoint(), attr):
            fontData.SetInitialFont(attr.GetFont())
        with wx.FontDialog(self, fontData) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                fontData = dlg.GetFontData()
                font = fontData.GetChosenFont()
                if font:
                    attr.SetFlags(wx.TEXT_ATTR_FONT)
                    attr.SetFont(font)
                    self.SetStyle(range, attr)
        self.SetFocus()

    def enlarge_text(self, event):
        "change text style"

    def shrink_text(self, event):
        "change text style"

    def linespacing_1(self, event):
        "enkele regelafstand instellen"
        self.set_linespacing(10)

    def linespacing_15(self, event):
        "anderhalve regelafstand instellen"
        self.set_linespacing(15)

    def linespacing_2(self, event):
        "dubbele regelafstand instellen"
        self.set_linespacing(20)

    def set_linespacing(self, amount):
        "regelafstand instellen"
        if not self.HasFocus():
            return
        attr = wxrt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            r = wxrt.RichTextRange(ip, ip)
            if self.HasSelection():
                r = self.GetSelectionRange()
            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(amount)
            self.SetStyle(r, attr)

    def increase_paragraph_spacing(self, event):
        "ruimte tussen alinea's vergroten"
        if not self.HasFocus():
            return
        self.set_paragraph_spacing(more=True)

    def decrease_paragraph_spacing(self, event):
        "ruimte tussen alinea's verkleinen"
        if not self.HasFocus():
            return
        self.set_paragraph_spacing(less=True)

    def set_paragraph_spacing(self, more=False, less=False):
        "ruimte tussen alinea's instellen"
        unit = 20
        attr = wxrt.RichTextAttr()
        if more:
            factor = unit
        elif less:
            if attr.GetParagraphSpacingAfter() < unit:
                return
            factor = -1 * unit
        else:
            return  # for now only increase or decrease
        new_spacing = attr.GetParagraphSpacingAfter() + factor
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            range = wxrt.RichTextRange(ip, ip)
            if self.HasSelection():
                range = self.GetSelectionRange()
            attr.SetParagraphSpacingAfter(new_spacing)
            attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
            self.SetStyle(range, attr)

    def font_changed(self, font):
        """fontgegevens aanpassen

        de selectie in de comboboxen wordt aangepast, de van toepassing zijnde
        menuopties worden aangevinkt, en en de betreffende toolbaricons worden
        geaccentueerd"""

    def update_bold(self, evt):
        "het betreffende menuitem aanvinken indien van toepassing"
        evt.Check(self.IsSelectionBold())

    def update_italic(self, evt):
        "het betreffende menuitem aanvinken indien van toepassing"
        evt.Check(self.IsSelectionItalics())

    def update_underline(self, evt):
        "het betreffende menuitem aanvinken indien van toepassing"
        evt.Check(self.IsSelectionUnderlined())

    def _check_dirty(self):
        "check for modifications"
        return self.IsModified()

    def _mark_dirty(self, value):
        "manually turn modified flag on/off (mainly intended for off)"
        self.SetModified(not value)

    def _openup(self, value):
        "make text accessible (or not)"
        self.Enable(value)


class Page0Gui(PageGui, listmix.ColumnSorterMixin):
    "pagina 0: overzicht acties"
    def __init__(self, parent, master):  # , widths):
        # self.parent = parent
        # self.master = master
        super().__init__(parent, master)

        self.imglist = wx.ImageList(16, 16)
        self.up_arrow = self.imglist.Add(wx.Bitmap(wx.Image(os.path.join(HERE, 'icons/up.png'),
                                                            wx.BITMAP_TYPE_PNG)))
        self.down_arrow = self.imglist.Add(wx.Bitmap(wx.Image(os.path.join(HERE, 'icons/down.png'),
                                                              wx.BITMAP_TYPE_PNG)))
        self.vsizer = wx.BoxSizer(wx.VERTICAL)

    def add_list(self, titles, widths):
        "add the selection list to the display"
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        p0list = MyListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL)
        p0list.SetImageList(self.imglist, wx.IMAGE_LIST_SMALL)

        self.itemDataMap = self.parent.data
        self.p0list = p0list  # referentie nodig voor GetListCtrl methodei die de mixin aanroept
        listmix.ColumnSorterMixin.__init__(self, len(titles))
        for indx, wid in enumerate(widths):
            p0list.InsertColumn(indx, titles[indx])
            p0list.SetColumnWidth(indx, wid)
        self.SortListItems(0)  # , True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_change_selected, p0list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_activate_item, p0list)
        # self.Bind(wx.EVT_LIST_COL_CLICK, self.on_column_clicked, p0list)
        p0list.Bind(wx.EVT_LEFT_DCLICK, self.on_doubleclick)
        # self.p0list.Bind(wx.EVT_KEY_DOWN, self.on_key)
        # self.Bind(wx.EVT_KEY_DOWN, self.on_key)
        sizer.Add(p0list, 1, wx.EXPAND | wx.ALL, 2)
        self.vsizer.Add(sizer, 1, wx.EXPAND | wx.ALL, 5)
        return p0list

    # def add_buttons(self, buttondefs):
    #     "add a button strip to the display"
    #     sizer = wx.BoxSizer(wx.HORIZONTAL)
    #     for text, callback in buttondefs:
    #         button = wx.Button(self, label=text)
    #         self.Bind(wx.EVT_BUTTON, callback, button)
    #         sizer.Add(button, 0, wx.ALL, 3)
    #     self.sizer.Add(sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 0)

    def finish_display(self):
        "final actions to show the screen"
        # setup_accels(self, self.accel_data)
        self.SetAutoLayout(True)
        self.SetSizer(self.vsizer)
        self.vsizer.Fit(self)
        self.vsizer.SetSizeHints(self)

    def enable_sorting(self, p0list, value):
        "stel in of sorteren mogelijk is"
        # is afhankelijk van MainWindow.sort_via_options instelling
        # hoe moet dit gerealiseerd (ColumnSorterMxin uitzetten of zoiets?)

    def GetListCtrl(self):
        "reimplemented methode tbv correcte werking sorteer mixin"
        # referentie is al in
        return self.p0list

    def GetSortImages(self):
        "reimplimented methode tbv correcte werking sorteer mixin"
        return (self.down_arrow, self.up_arrow)

    def on_change_selected(self, event):
        "callback voor selectie van item"
        # self.parent.current_item = event.Index
        # seli = self.p0list.GetItemData(self.parent.current_item)
        # self.readp(self.parent.data[seli][0])
        # hlp = "&Herleef" if self.parent.pagedata.arch else "&Archiveer"
        # self.archive_button.SetLabel(hlp)
        self.master.change_selected(event.Index)
        # event.Skip()

    def on_activate_item(self, event):
        "callback voor activeren van item"
        # self.parent.current_item = event.Index
        self.master.activate_item()

    def on_doubleclick(self, event):
        "callback voor dubbelklikken op item"
        self.master.goto_actie()
        # event.Skip()

    def clear_list(self, p0list):
        "initialize the list"
        p0list.DeleteAllItems()
        p0list.has_selection = False

    def add_listitem(self, p0list, data):
        "add an item to the list"
        itemindex = p0list.InsertItem(p0list.GetItemCount(), data)
        p0list.SetItemData(itemindex, int(''.join(data.split('-'))))
        return itemindex

    # def set_listitem_values(self, itemindex, data):
    #     "set column values for list entry"
    #     for col, value in enumerate(data):
    #         if col == 0 and data[-1]:
    #             value = value + ' (A)'
    #         elif col == 1:
    #             pos = value.index(".") + 1
    #             value = value[pos:pos + 1].upper()
    #         elif col == 2:
    #             pos = value.index(".") + 1
    #             value = value[pos:]
    #         if col < len(data) - 1:
    #             self.p0list.SetItem(itemindex, col, value)
    #     self.p0list.has_selection = True

    def get_items(self, p0list):
        "retrieve all listitems"
        return [p0list.GetItem(i) for i in range(p0list.GetItemCount())]

    # itemindicator is bij Qt een item, bij Wx een itemindex
    def get_item_text(self, p0list, itemindicator, column):
        "get the item's text for a specified column"
        try:
            int(itemindicator)
        except TypeError:
            itemindicator = itemindicator.GetId()
        return p0list.GetItemText(itemindicator, column)

    def set_item_text(self, p0list, itemindicator, column, text):
        "set the item's text for a specified column"
        p0list.SetItem(itemindicator, column, text)

    def get_first_item(self, p0list):
        "select the first item in the list"
        return 0  # self.p0list.GetItem(0)

    # def get_item_by_index(self, item_n):
    #     "select the indicated item in the list"
    #     return item_n

    def get_item_by_id(self, p0list, item_id):
        "select the item with the id requested"
        for i in range(p0list.GetItemCount()):
            if p0list.GetItemText(i, 0) == item_id:
                return i  # p0list.GetItem(i)
        return None

    # def has_selection(self):
    #     "return if list contains selection of data"
    #     return self.p0list.has_selection

    def set_selection(self, p0list):
        "set selected item if any"
        # if self.parent.current_item != -1:   # of komt hier kennelijk toch een item binnen?
        if self.parent.current_item:
            p0list.Select(self.parent.current_item)

    def get_selection(self, p0list):
        "get selected item"
        return p0list.GetFirstSelected()

    def ensure_visible(self, p0list, item):
        "make sure listitem is visible"
        if item:    # hier komt kennelijk toch een item binnen?
            p0list.EnsureVisible(item)

    def set_button_text(self, button, txt):
        "set button text according to archive status"
        button.SetLabel(txt)

    def get_selected_action(self, p0list):
        "return the key of the selected action"
        data = str(p0list.GetItemData(p0list.GetFirstSelected()))
        return '-'.join((data[:4], data[4:]))

    def get_list_row(self, p0list):
        "return the event list's selected row index"
        return p0list.GetFirstSelected()  # currentRow()

    def set_list_row(self, p0list, num):
        "set the event list's row selection"
        p0list.Select(num)  # setCurrentRow(num)


class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    "list control mixed in with width adapter"
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, pos=pos, size=size, style=style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.has_selection = False


class Page1Gui(PageGui):
    "pagina 1: startscherm actie"
    def __init__(self, parent, master):
        # self.parent = parent
        self.master = master
        super().__init__(parent, master)
        # self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.gsizer = wx.GridBagSizer(3, 12)  # rows, cols, hgap, vgap
        self.vsizer.Add(self.gsizer)
        self.row = 0
        self.accel_data = []
        # dit moet mogelijk pas bij het afmaken van de display
        self.SetAutoLayout(True)
        self.SetSizer(self.vsizer)
        self.vsizer.Fit(self)
        self.vsizer.SetSizeHints(self)

    def add_textentry_line(self, labeltext, width, callback=None):
        "add a line with a text entry field to the display"
        self.row += 1
        self.gsizer.Add(wx.StaticText(self, label=labeltext), (self.row, 0),
                        flag=wx.ALL | wx.ALIGN_TOP, border=10)
        field = wx.TextCtrl(self, size=(width, -1))
        self.gsizer.Add(field, (self.row, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        if callback:
            self.Bind(wx.EVT_TEXT, callback, field)
        return field

    def add_combobox_line(self, labeltext, width, callback):
        "add a line with a combobox to the display"
        self.row += 1
        self.gsizer.Add(wx.StaticText(self, label=labeltext), (self.row, 0),
                        flag=wx.ALL | wx.ALIGN_TOP, border=10)
        field = wx.ComboBox(self, size=(width, -1), style=wx.CB_DROPDOWN | wx.CB_READONLY)
        if callback:
            self.Bind(wx.EVT_TEXT, callback, field)
        self.gsizer.Add(field, (self.row, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        return field

    def add_pushbutton_line(self, labeltext, buttontext, callback):
        "add a line with a pushbutton to the display"
        self.row += 1
        lbl = wx.StaticText(self, label="")
        self.gsizer.Add(lbl, (self.row, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM,
                        border=10)
        self.row += 1
        btn = wx.Button(self, label=buttontext)
        self.Bind(wx.EVT_BUTTON, callback, btn)
        self.gsizer.Add(btn, (self.row, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.TOP, border=5)
        return lbl, btn

    def add_textbox_line(self, labeltext, callback):
        "add a line with a large text entry field to the display"
        self.row += 1
        self.gsizer.Add(wx.StaticText(self, label=labeltext), (self.row, 0),
                        flag=wx.TOP | wx.BOTTOM, border=10)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        fld = wx.TextCtrl(self, size=(800, 200),
                          style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB | wx.TE_RICH2 | wx.TE_WORDWRAP)
        self.Bind(wx.EVT_TEXT, callback, fld)
        sizer.Add(fld)
        self.gsizer.Add(sizer, (self.row, 1), span=(1, 2), flag=wx.TOP | wx.BOTTOM, border=10)
        return fld

    # moet dit nog?
    # def finalize_grid(self):
    #     self.gsizer.Add((-1, 186), (9, 0))
    #     self.gsizer.AddGrowableRow(8)
    #     self.gsizer.AddGrowableCol(1)

    def show_button(self, button, value):
        "hide or shown button"
        if value:
            button.Show()
        else:
            button.Hide()

    def set_textfield_value(self, field, value):
        "set textfield value"
        field.SetValue(value)

    def set_label_value(self, field, value):
        "set textfield value"
        # field.SetValue(value)
        field.SetLabel(value)

    def set_textbox_value(self, field, value):
        "set textfield value"
        field.SetValue(value)

    def get_textfield_value(self, field):  # , value):
        "get textfield value"
        return field.GetValue()

    # def get_label_value(self, field):  # , value):
    #     "get textfield value"
    #     return field.GetLabel()

    def get_textbox_value(self, field):  # , value):
        "get textfield value"
        return field.GetValue()

    def set_choice(self, field, domain, value):
        "set selected entry in a combobox"
        for x in range(len(domain)):
            code = field.GetClientData(x)
            if code == value:
                field.SetSelection(x)
                break

    def get_choice_index(self, field):
        "get index of selected entry in a combobox"
        return field.GetSelection()

    def get_choice_data(self, field):
        "get selected entry in a combobox"
        idx = field.GetSelection()
        code = field.GetClientData(idx)
        text = field.GetStringSelection()
        return code, text

    def set_button_text(self, button, value):
        "set the text for the archive button"
        button.SetLabel(value)

    def clear_combobox(self, combobox):
        "initialize choices in a combobox"
        combobox.Clear()

    # def clear_stats(self):
    #     "initialize status choices"
    #     self.stat_choice.Clear()

    # def clear_cats(self):
    #     "initialize category choices"
    #     self.cat_choice.Clear()

    def add_combobox_choice(self, combobox, text, value):
        "add combobox choice"
        combobox.Append(text, value)

    # def add_cat_choice(self, text, value):
    #     "add category choice"
    #     self.cat_choice.Append(text, value)

    # def add_stat_choice(self, text, value):
    #     "add status choice"
    #     self.stat_choice.Append(text, value)


class Page6Gui(PageGui):
    "pagina 6: voortgang"
    def __init__(self, parent, master):
        # self.parent = parent
        self.master = master
        super().__init__(parent, master)
        # self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        # high = 200 if LIN else 280
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.pnl = wx.SplitterWindow(self, size=(500, 400), style=wx.SP_LIVE_UPDATE)
        hsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer.Add(self.pnl, 1, wx.EXPAND | wx.ALL, 4)
        self.vsizer.Add(hsizer, 1, wx.EXPAND | wx.ALL, 8)
        self.accel_data = []

    def create_list(self):
        "maak het lijstgedeelte van de display"
        plist = MyListCtrl(self.pnl, size=(250, -1),  # high),
                           style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_SINGLE_SEL)
        if not self.appbase.work_with_user:
            self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_activate_item, plist)
            self.accel_data.append(('new-item', self.on_activate_item, 'Shift-Ctrl-N'))
        # plist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select_item)
        # plist.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_deselect_item)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select_item, plist)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_deselect_item, plist)
        plist.InsertColumn(0, 'Momenten')
        self.accel_data += [('goto-prev', self.master.goto_prev, 'Shift+Ctrl+Up'),
                            ('goto-next', self.master.goto_next, 'Shift+Ctrl+Down')]
        return plist

    def create_textfield(self, width, height, callback):
        "maak het textarea gedeelte van de display"
        # high = 100 if LIN else 110
        self.textpanel = wx.Panel(self.pnl)
        vbox = wx.BoxSizer(wx.VERTICAL)
        # ptext = super().create_text_field(vbox, width, height, callback)
        ptext = self.create_text_field(vbox, width, height, callback, parent=self.textpanel)
        if self.appbase.use_rt:
            data = self.master.get_toolbar_data(ptext)
            # self.toolbar = super().create_toolbar(vbox, ptext, data)
            self.toolbar = self.create_toolbar(vbox, ptext, data, parent=self.textpanel)
            # vbox.Add(self.toolbar, 0, wx.EXPAND)
            # vbox.Add(ptext, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        # else:
        #     vbox.Add(ptext, 1, wx.EXPAND | wx.ALL, 8)
        self.textpanel.SetAutoLayout(True)
        self.textpanel.SetSizer(vbox)
        vbox.Fit(self.textpanel)
        return ptext

    # def add_buttons(self):
    #     self.save_button = wx.Button(self, label='Sla wijzigingen op (Ctrl-S)')
    #     self.Bind(wx.EVT_BUTTON, self.master.savep, self.save_button)
    #     self.cancel_button = wx.Button(self, label='Maak wijzigingen ongedaan (Alt-Ctrl-Z)')
    #     self.Bind(wx.EVT_BUTTON, self.master.restorep, self.cancel_button)
    #     sizer2 = wx.BoxSizer(wx.HORIZONTAL)
    #     sizer2.Add(self.save_button, 0, wx.ALL, 3)
    #     # sizer2.Add(self.saveandgo_button, 0, wx.ALL, 3)
    #     sizer2.Add(self.cancel_button, 0, wx.ALL, 3)
    #     self.sizer.Add(sizer2, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

    #     accel_data += [('savep', self.master.savep, 'Ctrl+S'),
    #                    ('restorep', self.master.restorep, 'Alt+Ctrl+Z'),

    def finish_display(self):
        "final actions to show the screen"
        setup_accels(self, self.accel_data)
        self.pnl.SplitHorizontally(self.master.progress_list, self.textpanel)
        self.pnl.SetSashPosition(250)
        self.SetAutoLayout(True)
        self.SetSizer(self.vsizer)
        self.vsizer.Fit(self)
        self.vsizer.SetSizeHints(self)

    def on_activate_item(self, event):
        """callback voor activeren van een item

        wanneer dit gebeurt op het eerste item kan een nieuwe worden aangemaakt
        """
        if event.Index == 0:
            # self.add_item()
            self.master.initialize_new_event()

    def on_deselect_item(self, evt):
        """callback voor het niet meer geselecteerd zijn van een item

        selecteren van (klikken op) een regel in de listbox doet de inhoud van de textctrl
        ook veranderen. eerst controleren of de tekst veranderd is
        dat vragen moet ook in de situatie dat je op een geactiveerde knop klikt,
        het panel wilt verlaten of afsluiten
        de knoppen onderaan doen de hele lijst bijwerken in self.parent.book.p
        """
        idx = evt.Index
        if idx == 0:
            return
        maxlen = 80
        tekst = self.get_textfield_contents(self.master.progress_text)
        # tekst = self.master.progress_text.get_contents()
        if tekst != self.master.oldtext:
            self.master.event_data[idx - 1] = tekst
            self.master.oldtext = tekst
            short_text = tekst.split("\n")[0]
            short_text = short_text if len(short_text) < maxlen else short_text[:maxlen] + "..."
            self.master.progress_list.SetItem(
                idx, 0, f"{self.master.event_list[idx - 1]} - {short_text}")
            self.master.progress_list.SetItemData(idx, idx - 1)
        evt.Skip()

    def on_select_item(self, event):
        """callback voor het selecteren van een item

        selecteren van (klikken op) een regel in de listbox doet de inhoud van de textctrl
        ook veranderen. eerst controleren of de tekst veranderd is
        dat vragen moet ook in de situatie dat je op een geactiveerde knop klikt,
        het panel wilt verlaten of afsluiten
        de knoppen onderaan doen de hele lijst bijwerken in self.parent.book.p
        """
        self.current_item = event.Index  # - 1
        if self.current_item == 0:
            return
        self.master.progress_text.SetEditable(False)
        if not self.parent.pagedata.arch:
            self.master.progress_text.SetEditable(True)
        self.master.oldtext = self.master.event_data[self.current_item - 1]
        self.master.initializing = True
        self.set_textfield_contents(self.master.progress_text, self.master.oldtext)
        self.master.initializing = False
        self.master.progress_text.Enable(True)
        self.master.progress_text.SetFocus()
        # event.Skip()

    # def init_textfield(self):
    #     "set up text field"
    #     self.clear_textfield()
    #     self.protect_textfield()

    def create_new_listitem(self, listbox, textfield, datum, oldtext):
        """update widgets with new event
        """
        listbox.InsertItem(1, f'{datum} - {oldtext}')
        listbox.SetSelection(1)
        textfield.set_contents(oldtext)
        textfield.SetEditable(True)   # .Enable(True)

        textfield.SetFocus()

    def clear_list(self, listbox):
        "clear out events list widget"
        listbox.DeleteAllItems()

    def add_first_listitem(self, listbox, text):
        "set up top item to add new event when doubleclickes"
        index = listbox.InsertItem(0, text)
        listbox.SetItem(index, 0, text)
        listbox.SetItemData(index, -1)

    def add_item_to_list(self, listbox, textfield, idx, datum):
        """add an entry to the events list widget (when initializing)
        first convert to HTML (if needed) and back
        """
        maxlen = 80
        tekst_plat = self.convert_text(textfield, self.master.event_data[idx], to='plain')
        try:
            text = tekst_plat.split("\n")[0].strip()
        except AttributeError:
            text = tekst_plat or ""
        text = text if len(text) < maxlen else text[:maxlen] + "..."
        index = listbox.InsertItem(sys.maxsize, datum)
        if len(datum) > len('eejj-mm-dd hh:mm:ss'):  # 18:
            datum = datum[:19]
        listbox.SetItem(index, 0, f"{datum} - {text}")
        listbox.SetItemData(index, idx)

    def set_list_callbacks(self, listbox, callback0, callback1):
        """bind or unbind depending on user's permissions

        callback1 geeft het geactiveerde item mee en kan hier niet gebruikt worden
        """
        if self.appbase.is_user:
            self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, callback0, listbox)
            listbox.Bind(wx.EVT_LEFT_UP, callback0)
        else:
            self.Unbind(wx.EVT_LIST_ITEM_ACTIVATED, listbox)
            listbox.Unbind(wx.EVT_LEFT_UP)

    def set_listitem_text(self, listbox, itemindex, text):
        "set text for the given listitem"
        listbox.SetItemText(itemindex, text)

    def set_listitem_data(self, listbox, itemindex):
        "set the given listitem's data"
        listbox.SetItemData(itemindex, itemindex - 1)

    def get_listitem_text(self, listbox, itemindex):
        "return the indicated listitem's text"
        return listbox.GetItemText(itemindex, 0)

    def get_list_row(self, listbox):
        "return the event list's selected row index"
        return listbox.GetFirstSelected()  # currentRow()

    def set_list_row(self, listbox, num):
        "set the event list's row selection"
        listbox.Select(num)  # setCurrentRow(num)

    def get_list_rowcount(self, listbox):
        "return the number of rows in the event list (minus the top one)"
        return listbox.GetItemCount()

    def clear_textfield(self, textbox):
        "empty textfield context"
        textbox.Clear()

    def get_textfield_contents(self, textbox):
        "return contents of text area"
        return textbox.get_contents()

    def set_textfield_contents(self, textbox, text):
        "set contents of textarea"
        textbox.set_contents(text)

    def move_cursor_to_end(self, textbox):
        "position the cursor at the end of the text"
        textbox.MoveEnd()

    def convert_text(self, textbox, text, to):
        """convert plain text to html or back and return the result

        `to` should be "html" or "plain"
        """
        retval = ''
        if to == 'rich':
            textbox.set_contents(text)
            retval = textbox.get_contents()
        elif to == 'plain':
            retval = text  # text.GetValue()
        return retval


class EasyPrinter(wx.html.HtmlEasyPrinting):
    "class om printen via html layout mogelijk te maken"
    def __init__(self):
        wx.html.HtmlEasyPrinting.__init__(self)

    def print(self, text, doc_name):
        "het daadwerkelijke printen"
        self.SetHeader(doc_name)
        self.PreviewText(text)


class SortOptionsDialogGui(wx.Dialog):
    "dialoog om de sorteer opties in te stellen"
    def __init__(self, master, parent, title):
        # self.parent = parent
        self.master = master
        # wx.Dialog.__init__(self, parent.gui, title=title,
        super().__init__(parent.gui, title=title, pos=wx.DefaultPosition,
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid = wx.GridBagSizer(2, 2)
        self.sizer.Add(self.grid, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.row = 0
        # misschien moet dit pas aan het eind van het scherm opbouwen
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.Fit(self)

    def add_checkbox_line(self, tekst, checked, callback):
        "add a line with a checkbox to the grid (full width)"
        cb = wx.CheckBox(self, label=tekst)
        cb.Bind(wx.EVT_CHECKBOX, self.enable_fields)
        self.grid.Add(cb, (self.row, 0), (1, 4))
        self.grid.AddGrowableCol(1)
        return cb

    def add_seqnumtext_to_list(self, label):
        "put a sequwnce number on the current line"
        self.row += 1
        lbl = wx.StaticText(self, label=f" {self.row}.")
        self.grid.Add(lbl, (self.row, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        return lbl

    def add_colnameselector_to_list(self, name, lijst):
        "add a combobox to the current line"
        cmb = wx.ComboBox(self, size=(90, -1), choices=lijst, style=wx.CB_DROPDOWN)
        cmb.SetSelection(0)
        self.grid.Add(cmb, (self.row, 1))
        return cmb

    def add_radiobuttons_to_line(self, buttondefs):
        """add a radiobutton to the current line

        also add it to the buttongroup that is created with the first button
        """
        col = 1
        buttons = []
        for text, direction_id, checked in buttondefs:
            # direction_id wordt in de wx variant niet gebruikt
            if col == 1:
                rb = wx.RadioButton(self, label=text, style=wx.RB_GROUP)
            else:
                rb = wx.RadioButton(self, label=text)
            rb.SetValue(checked)
            col += 1
            self.grid.Add(rb, (self.row, col), flag=wx.ALIGN_CENTER_VERTICAL)
            buttons.append(rb)
        return buttons

    def add_okcancel_buttonbox(self):
        "add the action buttons to the bottom of the dialog"
        # btnsizer = wx.StdDialogButtonSizer()
        # btn = wx.Button(self, wx.ID_OK)
        # # hoe map je dit ook weer naar een eigen callback?
        # # dat hoeft niet omdat je het resultaat uitvraagt tijdens de showmodal afhandeling
        # btn.SetDefault()
        # btnsizer.AddButton(btn)
        # btn = wx.Button(self, wx.ID_CANCEL)
        # btnsizer.AddButton(btn)
        # btnsizer.Realize()
        # self.sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL),
                       0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

    def enable_fields(self, event):
        "enable/disable widgets"
        # state = self.on_off.GetValue()
        state = event.GetEventWidget().GetValue()
        for lbl, cmb, rbg in self.parent.widgets:
            lbl.Enable(state)
            cmb.Enable(state)
            rbg[0].Enable(state)
            rbg[1].Enable(state)

    def accept(self):
        """sorteerkolommen en -volgordes teruggeven aan hoofdscherm
        """
        return self.master.confirm()

    def get_combobox_value(self, cmb):
        "return the selected value of a combobox"
        return cmb.GetStringSelection()

    def get_rbgroup_value(self, rbg):
        "return the id of teh checked button in a radiobutton group"
        for ix, rb in enumerate(rbg):
            if rb.GetValue():
                return ix + 1

    def get_checkbox_value(self, cb):
        "return the state of a checkbox"
        return cb.IsChecked()


class SelectOptionsDialogGui(wx.Dialog):
    """dialoog om de selectie op te geven
    """
    def __init__(self, master, parent, title):
        self.master = master
        # self.datatype = self.parent.parent.parent.datatype
        # wx.Dialog.__init__(self, parent.gui, -1, title="Selecteren",
        super().__init__(parent.gui, title="Selecteren",
                         ## size=(250,  250),  pos=wx.DefaultPosition,
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid = wx.FlexGridSizer(2, 2, 2)  # cols, hgap, vgap
        self.sizer.Add(self.grid)

    def add_checkbox_to_grid(self, title, row, col):
        "set up a checkbox on the left hand side, for a search option"
        cb = wx.CheckBox(self, label=title)
        self.grid.Add(cb, 0, wx.TOP, 10)
        return cb

    def start_optionsblock(self):
        "set up space on the right hand size to specify search criteria"
        box = wx.FlexGridSizer(2, 2, 2)
        return box

    def add_textentry_line_to_block(self, block, labeltext, callback, first=False):
        "add a caption and a text entry field to the block"
        lbl = wx.StaticText(self, label=labeltext, size=(90, -1))
        text = wx.TextCtrl(self, value="", size=(153, -1))
        self.Bind(wx.EVT_TEXT, callback, text)
        flag = wx.TOP if first else wx.TOP | wx.BOTTOM
        block.AddMany([(lbl, 0, flag, 10), (text, 0, flag, 5)])
        return text

    def add_radiobuttonrow_to_block(self, block, buttondefs, callback=None, alignleft=True):
        "add a row of radiobuttons to the block"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        rb1 = wx.RadioButton(self, label=buttondefs[0], style=wx.RB_GROUP)
        if callback:
            self.Bind(wx.EVT_RADIOBUTTON, callback, rb1)
        hbox.Add(rb1, 0, wx.ALIGN_CENTER_VERTICAL)
        rb2 = wx.RadioButton(self, label=buttondefs[1])
        if callback:
            self.Bind(wx.EVT_RADIOBUTTON, callback, rb2)
        hbox.Add(rb2, 0, wx.ALIGN_CENTER_VERTICAL)
        if alignleft:
            spacer = wx.StaticText(self, label="", size=(70, -1))
            block.AddMany([(hbox, 0), (spacer, 0)])
            self.lbl = spacer  # alleen voor unittest
        else:
            block.Add(hbox, 0, wx.TOP, 10)
        return rb1, rb2

    def add_checkboxlist_to_block(self, block, namelist, callback):
        "add a caption and a list of checkboxes to the block"
        clb = wx.CheckListBox(self, size=(-1, 120), choices=namelist)
        self.Bind(wx.EVT_CHECKLISTBOX, callback, clb)
        lbl = wx.StaticText(self, label="selecteer\neen of meer:", size=(70, -1))
        block.Add(lbl, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 5)
        block.Add(clb, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 5)
        return clb

    def finish_block(self, block, row, col):
        "finish the block layout"
        self.grid.Add(block, row, col)

    # def add_oms_stuff(self):
    #     boxv_text = wx.BoxSizer(wx.VERTICAL)
    #     box_text = wx.BoxSizer(wx.HORIZONTAL)
    #     if self.parent.parent.parent.use_separate_subject:
    #         self.cb_text = wx.CheckBox(self, label='zoek in    -')
    #         self.t_text = wx.TextCtrl(self, value="", size=(153, -1))
    #         self.Bind(wx.EVT_TEXT, self.on_text, self.t_text)
    #         self.rb_and_2 = wx.RadioButton(self, label="en", style=wx.RB_GROUP)
    #         self.rb_or_2 = wx.RadioButton(self, label="of")
    #         self.t_text_2 = wx.TextCtrl(self, value="", size=(153, -1))
    #         self.Bind(wx.EVT_TEXT, self.on_text, self.t_text_2)
    #         box_text.Add(wx.StaticText(self, label=self.parent.parent.ctitels[4] + ':',
    #                                    size=(70, -1)), 0,
    #                      wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 10)
    #         box_text.Add(self.t_text, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 5)
    #         boxv_text.Add(box_text, 0)
    #         box_text = wx.BoxSizer(wx.HORIZONTAL)
    #         box_text.Add(self.rb_and_2, 0, wx.ALIGN_CENTER_HORIZONTAL)
    #         box_text.Add(self.rb_or_2, 0, wx.ALIGN_CENTER_HORIZONTAL)
    #         boxv_text.Add(box_text, 0)
    #         box_text.Add(wx.StaticText(self, label=self.parent.parent.ctitels[5] + ':',
    #                                    size=(70, -1)), 0,
    #                      wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 10)
    #         box_text.Add(self.t_text_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 5)
    #     else:
    #         self.cb_text = wx.CheckBox(self, label=parent.parent.ctitels[4].join((" ", " -")))
    #         self.t_text = wx.TextCtrl(self, value="", size=(153, -1))
    #         self.Bind(wx.EVT_TEXT, self.on_text, self.t_text)
    #         box_text.Add(wx.StaticText(self, label="zoek naar:", size=(70, -1)), 0,
    #                      wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 10)
    #         box_text.Add(self.t_text, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 5)
    #     boxv_text.Add(box_text, 0)

    # def add_arch_radiobutton_line(self):
    #     box_arch = wx.BoxSizer(wx.HORIZONTAL)
    #     self.cb_arch = wx.CheckBox(self, label="Archief")
    #     self.rb_aonly = wx.RadioButton(self, label="Alleen gearchiveerd", style=wx.RB_GROUP)
    #     self.Bind(wx.EVT_RADIOBUTTON, self.on_rightclick, self.rb_aonly)
    #     self.rb_aboth = wx.RadioButton(self, label="gearchiveerd en lopend")
    #     self.Bind(wx.EVT_RADIOBUTTON, self.on_rightclick, self.rb_aboth)
    #     box_arch.Add(self.rb_aboth, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)
    #     box_arch.Add(self.rb_aonly, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)
    #     grid.AddMany([, (box_actie, 0, wx.EXPAND | wx.TOP, 3),
    #                   (self.cb_soort, 0, wx.TOP, 5), (box_soort, 0, wx.EXPAND | wx.TOP, 3),
    #                   (self.cb_stat, 0, wx.TOP, 5), (box_stat, 0, wx.EXPAND | wx.TOP, 3),
    #                   (self.cb_text, 0, wx.TOP, 10), (boxv_text, 0, wx.EXPAND | wx.TOP, 3),
    #                   (self.cb_arch, 0, wx.TOP, 10), (box_arch, 0, wx.EXPAND)])
    #     grid.AddGrowableCol(1)
    #     sizer.Add(grid, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

    def add_okcancel_buttonbar(self):
        "add action buttons to the dialog"
        # btnsizer = wx.StdDialogButtonSizer()
        # btn = wx.Button(self, wx.ID_OK)
        # btn.SetDefault()
        # btnsizer.AddButton(btn)
        # btn = wx.Button(self, wx.ID_CANCEL)
        # btnsizer.AddButton(btn)
        # btnsizer.Realize()
        # sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL),
                       0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

    def finalize_display(self):
        "final actions to realize the screen"
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.Fit(self)

    def set_textentry_value(self, textentry, value):
        "set the value of a text entry box"
        textentry.SetValue(value)

    def set_radiobutton_value(self, radiobutton, value):
        "check or uncheck a radiobutton"
        radiobutton.SetValue(value)

    def set_checkbox_value(self, checkbox, value):
        "check or ncheck a checkbox"
        checkbox.SetValue(value)

    # def set_default_values(self, sel_args):
    #     """get search settings and present them in the dialog
    #     """

    def on_text(self, evt):
        "callback voor EVT_TEXT"
        obj = evt.GetEventObject()
        if obj in (self.master.text_gt, self.master.text_lt):
            target = self.master.cb_actie
        elif obj in (self.master.text_zoek, self.master.text_zoek2):
            target = self.master.cb_text
        if evt.GetString() == "":
            target.SetValue(False)
        else:
            target.SetValue(True)
        return target   # alleen t.b.v. unittest

    def on_cb_checked(self, evt):
        "callback voor EVT_CHECK / EVT_RADIO"
        index = evt.GetSelection()
        obj = evt.GetEventObject()
        obj.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
        if obj == self.master.clb_soort:
            target = self.master.cb_soort
        elif obj == self.master.clb_stat:
            target = self.master.cb_status
        oneormore = False
        for i in range(obj.GetCount()):
            if obj.IsChecked(i):
                oneormore = True
                break
        if oneormore:
            target.SetValue(True)
        else:
            target.SetValue(False)
        return target  # alleen t.b.v. unittest

    def on_rb_checked(self, evt=None):
        "callback voor EVT_RADIO - alleen bij archiefselectie"
        # obj = evt.GetEventObject()
        self.master.cb_arch.SetValue(True)

    def accept(self):  # set_options(self, evt=None):
        "aangegeven opties verwerken in sel_args dictionary"
        return self.master.confirm()

    def get_textentry_value(self, textentry):
        "return the value of a text entry box"
        return textentry.GetValue()

    def get_radiobutton_value(self, radiobutton):
        "return the state of a radiobutton"
        return radiobutton.GetValue()

    def get_checkbox_value(self, checkbox):
        "return the state of a checkbox"
        return checkbox.IsChecked()

    def set_focus_to(self, widget):
        "set the input focus to the specified widget"
        widget.SetFocus()


class SettOptionsDialogGui(wx.Dialog):
    """generic dialog to maintain options

    the specific type of option(s) is passed in via the cls argument
    """
    def __init__(self, master, parent, title):  # args):
        self.master = master
        super().__init__(parent.gui, title=title, size=(300, 300))
        self.sizer = wx.BoxSizer(wx.VERTICAL)

    def add_listbox_with_buttons(self, titel, data, actions):
        """maak een listbox waarvan de items aangepast kunnen worden
        met een rij buttons eronder
        wx heeft hiervoor een dedicated widget
        """
        options = wx.adv.EL_ALLOW_EDIT
        if actions.get('can_add_remove', False):
            options |= wx.adv.EL_ALLOW_NEW | wx.adv.EL_ALLOW_DELETE
        # setup_accels(self, (('edit', self.edit, 'F2'),), [])
        elb = wx.adv.EditableListBox(self, label=titel, pos=(50, 50), size=(250, 250),
                                     style=options)
        elb.SetStrings(data)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(elb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(box, 0, wx.ALL, 5)
        return elb

    def add_label(self, infotext):
        "add some explanatory text to the display"
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "\n".join(infotext))
        box.Add(label, 0, wx.ALL, 5)
        self.sizer.Add(box, 0, wx.GROW | wx.ALL, 5)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        self.sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)

    def add_okcancel_buttonbox(self):
        "add action buttons to confirm or discard the dialog"
        # btnsizer = wx.StdDialogButtonSizer()
        # btn = wx.Button(self, wx.ID_OK)
        # btn.SetDefault()
        # btnsizer.AddButton(btn)
        # btn = wx.Button(self, wx.ID_CANCEL)
        # btnsizer.AddButton(btn)
        # btnsizer.Realize()
        # self.sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL), 0, wx.ALL, 5)

    def finish_display(self):
        "final actions before displaying the screen"
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.Fit(self)

    # geen idee of dit ooit gewerkt heeft
    # def edit(self, event):
    #     "edit a line"
    #     # hopefully simulating pressing the edit button works
    #     # btn = self.elb.GetEditButton()
    #     # btn.Command(wx.CommandEvent(wx.EVT_BUTTON)) nou dit werkt in elk geval niet

    def accept(self):
        """Confirm changes to parent window
        """
        self.master.confirm()

    def read_listbox_data(self, elb):
        "return the updated listbox items"
        return elb.GetStrings()


class LoginBoxGui(wx.Dialog):
    """Sign in with userid & password
    """
    def __init__(self, master, parent):
        self.master = master
        super().__init__(parent.gui)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.grid = wx.GridBagSizer()
        self.vbox.Add(self.grid, 0, wx.ALL, 4)
        self.row = -1

    def add_textinput_line(self, text, hide=False):
        "add a line with some text and an input field to the display"
        self.row += 1
        lbl = wx.StaticText(self, label='Userid')
        self.grid.Add(lbl, (self.row, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        if hide:
            textfield = wx.TextCtrl(self, size=(120, -1), style=wx.TE_PASSWORD)
        else:
            textfield = wx.TextCtrl(self, size=(120, -1))
        self.grid.Add(textfield, (self.row, 1), flag=wx.LEFT, border=2)
        return textfield

    def add_okcancel_buttonbox(self):
        "add action buttons to confirm or dismiss the dialog"
        # bbox = wx.BoxSizer(wx.HORIZONTAL)
        # b_ok = wx.Button(self, id=wx.ID_OK)
        # b_cancel = wx.Button(self, id=wx.ID_CANCEL)
        # bbox.AddMany((b_ok, b_cancel))
        # self.vbox.Add(bbox, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.vbox.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL), 0, wx.ALIGN_CENTER_HORIZONTAL)

    def finish_display(self):
        "final actions before showing"
        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.vbox.Fit(self)
        # vbox.SetSizeHints(self)

    def accept(self):
        "exchange dialog data"
        self.master.confirm()

    def get_textinput_value(self, field):
        "return the value of a text input field"
        return field.GetValue()
