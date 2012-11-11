#! usr/bin/env python
# -*- coding: UTF-8 -*-
"""Actie (was: problemen) Registratie, GUI versie
"""

import sys, os
LIN = True if os.name == 'posix' else False
from datetime import datetime
import pprint
import wx
import wx.html as html
import wx.lib.mixins.listctrl  as  listmix
import wx.gizmos   as  gizmos
import images
import pr_globals as pr
from dml_sql import DataError, get_acties, Actie, Settings
from config_sql import APPS

def get_dts():
    "routine om een geformatteerd date/time stamp te verkrijgen"
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    "list control mixed in with width adapter"
    def __init__(self, parent, id_, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, id_, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

class Page(wx.Panel):
    "base class for notebook page"
    def __init__(self, parent, id_, wants_chars = True):
        self.parent = parent
        if wants_chars:
            wx.Panel.__init__(self, parent, id_, style=wx.WANTS_CHARS)
        else:
            wx.Panel.__init__(self, parent, id_)
            return
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        high = 330 if LIN else 430
        self.text1 = wx.TextCtrl(self, -1, size=(490, high),
                                style=wx.TE_MULTILINE
                                | wx.TE_PROCESS_TAB
                                | wx.TE_RICH2
                                | wx.TE_WORDWRAP
                                )
        self.text1.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_TEXT, self.on_text, self.text1)
        self.save_button = wx.Button(self, -1, 'Sla wijzigingen op (Ctrl-S)')
        self.Bind(wx.EVT_BUTTON, self.savep, self.save_button)
        self.saveandgo_button = wx.Button(self, -1, 'Sla op en ga verder (Ctrl-G)')
        self.Bind(wx.EVT_BUTTON, self.savepgo, self.saveandgo_button)
        self.cancel_button = wx.Button(self, -1, 'Zet originele tekst terug (Ctrl-Z)')
        self.Bind(wx.EVT_BUTTON, self.restorep, self.cancel_button)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)

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

    def vulp(self, evt = None):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        self.initializing = True
        self.enable_buttons(False)
        if self.parent.current_tab == 0:
            text = self.seltitel
        else:
            text = self.parent.tabs[self.parent.current_tab].split(None,1)
            if self.parent.pagedata:
                text = self.parent.pagedata.id + ' ' + self.parent.pagedata.titel
        self.parent.parent.SetTitle("{} | {}".format(self.parent.parent.title,
            text))
        self.parent.parent.SetStatusText(
            self.parent.pagehelp[self.parent.current_tab])
        if 1 < self.parent.current_tab < 6:
            self.oldbuf = ''
            if self.parent.pagedata is not None:
                if self.parent.current_tab == 2 and self.parent.pagedata.melding:
                    self.oldbuf = self.parent.pagedata.melding
                if self.parent.current_tab == 3 and self.parent.pagedata.oorzaak:
                    self.oldbuf = self.parent.pagedata.oorzaak
                if self.parent.current_tab == 4 and self.parent.pagedata.oplossing:
                    self.oldbuf = self.parent.pagedata.oplossing
                if self.parent.current_tab == 5 and self.parent.pagedata.vervolg:
                    self.oldbuf = self.parent.pagedata.vervolg
                if self.parent.pagedata.arch:
                    self.text1.SetEditable(False)
                else:
                    self.text1.SetEditable(True)
            self.text1.SetValue(self.oldbuf)
        self.initializing = False
        self.parent.checked_for_leaving = True

    def readp(self, pid):
        "lezen van een actie"
        self.parent.pagedata = Actie(self.parent.fnaam, pid)
        self.parent.old_id = self.parent.pagedata.id
        self.parent.newitem = False

    def nieuwp(self, evt = None):
        """voorbereiden opvoeren nieuwe actie"""
        if self.leavep():
            self.parent.pagedata = Actie(self.parent.fnaam, 0)
            self.parent.newitem = True
            if self.parent.current_tab == 1:
                self.vulp() # om de velden leeg te maken
                self.proc_entry.SetFocus()
            else:
                self.goto_page(1, check=False)
        else:
            print "leavep() geeft False: nog niet klaar met huidige pagina"

    def leavep(self):
        "afsluitende acties uit te voeren alvorens de pagina te verlaten"
        if self.parent.current_tab == 1:
            newbuf = (self.proc_entry.GetValue(), self.desc_entry.GetValue(),
                self.stat_choice.GetSelection(), self.cat_choice.GetSelection())
            if self.parent.newitem and newbuf[0] == "" and newbuf[1] == "" \
                and not self.parent.parent.exiting:
                self.parent.newitem = False
                self.parent.pagedata = Actie(self.parent.fnaam, self.parent.old_id)
        elif self.parent.current_tab == 6:
            newbuf = (self.event_list, self.event_data)
        elif self.parent.current_tab > 1:
            newbuf = self.text1.GetValue()
        ok_to_leave = True
        self.parent.checked_for_leaving = True
        if self.parent.current_tab > 0 and newbuf != self.oldbuf:
            dlg = wx.MessageDialog(self, "\n".join((
                "De gegevens op de pagina zijn gewijzigd, ",
                "wilt u de wijzigingen opslaan voordat u verder gaat?")),
                self.parent.parent.title,
                wx.YES_NO | wx.CANCEL | wx.ICON_EXCLAMATION
            )
            retval = dlg.ShowModal()
            if retval == wx.ID_YES:
                ok_to_leave = self.savep()
            elif retval == wx.ID_CANCEL:
                self.parent.checked_for_leaving = ok_to_leave = False
            dlg.Destroy()
        return ok_to_leave

    def savep(self, evt = None):
        "gegevens van een actie opslaan afhankelijk van pagina"
        self.enable_buttons(False)
        if self.parent.current_tab <= 1 or self.parent.current_tab == 6:
            return
        wijzig = False
        text = self.text1.GetValue()
        if self.parent.current_tab == 2 and text != self.parent.pagedata.melding:
            self.oldbuf = self.parent.pagedata.melding = text
            self.parent.pagedata.events.append((get_dts(),"Meldingtekst aangepast"))
            wijzig = True
        if self.parent.current_tab == 3 and text != self.parent.pagedata.oorzaak:
            self.oldbuf = self.parent.pagedata.oorzaak = text
            self.parent.pagedata.events.append((get_dts(),"Beschrijving oorzaak aangepast"))
            wijzig = True
        if self.parent.current_tab == 4 and text != self.parent.pagedata.oplossing:
            self.oldbuf = self.parent.pagedata.oplossing = text
            self.parent.pagedata.events.append((get_dts(),"Beschrijving oplossing aangepast"))
            wijzig = True
        if self.parent.current_tab == 5 and text != self.parent.pagedata.vervolg:
            self.oldbuf = self.parent.pagedata.vervolg = text
            self.parent.pagedata.events.append((get_dts(),"Tekst vervolgactie aangepast"))
            wijzig = True
        if wijzig:
            self.update_actie()
        try:
            self.parent.page0.p0list.SetStringItem(self.parent.current_item, 4,
                self.parent.pagedata.updated) # bijwerken in panel 0
        except wx._core.PyAssertionError:
            pass
        return True

    def savepgo(self, evt = None):
        "opslaan en naar de volgende pagina"
        if self.savep():
            self.goto_next()
        else:
            self.enable_buttons()

    def restorep(self, evt = None):
        "oorspronkelijke (laatst opgeslagen) inhoud van de pagina herstellen"
        self.vulp()

    def on_key(self, evt):
        "callback voor EVT_KEYUP"
        keycode = evt.GetKeyCode()
        togo = keycode - 48
        if evt.GetModifiers() == wx.MOD_ALT: # evt.AltDown()
            if keycode == wx.WXK_LEFT or keycode == wx.WXK_NUMPAD_LEFT: #  keycode == 314
                self.goto_prev()
            elif keycode == wx.WXK_RIGHT or keycode == wx.WXK_NUMPAD_RIGHT: #  keycode == 316
                self.goto_next()
            elif togo >= 0 and togo <= self.parent.pages: # Alt-0 t/m Alt-6
                if togo != self.parent.current_tab:
                    self.goto_page(togo)
            elif keycode == 83: # Alt-S
                if self.parent.current_tab == 0:
                    self.sort()
            elif keycode == 70: # Alt-F
                if self.parent.current_tab == 0:
                    self.select()
            elif keycode == 71: # Alt-G
                if self.parent.current_tab == 0:
                    self.goto_actie()
            elif keycode == 78: # Alt-N
                self.nieuwp()
            else:
                evt.Skip()
        elif evt.GetModifiers() == wx.MOD_CONTROL: # evt.ControlDown()
            if keycode == 81: # Ctrl-Q
                self.parent.parent.exit_app()
            elif keycode == 80: # Ctrl-P
                self.print_(evt)
            elif keycode == 79: # Ctrl-O
                self.parent.parent.open_file(evt)
            elif keycode == 78: # Ctrl-N
                self.parent.parent.new_file(evt)
            elif keycode == 72: # Ctrl-H
                self.parent.parent.hotkey_help(evt)
                ## self.parent.parent.hotkey_settings(evt)
            elif keycode == 83: # Ctrl-S
                if self.parent.current_tab > 0:
                    if self.save_button.IsEnabled():
                        self.savep()
            elif keycode == 71: # Ctrl-G
                if self.parent.current_tab > 0:
                    if self.saveandgo_button.IsEnabled():
                        self.savepgo()
            elif keycode == 90: # Ctrl-Z
                if self.parent.current_tab > 0:
                    if self.cancel_button.IsEnabled():
                        self.restorep()
            else:
                evt.Skip()
        elif keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:# 13 or 372: # Enter
            if self.parent.current_tab == 0:
                self.goto_next()
            else:
                evt.Skip()
        else:
            evt.Skip()

    def on_text(self, evt):
        """callback voor EVT_TEXT

        de initializing flag wordt uitgevraagd omdat deze event ook tijdens vulp()
        plaatsvindt"""
        if not self.initializing:
            self.enable_buttons()

    def on_choice(self, evt):
        "callback voor EVT_COMBOBOX"
        self.enable_buttons()

    def update_actie(self):
        ## self.parent.pagedata.list() # NB element 0 is leeg
        self.parent.pagedata.write()
        self.checked_for_leaving = True
        self.mag_weg = True
        self.parent.pagedata.read()    # om "updated" attribuut op te halen

    def enable_buttons(self, state = True):
        "buttons wel of niet klikbaar maken"
        if state:
            self.parent.checked_for_leaving = False
        self.save_button.Enable(state)
        self.saveandgo_button.Enable(state)
        self.cancel_button.Enable(state)

    def goto_actie(self, evt = None):
        "naar startpagina actie gaan"
        self.goto_page(1)

    def goto_next(self):
        "naar de volgende pagina gaan"
        if not self.leavep():
            return
        if self.parent.current_tab < self.parent.pages:
            self.parent.AdvanceSelection()
        else:
            self.parent.SetSelection(0)

    def goto_prev(self):
        "naar de vorige pagina gaan"
        if not self.leavep():
            return
        if self.parent.current_tab > 0:
            self.parent.AdvanceSelection(False)
        else:
            self.parent.SetSelection(6)

    def goto_page(self, page_num, check=True):
        "naar de aangegeven pagina gaan"
        if check and not self.leavep():
            return
        if 0 <= page_num <= self.parent.pages:
            self.parent.SetSelection(page_num)

    def print_(self, evt):
        """callback voor ctrl-P(rint)

        vraag om printen scherm of actie, bv. met een radioboxdialog -
        nou die hebben we niet dat wordt een SingleChoiceDialog"""
        dlg = wx.SingleChoiceDialog(self, 'Wat wil je afdrukken', 'Vraagje',
            ['huidig scherm', 'huidige actie'],wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            if dlg.GetSelection() == 0:
                self.parent.parent.print_scherm(evt)
            else:
                self.parent.parent.print_actie(evt)

class Page0(Page, listmix.ColumnSorterMixin):
    "pagina 0: overzicht acties"
    def __init__(self, parent, id_):
        self.parent = parent
        Page.__init__(self, parent, id_, False)
        self.selection = 'excl. gearchiveerde'
        self.sel_args = {}
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        self.imglist = wx.ImageList(16, 16)

        self.idx1 = self.imglist.Add(images.getPtBitmap())
        self.up_arrow = self.imglist.Add(images.getSmallUpArrowBitmap())
        self.down_arrow = self.imglist.Add(images.getSmallDnArrowBitmap())

        self.p0list = MyListCtrl(self, -1, style = wx.LC_REPORT |
                                                   wx.BORDER_SUNKEN |
                                                   wx.LC_SINGLE_SEL)
        ## high = 400 if LIN else 444
        ## self.p0list.SetMinSize((440,high))

        self.p0list.SetImageList(self.imglist, wx.IMAGE_LIST_SMALL)

        self.populate_list()

        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        self.itemDataMap = self.parent.data
        listmix.ColumnSorterMixin.__init__(self, 7)
        self.SortListItems(1) #, True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select_item, self.p0list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_activate_item, self.p0list)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.on_column_clicked, self.p0list)
        self.p0list.Bind(wx.EVT_LEFT_DCLICK, self.on_doubleclick)
        self.p0list.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.sort_button = wx.Button(self, pr.ID_SORT, 'S&Orteer')
        self.filter_button = wx.Button(self, pr.ID_ZOEK, 'F&Ilter')
        self.go_button = wx.Button(self, pr.ID_GANAAR, '&Ga naar melding')
        self.archive_button = wx.Button(self, pr.ID_ARCH, '&Archiveer')
        self.new_button = wx.Button(self, pr.ID_MELD, 'Voer &Nieuwe melding op')
        self.Bind(wx.EVT_BUTTON, self.sort, self.sort_button)
        self.Bind(wx.EVT_BUTTON, self.select, self.filter_button)
        self.Bind(wx.EVT_BUTTON, self.goto_actie, self.go_button)
        self.Bind(wx.EVT_BUTTON, self.archiveer, self.archive_button)
        self.Bind(wx.EVT_BUTTON, self.nieuwp, self.new_button)

    def doelayout(self):
        "layout page"
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.p0list, 1, wx.EXPAND, 0)
        sizer0.Add(sizer1, 1, wx.EXPAND, 0)
        sizer2.Add(self.sort_button, 0,  wx.ALL, 3)
        sizer2.Add(self.filter_button, 0,  wx.ALL, 3)
        sizer2.Add(self.go_button, 0, wx.ALL, 3)
        sizer2.Add(self.archive_button, 0, wx.ALL, 3)
        sizer2.Add(self.new_button, 0, wx.ALL, 3)
        sizer0.Add(sizer2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer0)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)

    ## def leavep(self):
        ## "afsluitende acties uit te voeren alvorens de pagina te verlaten"
        ## return True # niks doen, doorgaan

    def vulp(self, evt = None):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        self.seltitel = 'alle meldingen ' + self.selection
        Page.vulp(self)
        if self.parent.rereadlist:
            self.parent.data = {}
            select = self.sel_args.copy()
            arch = ""
            if "arch" in select:
                arch = select.pop("arch")
            try:
                data = get_acties(self.parent.fnaam, select, arch)
            except DataError as msg:
                print "samenstellen lijst mislukt: " + str(msg)
                ## raise(msg)
            else:
                for idx, item in enumerate(data):
                    nummer, start, stat_title, stat_value, cat_title, cat_value, \
                    about, titel, gewijzigd = item
                    self.parent.data[idx] = (nummer, start, ".".join((cat_value, cat_title)), \
                        ".".join((str(stat_value), stat_title)), gewijzigd, about, titel)
            self.populate_list()
            if self.parent.sorter is not None:
                self.p0list.SortItems(self.parent.sorter)
            self.parent.rereadlist = False
        self.parent.parent.SetStatusText("{0} - {1} items".format(
            self.parent.pagehelp[self.parent.current_tab], len(self.parent.data)))
        self.p0list.Select(self.parent.current_item)
        self.p0list.EnsureVisible(self.parent.current_item)

    def populate_list(self):
        "list control vullen"
        self.p0list.DeleteAllItems()
        self.p0list.DeleteAllColumns()
        self.itemDataMap = self.parent.data

        # Adding columns with width and images on the column header
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT | wx.LIST_MASK_WIDTH
        info.m_format = 0
        info.m_width = 0
        info.m_text = ""
        self.p0list.InsertColumnInfo(0, info)

        info.m_width = 84 if LIN else 64
        info.m_text = self.parent.ctitels[0]
        self.p0list.InsertColumnInfo(1, info)

        info.m_width = 24
        info.m_text = self.parent.ctitels[1]
        self.p0list.InsertColumnInfo(2, info)

        info.m_width = 146 if LIN else 114
        info.m_text = self.parent.ctitels[2]
        self.p0list.InsertColumnInfo(3, info)

        info.m_width = 90 if LIN else 72
        info.m_text = self.parent.ctitels[3]
        self.p0list.InsertColumnInfo(4, info)

        info.m_width = 90 if LIN else 72
        info.m_text = self.parent.ctitels[4]
        self.p0list.InsertColumnInfo(5, info)

        info.m_width = 310 if LIN else 220
        info.m_text = self.parent.ctitels[5]
        self.p0list.InsertColumnInfo(6, info)

        self.parent.rereadlist = False
        items = self.parent.data.items()
        if items is None or len(items) == 0:
            print "no items to show?"
            return

        for key, data in items:
            actie, _, soort, status, l_wijz, over, titel = data
            idx = self.p0list.InsertStringItem(sys.maxint, actie)
            self.p0list.SetStringItem(idx, 1, actie)
            pos = soort.index(".") + 1
            self.p0list.SetStringItem(idx, 2, soort[pos:pos+1].upper())
            pos = status.index(".") + 1
            self.p0list.SetStringItem(idx, 3, status[pos:])
            self.p0list.SetStringItem(idx, 4, l_wijz[:19])
            self.p0list.SetStringItem(idx, 5, over)
            self.p0list.SetStringItem(idx, 6, titel)
            self.p0list.SetItemData(idx, key)
        self.colorize()

    def GetListCtrl(self):
        "methode tbv correcte werking sorteer mixin"
        return self.p0list

    def GetSortImages(self):
        "methode tbv correcte werking sorteer mixin"
        return (self.down_arrow, self.up_arrow)

    def colorize(self):
        """de regels om en om kleuren"""
        kleur = False
        for key in xrange(self.p0list.GetItemCount()):
        ## for key in range(len(self.data.items)):
            if kleur:
                self.p0list.SetItemBackgroundColour(key,
                    wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            else:
                self.p0list.SetItemBackgroundColour(key,
                    wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
            kleur = not kleur

    def on_select_item(self, event):
        "callback voor selectie van item"
        self.parent.current_item = event.m_itemIndex
        seli = self.p0list.GetItemData(self.parent.current_item)
        self.readp(self.parent.data[seli][0])
        hlp = "&Herleef" if self.parent.pagedata.arch else "&Archiveer"
        self.archive_button.SetLabel(hlp)
        event.Skip()

    def on_activate_item(self, event):
        "callback voor activeren van item"
        self.parent.current_item = event.m_itemIndex

    def on_column_clicked(self, event):
        "callback voor klikken op column header"
        self.parent.sorter = self.GetColumnSorter()
        self.colorize() # heeft niet zoveel zin want het sorteren komt hierna pas?
        event.Skip()

    def on_doubleclick(self, event):
        "callback voor dubbelklikken op item"
        self.goto_actie()
        event.Skip()

    def select(self, evt = None):
        """tonen van de selectie dialoog

        niet alleen selecteren op tekst(deel) maar ook op status, soort etc"""
        while True:
            dlg = SelectOptionsDialog(self, self.sel_args)
            test = dlg.ShowModal()
            if test != wx.ID_OK: # Shows it
                break
            self.sel_args = dlg.set_options()
            self.parent.rereadlist = True
            try:
                self.vulp()
            except DataError as msg:
                self.parent.rereadlist = False
                wx.MessageBox(str(msg), "Oeps", wx.OK, parent=self)
            else:
                break
        dlg.Destroy() # finally destroy it when finished.
        self.parent.parent.zetfocus(0)

    def sort(self, evt = None):
        """tonen van de sorteer-opties dialoog

        sortering mogelijk op datum/tijd, soort, titel, status via schermpje met
        2x4 comboboxjes waarin je de volgorde van de rubrieken en de sorteervolgorde
        per rubriek kunt aangeven"""
        ## d = wx.MessageDialog( self, "Sorry, werkt nog niet", "Oeps", wx.OK)
        dlg = SortOptionsDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            wx.MessageBox("Sorry, werkt nog niet", "Oeps", wx.OK)
            # self.colorize() # formerly known as self.AfterSort()
        dlg.Destroy() # finally destroy it when finished.
        self.parent.parent.zetfocus(0)

    def archiveer(self, evt = None):
        "archiveren of herleven van het geselecteerde item"
        print('archiveren op panel 0')
        seli = self.p0list.GetItemData(self.parent.current_item)
        self.readp(self.parent.data[seli][0])
        ## self.parent.pagedata.arch = not self.parent.pagedata.arch
        ## hlp = "gearchiveerd" if self.parent.pagedata.arch else "herleefd"
        ## self.parent.pagedata.events.append((get_dts(), "Actie {0}".format(hlp)))
        self.parent.pagedata.set_arch(not self.parent.pagedata.arch)
        self.parent.pagedata.write()
        self.parent.rereadlist = True
        self.vulp()
        self.parent.parent.zetfocus(0)
        # het navolgende geldt alleen voor de selectie "gearchiveerd en actief"
        if self.sel_args.get("arch", "") == "alles":
            self.p0list.EnsureVisible(seli)
            hlp = "&Herleef" if self.parent.pagedata.arch else "&Archiveer"
            self.archive_button.SetLabel(hlp)

    def enable_buttons(self, state = True):
        "zorgen dat de gelijknamige methode van de base class niet wordt geactiveerd"
        pass

class Page1(Page):
    "pagina 1: startscherm actie"
    def __init__(self, parent, id_):
        Page.__init__(self, parent, id_, False)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        self.id_text = wx.TextCtrl(self, -1, size=(125, -1))
        self.id_text.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.date_text = wx.TextCtrl(self, -1, size=(125, -1))
        self.date_text.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.proc_entry = wx.TextCtrl(self, -1, size=(125, -1))
        self.proc_entry.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_TEXT, self.on_text, self.proc_entry)
        self.desc_entry = wx.TextCtrl(self, -1, size=(360, -1))
        self.desc_entry.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_TEXT, self.on_text, self.desc_entry)

        self.cat_choice = wx.ComboBox(self, -1, size = (180, -1),
            style = wx.CB_DROPDOWN | wx.CB_READONLY
            )
        self.Bind(wx.EVT_TEXT, self.on_text, self.cat_choice)
        self.cat_choice.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.stat_choice = wx.ComboBox(self, -1, size = (140, -1),
            style = wx.CB_DROPDOWN | wx.CB_READONLY
            )
        self.Bind(wx.EVT_TEXT, self.on_text, self.stat_choice)
        self.stat_choice.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.vul_combos()

        self.archive_text = wx.StaticText(self, -1, "")
        ## self.archive_text.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.archive_button = wx.Button(self, -1, "Archiveren")
        self.archive_button.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_BUTTON, self.archiveer, self.archive_button)

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
        sizer1 = wx.GridBagSizer(3, 12) # rows, cols, hgap, vgap
        sizer1.Add(wx.StaticText(self,  -1, "Actie-id:"), (0, 0),
            flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_TOP, border = 10)
        sizer1.Add(self.id_text,  (0, 1), flag = wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self,  -1, "Datum/tijd:"), (1, 0),
            flag = wx.ALL | wx.ALIGN_TOP, border = 10)
        sizer1.Add(self.date_text, (1, 1), flag = wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self,  -1, "Job/\ntransactie:"), (2, 0),
            flag = wx.ALL | wx.ALIGN_TOP, border = 10)
        sizer1.Add(self.proc_entry, (2, 1), flag = wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self,  -1, "Melding/code/\nomschrijving:"), (3, 0),
            flag = wx.ALL | wx.ALIGN_TOP, border = 10)
        sizer1.Add(self.desc_entry, (3, 1), flag = wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self,  -1, "Categorie:"), (4, 0),
            flag = wx.ALL | wx.ALIGN_TOP, border = 10)
        sizer1.Add(self.cat_choice, (4, 1), flag = wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self,  -1, "Status:"), (5, 0),
            flag = wx.ALL | wx.ALIGN_TOP, border = 10)
        sizer1.Add(self.stat_choice, (5, 1), flag = wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(self.archive_text, (6, 1), flag = wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM,
            border = 10)
        sizer1.Add(self.archive_button, (7, 1), flag = wx.ALIGN_CENTER_VERTICAL | wx.TOP,
            border = 5)
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

    def vulp(self, evt=None):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        Page.vulp(self)
        self.initializing = True
        self.id_text.SetValue("")
        self.date_text.SetValue("")
        self.proc_entry.SetValue("")
        self.desc_entry.SetValue("")
        self.archive_text.SetLabel("")
        self.cat_choice.SetSelection(0)
        self.stat_choice.SetSelection(0)
        if self.parent.pagedata is not None: # and not self.parent.newitem:
            self.id_text.SetValue(self.parent.pagedata.id)
            self.date_text.SetValue(self.parent.pagedata.datum)
            self.parch = self.parent.pagedata.arch
            self.proc_entry.SetValue(self.parent.pagedata.over)
            self.desc_entry.SetValue(self.parent.pagedata.titel)
            for x in range(len(self.parent.stats)):
                if self.stat_choice.GetClientData(x) == self.parent.pagedata.status:
                    self.stat_choice.SetSelection(x)
                    break
            for x in range(len(self.parent.cats)):
                if self.cat_choice.GetClientData(x) == self.parent.pagedata.soort:
                    self.cat_choice.SetSelection(x)
                    break
        self.oldbuf = (self.proc_entry.GetValue(), self.desc_entry.GetValue(),
            self.stat_choice.GetSelection(), self.cat_choice.GetSelection())
        ## self.initializing = False # gebeurt al in Page.vulp()?
        if self.parch:
            aanuit = False
            self.archive_text.SetLabel("Deze actie is gearchiveerd")
            self.archive_button.SetLabel("Herleven")
        else:
            aanuit = True
            self.archive_text.SetLabel("")
            self.archive_button.SetLabel("Archiveren")
        self.id_text.Enable(False)
        self.date_text.Enable(False)
        self.proc_entry.Enable(aanuit)
        self.desc_entry.Enable(aanuit)
        self.cat_choice.Enable(aanuit)
        self.stat_choice.Enable(aanuit)
        if self.parent.newitem:
            self.archive_button.Enable(False)
        else:
            self.archive_button.Enable(True)
        self.initializing = False

    def savep(self, evt=None):
        "opslaan van de paginagegevens"
        print('wijzigen op panel 1')
        Page.savep(self)
        proc = self.proc_entry.GetValue()
        ## try:
        proc = proc.capitalize() # [0].upper() + s1[1:]
        self.proc_entry.SetValue(proc)
        self.enable_buttons(False)
        ## except IndexError:
            ## pass
        desc = self.desc_entry.GetValue()
        if proc == "" or desc == "":
            wx.MessageBox("Beide tekstrubrieken moeten worden ingevuld","Oeps")
            return False
        wijzig = False
        if self.parent.newitem:
            self.parent.pagedata.events.append(
                (get_dts(), "Actie opgevoerd"))
        procdesc = " - ".join((proc, desc))
        if procdesc != self.parent.pagedata.titel:
            self.parent.pagedata.over = proc
            self.parent.pagedata.titel = desc
            self.parent.pagedata.events.append(
                (get_dts(), 'Titel gewijzigd in "{0}"'.format(procdesc)))
            wijzig = True
        newstat = self.stat_choice.GetClientData(self.stat_choice.GetSelection())
        print(newstat, type(newstat))
        print(self.parent.pagedata.status, type(self.parent.pagedata.status))
        if newstat != self.parent.pagedata.status:
            self.parent.pagedata.status = newstat
            sel = self.stat_choice.GetStringSelection()
            self.parent.pagedata.events.append(
                (get_dts(), 'Status gewijzigd in "{0}"'.format(sel)))
            wijzig = True
        newcat = self.cat_choice.GetClientData(self.cat_choice.GetSelection())
        print(newcat, type(newcat))
        print(self.parent.pagedata.soort, type(self.parent.pagedata.soort))
        if newcat != self.parent.pagedata.soort:
            self.parent.pagedata.soort = newcat
            sel = self.cat_choice.GetStringSelection()
            self.parent.pagedata.events.append(
                (get_dts(), 'Categorie gewijzigd in "{0}"'.format(sel)))
            wijzig = True
        if self.parch != self.parent.pagedata.arch:
            self.parent.pagedata.set_arch(self.parch)
            hlp = "gearchiveerd" if self.parch else "herleefd"
            self.parent.pagedata.events.append(
                (get_dts(), "Actie {0}".format(hlp)))
            wijzig = True
        if wijzig:
            self.update_actie()
            if self.parent.newitem:
                self.parent.current_item = len(self.parent.data) # + 1
                self.parent.data[self.parent.current_item] = (self.date_text.GetValue(), \
                    " - ".join((self.proc_entry.GetValue(), self.desc_entry.GetValue())), \
                    self.stat_choice.GetSelection(), self.cat_choice.GetSelection(), \
                    self.id_text.GetValue())
                self.parent.newitem = False
                self.parent.rereadlist = True
            try:
                self.parent.page0.p0list.SetStringItem(self.parent.current_item,
                    2, self.parent.pagedata.get_soorttext()) # self.parent.pagedata.soort)[0][0].upper())
            except wx._core.PyAssertionError:
                pass
            try:
                self.parent.page0.p0list.SetStringItem(self.parent.current_item,
                    3, self.parent.pagedata.get_statustext()) # self.parent.pagedata.status)[0])
            except wx._core.PyAssertionError:
                pass
            try:
                self.parent.page0.p0list.SetStringItem(self.parent.current_item,
                    4, self.parent.pagedata.updated)
            except wx._core.PyAssertionError:
                pass
            try:
                self.parent.page0.p0list.SetStringItem(self.parent.current_item,
                    5, self.parent.pagedata.titel)
            except wx._core.PyAssertionError:
                pass
            self.oldbuf = (self.proc_entry.GetValue(), self.desc_entry.GetValue(), \
                self.stat_choice.GetSelection(), self.cat_choice.GetSelection())
        return True

    def archiveer(self, evt=None):
        "archiveren/herleven"
        self.parch = not self.parch
        self.savep()
        self.parent.rereadlist = True
        self.vulp()
        ## self.goto_prev() # waarom? oorspronkelijk zou ik in dit geval terug naar de lijst

    def vul_combos(self):
        "vullen comboboxen"
        self.stat_choice.Clear()
        self.cat_choice.Clear()
        for key in sorted(self.parent.cats.keys()):
            text, value = self.parent.cats[key][:2]
            self.cat_choice.Append(text, value)
        for key in sorted(self.parent.stats.keys()):
            text, value = self.parent.stats[key][:2]
            self.stat_choice.Append(text, value)

class Page6(Page):
    "pagina 6: voortgang"
    def __init__(self, parent, id_):
        Page.__init__(self, parent, id_, False)
        self.current_item = 0
        self.oldtext = ""
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        high = 200 if LIN else 280
        self.pnl = wx.SplitterWindow(self, -1, style = wx.SP_LIVE_UPDATE)

        self.progress_list = MyListCtrl(self.pnl, -1, size=(500, -1), #high),
            style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL)
        self.progress_list.InsertColumn(0,'Momenten')
        high = 100 if LIN else 110
        self.progress_text = wx.TextCtrl(self.pnl, -1, size=(500, -1), #high),
            style=wx.TE_MULTILINE
            ## | wx.TE_PROCESS_TAB
            | wx.TE_RICH2
            | wx.TE_WORDWRAP
            )
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
        Page.vulp(self)
        self.initializing = True
        self.event_list, self.event_data, self.old_list, self.old_data = [], [], [], []
        self.progress_text.Clear()
        self.progress_text.Enable(False) # SetEditable(False)
        if self.parent.pagedata: # and not self.parent.newitem:
            self.event_list = [x[0] for x in self.parent.pagedata.events]
            self.event_list.reverse()
            self.old_list = self.event_list[:]
            self.event_data = [x[1] for x in self.parent.pagedata.events]
            self.event_data.reverse()
            self.old_data = self.event_data[:]
            self.progress_list.DeleteAllItems()
            y = '-- (double)click to add new item --'
            index = self.progress_list.InsertStringItem(sys.maxint, y)
            self.progress_list.SetStringItem(index, 0, y)
            self.progress_list.SetItemData(index, -1)
            for idx, datum in enumerate(self.event_list):
                index = self.progress_list.InsertStringItem(sys.maxint, datum)
                try:
                    text = self.event_data[idx].split("\n")[0].strip()
                except AttributeError:
                    text = self.event_data[idx] or ""
                text = text if len(text) < 80 else text[:80] + "..."
                self.progress_list.SetStringItem(index, 0, "{} - {}".format(datum[:19], text))
                self.progress_list.SetItemData(index, idx)
        ## self.oldbuf = (self.txtStat.GetValue(),self.old_list,self.old_data)
        self.oldbuf = (self.old_list, self.old_data)
        self.oldtext = ''
        self.initializing = False

    def savep(self, evt=None):
        "opslaan van de paginagegevens"
        Page.savep(self)
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
            self.progress_list.SetStringItem(idx + 1, 0,
                "{} - {}".format(self.event_list[idx], short_text))
            self.progress_list.SetItemData(idx + 1, idx)
        ## s1 = self.txtStat.GetValue()
        ## if s1 == "" and len(self.event_list) > 0:
            ## wx.MessageBox("Stand van zaken moet worden ingevuld","Oeps")
            ## return False
        wijzig = False
        ## if s1 != self.parent.pagedata.stand:
            ## self.parent.pagedata.stand = s1
            ## wijzig = True
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
            try:
                self.parent.page0.p0list.SetStringItem(self.parent.current_item,
                    4, self.parent.pagedata.updated) # bijwerken in panel 0
            except wx._core.PyAssertionError:
                pass
            self.old_list = self.event_list[:]
            self.old_data = self.event_data[:]
            ## self.oldbuf = (self.txtStat.GetValue(),self.old_list,self.old_data)
            self.oldbuf = (self.old_list, self.old_data)
        else:
            print "Leuk hoor, er was niks gewijzigd ! @#%&*Grrr"
        return True

    def on_left_release(self, event):
        x = event.GetX()
        y = event.GetY()
        item, flags = self.progress_list.HitTest((x, y))
        tekst = self.progress_list.GetItemText(item) # niet gebruikt
        print "on left release:", item, tekst
        if item == 0:
            hlp = get_dts()
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
        self.current_item = event.m_itemIndex # - 1
        tekst = self.progress_list.GetItemText(self.current_item) # niet gebruikt
        self.progress_text.SetEditable(False)
        if self.current_item == 0:
            self.oldtext = ""
        else:
            self.oldtext = self.event_data[self.current_item - 1]
        self.progress_text.SetValue(self.oldtext)
        self.progress_text.Enable(True)
        self.progress_text.SetFocus()
        #~ event.Skip()

    def on_deselect_item(self, evt):
        "callback voor het niet meer geselecteerd zijn van een item"
        item = evt.GetItem()  # niet gebruikt
        idx = evt.m_itemIndex
        tekst = self.progress_text.GetValue() # self.progress_list.GetItemText(idx)
        if tekst != self.oldtext:
            self.event_data[idx-1] = tekst
            self.oldtext = tekst
            short_text = tekst.split("\n")[0]
            short_text = short_text if len(short_text) < 80 else short_text[:80] + "..."
            self.progress_list.SetStringItem(idx, 0,
                "{} - {}".format(self.event_list[idx - 1], short_text))
            self.progress_list.SetItemData(idx, idx - 1)
        evt.Skip()

    def on_text(self, evt):
        """callback voor EVT_TEXT

        de initializing flag wordt uitgevraagd omdat deze event ook tijdens vulp()
        plaatsvindt"""
        if not self.initializing:
            ## idx = self.current_item # self.progress_list.Selection # niet gebruikt
            tekst = self.progress_text.GetValue() # self.progress_list.GetItemText(ix)
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
    def __init__(self, parent):
        self.parent = parent
        lijst = ["(geen)"]
        for idx, text in enumerate(parent.parent.ctitels):
            if idx == 1:
                lijst.append("Soort")
            else:
                lijst.append(text)
        wid = 600 # if LIN else 450
        hig = 600 # if LIN else 450
        wx.Dialog.__init__(self, parent, -1, title="Sorteren op meer dan 1 kolom",
            size=(wid, hig),
            pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        txt1 = wx.StaticText(self, -1, "  1.", size=(20, -1))
        cmb1 = wx.ComboBox(self, -1, value="(geen)", size=(80, -1),
            choices=lijst, style=wx.CB_DROPDOWN) #|wxTE_PROCESS_ENTER    )
        rb1a = wx.RadioButton(self, -1, " Asc ", style = wx.RB_GROUP )
        rb1b = wx.RadioButton(self, -1, " Desc " )
        txt2 = wx.StaticText(self, -1, "  2.", size=(20, -1))
        cmb2 = wx.ComboBox(self, -1, value="(geen)", size=(80, -1),
            choices=lijst, style=wx.CB_DROPDOWN) #|wxTE_PROCESS_ENTER    )
        rb2a = wx.RadioButton(self, -1, " Asc ", style = wx.RB_GROUP )
        rb2b = wx.RadioButton(self, -1, " Desc " )
        txt3 = wx.StaticText(self, -1, "  3.", size=(20, -1))
        cmb3 = wx.ComboBox(self, -1, value="(geen)", size=(80, -1),
            choices=lijst, style=wx.CB_DROPDOWN) #|wxTE_PROCESS_ENTER    )
        rb3a = wx.RadioButton(self, -1, " Asc ", style = wx.RB_GROUP )
        rb3b = wx.RadioButton(self, -1, " Desc " )
        txt4 = wx.StaticText(self, -1, "  4.", size=(20, -1))
        cmb4 = wx.ComboBox(self, -1, value="(geen)", size=(80, -1),
            choices=lijst, style=wx.CB_DROPDOWN) #|wxTE_PROCESS_ENTER    )
        rb4a = wx.RadioButton(self, -1, " Asc ", style = wx.RB_GROUP )
        rb4b = wx.RadioButton(self, -1, " Desc " )
        sizer = wx.BoxSizer(wx.VERTICAL)

        fgs = wx.FlexGridSizer(4, 4, 2, 2)  # rows, cols, hgap, vgap
        fgs.AddMany([(txt1, 0, wx.TOP, 5), (cmb1, 0, wx.RIGHT, 10),
                     (rb1a, 0, wx.EXPAND), (rb1b, 0, wx.EXPAND | wx.RIGHT, 2),
                     (txt2, 0, wx.TOP, 5), (cmb2, 0, wx.RIGHT, 10),
                     (rb2a, 0, wx.EXPAND), (rb2b, 0, wx.EXPAND | wx.RIGHT, 2),
                     (txt3, 0, wx.TOP, 5), (cmb3, 0, wx.RIGHT, 10),
                     (rb3a, 0, wx.EXPAND), (rb3b, 0, wx.EXPAND | wx.RIGHT, 2),
                     (txt4, 0, wx.TOP, 5), (cmb4, 0, wx.RIGHT, 10),
                     (rb4a, 0, wx.EXPAND), (rb4b, 0, wx.EXPAND | wx.RIGHT, 2)])
        fgs.AddGrowableCol(1)
        sizer.Add(fgs, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)

class SelectOptionsDialog(wx.Dialog):
    """dialoog om de selectie op te geven

    sel_args is de dictionary waarin de filterwaarden zitten, bv:
    {'status': ['probleem'], 'idlt': '2006-0009', 'titel': 'x', 'soort': ['gemeld'],
    'id': 'and', 'idgt': '2005-0019'}"""
    def __init__(self, parent, sel_args):
        self.parent = parent
        wx.Dialog.__init__(self, parent, -1, title="Selecteren",
            ## size=(250,  250),  pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.cb1 = wx.CheckBox(self, -1, parent.parent.ctitels[0].join((" ", " -")))
        label_gt = wx.StaticText(self, -1, "groter dan:", size=(90, -1)) # was 70
        self.t1a = wx.TextCtrl(self, pr.ID_T1A, "", size=(153, -1))
        self.Bind(wx.EVT_TEXT, self.on_text, self.t1a)
        spacer_1 = wx.StaticText(self, -1, "", size=(70, -1))
        self.rb1a = wx.RadioButton(self, -1, "en", style=wx.RB_GROUP)
        self.rb1b = wx.RadioButton(self, -1, "of")
        label_lt = wx.StaticText(self, -1, "kleiner dan:", size=(90, -1)) # was 70
        self.t1b = wx.TextCtrl(self, pr.ID_T1B, "", size=(153, -1))
        self.Bind(wx.EVT_TEXT, self.on_text, self.t1b)
        if "idgt" in sel_args:
            self.t1a.SetValue(sel_args["idgt"])
        if "id" in sel_args:
            if sel_args["id"] == "and":
                self.rb1a.SetValue(True)
            else:
                self.rb1b.SetValue(True)
        if "idlt" in sel_args:
            self.t1b.SetValue(sel_args["idlt"])
        self.cb2 = wx.CheckBox(self, -1, " soort -")
        labelsel = wx.StaticText(self, -1, "selecteer\neen of meer:", size=(70, -1))
        ## h = self.parent.parent.cats.keys()
        ## h.sort()
        self.cl2 = wx.CheckListBox(self, pr.ID_CL2,
            size=(-1,120),
            ## choices=[x[0] for x in [self.parent.parent.cats[y] for y in h]])
            choices = [x[0] for x in [self.parent.parent.cats[y] for y in sorted(
                self.parent.parent.cats.keys())]])
        self.Bind(wx.EVT_CHECKLISTBOX, self.on_checked, self.cl2)
        if "soort" in sel_args:
            for x in self.parent.parent.cats.keys():
                if self.parent.parent.cats[x][2] in sel_args["soort"]:
                    self.cl2.Check(int(x))
            self.cb2.SetValue(True)

        self.cb3 = wx.CheckBox(self, -1, parent.parent.ctitels[2].join((" ", " -")))
        labelsl2 = wx.StaticText(self, -1, "selecteer\neen of meer:", size=(70, -1))
        ## h = self.parent.parent.stats.keys()
        ## h.sort()
        self.cl3 = wx.CheckListBox(self, pr.ID_CL3,
            size=(-1,120),
            ## choices=[x[0] for x in [self.parent.parent.stats[y] for y in h]])
            choices = [x[0] for x in [self.parent.parent.stats[y] for y in sorted(
                self.parent.parent.stats.keys())]])
        self.Bind(wx.EVT_CHECKLISTBOX, self.on_checked, self.cl3)
        if "status" in sel_args:
            for x in self.parent.parent.stats.keys():
                if self.parent.parent.stats[x][2] in sel_args["status"]:
                    self.cl3.Check(int(x))
            self.cb3.SetValue(True)

        self.cb4 = wx.CheckBox(self, -1, parent.parent.ctitels[4].join((" ", " -")))
        label_zk = wx.StaticText(self, -1, "zoek naar:", size=(70, -1))
        self.txt4 = wx.TextCtrl(self, pr.ID_T4, "", size=(153, -1))
        self.Bind(wx.EVT_TEXT, self.on_text, self.txt4)
        if "titel" in sel_args:
            self.txt4.SetValue(sel_args["titel"])
            self.cb4.SetValue(True)
        self.cb5 = wx.CheckBox(self, -1, "Archief")
        self.rb5a = wx.RadioButton(self, pr.ID_RB5A, "Alleen gearchiveerd",
            style=wx.RB_GROUP)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_rightclick, self.rb5a)
        self.rb5b = wx.RadioButton(self, pr.ID_RB5B, "gearchiveerd en lopend")
        self.Bind(wx.EVT_RADIOBUTTON, self.on_rightclick, self.rb5b)
        if "arch" in sel_args:
            self.cb5.SetValue(True)
            if sel_args["arch"] == "arch":
                self.rb5a.SetValue(True)
            if sel_args["arch"] == "alles":
                self.rb5b.SetValue(True)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sz01 = wx.BoxSizer(wx.HORIZONTAL)
        sz01.Add(self.rb1a, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sz01.Add(self.rb1b, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sz1 = wx.FlexGridSizer(2, 2, 2, 2)
        sz1.AddMany([(label_gt, 0, wx.TOP, 10), (self.t1a, 0, wx.TOP, 5),
                     (sz01, 0 ), (spacer_1, 0),
                     (label_lt, 0, wx.TOP|wx.BOTTOM, 5), (self.t1b, 0, wx.BOTTOM, 5)])
        sz2 = wx.BoxSizer(wx.HORIZONTAL)
        sz2.Add(labelsel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5)
        sz2.Add(self.cl2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5)
        sz3 = wx.BoxSizer(wx.HORIZONTAL)
        sz3.Add(labelsl2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5)
        sz3.Add(self.cl3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5)
        sz4 = wx.BoxSizer(wx.HORIZONTAL)
        sz4.Add(label_zk, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 10)
        sz4.Add(self.txt4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5)
        sz5 = wx.BoxSizer(wx.HORIZONTAL)
        sz5.Add(self.rb5a, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 10)
        sz5.Add(self.rb5b, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 10)

        fgs = wx.FlexGridSizer(5, 2, 2, 2)  # rows, cols, hgap, vgap
        fgs.AddMany([(self.cb1, 0, wx.TOP, 10), (sz1, 0, wx.EXPAND|wx.TOP, 3),
                     (self.cb2, 0, wx.TOP, 5),  (sz2, 0, wx.EXPAND|wx.TOP, 3),
                     (self.cb3, 0, wx.TOP, 5),  (sz3, 0, wx.EXPAND|wx.TOP, 3),
                     (self.cb4, 0, wx.TOP, 10), (sz4, 0, wx.EXPAND|wx.TOP, 3),
                     (self.cb5, 0, wx.TOP, 10), (sz5, 0, wx.EXPAND)
                     ])
        fgs.AddGrowableCol(1)
        sizer.Add(fgs, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)

    def on_text(self, evt=None):
        "callback voor EVT_TEXT"
        ## it = evt.GetEventObject() # unused
        idee = evt.GetId()
        if idee == pr.ID_T1A or idee == pr.ID_T1B:
            obj2 = self.cb1
        if idee == pr.ID_T4:
            obj2 = self.cb4
        if evt.GetString() == "":
            obj2.SetValue(False)
        else:
            obj2.SetValue(True)

    def on_checked(self, evt=None):
        "callback voor EVT_CHECK"
        index = evt.GetSelection()
        obj = evt.GetEventObject()
        obj.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
        idee = evt.GetId()
        if idee == pr.ID_CL2:
            obj2 = self.cb2
        if idee == pr.ID_CL3:
            obj2 = self.cb3
        oneormore = False
        for x in range(obj.GetCount()):
            if obj.IsChecked(x):
                oneormore = True
                break
        if oneormore:
            obj2.SetValue(True)
        else:
            obj2.SetValue(False)

    def on_rightclick(self, evt=None):
        "callback voor EVT_RADIO"
        ## obj = evt.GetEventObject()
        idee = evt.GetId()
        if idee == pr.ID_RB5A or idee == pr.ID_RB5B:
            self.cb5.SetValue(True)

    def set_options(self, evt=None):
        "aangegeven opties verwerken in sel_args dictionary"
        selection = 'excl.gearchiveerde'
        sel_args = {}
        if self.cb1.IsChecked(): #  checkbox voor "id"
            selection = '(gefilterd)'
            id_gt, id_lt = self.t1a.GetValue(), self.t1b.GetValue()
            if id_gt:
                sel_args["idgt"] = id_gt
            if id_lt:
                sel_args["idlt"] = id_lt
            if self.rb1a.GetValue():
                sel_args["id"] = "and"
            if self.rb1b.GetValue():
                sel_args["id"] = "or"
        if self.cb2.IsChecked(): #  checkbox voor "soort"
            selection = '(gefilterd)'
            lst = []
            for x in range(len(self.parent.parent.cats.keys())):
                print x,
                if self.cl2.IsChecked(x):
                    print 'is checked;',
                    print self.parent.parent.cats[x],
                    lst.append(self.parent.parent.cats[x][2])
                print
            ## for idx, val in enumerate(self.parent.parent.cats.keys()):
                ## if self.cl2.IsChecked(idx):
                    ## lst.append(val[1])
            ## lst = [self.parent.parent.cats[str(x)][1] for x in range(
                    ## len(self.parent.parent.cats.keys())) if self.cl2.IsChecked(x)]
            if len(lst) > 0:
                sel_args["soort"] = lst
        if self.cb3.IsChecked(): #  checkbox voor "status"
            selection = '(gefilterd)'
            lst = [self.parent.parent.stats[x][2] for x in range(
                    len(self.parent.parent.stats.keys())) if self.cl3.IsChecked(x)]
            if len(lst) > 0:
                sel_args["status"] = lst
        if self.cb4.IsChecked(): # checkbox voor "titel bevat"
            selection = '(gefilterd)'
            txt = self.txt4.GetValue()
            sel_args["titel"] = txt
        if self.cb5.IsChecked(): # checkbox voor "archiefstatus"
            if self.rb5a.GetValue():
                sel_args["arch"] = "arch"
                if selection != '(gefilterd)':
                    selection = '(gearchiveerd)'
            if self.rb5b.GetValue():
                sel_args["arch"] = "alles"
                if selection != '(gefilterd)':
                    selection = ''
        self.parent.selection = selection
        return sel_args

class OptionsDialog(wx.Dialog):
    "base class voor de opties dialogen"
    def __init__(self, parent, id_, title, size=(300, 300), pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE):
        self.parent = parent
        wx.Dialog.__init__(self, parent, id_, title, pos, size, style)
        self.initstuff()
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.elb = gizmos.EditableListBox(self, -1, self.titel, pos=(50, 50),
            size=(250, 250), style= self.options)
        self.elb.SetStrings(self.data)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.elb, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "\n".join(self.tekst))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)

    def initstuff(self):
        "placeholder voor aanvullende initialisatie methode"
        self.titel = ""
        self.data = []
        self.tekst = ["", ""]
        self.options = gizmos.EL_ALLOW_EDIT

class TabOptions(OptionsDialog):
    "dialoog voor mogelijke tab headers"
    def initstuff(self):
        "aanvullende initialisatie"
        self.titel = "Tab titels"
        self.data = []
        ## h = self.parent.book.tabs.keys()
        ## h.sort()
        ## for key in h:
        for key in sorted(self.parent.book.tabs.keys()):
            tab_id, tab_text = self.parent.book.tabs[key].split(" ", 1)
            self.data.append(tab_text)
        self.tekst = ["De tab titels worden getoond in de volgorde",
            "zoals ze van links naar rechts staan.",
            "Er kunnen geen tabs worden verwijderd of",
            "toegevoegd."
            ]
        self.options = gizmos.EL_ALLOW_EDIT

    def leesuit(self):
        "wijzigingen doorvoeren"
        self.newtabs = {}
        for idx, item in enumerate(self.elb.GetStrings()):
            self.newtabs[str(idx)] = item

class StatOptions(OptionsDialog):
    "dialoog voor de mogelijke statussen"
    def initstuff(self):
        "aanvullende initialisatie"
        self.titel = "Status codes en waarden"
        self.data = []
        for key in sorted(self.parent.book.stats.keys()):
            item_text, item_value, row_id = self.parent.book.stats[key]
            self.data.append(": ".join((item_value, item_text, row_id)))
        self.tekst = [
            "De waarden voor de status worden getoond in",
            "dezelfde volgorde als waarin ze in de combobox",
            "staan.",
            "Vóór de dubbele punt staat de code, erachter",
            "de waarde.",
            "Denk erom dat als je codes wijzigt of statussen",
            "verwijdert, deze ook niet meer getoond en",
            "gebruikt kunnen worden in de registratie."
            ]
        self.options = gizmos.EL_ALLOW_NEW | gizmos.EL_ALLOW_EDIT | gizmos.EL_ALLOW_DELETE

    def leesuit(self):
        "wijzigingen doorvoeren"
        self.newstats = {}
        for sortkey, item in enumerate(self.elb.GetStrings()):
            try:
                value, text = item.split(": ")
            except ValueError:
                raise
            self.newstats[value] = (text, sortkey)

class CatOptions(OptionsDialog):
    "dialoog voor de mogelijke categorieen"
    def initstuff(self):
        "aanvullende initialisatie"
        self.titel = "Soort codes en waarden"
        self.data = []
        for key in sorted(self.parent.book.cats.keys()):
            item_value, item_text, row_id = self.parent.book.cats[key]
            self.data.append(": ".join((item_text, item_value, str(row_id))))
        self.tekst = ["De waarden voor de soorten worden getoond in",
            "dezelfde volgorde als waarin ze in de combobox",
            "staan.",
            "Vóór de dubbele punt staat de code, erachter",
            "de waarde.",
            "Denk erom dat als je codes wijzigt of statussen",
            "verwijdert, deze ook niet meer getoond en",
            "gebruikt kunnen worden in de registratie."
            ]
        self.options = gizmos.EL_ALLOW_NEW | gizmos.EL_ALLOW_EDIT | gizmos.EL_ALLOW_DELETE

    def leesuit(self):
        "wijzigingen doorvoeren"
        self.newcats = {}
        for sortkey, data in enumerate(self.elb.GetStrings()):
            try:
                value, text = data.split(": ")
            except ValueError:
                raise
            self.newcats[value] = (text, sortkey)

class MainWindow(wx.Frame):
    """Hoofdscherm met menu, statusbalk, notebook en een "quit" button"""
    def __init__(self, parent, id_):
        self.parent = parent
        self.exiting = False
        self.mag_weg = True
        self.filename = ""
        self.title = 'Actieregistratie'
        self.printer = EasyPrinter()
        self.pagedata = self.oldbuf = None
        self.newfile = self.newitem = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []

        if LIN:
            wide, high, left, top = 764, 720, 2, 2
        else:
            wide, high, left, top = 588, 594, 20, 32
        wx.Frame.__init__(self, parent, id_, self.title, pos=(left, top),
                size=(wide, high),
                style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        sbar = self.CreateStatusBar()
        ## self.SetStatusBar(sbar)

    # --- menu opbouwen -------------------------------------------------------------------------
        filemenu = wx.Menu()
        ## filemenu.Append(pr.ID_NEW, "&New (Ctrl-N)", " Create a new file")
        filemenu.Append(pr.ID_OPEN, "&Open project (Ctrl-O)", " Select a project")
        filemenu.AppendSeparator()
        submenu = wx.Menu()
        submenu.Append(pr.ID_PRINTS, "Dit &Scherm", " ")
        submenu.Append(pr.ID_PRINTA, "Deze &Actie", " ")
        filemenu.AppendMenu(-1, "&Print (Ctrl-P)", submenu) # " Print scherminhoud of actie")
        filemenu.AppendSeparator()
        filemenu.Append(pr.ID_EXIT, "&Quit (Ctrl-Q)", " Terminate the program")
        setupmenu = wx.Menu()
        submenu = wx.Menu()
        submenu.Append(pr.ID_SETFONT, "&Lettertype", " Change the size and font of the text")
        submenu.Append(pr.ID_SETCOLR, "&Kleuren", " Change the colours of various items")
        #~ submenu.Append(pr.ID_SETKEYS,  "S&neltoetsen", " Change shortcut keys")
        setupmenu.AppendMenu(-1, "&Applicatie", submenu) # " Settings voor de hele applicatie")
        submenu = wx.Menu()
        submenu.Append(pr.ID_SETTABS, "  &Tabs", " Change the titles of the tabs")
        submenu.Append(pr.ID_SETCATS, "  &Soorten", " Add/change type categories")
        submenu.Append(pr.ID_SETSTATS, "  St&atussen", " Add/change status categories")
        setupmenu.AppendMenu(-1, "&Data", submenu) # " Settings voor dit actiesbestand")
        setupmenu.Append(pr.ID_SETFOLLY, "&Het leven", " Change the way you look at life")
        helpmenu = wx.Menu()
        helpmenu.Append(pr.ID_ABOUT, "&About", " Information about this program")
        helpmenu.Append(pr.ID_KEYS, "&Keys", " List of shortcut keys")
        menu_bar = wx.MenuBar()
        menu_bar.Append(filemenu, "&File")
        menu_bar.Append(setupmenu, "&Settings")
        menu_bar.Append(helpmenu, "&Help")
        self.SetMenuBar(menu_bar)
        ## self.Connect(pr.ID_NEW, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.new_file)
        self.Connect(pr.ID_OPEN, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.open_file)
        self.Connect(pr.ID_PRINTS, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.print_scherm)
        self.Connect(pr.ID_PRINTA, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.print_actie)
        self.Connect(pr.ID_EXIT, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.exit_app)
        self.Connect(pr.ID_SETFONT, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.font_settings)
        self.Connect(pr.ID_SETCOLR, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.colour_settings)
        #~ self.Connect(pr.ID_SETKEYS,  -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.hotkey_settings)
        self.Connect(pr.ID_SETFOLLY, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.silly_menu)
        self.Connect(pr.ID_SETTABS, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.tab_settings)
        self.Connect(pr.ID_SETCATS, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.cat_settings)
        self.Connect(pr.ID_SETSTATS, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.stat_settings)
        self.Connect(pr.ID_ABOUT, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.about_help)
        self.Connect(pr.ID_KEYS, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.hotkey_help)
        self.help = ["=== Albert's actiebox ===\n",
            "Keyboard shortcuts:",
            "    Alt left/right: verder - terug",
            "    Alt-0 t/m Alt-5: naar betreffende pagina",
            "    Alt-O op tab 1: S_o_rteren",
            "    Alt-I op tab 1: F_i_lteren",
            "    Alt-G of Enter op tab 1: _G_a naar aangegeven actie",
            "    Alt-N op elke tab: _N_ieuwe actie opvoeren",
            "    Ctrl-O: selecteer een (ander) pr_o_ject",
            ## "    Ctrl-N: maak een nieuw actiebestand",
            "    Ctrl-P: _p_rinten (scherm of actie)",
            "    Ctrl-Q: _q_uit actiebox",
            "    Ctrl-H: _h_elp (dit scherm)",
            "    Ctrl-S: gegevens in het scherm op_s_laan",
            "    Ctrl-G: oplaan en _g_a door naar volgende tab",
            "    Ctrl-Z: wijzigingen ongedaan maken"]
        self.helptext = "\n".join(self.help)
    # --- schermen opbouwen: controls plaatsen ------------------------------------------------
        self.SetTitle(self.title)
        #~ self.SetIcon(wx.Icon("task.ico",wx.BITMAP_TYPE_ICO))
        self.SetIcon(images.gettaskIcon())
        #~ self.SetMinSize((476, 560))
        self.pnl = wx.Panel(self, -1)
        self.book = wx.Notebook(self.pnl, -1, size=(300,300))
        self.book.parent = self
        self.book.fnaam = ""
        self.book.sorter = None
        self.book.data = {}
        self.book.rereadlist = True
        self.lees_settings()
        self.book.ctitels = ("actie", " ", "status", "L.wijz.", "betreft", "omschrijving")
        self.book.current_tab = 0
        self.book.newitem = False
        self.book.current_item = 0
        self.book.pagedata = None
        #~ self.book.SetMinSize((486,496))
        self.book.page0 = Page0(self.book, -1)
        self.book.page1 = Page1(self.book, -1)
        self.book.page2 = Page(self.book, -1)
        self.book.page3 = Page(self.book, -1)
        self.book.page4 = Page(self.book, -1)
        self.book.page5 = Page(self.book, -1)
        self.book.page6 = Page6(self.book, -1)
        self.book.pages = 7
        self.book.checked_for_leaving = True
        self.exit_button = wx.Button(self.pnl, id=wx.ID_EXIT)
        self.Bind(wx.EVT_BUTTON, self.exit_app , self.exit_button)
        self.book.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)
        ## self.Bind(wx.EVT_CLOSE, self.exit_app)
        self.book.Bind(wx.EVT_LEFT_UP, self.on_left_release)
        self.book.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changed)
        self.book.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.on_page_changing)

    # --- schermen opbouwen: layout -------------------------------------------------------------
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        self.book.AddPage(self.book.page0, "&" + self.book.tabs[0])
        self.book.page0.doelayout()
        self.book.AddPage(self.book.page1, "&" + self.book.tabs[1])
        self.book.page1.doelayout()
        self.book.AddPage(self.book.page2, "&" + self.book.tabs[2])
        self.book.page2.doelayout()
        self.book.AddPage(self.book.page3, "&" + self.book.tabs[3])
        self.book.page3.doelayout()
        self.book.AddPage(self.book.page4, "&" + self.book.tabs[4])
        self.book.page4.doelayout()
        self.book.AddPage(self.book.page5, "&" + self.book.tabs[5])
        self.book.page5.doelayout()
        self.book.AddPage(self.book.page6, "&" + self.book.tabs[6])
        self.book.page6.doelayout()
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.book, 1, wx.EXPAND)
        sizer0.Add(sizer1, 1, wx.EXPAND)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(self.exit_button, 0,
            wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer0.Add(sizer2, 0, wx.EXPAND )
        self.pnl.SetSizer(sizer0)
        self.pnl.SetAutoLayout(True)
        sizer0.Fit(self.pnl)
        sizer0.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.Show(True)
        if self.filename == "":
            self.open_file(None)
        else:
            self.startfile()
        self.zetfocus(0) # book.page0.SetFocus()

    ## def new_file(self, evt):
        ## "Menukeuze: nieuw file"
        ## self.newfile = False
        ## self.dirname = os.getcwd()
        ## dlg = wx.FileDialog(self, self.title + " - nieuw gegevensbestand",
            ## self.dirname, "", "XML files|*.xml", wx.SAVE | wx.OVERWRITE_PROMPT)
        ## if dlg.ShowModal() == wx.ID_OK:
            ## self.filename = dlg.GetFilename()
            ## self.dirname = dlg.GetDirectory()
            ## self.newfile = True
            ## self.startfile()
            ## self.newfile = False
        ## dlg.Destroy()

    def open_file(self, evt):
        "Menukeuze: open project"
        data = []
        with open(APPS) as f_in:
            for line in f_in:
                sel, naam, titel, oms = line.strip().split(";")
                if sel == "X":
                    data.append((naam.capitalize(),titel.capitalize(),oms))
        data = data # [1:]
        data.sort()
        dlg = wx.SingleChoiceDialog(self, 'Kies een project om te openen',
            'Vraagje', [": ".join((h[1],h[2])) for h in data],wx.CHOICEDLG_STYLE)
        print(self.filename)
        for idx, h in enumerate(data):
            print(h)
            if h[0] == self.filename or \
                    (self.filename == "_basic" and h[0] == "Basic"):
                dlg.SetSelection(idx)
        if dlg.ShowModal() == wx.ID_OK:
            n = dlg.GetSelection()
            self.filename = data[n][0]
            if self.filename == "Basic":
                self.filename = "_basic"
            self.startfile()
        dlg.Destroy()

    def print_scherm(self, evt = None):
        "Menukeuze: print dit scherm"
        self.text = []
        self.hdr = ("Actie: %s %s" % (self.book.pagedata.id, self.book.pagedata.titel))
        if self.book.current_tab == 0:
            self.hdr = "Overzicht acties uit " + self.filename
            self.text.append("<table>")
            for x in range(len(self.book.data.items())):
                y = self.book.page0.p0list.GetItemData(x)
                actie, started, soort, status, l_wijz, over, titel = self.book.data[y]
                if l_wijz != "":
                    l_wijz = "".join(("laatst behandeld op ", l_wijz[:19]))
                code, text = status.split(".")
                if code != "0":
                    l_wijz = "status: {}, {} ".format(text, l_wijz)
                ## else:
                    ## l_wijz = ""
                self.text.append('<tr><td>{}&nbsp;&nbsp;</td><td>{} - {}</td></tr>'
                    '<tr><td></td><td>{} gemeld op {}<br>{}</td></tr>'.format(
                        actie, over, titel, soort.split(".")[1], started[:19], l_wijz))
            self.text.append("</table>")
        elif self.book.current_tab == 1:
            self.hdr = ("Informatie over actie {}: samenvatting".format(
                self.book.page1.id_text.GetValue()))
            self.text.append("<table>")
            self.text.append("<tr><td>Actie:</td><td>{}</td></tr>".format(
                self.book.page1.id_text.GetValue()))
            self.text.append("<tr><td>Gemeld op:</td><td>{}</td></tr>".format(
                self.book.page1.date_text.GetValue()))
            self.text.append("<tr><td>Betreft:</td><td>{}</td></tr>".format(
                self.book.page1.proc_entry.GetValue()))
            self.text.append("<tr><td>Melding:</td><td>{}</td></tr>".format(
                self.book.page1.desc_entry.GetValue()))
            self.text.append("<tr><td>Soort actie:</td><td>{}</td></tr>".format(
                self.book.page1.cat_choice.GetValue()))
            self.text.append("<tr><td>Status:</td><td>{}</td></tr>".format(
                self.book.page1.stat_choice.GetValue()))
            self.text.append("</table>")
        elif self.book.current_tab == 2:
            text = self.book.page2.text1.GetValue()
            if text is not None:
                self.text.append("<u>{}s</u><br>".format(
                    self.book.tabs[2].split(None, 1)[1]))
                self.text.append("<p>{}s</p>".format(
                    self.book.pagedata.melding.replace('\n', '<br>')))
        elif self.book.current_tab == 3:
            text = self.book.page2.text1.GetValue()
            if text is not None:
                self.text.append("<u>{}s</u><br>".format(
                    self.book.tabs[3].split(None, 1)[1]))
                self.text.append("<p>{}s</p>".format(
                    self.book.pagedata.oorzaak.replace('\n', '<br>')))
        elif self.book.current_tab == 4:
            text = self.book.page2.text1.GetValue()
            if text is not None:
                self.text.append("<u>{}s</u><br>".format(
                    self.book.tabs[4].split(None, 1)[1]))
                self.text.append("<p>{}s</p>".format(
                    self.book.pagedata.oplossing.replace('\n', '<br>')))
        elif self.book.current_tab == 5:
            text = self.book.page2.text1.GetValue()
            if text is not None:
                self.text.append("<u>{}s</u><br>".format(
                    self.book.tabs[5].split(None, 1)[1]))
                self.text.append("<p>{}s</p>".format(
                    self.book.pagedata.vervolg.replace('\n', '<br>')))
        elif self.book.current_tab == 6:
            self.text.append("<u>{}s</u><br>".format(self.book.tabs[6].split(None, 1)[1]))
            ## text = self.book.page6.txtStat.GetValue()
            ## if text is not None:
                ## self.text.append("<p>{}s</p>".format(text.replace('\n', '<br>')))
            if len(self.book.page6.event_list) > 0:
                for idx, data in enumerate(self.book.page6.event_list):
                    self.text.append("<p><b>{}</b><br>{}</p>".format(
                        data[:19].replace('\n', '<br>'),
                        self.book.page6.event_data[idx].replace('\n', '<br>')))
        self.afdrukken()

    def print_actie(self, evt = None):
        "Menukeuze: print deze actie"
        if self.book.pagedata is None or self.book.newitem:
            # afbreken met melding geen actie geselecteerd
            dlg = wx.MessageDialog(self,
                "Wel eerst een actie kiezen om te printen",
                self.parent.parent.title,
                wx.ICON_EXCLAMATION
            )
            dlg.ShowModal()
            dlg.Destroy()
            return
        self.hdr = ("Actie: {} {}".format(self.book.pagedata.id, self.book.pagedata.titel))
        self.text = ["<table>"]
        self.text.append("<tr><td>Actie:</td><td>{}</td></tr>".format(self.book.pagedata.id))
        self.text.append("<tr><td>Gemeld op:</td><td>{}</td></tr>".format(self.book.pagedata.datum))
        oms, tekst = self.book.pagedata.titel.split(" - ", 1)
        self.text.append("<tr><td>Betreft:</td><td>{}</td></tr>".format(oms))
        self.text.append("<tr><td>Melding:</td><td>{}</td></tr>".format(tekst))
        srt = "(onbekende soort)"
        for oms, code in self.book.cats.values():
            if code == self.book.pagedata.soort:
                srt = oms
                break
        self.text.append("<tr><td>Soort actie:</td><td>{}</td></tr>".format(srt))
        stat = "(onbekende status)"
        for oms, code in self.book.stats.values():
            if code == self.book.pagedata.status:
                stat = oms
                break
        self.text.append("<tr><td>Status:</td><td>{}</td></tr>".format(stat))
        self.text.append("</table>")
        self.text.append("<hr>")
        self.text.append("<b>{}</b><p>".format(self.book.tabs[2].split(None, 1)[1]))
        if self.book.pagedata.melding is not None:
            self.text.append(self.book.pagedata.melding.replace('\n', '<br>'))
        else:
            self.text.append("(nog niet beschreven)")
        self.text.append("</p><hr>")
        self.text.append("<b>{0}</b><p>".format(self.book.tabs[3].split(None, 1)[1]))
        if self.book.pagedata.oorzaak is not None:
            self.text.append(self.book.pagedata.oorzaak.replace('\n', '<br>'))
        else:
            self.text.append("(nog niet beschreven)")
        self.text.append("</p><hr>")
        self.text.append("<b>{0}</b><p>".format(self.book.tabs[4].split(None, 1)[1]))
        if self.book.pagedata.oplossing is not None:
            self.text.append(self.book.pagedata.oplossing.replace('\n', '<br>'))
        else:
            self.text.append("(nog niet beschreven)")
        self.text.append("</p>")
        if self.book.pagedata.vervolg is not None:
            self.text.append("<hr>")
            self.text.append("<b>{0}</b><p>".format(self.book.tabs[5].split(None, 1)[1]))
            self.text.append(self.book.pagedata.vervolg.replace('\n', '<br>'))
            self.text.append("</p>")
        if len(self.book.pagedata.events) > 0:
            for date, tekst in self.book.pagedata.events:
                self.text.append("<br><br><b>{0}</b><br>{1}</p>".format(
                    date[:19].replace('\n', '<br>'),tekst.replace('\n', '<br>')))
            self.text.append("</p>")
        self.afdrukken()

    def exit_app(self, evt = None):
        "Menukeuze: exit applicatie"
        self.exiting = True
        if self.book.current_tab == 0:
            ok_to_leave = self.book.page0.leavep()
        elif self.book.current_tab == 1:
            ok_to_leave = self.book.page1.leavep()
        elif self.book.current_tab == 2:
            ok_to_leave = self.book.page2.leavep()
        elif self.book.current_tab == 3:
            ok_to_leave = self.book.page3.leavep()
        elif self.book.current_tab == 4:
            ok_to_leave = self.book.page4.leavep()
        elif self.book.current_tab == 5:
            ok_to_leave = self.book.page5.leavep()
        elif self.book.current_tab == 6:
            ok_to_leave = self.book.page6.leavep()
        if ok_to_leave:
            self.Close(True)

    def tab_settings(self, evt):
        "Menukeuze: settings - data - tab titels"
        dlg = TabOptions(self, -1, "Wijzigen tab titels", size=(350, 200),
            style = wx.DEFAULT_DIALOG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.leesuit()
            self.save_settings("tab", dlg.newtabs)
        dlg.Destroy()

    def stat_settings(self, evt):
        "Menukeuze: settings - data - statussen"
        dlg = StatOptions(self, -1, "Wijzigen statussen", size=(350, 200),
            style = wx.DEFAULT_DIALOG_STYLE)
        ## if dlg.ShowModal() == wx.ID_OK:
        while True:
            result = dlg.ShowModal()
            if result != wx.ID_OK:
                break
            try:
                dlg.leesuit()
            except ValueError:
                wx.MessageBox('Foutieve waarde: bevat geen dubbele punt', 'Probreg',
                    parent=dlg)
            else:
                self.save_settings("stat", dlg.newstats)
                break
        dlg.Destroy()

    def cat_settings(self, evt):
        "Menukeuze: settings - data - soorten"
        dlg = CatOptions(self, -1, "Wijzigen categorieen", size=(350, 200),
            style = wx.DEFAULT_DIALOG_STYLE)
        while True:
            result = dlg.ShowModal()
            if result != wx.ID_OK:
                break
            try:
                dlg.leesuit()
            except ValueError:
                wx.MessageBox('Foutieve waarde: bevat geen dubbele punt', 'Probreg',
                    parent=dlg)
            else:
                self.save_settings("cat", dlg.newcats)
                break
        dlg.Destroy()

    def font_settings(self, evt):
        "Menukeuze: settings - applicatie - lettertype"
        ## def propagatefont(win, font):
            ## "local function to apply font to all children recursively"
            ## win.SetFont(font)
            ## for child in win.GetChildren():
                ## propagatefont(child, font)
        ## font = self.GetFont()
        ## colour = self.GetForegroundColour()
        ## data = wx.FontData()
        ## data.EnableEffects(True)
        ## data.SetColour(colour)
        ## data.SetInitialFont(font)
        ## dlg = wx.FontDialog(self, data)
        ## if dlg.ShowModal() == wx.ID_OK:
            ## data = dlg.GetFontData()
            ## font = data.GetChosenFont()
            ## colour = data.GetColour()
            ## propagatefont(self, font)
        dlg = wx.MessageDialog(self, "Sorry, werkt nog niet", "Oeps", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def colour_settings(self, evt):
        "Menukeuze: settings - applicatie - kleuren"
        ## def propagatecolour(win, colour):
            ## "local function to apply font to all children recursively"
            ## win.SetForegroundColour(colour)
            ## for child in win.GetChildren():
                ## propagatecolour(child, colour)
        ## colour = self.GetForegroundColour()
        ## data = wx.ColourData()
        ## data.SetColour(colour)
        ## dlg = wx.ColourDialog(self, data)
        ## dlg.GetColourData().SetChooseFull(True) # Windows only
        ## if dlg.ShowModal() == wx.ID_OK:
            ## data = dlg.GetColourData()
            ## colour = data.GetColour()
            ## propagatecolour(self, colour)
        dlg = wx.MessageDialog(self, "Sorry, werkt nog niet", "Oeps", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def hotkey_settings(self, evt):
        "Menukeuze: settings - applicatie- hotkeys (niet geactiveerd)"
        dlg = wx.MessageDialog(self, "Sorry, werkt nog niet", "Oeps", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def about_help(self, evt):
        "Menukeuze: help - about"
        wx.MessageBox("wxPython versie van mijn actiebox", "Help", wx.ICON_INFORMATION)

    def hotkey_help(self, evt):
        "menukeuze: help - keys"
        wx.MessageBox(self.helptext, "Help")

    def silly_menu(self, evt):
        "Menukeuze: settings - het leven"
        wx.MessageBox("Yeah you wish...\nHet leven is niet in te stellen helaas", "Haha")

    def startfile(self):
        "initialisatie t.b.v. nieuw bestand"
        self.book.fnaam = self.title = self.filename
        self.book.rereadlist = True
        self.book.sorter = None
        self.lees_settings()
        for x in self.book.tabs.keys():
            self.book.SetPageText(x, self.book.tabs[x])
        self.book.page0.sel_args = {}
        self.book.page1.vul_combos()
        if self.book.current_tab == 0:
            self.book.page0.vulp()
        else:
            self.book.SetSelection(0)
        self.book.checked_for_leaving = True

    def lees_settings(self):
        """instellingen (tabnamen, actiesoorten en actiestatussen) inlezen"""
        try:
            data = Settings(self.book.fnaam)
        except DataError as err:
            wx.MessageBox(str(err), "Oh-oh!")
            return
        self.book.stats = {}
        self.book.cats = {}
        self.book.tabs = {}
        self.book.pagehelp = ["Overzicht van alle acties",
        "Identificerende gegevens van de actie",
        "Beschrijving van het probleem of wens",
        "Analyse van het probleem of wens",
        "Voorgestelde oplossing",
        "Eventuele vervolgactie(s)",
        "Overzicht stand van zaken"]
        for item_value, item in data.stat.iteritems():
            item_text, sortkey, row_id = item
            self.book.stats[int(sortkey)] = (item_text, item_value, row_id)
        for item_value, item in data.cat.iteritems():
            item_text, sortkey, row_id = item
            self.book.cats[int(sortkey)] = (item_text, item_value, row_id)
        for tab_num, tab_data in data.kop.iteritems():
            tab_text, tab_adr = tab_data
            self.book.tabs[int(tab_num)] = " ".join((tab_num, tab_text.title()))

    def save_settings(self, srt, data):
        """instellingen (tabnamen, actiesoorten of actiestatussen) terugschrijven

        argumenten: soort, data
        data is een dictionary die in een van de dialogen TabOptions, CatOptions
        of StatOptions wordt opgebouwd"""
        settings = Settings(self.book.fnaam)
        print('saving settings')
        print('- old settings:')
        pprint.pprint(settings.__dict__)
        print('- new settings:')
        pprint.pprint(data)
        if srt == "tab":
            settings.kop = data
            settings.write('kop')
            self.book.tabs = {}
            for item_value, item_text in data.iteritems():
                item = " ".join((item_value, item_text))
                self.book.tabs[int(item_value)] = item
                self.book.SetPageText(int(item_value), item)
        elif srt == "stat":
            settings.stat = data
            settings.write(srt)
            self.book.stats = {}
            for item_value, item in data.iteritems():
                item_text, sortkey, row_id = item
                self.book.stats[sortkey] = (item_text, item_value, row_id)
        elif srt == "cat":
            settings.cat = data
            settings.write(srt)
            self.book.cats = {}
            for item_value, item in data.iteritems():
                print item
                item_text, sortkey, row_id = item
                self.book.cats[sortkey] = (item_text, item_value, row_id)
        self.book.page1.vul_combos()

    def on_key(self, evt):
        """
        met behulp van deze methode wordt vanaf globaal (applicatie) niveau dezelfde
        toetsenafhandelingsroutine aangeroepen als vanaf locaal (tab) niveau
        """
        if self.book.current_tab == 0:
            self.book.page0.on_key(evt)
        elif self.book.current_tab == 1:
            self.book.page1.on_key(evt)
        elif self.book.current_tab == 2:
            self.book.page2.on_key(evt)
        elif self.book.current_tab == 3:
            self.book.page3.on_key(evt)
        elif self.book.current_tab == 4:
            self.book.page4.on_key(evt)
        elif self.book.current_tab == 5:
            self.book.page5.on_key(evt)
        elif self.book.current_tab == 6:
            self.book.page6.on_key(evt)
        evt.Skip()

    def on_page_changing(self, event):
        """
        deze methode is bedoeld om wanneer er van pagina gewisseld gaat worden
        te controleren of dat wel mogelijk is en zo niet, te melden waarom en de
        paginawissel tegen te houden.
        """
        old = event.GetOldSelection()
        new = event.GetSelection() # unused
        sel = self.book.GetSelection() # unused
        msg = ""
        if old == -1:
            pass
        elif self.book.fnaam == "":
            msg = "Kies eerst een project om mee te werken"
            self.mag_weg = False
        elif len(self.book.data) == 0 and not self.book.newitem:
            msg = "Voer eerst één of meer acties op"
            self.mag_weg = False
        elif self.book.current_item == -1 and not self.book.newitem:
            msg = "Selecteer eerst een actie"
            self.mag_weg = False
        if not self.book.checked_for_leaving:
            self.mag_weg = True
            if self.book.current_tab == 0:
                self.mag_weg = self.book.page0.leavep()
            elif self.book.current_tab == 1:
                self.mag_weg = self.book.page1.leavep()
            elif self.book.current_tab == 2:
                self.mag_weg = self.book.page2.leavep()
            elif self.book.current_tab == 3:
                self.mag_weg = self.book.page3.leavep()
            elif self.book.current_tab == 4:
                self.mag_weg = self.book.page4.leavep()
            elif self.book.current_tab == 5:
                self.mag_weg = self.book.page5.leavep()
            elif self.book.current_tab == 6:
                self.mag_weg = self.book.page6.leavep()
        if not self.mag_weg:
            if msg != "":
                dlg = wx.MessageDialog(self, msg, "Navigatie niet toegestaan",
                    wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
            self.book.SetSelection(self.book.current_tab)
            event.Veto()
        else:
            event.Skip()

    def on_page_changed(self, event):
        """
        deze methode is bedoeld om na het wisselen van pagina het veld / de velden
        van de nieuwe pagina een waarde te geven met behulp van de vulp methode
        """
        old = event.GetOldSelection() # unused
        new = self.book.current_tab = event.GetSelection()
        sel = self.book.GetSelection() # unused
        if LIN and old == -1: # bij initialisatie en bij afsluiten - op Windows is deze altijd -1?
            return
        if new == 0:
            self.book.page0.vulp()
        elif new == 1:
            self.book.page1.vulp()
        elif new == 2:
            self.book.page2.vulp()
        elif new == 3:
            self.book.page3.vulp()
        elif new == 4:
            self.book.page4.vulp()
        elif new == 5:
            self.book.page5.vulp()
        elif new == 6:
            self.book.page6.vulp()
        self.zetfocus(self.book.current_tab)
        ## event.Skip()


    def on_left_release(self, evt=None):
        self.zetfocus(self.book.current_tab)
        evt.Skip()

    def zetfocus(self, tabno):
        "focus geven aan de gekozen tab"
        #~ self.setFocus()
        if tabno == 0:
            self.book.page0.p0list.SetFocus()
        elif tabno == 1:
            self.book.page1.proc_entry.SetFocus()
        elif tabno == 2:
            self.book.page2.text1.SetFocus()
        elif tabno == 3:
            self.book.page3.text1.SetFocus()
        elif tabno == 4:
            self.book.page4.text1.SetFocus()
        elif tabno == 5:
            self.book.page5.text1.SetFocus()
        elif tabno == 6:
            self.book.page6.progress_list.SetFocus()

    def afdrukken(self):
        "wordt aangeroepen door de menuprint methodes"
        self.css = ""
        if self.css != "":
            self.css = self.css.join(("<style>", "</style>"))
        self.text.insert(0, self.css.join(("<html><head><title>titel</title>",
            "</head><body>")))
        self.text.append("</body></html>")
        self.printer.print_("".join(self.text), self.hdr)
        return

def main():
    "opstart routine"
    app = wx.App(redirect=True, filename="probreg_sql.log")
    print('\n** {} **\n'.format(get_dts()))
    frame = MainWindow(None, -1)
    app.MainLoop()

if __name__ == '__main__':
    main()
    ## main(fn)
