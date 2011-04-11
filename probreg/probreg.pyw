#! C:/python25/python
# -*- coding: UTF-8 -*-

import sys, os
LIN = True if os.name == 'posix' else False
import wx
import wx.html as html
import wx.lib.mixins.listctrl  as  listmix
import wx.gizmos   as  gizmos
import images
import pr_globals as pr
from datetime import datetime
def get_dts():
    dts = datetime.now()
    if sys.version >= '2.6':
        return "{0}-{1:02}-{2:02} {3:02}:{4:02}:{5:02}".format(
            dts.year,dts.month,dts.day,dts.hour,dts.minute,dts.second)
    else:
        return "%i-%02i-%02i %02i:%02i:%02i" % (
            (dts.year,dts.month,dts.day,dts.hour,dts.minute,dts.second))

from dml import checkfile,Acties, Actie, Settings

class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

class Page(wx.Panel):
    def __init__(self,parent,id):
        self.parent = parent
        wx.Panel.__init__(self,parent,wx.ID_ANY, style=wx.WANTS_CHARS)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        high = 350 if LIN else 430
        self.text1 = wx.TextCtrl(self, -1, size=(490, high),
                                style=wx.TE_MULTILINE
                                | wx.TE_PROCESS_TAB
                                | wx.TE_RICH2
                                | wx.TE_WORDWRAP
                                )
        self.text1.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        self.Bind(wx.EVT_TEXT, self.OnEvtText, self.text1)
        self.btnSave = wx.Button(self, -1, 'Sla wijzigingen op (Ctrl-S)')
        self.Bind(wx.EVT_BUTTON, self.savep, self.btnSave)
        self.btnSaveGo = wx.Button(self, -1, 'Sla op en ga verder (Ctrl-G)')
        self.Bind(wx.EVT_BUTTON, self.savepgo, self.btnSaveGo)
        self.btnCancel = wx.Button(self, -1, 'Zet originele tekst terug (Ctrl-Z)')
        self.Bind(wx.EVT_BUTTON, self.restorep, self.btnCancel)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

    def doelayout(self):
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.text1, 1, wx.ALL | wx.EXPAND, 4)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(sizer1,1,wx.EXPAND)
        sizer2.Add(self.btnSave,0,wx.ALL,3)
        sizer2.Add(self.btnSaveGo,0,wx.ALL,3)
        sizer2.Add(self.btnCancel,0,wx.ALL,3)
        sizer0.Add(sizer2,0,wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer0)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)

    def vulp(self,evt=None):
        ## print "vulp: currentTab is ",self.parent.currentTab,self.__class__
        self.init = True
        self.enableButtons(False)
        if self.parent.currentTab == 0:
            self.parent.parent.SetTitle(" - ".join((self.parent.parent.title,self.seltitel)))
        else:
            self.parent.parent.SetTitle(" - ".join((self.parent.parent.title,
                ' '.join((self.parent.p.id,self.parent.p.titel)))))
            self.parent.parent.SetStatusText(self.parent.pagehelp[self.parent.currentTab])
        if self.parent.currentTab <= 1 or self.parent.currentTab == 6:
            return
        self.oldbuf = ''
        if self.parent.p != None:
            if self.parent.currentTab == 2 and self.parent.p.melding != None:
                self.oldbuf = self.parent.p.melding
            if self.parent.currentTab == 3 and self.parent.p.oorzaak != None:
                self.oldbuf = self.parent.p.oorzaak
            if self.parent.currentTab == 4 and self.parent.p.oplossing != None:
                self.oldbuf = self.parent.p.oplossing
            if self.parent.currentTab == 5 and self.parent.p.vervolg != None:
                self.oldbuf = self.parent.p.vervolg
            if self.parent.p.arch:
                self.text1.SetEditable(False)
            else:
                self.text1.SetEditable(True)
        self.text1.SetValue(self.oldbuf)
        self.init = False

    def readp(self,pid):
        self.parent.p = Actie(self.parent.fnaam,pid)
        self.parent.oldId = self.parent.p.id
        self.parent.newitem = False

    def nieuwp(self,evt=None):
        #~ print "nieuwp, eerst kijken of we wel klaar zijn"
        if self.leavep():
            ## print self.parent.fnaam
            self.parent.p = Actie(self.parent.fnaam,0)
            self.parent.newitem = True
            if self.parent.currentTab == 1:
                self.vulp() # om de velden leeg te maken
            else:
                self.gotoPage(1)
        else:
            print "nee we waren nog niet klaar"

    def leavep(self):
        ## print "leave page - huidige scherm is",self.parent.currentTab,self.__class__
        if self.parent.currentTab == 1:
            newbuf = (self.txtPrc.GetValue(),self.txtMld.GetValue(),self.cmbStat.GetSelection(),self.cmbCat.GetSelection())
            if self.parent.newitem and newbuf[0] == "" and newbuf [1] == "" and not self.parent.parent.abort:
                self.parent.newitem = False
                self.parent.p = Actie(self.parent.fnaam,self.parent.oldId) # om de gegevens terug te zetten
                #~ d = wx.MessageDialog(self,
                        #~ "U moet wel iets melden",
                        #~ self.parent.parent.title,
                        #~ wx.OK | wx.ICON_EXCLAMATION
                #~ )
                #~ d.ShowModal()
                #~ d.Destroy()
                #~ return False
        elif self.parent.currentTab == 6:
            ## newbuf = (self.txtStat.GetValue(),self.elijst,self.edata)
            newbuf = (self.elijst,self.edata)
            ## print self.oldbuf
            ## print newbuf
        elif self.parent.currentTab > 1:
            newbuf = self.text1.GetValue()
        ok = True
        if self.parent.currentTab > 0 and newbuf != self.oldbuf:
            d = wx.MessageDialog(self,
                "De gegevens op de pagina zijn gewijzigd, wilt u\nde wijzigingen opslaan voordat u verder gaat?",
                self.parent.parent.title,
                wx.YES_NO | wx.CANCEL | wx.ICON_EXCLAMATION
            )
            r = d.ShowModal()
            if r == wx.ID_YES:
                if self.parent.currentTab == 6:
                    ok = self.parent.page6.savep()
                else:
                    ok = self.savep()
            elif r == wx.ID_CANCEL:
                ok = False
            d.Destroy()
        ## print "klaar met controleren, ok is",ok
        return ok

    def savep(self,evt=None):
        ## print "savep: currentTab is ",self.parent.currentTab,self.__class__
        self.enableButtons(False)
        if self.parent.currentTab <= 1 or self.parent.currentTab == 6:
            return
        t = self.text1.GetValue()
        if self.parent.currentTab == 2 and t != self.parent.p.melding:
            self.oldbuf = self.parent.p.melding = t
            self.parent.p.events.append((get_dts(),"Meldingtekst aangepast"))
            self.parent.p.write()
        if self.parent.currentTab == 3 and t != self.parent.p.oorzaak:
            self.oldbuf = self.parent.p.oorzaak = t
            self.parent.p.events.append((get_dts(),"Beschrijving oorzaak aangepast"))
            self.parent.p.write()
        if self.parent.currentTab == 4 and t != self.parent.p.oplossing:
            self.oldbuf = self.parent.p.oplossing = t
            self.parent.p.events.append((get_dts(),"Beschrijving oplossing aangepast"))
            self.parent.p.write()
        if self.parent.currentTab == 5 and t != self.parent.p.vervolg:
            self.oldbuf = self.parent.p.vervolg = t
            self.parent.p.events.append((get_dts(),"Tekst vervolgactie aangepast"))
            self.parent.p.write()
        return True

    def savepgo(self,evt=None):
        if self.savep():
            self.gotoNextPage()
        else:
            self.enableButtons()

    def restorep(self,evt=None):
        self.vulp()

    def OnKeyPress(self, evt):
        ## print "page.onkeypress"
        keycode = evt.GetKeyCode()
        togo = keycode - 48
        ## print togo
        if evt.GetModifiers() == wx.MOD_ALT: # evt.AltDown()
            if keycode == wx.WXK_LEFT or keycode == wx.WXK_NUMPAD_LEFT: #  keycode == 314
                self.gotoPrevPage()
            elif keycode == wx.WXK_RIGHT or keycode == wx.WXK_NUMPAD_RIGHT: #  keycode == 316
                self.gotoNextPage()
            elif togo >= 0 and togo <= self.parent.pages: # Alt-0 t/m Alt-6
                ## print togo,self.parent.currentTab
                if togo != self.parent.currentTab:
                    self.gotoPage(togo)
            elif keycode == 83: # Alt-S
                if self.parent.currentTab == 0:
                    self.sort()
            elif keycode == 70: # Alt-F
                if self.parent.currentTab == 0:
                    self.select()
            elif keycode == 71: # Alt-G
                if self.parent.currentTab == 0:
                    self.gotoActie()
            elif keycode == 78: # Alt-N
                if self.parent.currentTab > 0:
                    self.leavep()
                    ## self.savep()
                self.nieuwp()
        elif evt.GetModifiers() == wx.MOD_CONTROL: # evt.ControlDown()
            if keycode == 81: # Ctrl-Q
                self.parent.parent.MenuExit()
            elif keycode == 80: # Ctrl-P
                self.keyprint(evt)
            elif keycode == 79: # Ctrl-O
                self.parent.parent.MenuOpen(evt)
            elif keycode == 78: # Ctrl-N
                self.parent.parent.MenuNew(evt)
            elif keycode == 70: # Ctrl-H
                self.parent.parent.MenuHelpKeys(evt)
            elif keycode == 83: # Ctrl-S
                if self.parent.currentTab > 0:
                    if self.btnSave.IsEnabled():
                        self.savep()
            elif keycode == 71: # Ctrl-G
                if self.parent.currentTab > 0:
                    if self.btnSaveGo.IsEnabled():
                        self.savepgo()
            elif keycode == 90: # Ctrl-Z
                if self.parent.currentTab > 0:
                    if self.btnCancel.IsEnabled():
                        self.restorep()
        elif keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:# 13 or 372: # Enter
            if self.parent.currentTab == 0:
                self.gotoNextPage()
            #~ else:                       # -- waarvoor was dit ook alweer?
                #~ evt.Skip()
        #~ else:
            #~ evt.Skip()
        evt.Skip()

    def OnEvtText(self,evt):
        ## print "self.init is", self.init
        if not self.init:
            ## print "ok, enabling buttons"
            self.enableButtons()

    def OnEvtComboBox(self,evt):
        self.enableButtons()

    def enableButtons(self,state=True):
        self.btnSave.Enable(state)
        self.btnSaveGo.Enable(state)
        self.btnCancel.Enable(state)
        ## print "abled buttons to",state

    def gotoActie(self,evt=None):
        self.gotoPage(1)

    def gotoNextPage(self):
        #~ print "goto next page from", self.parent.currentTab
        if not self.leavep():
            ## print "gotonextpage: mag niet weg"
            return
        if self.parent.currentTab < self.parent.pages:
            self.parent.AdvanceSelection()
            self.parent.parent.zetfocus(self.parent.currentTab)
        else:
            self.parent.SetSelection(1)
            self.parent.parent.zetfocus(self.parent.currentTab)

    def gotoPrevPage(self):
        #~ print "goto prev page from", self.parent.currentTab
        if not self.leavep():
            ## print "gotoprevpage: mag niet weg"
            return
        if self.parent.currentTab > 0:
            self.parent.AdvanceSelection(False)
            self.parent.parent.zetfocus(self.parent.currentTab)

    def gotoPage(self,n):
        #~ print "goto page",n,"from", self.parent.currentTab
        if not self.leavep():
            ## print "gotopage: mag niet weg"
            return
        if n >= 0 and n <= self.parent.pages:
            self.parent.SetSelection(n)
            self.parent.parent.zetfocus(self.parent.currentTab)

    def keyprint(self,evt):
        pass # vraag om printen scherm of actie, bv. met een radioboxdialog - nou die hebben we niet dat wordt een SingleChoiceDialog
        dlg = wx.SingleChoiceDialog(self, 'Wat wil je afdrukken', 'Vraagje',['huidig scherm', 'huidige actie'],wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            if dlg.GetSelection() == 0:
                self.parent.parent.MenuPrintScherm(evt)
            else:
                self.parent.parent.MenuPrintActie(evt)

class Page0(Page, listmix.ColumnSorterMixin):
    def __init__(self,parent,id):
        self.parent = parent
        self.seltitel = 'alle meldingen'
        wx.Panel.__init__(self,parent,wx.ID_ANY
        #~ style=wx.WANTS_CHARS
        )
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        tID = wx.NewId()

        self.il = wx.ImageList(16, 16)

        self.idx1 = self.il.Add(images.getPtBitmap())
        self.sm_up = self.il.Add(images.getSmallUpArrowBitmap())
        self.sm_dn = self.il.Add(images.getSmallDnArrowBitmap())

        self.p0list = MyListCtrl(self, tID,
                                 style=wx.LC_REPORT
                                 | wx.BORDER_SUNKEN
                                 #~ | wx.LC_VRULES
                                 #~ | wx.LC_HRULES
                                 | wx.LC_SINGLE_SEL
                                 )
        high = 400 if LIN else 444
        self.p0list.SetMinSize((440,high))

        self.p0list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        self.PopulateList()

        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        self.itemDataMap = self.parent.data
        listmix.ColumnSorterMixin.__init__(self, 6)
        #self.SortListItems(0, True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.p0list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.p0list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.p0list)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.p0list)
        self.p0list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.p0list.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

        self.btnSort = wx.Button(self, pr.ID_SORT, '&Sorteren')
        self.btnZoek = wx.Button(self, pr.ID_ZOEK, '&Filteren')
        self.btnGa = wx.Button(self, pr.ID_GANAAR, '&Ga naar melding')
        self.btnArch = wx.Button(self, pr.ID_ARCH, '&Archiveer')
        self.btnNieuw = wx.Button(self, pr.ID_MELD, '&Nieuwe melding opvoeren')
        self.Bind(wx.EVT_BUTTON, self.sort,self.btnSort)
        self.Bind(wx.EVT_BUTTON, self.select,self.btnZoek)
        self.Bind(wx.EVT_BUTTON, self.gotoActie,self.btnGa)
        self.Bind(wx.EVT_BUTTON, self.archiveer,self.btnArch)
        self.Bind(wx.EVT_BUTTON, self.nieuwp,self.btnNieuw)

    def doelayout(self):
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.p0list,1,wx.EXPAND,0)
        sizer0.Add(sizer1,1,wx.EXPAND,0)
        sizer2.Add(self.btnSort,0,wx.ALL,3)
        sizer2.Add(self.btnZoek,0,wx.ALL,3)
        sizer2.Add(self.btnGa,0,wx.ALL,3)
        sizer2.Add(self.btnArch,0,wx.ALL,3)
        sizer2.Add(self.btnNieuw,0,wx.ALL,3)
        sizer0.Add(sizer2,0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer0)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)

    def leavep(self):
        return True # niks doen, doorgaan

    def vulp(self):
        Page.vulp(self)
        if not self.parent.rereadlist:
            self.parent.parent.SetStatusText("%s - %i items" % (self.parent.pagehelp[self.parent.currentTab],len(self.parent.data)))
            return
        self.parent.data = {}
        select = self.sel.copy()
        ## print select
        arch = ""
        if "arch" in select: arch = select.pop("arch")
        ## print arch, select
        try:
            h = Acties(self.parent.fnaam,select,arch)
            ## for x in h.lijst:
                ## print x
        except:
            print "samenstellen lijst mislukt"
        else:
            for y in enumerate(h.lijst):
                ## print y
                x = y[1]
                ## print x
                if len(x) < 5:
                    x.append('')
                # let op: voor correct sorteren moet de volgorde van rubrieken in self.data overeenkomen met die op het scherm
                self.parent.data[y[0]] = (x[0],x[1],".".join((str(x[3][1]),x[3][0])),".".join((str(x[2][1]),x[2][0])),x[5],x[4])
        self.PopulateList()
        self.parent.parent.SetStatusText("%s - %i items" % (self.parent.pagehelp[self.parent.currentTab],len(self.parent.data)))
        #~ print len(self.parent.data),self.parent.currentItem
        if self.parent.sorter is not None:
            ## print "maar wel opnieuw sorteren"
            self.p0list.SortItems(self.parent.sorter)
        self.parent.rereadlist = False
        self.p0list.Select(self.parent.currentItem)
        self.p0list.EnsureVisible(self.parent.currentItem)

    def PopulateList(self):
        #~ print "populating list..."
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

        info.m_width = 64
        info.m_text = self.parent.ctitels[0]
        self.p0list.InsertColumnInfo(1, info)

        info.m_width = 24
        info.m_text = self.parent.ctitels[1]
        self.p0list.InsertColumnInfo(2, info)

        info.m_width = 114
        info.m_text = self.parent.ctitels[2]
        self.p0list.InsertColumnInfo(3, info)

        info.m_width = 72
        info.m_text = self.parent.ctitels[3]
        self.p0list.InsertColumnInfo(4, info)

        info.m_width = 292
        info.m_text = self.parent.ctitels[4]
        self.p0list.InsertColumnInfo(5, info)

        self.parent.rereadlist = False
        items = self.parent.data.items()
        if items is None or len(items) == 0:
            return

        kleur = False
        for key, data in items:
            ## print data
            index = self.p0list.InsertStringItem(sys.maxint, data[0])
            self.p0list.SetStringItem(index, 1, data[0])
            self.p0list.SetStringItem(index, 2, data[2][data[2].index(".")+1:data[2].index(".")+2].upper())
            self.p0list.SetStringItem(index, 3, data[3][data[3].index(".")+1:])
            self.p0list.SetStringItem(index, 4, data[4])
            self.p0list.SetStringItem(index, 5, data[5])
            self.p0list.SetItemData(index, key)
        self.Colorize()

    def GetListCtrl(self):
        return self.p0list

    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)

    def Colorize(self):
        """ na het sorteren moeten de regels weer om en om gekleurd worden"""
        kleur = False
        for key in xrange(self.p0list.GetItemCount()):
        ## for key in range(len(self.data.items)):
            if kleur:
                #~ self.p0list.SetItemBackgroundColour(key,wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))
            #~ else:
                self.p0list.SetItemBackgroundColour(key,wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
            kleur = not kleur

    def OnItemSelected(self, event):
        self.parent.currentItem = event.m_itemIndex
        #~ print self.parent.currentItem
        seli = self.p0list.GetItemData(self.parent.currentItem)
        ## print "Itemselected",seli,self.parent.data[seli][0]
        self.readp(self.parent.data[seli][0])
        hlp = "&Herleef" if self.parent.p.arch else "&Archiveer"
        self.btnArch.SetLabel(hlp)
        event.Skip()

    def OnItemDeselected(self, evt):
        item = evt.GetItem()

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex

    def OnColClick(self, event):
        ## print "OnColClick: %d\n" % event.GetColumn()
        self.parent.sorter = self.GetColumnSorter()
        self.Colorize()
        event.Skip()

    def OnDoubleClick(self, event):
        self.gotoActie()
        # self.log.WriteText("OnDoubleClick item %s\n" % self.p0list.GetItemText(self.currentItem))
        event.Skip()

    def select(self,evt=None):
        """niet alleen selecteren op tekst(deel) maar ook op status, soort etc"""
        d = SelectOptionsDialog(self,self.sel)
        if d.ShowModal() == wx.ID_OK: # Shows it
            self.sel = d.SetOptions()
            ## print self.parent.fnaam,self.sel
            self.parent.rereadlist = True
            self.vulp()
            ## e = wx.MessageDialog( self, "Sorry, werkt nog niet", "Oeps", wx.OK)  # Create a message dialog box
            ## e.ShowModal() # Shows it
            ## e.Destroy() # finally destroy it when finished.
        d.Destroy() # finally destroy it when finished.
        self.parent.parent.zetfocus(0)

    def sort(self,evt=None):
        """sortering mogelijk op datum/tijd, soort, titel, status via
        schermpje met 2x4 comboboxjes waarin de volgorde van de rubrieken en de sorteervolgorde per rubriek kunt aangeven"""
        ## d = wx.MessageDialog( self, "Sorry, werkt nog niet", "Oeps", wx.OK)  # Create a message dialog box
        d = SortOptionsDialog(self)
        if d.ShowModal() == wx.ID_OK: # Shows it
            e = wx.MessageDialog( self, "Sorry, werkt nog niet", "Oeps", wx.OK)  # Create a message dialog box
            e.ShowModal() # Shows it
            e.Destroy() # finally destroy it when finished.
            # self.Colorize() # formerly known as self.AfterSort()
        d.Destroy() # finally destroy it when finished.
        self.parent.parent.zetfocus(0)

    def archiveer(self,evt=None):
        seli = self.p0list.GetItemData(self.parent.currentItem)
        self.readp(self.parent.data[seli][0])
        self.parent.p.arch = not self.parent.p.arch
        hlp = "gearchiveerd" if self.parent.p.arch else "herleefd"
        self.parent.p.events.append((get_dts(),"Actie {0}".format(hlp)))
        self.parent.p.write()
        self.parent.rereadlist = True
        self.vulp()
        self.parent.parent.zetfocus(0)
        # het navolgende geldt alleen voor de selectie "gearchiveerd en actief"
        if self.sel.get("arch","") == "alles":
            self.p0list.EnsureVisible(seli)
            hlp = "&Herleef" if self.parent.p.arch else "&Archiveer"
            self.btnArch.SetLabel(hlp)

    def enableButtons(self,state=True):
        pass # anders wordt de methode van de Page class geactiveerd

class Page1(Page):
    def __init__(self,parent,id):
        self.parent = parent
        wx.Panel.__init__(self,parent,wx.ID_ANY,
        #~ style=wx.WANTS_CHARS
        )
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        t1 = wx.TextCtrl(self, -1, size=(125, -1))
        self.txtId = t1
        t1.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

        t2 = wx.TextCtrl(self, -1, size=(125, -1))
        self.txtDat = t2
        t2.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

        t3 = wx.TextCtrl(self, -1, size=(125, -1))
        self.Bind(wx.EVT_TEXT, self.OnEvtText, t3)
        self.txtPrc = t3
        t3.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

        t4 = wx.TextCtrl(self, -1, size=(360, -1))
        self.Bind(wx.EVT_TEXT, self.OnEvtText, t4)
        self.txtMld = t4
        t4.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

        cb1 = wx.ComboBox(self, -1, size=(180, -1), style=wx.CB_DROPDOWN |wx.CB_READONLY)
        self.Bind(wx.EVT_TEXT, self.OnEvtText, cb1)
        self.cmbCat = cb1
        cb1.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

        cb2 = wx.ComboBox(self, -1, size=(140, -1), style=wx.CB_DROPDOWN |wx.CB_READONLY)
        self.Bind(wx.EVT_TEXT, self.OnEvtText, cb2)
        self.cmbStat = cb2
        cb2.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        self.VulCombos()

        t5 = wx.StaticText(self, -1, "")
        self.txtArch = t5
        t5.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        b5 = wx.Button(self, -1, "Archiveren")
        self.btnArch = b5
        self.Bind(wx.EVT_BUTTON, self.archiveer, self.btnArch)
        b5.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

        self.btnSave = wx.Button(self, -1, 'Sla wijzigingen op (Ctrl-S)')
        self.Bind(wx.EVT_BUTTON, self.savep, self.btnSave)
        self.btnSaveGo = wx.Button(self, -1, 'Sla op en ga verder (Ctrl-G)')
        self.Bind(wx.EVT_BUTTON, self.savepgo, self.btnSaveGo)
        self.btnCancel = wx.Button(self, -1, 'Maak wijzigingen ongedaan (Ctrl-Z)')
        self.Bind(wx.EVT_BUTTON, self.restorep, self.btnCancel)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

    def doelayout(self):
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.GridBagSizer(3,12) # rows, cols, hgap, vgap
        sizer1.Add(wx.StaticText(self, -1, "Actie-id:"), (0,0), flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_TOP, border = 10)
        sizer1.Add(self.txtId,  (0,1), flag = wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self, -1, "Datum/tijd:"), (1,0), flag = wx.ALL | wx.ALIGN_TOP, border = 10)
        sizer1.Add(self.txtDat, (1,1), flag = wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self, -1, "Job/\ntransactie:"), (2,0), flag = wx.ALL | wx.ALIGN_TOP, border = 10)
        sizer1.Add(self.txtPrc, (2,1), flag = wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self, -1, "Melding/code/\nomschrijving:"), (3,0), flag = wx.ALL | wx.ALIGN_TOP, border = 10)
        sizer1.Add(self.txtMld, (3,1), flag = wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self, -1, "Categorie:"), (4,0), flag = wx.ALL | wx.ALIGN_TOP, border = 10)
        sizer1.Add(self.cmbCat, (4,1), flag = wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(wx.StaticText(self, -1, "Status:"), (5,0), flag = wx.ALL | wx.ALIGN_TOP, border = 10)
        sizer1.Add(self.cmbStat, (5,1), flag = wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(self.txtArch, (6,1), flag = wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM, border = 10)
        sizer1.Add(self.btnArch, (7,1), flag = wx.ALIGN_CENTER_VERTICAL | wx.TOP, border = 5)
        sizer1.Add((-1,186), (9,0))
        sizer1.AddGrowableRow(8)
        sizer1.AddGrowableCol(2)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(sizer1,1,wx.EXPAND | wx.ALL,8)
        sizer2.Add(self.btnSave,0,wx.ALL,3)
        sizer2.Add(self.btnSaveGo,0,wx.ALL,3)
        sizer2.Add(self.btnCancel,0,wx.ALL,3)
        sizer0.Add(sizer2,0,wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer0)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)

    def vulp(self):
        Page.vulp(self)
        self.txtId.SetValue("")
        self.txtDat.SetValue("")
        self.txtPrc.SetValue("")
        self.txtMld.SetValue("")
        self.txtArch.SetLabel("")
        self.cmbCat.SetSelection(0)
        self.cmbStat.SetSelection(0)
        if self.parent.p is not None: # and not self.parent.newitem:
            self.txtId.SetValue(self.parent.p.id)
            self.txtDat.SetValue(self.parent.p.datum)
            self.parch = self.parent.p.arch
            if self.parent.p.titel is not None:
                h = self.parent.p.titel.split(": ")
                self.txtPrc.SetValue(h[0])
                if len(h) > 1:
                    self.txtMld.SetValue(h[1])
            for x in range(len(self.parent.stats)):
                if self.cmbStat.GetClientData(x) == self.parent.p.status:
                    self.cmbStat.SetSelection(x)
                    break
            for x in range(len(self.parent.cats)):
                if self.cmbCat.GetClientData(x) == self.parent.p.soort:
                    self.cmbCat.SetSelection(x)
                    break
        self.oldbuf = (self.txtPrc.GetValue(),self.txtMld.GetValue(),self.cmbStat.GetSelection(),self.cmbCat.GetSelection())
        self.init = False
        if self.parch:
            aanuit = False
            self.txtArch.SetLabel("Deze actie is gearchiveerd")
            self.btnArch.SetLabel("Herleven")
        else:
            aanuit = True
            self.txtArch.SetLabel("")
            self.btnArch.SetLabel("Archiveren")
        self.txtId.Enable(False)
        self.txtDat.Enable(False)
        self.txtPrc.Enable(aanuit)
        self.txtMld.Enable(aanuit)
        self.cmbCat.Enable(aanuit)
        self.cmbStat.Enable(aanuit)
        if self.parent.newitem:
            self.btnArch.Enable(False)
        else:
            self.btnArch.Enable(True)
        ## print "klaar met vulp"

    def savep(self,evt=None):
        Page.savep(self)
        s1 = self.txtPrc.GetValue()
        try:
            s1 = s1[0].upper() + s1[1:]
            self.txtPrc.SetValue(s1)
            self.enableButtons(False)
        except IndexError:
            pass
        s2 = self.txtMld.GetValue()
        if s1 == "" or s2 == "":
            wx.MessageBox("Beide tekstrubrieken moeten worden ingevuld","Oeps")
            return False
        wijzig = False
        if self.parent.newitem:
            self.parent.p.events.append(
                (get_dts(),"Actie opgevoerd"))
        t = ": ".join((s1,s2))
        if t != self.parent.p.titel:
            self.parent.p.titel = t
            self.parent.p.events.append(
                (get_dts(),'Titel gewijzigd in "{0}"'.format(t)))
            wijzig = True
        s = self.cmbStat.GetClientData(self.cmbStat.GetSelection())
        if s != self.parent.p.status:
            self.parent.p.status = s
            sel = self.cmbStat.GetStringSelection()
            self.parent.p.events.append(
                (get_dts(),'Status gewijzigd in "{0}"'.format(sel)))
            wijzig = True
        s = self.cmbCat.GetClientData(self.cmbCat.GetSelection())
        if s != self.parent.p.soort:
            self.parent.p.soort = s
            sel = self.cmbCat.GetStringSelection()
            self.parent.p.events.append(
                (get_dts(),'Categorie gewijzigd in "{0}"'.format(sel)))
            wijzig = True
        if self.parch != self.parent.p.arch:
            ## if self.parch:
                ## self.parent.p.setArch(True)
            ## else:
                ## self.parent.p.setArch(False)
            self.parent.p.setArch(self.parch)
            hlp = "gearchiveerd" if self.parch else "herleefd"
            self.parent.p.events.append(
                (get_dts(),"Actie {0}".format(hlp)))
            wijzig = True
        if wijzig:
            #~ print "savep: schrijven",self.oldbuf
            self.parent.rereadlist = True
            self.parent.p.write()
            if self.parent.newitem:
                #~ print len(self.parent.data)
                self.parent.currentItem = len(self.parent.data) # + 1
                self.parent.data[self.parent.currentItem] = (self.txtDat.GetValue(), \
                    ": ".join((self.txtPrc.GetValue(),self.txtMld.GetValue())), \
                    self.cmbStat.GetSelection(),self.cmbCat.GetSelection(), \
                    self.txtId.GetValue())
                self.parent.newitem = False
            self.oldbuf = (self.txtPrc.GetValue(),self.txtMld.GetValue(), \
                self.cmbStat.GetSelection(),self.cmbCat.GetSelection())
        return True

    def archiveer(self,evt=None):
        self.parch = not self.parch
        self.savep()
        self.parent.rereadlist = True
        self.vulp()
        ## self.gotoPrevPage() # waarom?

    def VulCombos(self):
        #~ print "vullen combobox"
        self.cmbStat.Clear()
        self.cmbCat.Clear()
        s = self.parent.cats.keys()
        s.sort()
        for x in s:
            y = self.parent.cats[x]
            self.cmbCat.Append(y[0],y[1])
        s = self.parent.stats.keys()
        #~ print "voor sort:",s
        s.sort()
        #~ print "na sort:",s
        for x in s:
            y = self.parent.stats[x]
            self.cmbStat.Append(y[0],y[1])


class Page6(Page):
    def __init__(self,parent,id):
        # Left_Down op de listbox is er voor het opvoeren van een nieuwe entry of het aanpassen van een bestaande
        # Kill Focus op de listbox en de onderste textentry is er om de tekst aan te passen indein nodig
        # Key Down is voor de hotkeys
        # Evt TEST is voor de enableButtons
        self.parent = parent
        self.currentItem = 0
        self.oldtext = ""
        wx.Panel.__init__(self,parent,wx.ID_ANY,
        ## style=wx.WANTS_CHARS
            )
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        ## self.txtStat = wx.TextCtrl(self, -1, size=(500,40), style=wx.TE_MULTILINE
            ## # | wx.TE_PROCESS_TAB
            ## | wx.TE_RICH2
            ## | wx.TE_WORDWRAP
            ## )
        ## self.txtStat.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        ## self.txtStat.Bind(wx.EVT_TEXT, self.OnEvtText,))
        high = 200 if LIN else 280
        self.lstVoortg = MyListCtrl(self, -1, size=(500,high),
            style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL)
        self.lstVoortg.InsertColumn(0,'Momenten')
        high = 100 if LIN else 110
        self.txtVoortg = wx.TextCtrl(self, -1, size=(500,high), style=wx.TE_MULTILINE
            ## | wx.TE_PROCESS_TAB
            | wx.TE_RICH2
            | wx.TE_WORDWRAP
            )
        self.txtVoortg.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        self.lstVoortg.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.lstVoortg.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
        self.txtVoortg.Bind(wx.EVT_TEXT, self.OnEvtText)

        self.btnSave = wx.Button(self, -1, 'Sla wijzigingen op (Ctrl-S)')
        self.Bind(wx.EVT_BUTTON, self.savep, self.btnSave)
        self.btnSaveGo = wx.Button(self, -1, 'Sla op en ga verder (Ctrl-G)')
        self.Bind(wx.EVT_BUTTON, self.savepgo, self.btnSaveGo)
        self.btnCancel = wx.Button(self, -1, 'Maak wijzigingen ongedaan (Ctrl-Z)')
        self.Bind(wx.EVT_BUTTON, self.restorep, self.btnCancel)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

    def doelayout(self):
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        ## sizer1.Add(wx.StaticText(self, -1, "Korte omschrijving stand van zaken:"), 0, wx.EXPAND | wx.EAST | wx.WEST, 6)
        ## sizer1.Add(self.txtStat, 0, wx.EXPAND | wx.ALL, 4)
        ## sizer1.Add(wx.StaticText(self, -1, "Momenten:"), (2,0), flag = wx.ALL | wx.ALIGN_TOP, border = 4)
        sizer1.Add(self.lstVoortg, 1, wx.EXPAND | wx.ALL, 4)
        ## sizer1.Add(wx.StaticText(self, -1, "Beschrijving moment:"), (4,0), flag = wx.ALL | wx.ALIGN_TOP, border = 4)
        sizer1.Add(self.txtVoortg, 1, wx.EXPAND | wx.ALL, 4)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(sizer1,1,wx.EXPAND | wx.ALL,8)
        sizer2.Add(self.btnSave,0,wx.ALL,3)
        sizer2.Add(self.btnSaveGo,0,wx.ALL,3)
        sizer2.Add(self.btnCancel,0,wx.ALL,3)
        sizer0.Add(sizer2,0,wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer0)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)

    def vulp(self):
        Page.vulp(self)
        ## self.txtStat.Clear()
        self.elijst = self.edata = self.olijst = self.odata = []
        self.txtVoortg.Clear()
        self.txtVoortg.SetEditable(False)
        if self.parent.p is not None: # and not self.parent.newitem:
            self.elijst = [x[0] for x in self.parent.p.events]
            self.elijst.reverse()
            self.olijst = self.elijst[:]
            self.edata = [x[1] for x in self.parent.p.events]
            self.edata.reverse()
            self.odata = self.edata[:]
            ## self.txtStat.SetValue(self.parent.p.stand)
            self.lstVoortg.DeleteAllItems()
            y = '-- add new item --'
            index = self.lstVoortg.InsertStringItem(sys.maxint, y)
            self.lstVoortg.SetStringItem(index, 0, y)
            self.lstVoortg.SetItemData(index, -1)
            for x,y in enumerate(self.elijst):
                index = self.lstVoortg.InsertStringItem(sys.maxint, y)
                s = self.edata[x].split("\n")[0]
                s = s if len(s) < 80 else s[:80] + "..."
                self.lstVoortg.SetStringItem(index, 0, y + " - " +  s)
                self.lstVoortg.SetItemData(index, x)
        ## self.oldbuf = (self.txtStat.GetValue(),self.olijst,self.odata)
        self.oldbuf = (self.olijst,self.odata)
        self.oldtext = ''
        self.init = True
        ## print "klaar met vulp, edata is", self.edata

    def savep(self,evt=None):
        Page.savep(self)
        ## print "verder met eigen savep()"
        # voor het geval er na het aanpassen van een tekst direkt "sla op" gekozen is
        # nog even kijken of de tekst al in self.edata is aangepast.
        ix = self.currentItem
        hlp = self.txtVoortg.GetValue()
        if ix > 0:
            ix -= 1
        ## print ix, self.elijst[ix]
        if self.edata[ix] != hlp:
            self.edata[ix] = hlp
            self.oldtext = hlp
            s = hlp.split("\n")[0]
            s = s if len(s) < 80 else s[:80] + "..."
            self.lstVoortg.SetStringItem(ix+1, 0, self.elijst[ix] + " - " +  s)
            self.lstVoortg.SetItemData(ix+1, ix)
        ## s1 = self.txtStat.GetValue()
        ## if s1 == "" and len(self.elijst) > 0:
            ## wx.MessageBox("Stand van zaken moet worden ingevuld","Oeps")
            ## return False
        wijzig = False
        ## if s1 != self.parent.p.stand:
            ## self.parent.p.stand = s1
            ## wijzig = True
        if self.elijst != self.olijst or self.edata != self.odata:
            wijzig = True
            hlp = len(self.elijst) - 1
            for ix,data in enumerate(self.parent.p.events):
                ## print data
                ## print self.elijst[hlp - ix], self.edata[hlp - ix]
                ## print
                if data != (self.elijst[hlp - ix],self.edata[hlp - ix]):
                    self.parent.p.events[ix] = (self.elijst[hlp - ix],self.edata[hlp - ix])
            for ix in range(len(self.parent.p.events),hlp + 1):
                self.parent.p.events.append((self.elijst[hlp - ix],self.edata[hlp - ix]))
        if wijzig:
            #~ print "savep: schrijven"
            ## self.parent.p.list() # NB element 0 is leeg
            self.parent.p.write()
            self.olijst = self.elijst[:]
            self.odata = self.edata[:]
            ## self.oldbuf = (self.txtStat.GetValue(),self.olijst,self.odata)
            self.oldbuf = (self.olijst,self.odata)
        else:
            print "Leuk hoor, er was niks gewijzigd ! @#%&*Grrr"
        return True

    def OnItemSelected(self, event):
        ## print "onitemselected"
        # selecteren van (klikken op) een regel in de listbox doet de inhoud van de textctrl ook veranderen. eerst controleren of de tekst veranderd is
        # dat vragen moet ook in de situatie dat je op een geactiveerde knop klikt, het panel wilt verlaten of afsluiten
        # de knoppen onderaan doen de hele lijst bijwerken in self.parent.nb.p
        self.currentItem = event.m_itemIndex # - 1
        tekst = self.lstVoortg.GetItemText(self.currentItem)
        ## print "Selected Item", self.currentItem,tekst
        self.txtVoortg.SetEditable(False)
        if not self.parent.p.arch:
            self.txtVoortg.SetEditable(True)
            if self.currentItem == 0:
                hlp = get_dts()
                index = self.lstVoortg.InsertStringItem(1,hlp)
                self.elijst.insert(0,hlp)
                self.edata.insert(0,"")
                ## self.lstVoortg.Select(1)
                self.oldtext = ""
        if self.currentItem > 0:
            ## print len(self.edata), self.edata
            self.oldtext = self.edata[self.currentItem - 1]
        ## if self.currentItem == 0:
            ## self.lstVoortg.CloseEditor()
            ## index = self.lstVoortg.InsertStringItem(1,'')
        self.txtVoortg.SetValue(self.oldtext)
        ## print "oldtext:",self.oldtext
        self.txtVoortg.SetFocus()
        #~ event.Skip()

    def OnItemDeselected(self, evt):
        item = evt.GetItem()
        ix = evt.m_itemIndex
        tekst = self.txtVoortg.GetValue() # self.lstVoortg.GetItemText(ix)
        ## print "deselected item",ix,tekst # item
        if tekst != self.oldtext:
            self.edata[ix-1] = tekst
            self.oldtext = tekst
            s = tekst.split("\n")[0]
            s = s if len(s) < 80 else s[:80] + "..."
            self.lstVoortg.SetStringItem(ix, 0, self.elijst[ix-1] + " - " +  s)
            self.lstVoortg.SetItemData(ix, ix - 1)
        evt.Skip()

    def OnEvtText(self,evt):
        ## print "onevttext"
        ix = self.currentItem # self.lstVoortg.Selection
        tekst = self.txtVoortg.GetValue() # self.lstVoortg.GetItemText(ix)
        if tekst != self.oldtext:
            ## print "ok, enabling buttons"
            self.enableButtons()
        evt.Skip()

class EasyPrinter(html.HtmlEasyPrinting):
    def __init__(self):
        html.HtmlEasyPrinting.__init__(self)

    def Print(self, text, doc_name):
        self.SetHeader(doc_name)
        self.PreviewText(text)
        #~ self.PrintText(text,doc_name)

class Prtdata(wx.Printout):
    def HasPage(self, page):
        print ("wx.Printout.HasPage: %d\n" % page)
        if page <= 1:
            return True
        else:
            return False

    def OnPrintPage(self, page):
        print ("wx.Printout.OnPrintPage: %d\n" % page)
        dc = self.GetDC()

        #-------------------------------------------
        # One possible method of setting scaling factors...

        maxX = self.canvas.getWidth()
        maxY = self.canvas.getHeight()

        # Let's have at least 50 device units margin
        marginX = 50
        marginY = 50

        # Add the margin to the graphic size
        maxX = maxX + (2 * marginX)
        maxY = maxY + (2 * marginY)

        # Get the size of the DC in pixels
        (w, h) = dc.GetSizeTuple()

        # Calculate a suitable scaling factor
        scaleX = float(w) / maxX
        scaleY = float(h) / maxY

        # Use x or y scaling factor, whichever fits on the DC
        actualScale = min(scaleX, scaleY)

        # Calculate the position on the DC for centering the graphic
        posX = (w - (self.canvas.getWidth() * actualScale)) / 2.0
        posY = (h - (self.canvas.getHeight() * actualScale)) / 2.0

        # Set the scale and origin
        dc.SetUserScale(actualScale, actualScale)
        dc.SetDeviceOrigin(int(posX), int(posY))

        #-------------------------------------------

        self.canvas.DoDrawing(dc, True)
        dc.DrawText("Page: %d" % page, marginX/2, maxY-marginY)

        return True

class SortOptionsDialog(wx.Dialog):
    def __init__(self, parent):
        self.parent = parent
        lijst = ["(geen)"]
        for x in enumerate(parent.parent.ctitels):
            if x[0] == 1:
                lijst.append("Soort")
            else:
                lijst.append(x[1])

        wx.Dialog.__init__(self,parent,-1,title="Sorteren op meer dan 1 kolom", size=(450, 450), pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE)
        t1 = wx.StaticText(self, -1, "  1.", size=(20,-1))
        cmb1 = wx.ComboBox(self, -1, value="(geen)", size=(80,-1), choices=lijst, style=wx.CB_DROPDOWN) #|wxTE_PROCESS_ENTER    )
        rb1a = wx.RadioButton(self, -1, " Asc ", style = wx.RB_GROUP )
        rb1b = wx.RadioButton(self, -1, " Desc " )
        t2 = wx.StaticText(self, -1, "  2.", size=(20,-1))
        cmb2 = wx.ComboBox(self, -1, value="(geen)", size=(80,-1), choices=lijst, style=wx.CB_DROPDOWN) #|wxTE_PROCESS_ENTER    )
        rb2a = wx.RadioButton(self, -1, " Asc ", style = wx.RB_GROUP )
        rb2b = wx.RadioButton(self, -1, " Desc " )
        t3 = wx.StaticText(self, -1, "  3.", size=(20,-1))
        cmb3 = wx.ComboBox(self, -1, value="(geen)", size=(80,-1), choices=lijst, style=wx.CB_DROPDOWN) #|wxTE_PROCESS_ENTER    )
        rb3a = wx.RadioButton(self, -1, " Asc ", style = wx.RB_GROUP )
        rb3b = wx.RadioButton(self, -1, " Desc " )
        t4 = wx.StaticText(self, -1, "  4.", size=(20,-1))
        cmb4 = wx.ComboBox(self, -1, value="(geen)", size=(80,-1), choices=lijst, style=wx.CB_DROPDOWN) #|wxTE_PROCESS_ENTER    )
        rb4a = wx.RadioButton(self, -1, " Asc ", style = wx.RB_GROUP )
        rb4b = wx.RadioButton(self, -1, " Desc " )
        sizer = wx.BoxSizer(wx.VERTICAL)

        gs = wx.FlexGridSizer(4, 4, 2, 2)  # rows, cols, hgap, vgap
        gs.AddMany([ (t1,   0, wx.TOP, 5), (cmb1,   0, wx.RIGHT,10), (rb1a,   0, wx.EXPAND), (rb1b,   0, wx.EXPAND|wx.RIGHT,2),
                     (t2,   0, wx.TOP, 5), (cmb2,   0, wx.RIGHT,10), (rb2a,   0, wx.EXPAND), (rb2b,   0, wx.EXPAND|wx.RIGHT,2),
                     (t3,   0, wx.TOP, 5), (cmb3,   0, wx.RIGHT,10), (rb3a,   0, wx.EXPAND), (rb3b,   0, wx.EXPAND|wx.RIGHT,2),
                     (t4,   0, wx.TOP, 5), (cmb4,   0, wx.RIGHT,10), (rb4a,   0, wx.EXPAND), (rb4b,   0, wx.EXPAND|wx.RIGHT,2)
                 ])
        gs.AddGrowableCol(1)
        sizer.Add(gs,0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

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
    def __init__(self, parent,sel):
        # sel is de dictionary waarin de filterwaarden zitten, bv:
        # {'status': ['probleem'], 'idlt': '2006-0009', 'titel': 'x', 'soort': ['gemeld'], 'id': 'and', 'idgt': '2005-0019'}
        self.parent = parent

        wx.Dialog.__init__(self,parent,-1,title="Selecteren", size=(250, 250), pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE)
        self.cb1 = wx.CheckBox(self, -1, parent.parent.ctitels[0].join((" "," -")))
        l1a = wx.StaticText(self, -1, "groter dan:", size=(70,-1))
        self.t1a = wx.TextCtrl(self, pr.ID_T1A, "", size=(153, -1))
        self.Bind(wx.EVT_TEXT, self.OnEvtText, self.t1a)
        l1c = wx.StaticText(self, -1, "", size=(70,-1))
        self.rb1a = wx.RadioButton(self, -1, "en")
        self.rb1b = wx.RadioButton(self, -1, "of")
        l1b = wx.StaticText(self, -1, "kleiner dan:", size=(70,-1))
        self.t1b = wx.TextCtrl(self, pr.ID_T1B, "", size=(153, -1))
        self.Bind(wx.EVT_TEXT, self.OnEvtText, self.t1b)
        if "idgt" in sel: self.t1a.SetValue(sel["idgt"])
        if "id" in sel:
            if sel["id"] == "and":
                self.rb1a.SetValue(True)
            else:
                self.rb1b.SetValue(True)
        if "idlt" in sel: self.t1b.SetValue(sel["idlt"])

        self.cb2 = wx.CheckBox(self, -1, " soort -")
        l2 = wx.StaticText(self, -1, "selecteer\neen of meer:", size=(70,-1))
        h = self.parent.parent.cats.keys()
        h.sort()
        self.cl2 = wx.CheckListBox(self, pr.ID_CL2, choices=[x[0] for x in [self.parent.parent.cats[y] for y in h]])
        self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, self.cl2)
        if "soort" in sel:
            for x in self.parent.parent.cats.keys():
                if self.parent.parent.cats[x][1] in sel["soort"]: self.cl2.Check(int(x))
            self.cb2.SetValue(True)

        self.cb3 = wx.CheckBox(self, -1, parent.parent.ctitels[2].join((" "," -")))
        l3 = wx.StaticText(self, -1, "selecteer\n殚n of meer:", size=(70,-1))
        h = self.parent.parent.stats.keys()
        h.sort()
        self.cl3 = wx.CheckListBox(self, pr.ID_CL3, choices=[x[0] for x in [self.parent.parent.stats[y] for y in h]])
        self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, self.cl3)
        if "status" in sel:
            for x in self.parent.parent.stats.keys():
                if self.parent.parent.stats[x][1] in sel["status"]: self.cl3.Check(int(x))
            self.cb3.SetValue(True)

        self.cb4 = wx.CheckBox(self, -1, parent.parent.ctitels[4].join((" "," -")))
        l4 = wx.StaticText(self, -1, "zoek naar:", size=(70,-1))
        self.t4 = wx.TextCtrl(self, pr.ID_T4, "", size=(153, -1))
        self.Bind(wx.EVT_TEXT, self.OnEvtText, self.t4)
        if "titel" in sel:
            self.t4.SetValue(sel["titel"])
            self.cb4.SetValue(True)

        self.cb5 = wx.CheckBox(self, -1, "Archief")
        self.rb5a = wx.RadioButton(self, pr.ID_RB5A, "Alleen gearchiveerd")
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRBClick, self.rb5a)
        self.rb5b = wx.RadioButton(self, pr.ID_RB5B, "gearchiveerd en lopend")
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRBClick, self.rb5b)
        if "arch" in sel:
            self.cb5.SetValue(True)
            if sel["arch"] == "arch": self.rb5a.SetValue(True)
            if sel["arch"] == "alles": self.rb5b.SetValue(True)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sz01 = wx.BoxSizer(wx.HORIZONTAL)
        sz01.Add(self.rb1a,0, wx.ALIGN_CENTER_HORIZONTAL)
        sz01.Add(self.rb1b,0, wx.ALIGN_CENTER_HORIZONTAL)
        sz1 = wx.FlexGridSizer(2, 2, 2, 2)
        sz1.AddMany([ (l1a,   0, wx.TOP, 10), (self.t1a,   0, wx.TOP, 5),
                      (sz01,  0 ), (l1c,   0),
                      (l1b,   0, wx.TOP|wx.BOTTOM, 5), (self.t1b,   0, wx.BOTTOM, 5)
                 ])
        sz2 = wx.BoxSizer(wx.HORIZONTAL)
        sz2.Add(l2,0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5)
        sz2.Add(self.cl2,0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5)
        sz3 = wx.BoxSizer(wx.HORIZONTAL)
        sz3.Add(l3,0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5)
        sz3.Add(self.cl3,0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5)
        sz4 = wx.BoxSizer(wx.HORIZONTAL)
        sz4.Add(l4,0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 10)
        sz4.Add(self.t4,0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5)
        sz5 = wx.BoxSizer(wx.HORIZONTAL)
        sz5.Add(self.rb5a,0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP,10)
        sz5.Add(self.rb5b,0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP,10)

        gs = wx.FlexGridSizer(5, 2, 2, 2)  # rows, cols, hgap, vgap
        gs.AddMany([ (self.cb1,   0, wx.TOP, 10), (sz1,   0, wx.EXPAND),
                     (self.cb2,   0, wx.TOP, 5), (sz2,   0, wx.EXPAND),
                     (self.cb3,   0, wx.TOP, 5), (sz3,   0, wx.EXPAND),
                     (self.cb4,   0, wx.TOP, 10), (sz4,   0, wx.EXPAND),
                     (self.cb5,   0, wx.TOP, 10), (sz5,   0, wx.EXPAND)
                 ])
        gs.AddGrowableCol(1)
        sizer.Add(gs,0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

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

    def OnEvtText(self,evt=None):
        it = evt.GetEventObject()
        idee = evt.GetId()
        if idee == pr.ID_T1A or idee == pr.ID_T1B: it2 = self.cb1
        if idee == pr.ID_T4: it2 = self.cb4
        if evt.GetString() == "":
            it2.SetValue(False)
        else:
            it2.SetValue(True)

    def EvtCheckListBox(self,evt=None):
        index = evt.GetSelection()
        it = evt.GetEventObject()
        it.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
        idee = evt.GetId()
        if idee == pr.ID_CL2: it2 = self.cb2
        if idee == pr.ID_CL3: it2 = self.cb3
        ## print it.GetString(index)
        oneormore = False
        for x in range(it.GetCount()):
            if it.IsChecked(x):
                oneormore = True
                break
        if oneormore:
            it2.SetValue(True)
        else:
            it2.SetValue(False)

    def OnRBClick(self,evt=None):
        it = evt.GetEventObject()
        idee = evt.GetId()
        if idee == pr.ID_RB5A or idee == pr.ID_RB5B:
            self.cb5.SetValue(True)

    def SetOptions(self,evt=None):
        sel = {}
        if self.cb1.IsChecked(): #  checkbox voor "id"
            if self.t1a.GetValue() != "": #  textctrl voor groter dan
                sel["idgt"] = self.t1a.GetValue()
            if self.t1b.GetValue() != "": #  textctrl voor kleiner dan
                sel["idlt"] = self.t1b.GetValue()
            if self.rb1a.GetValue(): sel["id"] = "and"
            if self.rb1b.GetValue(): sel["id"] = "or"
        if self.cb2.IsChecked(): #  checkbox voor "soort"
            l = [self.parent.parent.cats[str(x)][1] for x in range(len(self.parent.parent.cats.keys())) if self.cl2.IsChecked(x)]
            if len(l) > 0: sel["soort"] = l
        if self.cb3.IsChecked(): #  checkbox voor "status"
            l = [self.parent.parent.stats[str(x)][1] for x in range(len(self.parent.parent.stats.keys())) if self.cl3.IsChecked(x)]
            if len(l) > 0: sel["status"] = l
        if self.cb4.IsChecked(): # checkbox voor "titel bevat"
            t = self.t4.GetValue()
            sel["titel"] = t
        if self.cb5.IsChecked(): # checkbox voor "titel bevat"
            if self.rb5a.GetValue(): sel["arch"] = "arch"
            if self.rb5b.GetValue(): sel["arch"] = "alles"
        return sel

class OptionsDialog(wx.Dialog):
    def __init__(self, parent, ID, title, size=(300,300), pos=wx.DefaultPosition,style=wx.DEFAULT_DIALOG_STYLE):
        self.parent = parent
        wx.Dialog.__init__(self,parent,-1,title,pos,size,style)
        self.initstuff()
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.elb = gizmos.EditableListBox(self, -1, self.titel, pos=(50,50), size=(250, 250) ,style= self.options)
        self.elb.SetStrings(self.data)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.elb, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "\n".join(self.tekst))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
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

class TabOptions(OptionsDialog):
    def initstuff(self):
        self.titel = "Tab titels"
        self.data = []
        h = self.parent.nb.tabs.keys()
        h.sort()
        for x in h:
            self.data.append(self.parent.nb.tabs[x].split(" ",1)[1])
        self.tekst = ["De tab titels worden getoond in de volgorde",
            "zoals ze van links naar rechts staan.",
            "Er kunnen geen tabs worden verwijderd of",
            "toegevoegd."
            ]
        self.options = gizmos.EL_ALLOW_EDIT

    def leesuit(self):
        h = self.elb.GetStrings()
        self.newtabs = {}
        for x in enumerate(h):
            self.newtabs[str(x[0])] = x[1]

class StatOptions(OptionsDialog):
    def initstuff(self):
        self.titel = "Status codes en waarden"
        self.data = []
        h = self.parent.nb.stats.keys()
        h.sort()
        for x in h:
            self.data.append(": ".join((self.parent.nb.stats[x][1],self.parent.nb.stats[x][0])))
        self.tekst = [
            "De waarden voor de status worden getoond in",
            "dezelfde volgorde als waarin ze in de combobox",
            "staan.",
            "V贸贸r de dubbele punt staat de code, erachter",
            "de waarde.",
            "Denk erom dat als je codes wijzigt of statussen",
            "verwijdert, deze ook niet meer getoond en",
            "gebruikt kunnen worden in de registratie."
            ]
        self.options = gizmos.EL_ALLOW_NEW | gizmos.EL_ALLOW_EDIT | gizmos.EL_ALLOW_DELETE

    def leesuit(self):
        h = self.elb.GetStrings()
        self.newstats = {}
        for x in enumerate(h):
            s = x[1].split(": ")
            self.newstats[s[0]] = (s[1],str(x[0]))

class CatOptions(OptionsDialog):
    def initstuff(self):
        self.titel = "Soort codes en waarden"
        self.data = []
        h = self.parent.nb.cats.keys()
        h.sort()
        for x in h:
            self.data.append(": ".join((self.parent.nb.cats[x][1],self.parent.nb.cats[x][0])))
        self.tekst = ["De waarden voor de soorten worden getoond in",
            "dezelfde volgorde als waarin ze in de combobox",
            "staan.",
            "V贸贸r de dubbele punt staat de code, erachter",
            "de waarde.",
            "Denk erom dat als je codes wijzigt of statussen",
            "verwijdert, deze ook niet meer getoond en",
            "gebruikt kunnen worden in de registratie."
            ]
        self.options = gizmos.EL_ALLOW_NEW | gizmos.EL_ALLOW_EDIT | gizmos.EL_ALLOW_DELETE

    def leesuit(self):
        h = self.elb.GetStrings()
        self.newcats = {}
        for x in enumerate(h):
            s = x[1].split(": ")
            self.newcats[s[0]] = (s[1],str(x[0]))

class MainWindow(wx.Frame):
    def __init__(self,parent,id,args):
        self.parent = parent
        self.abort = False
        self.mag_weg = True
        if len(args) == 0:
            self.fpad  = ""
        else:
            self.fpad = args[0]
            ext = os.path.splitext(self.fpad)[1]
            if ext == "" and not os.path.isdir(self.fpad):
                self.fpad += ".xml"
            elif ext != ".xml":
                self.fpad = ""
        (self.dirname,self.filename) = os.path.split(self.fpad)
        #~ print self.dirname,self.filename
        self.title = 'Actieregistratie'
        self.printer = EasyPrinter()
        self.p = self.oldbuf = None
        self.newfile = self.newitem = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []

        high = 680 if LIN else 594
        wx.Frame.__init__(self,parent,wx.ID_ANY, self.title,pos=(2,2),
                size = (588, high),
                            style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.sb = self.CreateStatusBar() # A Statusbar in the bottom of the window

    # --- menu opbouwen -----------------------------------------------------------------------------------------
        filemenu= wx.Menu()
        filemenu.Append(pr.ID_NEW, "&New (Ctrl-N)"," Create a new file")
        filemenu.Append(pr.ID_OPEN, "&Open (Ctrl-O)"," Open a new file")
        filemenu.AppendSeparator()
        submenu = wx.Menu()
        submenu.Append(pr.ID_PRINTS, "Dit &Scherm"," ")
        submenu.Append(pr.ID_PRINTA, "Deze &Actie"," ")
        filemenu.AppendMenu(-1,"&Print (Ctrl-P)", submenu) # " Print scherminhoud of actie")
        filemenu.AppendSeparator()
        filemenu.Append(pr.ID_EXIT,"&Quit (Ctrl-Q)"," Terminate the program")
        setupmenu= wx.Menu()
        submenu = wx.Menu()
        submenu.Append(pr.ID_SETFONT, "&Lettertype"," Change the size and font of the text")
        submenu.Append(pr.ID_SETCOLR, "&Kleuren"," Change the colours of various items")
        #~ submenu.Append(pr.ID_SETKEYS, "S&neltoetsen"," Change shortcut keys")
        setupmenu.AppendMenu(-1, "&Applicatie", submenu) # " Settings voor de hele applicatie")
        submenu = wx.Menu()
        submenu.Append(pr.ID_SETTABS, "  &Tabs"," Change the titles of the tabs")
        submenu.Append(pr.ID_SETCATS, "  &Soorten"," Add/change type categories")
        submenu.Append(pr.ID_SETSTATS, "  St&atussen"," Add/change status categories")
        setupmenu.AppendMenu(-1, "&Data", submenu) # " Settings voor dit specifieke meldingenbestand")
        setupmenu.Append(pr.ID_SETFOLLY, "&Het leven"," Change the way you look at life")
        helpmenu= wx.Menu()
        helpmenu.Append(pr.ID_ABOUT, "&About"," Information about this program")
        helpmenu.Append(pr.ID_KEYS, "&Keys"," List of shortcut keys")
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(setupmenu,"&Settings")
        menuBar.Append(helpmenu,"&Help")
        self.SetMenuBar(menuBar)
        self.Connect(pr.ID_NEW, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuNew)
        self.Connect(pr.ID_OPEN, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuOpen)
        self.Connect(pr.ID_PRINTS, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuPrintScherm)
        self.Connect(pr.ID_PRINTA, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuPrintActie)
        self.Connect(pr.ID_EXIT, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuExit)
        self.Connect(pr.ID_SETFONT, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuTextAttr)
        self.Connect(pr.ID_SETCOLR, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuColours)
        #~ self.Connect(pr.ID_SETKEYS, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuKeys)
        self.Connect(pr.ID_SETFOLLY, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuFolly)
        self.Connect(pr.ID_SETTABS, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuTabs)
        self.Connect(pr.ID_SETCATS, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuCats)
        self.Connect(pr.ID_SETSTATS, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuStats)
        self.Connect(pr.ID_ABOUT, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuHelpOver)
        self.Connect(pr.ID_KEYS, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.MenuHelpKeys)
        self.help = ["=== Albert's actiebox ===\n",
            "Keyboard shortcuts:",
            "    Alt left/right: verder - terug",
            "    Alt-0 t/m Alt-5: naar betreffende pagina",
            "    Alt-S op tab 1: Sorteren",
            "    Alt-F op tab 1: Filteren",
            "    Alt-G of Enter op tab 1: Ga naar aangegeven actie",
            "    Alt-N op elke tab: Nieuwe actie opvoeren",
            "    Ctrl-O: open een (ander) actiebestand",
            "    Ctrl-N: maak een nieuw actiebestand",
            "    Ctrl-P: printen (scherm of actie)",
            "    Ctrl-Q: quit actiebox",
            "    Ctrl-H: help (dit scherm)",
            "    Ctrl-S: gegevens in het scherm opslaan",
            "    Ctrl-G: oplaan en door naar volgende tab",
            "    Ctrl-Z: wijzigingen ongedaan maken"]
        self.helptext = "\n".join(self.help)
    # --- schermen opbouwen: controls plaatsen -----------------------------------------------------------------------------------------
        self.SetTitle(self.title)
        #~ self.SetIcon(wx.Icon("task.ico",wx.BITMAP_TYPE_ICO))
        self.SetIcon(images.gettaskIcon())
        #~ self.SetMinSize((476, 560))
        self.pnl = wx.Panel(self,-1)
        self.nb = wx.Notebook(self.pnl,-1)
        self.nb.parent = self
        self.nb.fnaam = ""
        self.nb.sorter = None
        self.nb.data = {}
        self.nb.rereadlist = True
        self.leesSettings()
        self.nb.ctitels = ("actie"," ","status","L.wijz.","titel")
        self.nb.currentTab = 0
        self.nb.newitem = False
        self.nb.currentItem = 0
        self.nb.p = None
        #~ self.nb.SetMinSize((486,496))
        self.nb.page0 = Page0(self.nb, -1)
        self.nb.page1 = Page1(self.nb, -1)
        self.nb.page2 = Page(self.nb, -1)
        self.nb.page3 = Page(self.nb, -1)
        self.nb.page4 = Page(self.nb, -1)
        self.nb.page5 = Page(self.nb, -1)
        self.nb.page6 = Page6(self.nb, -1)
        self.nb.pages = 6
        self.exitButton = wx.Button(self.pnl, id=wx.ID_EXIT)
        self.Bind(wx.EVT_BUTTON, self.MenuExit , self.exitButton)
        self.nb.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        self.nb.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.nb.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

    # --- schermen opbouwen: layout -----------------------------------------------------------------------------------------
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        self.nb.AddPage(self.nb.page0, "&" + self.nb.tabs[0])
        self.nb.page0.doelayout()
        self.nb.AddPage(self.nb.page1, "&" + self.nb.tabs[1])
        self.nb.page1.doelayout()
        self.nb.AddPage(self.nb.page2, "&" + self.nb.tabs[2])
        self.nb.page2.doelayout()
        self.nb.AddPage(self.nb.page3, "&" + self.nb.tabs[3])
        self.nb.page3.doelayout()
        self.nb.AddPage(self.nb.page4, "&" + self.nb.tabs[4])
        self.nb.page4.doelayout()
        self.nb.AddPage(self.nb.page5, "&" + self.nb.tabs[5])
        self.nb.page5.doelayout()
        self.nb.AddPage(self.nb.page6, "&" + self.nb.tabs[6])
        self.nb.page6.doelayout()
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.nb,1,wx.EXPAND)
        sizer0.Add(sizer1,1,wx.EXPAND)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(self.exitButton,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,4)
        sizer0.Add(sizer2,0,wx.EXPAND )
        self.pnl.SetSizer(sizer0)
        self.pnl.SetAutoLayout(True)
        sizer0.Fit(self.pnl)
        sizer0.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.Show(True)
        if self.filename == "":
            self.MenuOpen(None)
        else:
            self.startfile()

    def MenuNew(self,e):
        """Start a new file"""
        self.newfile = False
        self.dirname = os.getcwd()
        dlg = wx.FileDialog(self,self.title + " - nieuw gegevensbestand",self.dirname, "", "XML files|*.xml", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.newfile = True
            self.startfile()
            self.newfile = False
        dlg.Destroy()

    def MenuOpen(self,e):
        """ Open a file"""
        self.dirname = os.getcwd()
        dlg = wx.FileDialog(self, self.title + " - kies een gegevensbestand", self.dirname, "", "XML files|*.xml", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.startfile()
        dlg.Destroy()

    def MenuPrintScherm(self,e=None):
        self.text = []
        self.hdr = ("Actie: %s %s" % (self.nb.p.id,self.nb.p.titel))
        if self.nb.currentTab == 0:
            self.hdr = "Overzicht acties uit " + self.filename
            self.text.append("<table>")
            for x in range(len(self.nb.data.items())):
                y = self.nb.page0.p0list.GetItemData(x)
                p1 = self.nb.data[y][0]
                p2 = self.nb.data[y][1]
                p3 = self.nb.data[y][2]
                p4 = self.nb.data[y][3]
                p5 = self.nb.data[y][5]
                p6 = self.nb.data[y][4]
                if p6 != "":
                    p6 = "".join((", laatst behandeld op ",p6))
                h = p4.split(".")
                if h[0] != "0":
                    p6 = "status: %s%s" % (h[1],p6)
                else:
                    p6 = ""
                self.text.append('<tr><td>%s&nbsp;&nbsp;</td><td>%s</td></tr><tr><td></td><td>%s gemeld op %s<br>%s</td></tr>' % (p1,p5,p3.split(".")[1],p2,p6))
            self.text.append("</table>")
        elif self.nb.currentTab == 1:
            self.hdr = ("Informatie over actie %s: samenvatting" % self.nb.page1.txtId.GetValue()) # self.nb.p.id)
            self.text.append("<table>")
            self.text.append("<tr><td>Actie:</td><td>%s</td></tr>" % self.nb.page1.txtId.GetValue()) # self.nb.p.id)
            self.text.append("<tr><td>Gemeld op:</td><td>%s</td></tr>" % self.nb.page1.txtDat.GetValue()) # self.nb.p.datum)
            ## h = self.nb.p.titel.split(": ",1)
            h = (self.nb.page1.txtPrc.GetValue(),self.nb.page1.txtMld.GetValue())
            self.text.append("<tr><td>Betreft:</td><td>%s</td></tr>" % h[0])
            self.text.append("<tr><td>Melding:</td><td>%s</td></tr>" % h[1])
            ## h = "(onbekende soort)"
            ## for x in self.nb.cats.values():
                ## if x[1] == self.nb.p.soort:
                    ## h = x[0]
                    ## break
            h = self.nb.page1.cmbCat.GetValue()
            self.text.append("<tr><td>Soort actie:</td><td>%s</td></tr>" % h)
            ## h = "(onbekende status)"
            ## for x in self.nb.stats.values():
                ## if x[1] == self.nb.p.status:
                    ## h = x[0]
                    ## break
            h = self.nb.page1.cmbStat.GetValue()
            self.text.append("<tr><td>Status:</td><td>%s</td></tr>" % h)
            self.text.append("</table>")
        elif self.nb.currentTab == 2:
            t = self.nb.page2.text1.GetValue()
            ## t = self.nb.p.melding
            if t is not None:
                self.text.append("<u>%s</u><br>" % self.nb.tabs[2].split(None,1)[1])
                self.text.append("<p>%s</p>" % self.nb.p.melding.replace('\n', '<br>'))
        elif self.nb.currentTab == 3:
            t = self.nb.page2.text1.GetValue()
            ## t = self.nb.p.oorzaak
            if t is not None:
                self.text.append("<u>%s</u><br>" % self.nb.tabs[3].split(None,1)[1])
                self.text.append("<p>%s</p>" % self.nb.p.oorzaak.replace('\n', '<br>'))
        elif self.nb.currentTab == 4:
            t = self.nb.page2.text1.GetValue()
            ## t = self.nb.p.oplossing
            if t is not None:
                self.text.append("<u>%s</u><br>" % self.nb.tabs[4].split(None,1)[1])
                self.text.append("<p>%s</p>" % self.nb.p.oplossing.replace('\n', '<br>'))
        elif self.nb.currentTab == 5:
            t = self.nb.page2.text1.GetValue()
            ## t = self.nb.p.vervolg
            if t is not None:
                self.text.append("<u>%s</u><br>" % self.nb.tabs[5].split(None,1)[1])
                self.text.append("<p>%s</p>" % self.nb.p.vervolg.replace('\n', '<br>'))
        elif self.nb.currentTab == 6:
            print self.nb.tabs
            self.text.append("<u>%s</u><br>" % self.nb.tabs[6].split(None,1)[1])
            t = self.nb.p.stand
            t = self.nb.page6.txtStat.GetValue()
            if t is not None:
                self.text.append("<p>%s</p>" % t.replace('\n', '<br>'))
            ## if len(self.nb.p.events) > 0:
                ## for x in self.nb.p.events:
                    ## self.text.append("<p><b>%s</b><br>%s</p>" % (x[0].replace('\n', '<br>'),x[1].replace('\n', '<br>')))
            if len(self.nb.page6.elijst) > 0:
                for x in enumerate(self.nb.page6.elijst):
                    self.text.append("<p><b>%s</b><br>%s</p>" % (x[1].replace('\n', '<br>'),self.nb.page6.edata[x[0]].replace('\n', '<br>')))
        self.afdrukken()

    def MenuPrintActie(self,e=None):
        if self.nb.p is None or self.nb.newitem:
            # afbreken met melding geen actie geselecteerd
            d = wx.MessageDialog(self,
                "Wel eerst een actie kiezen om te printen",
                self.parent.parent.title,
                wx.ICON_EXCLAMATION
            )
            d.ShowModal()
            d.Destroy()
            return
        self.hdr = ("Actie: %s %s" % (self.nb.p.id,self.nb.p.titel))
        self.text = ["<table>"]
        self.text.append("<tr><td>Actie:</td><td>%s</td></tr>" % self.nb.p.id)
        self.text.append("<tr><td>Gemeld op:</td><td>%s</td></tr>" % self.nb.p.datum)
        h = self.nb.p.titel.split(": ",1)
        self.text.append("<tr><td>Betreft:</td><td>%s</td></tr>" % h[0])
        self.text.append("<tr><td>Melding:</td><td>%s</td></tr>" % h[1])
        h = "(onbekende soort)"
        for x in self.nb.cats.values():
            if x[1] == self.nb.p.soort:
                h = x[0]
                break
        self.text.append("<tr><td>Soort actie:</td><td>%s</td></tr>" % h)
        h = "(onbekende status)"
        for x in self.nb.stats.values():
            if x[1] == self.nb.p.status:
                h = x[0]
                break
        self.text.append("<tr><td>Status:</td><td>%s</td></tr>" % h)
        self.text.append("</table>")
        self.text.append("<hr>")
        self.text.append("<b>%s</b><p>" % self.nb.tabs[2].split(None,1)[1])
        if self.nb.p.melding is not None:
            self.text.append(self.nb.p.melding.replace('\n', '<br>'))
        else:
            self.text.append("(nog niet beschreven)")
        self.text.append("</p><hr>")
        self.text.append("<b>%s</b><p>" % self.nb.tabs[3].split(None,1)[1])
        if self.nb.p.oorzaak is not None:
            self.text.append(self.nb.p.oorzaak.replace('\n', '<br>'))
        else:
            self.text.append("(nog niet beschreven)")
        self.text.append("</p><hr>")
        self.text.append("<b>%s</b><p>" % self.nb.tabs[4].split(None,1)[1])
        if self.nb.p.oplossing is not None:
            self.text.append(self.nb.p.oplossing.replace('\n', '<br>'))
        else:
            self.text.append("(nog niet beschreven)")
        self.text.append("</p>")
        if self.nb.p.vervolg is not None:
            self.text.append("<hr>")
            self.text.append("<b>%s</b><p>" % self.nb.tabs[5].split(None,1)[1])
            self.text.append(self.nb.p.vervolg.replace('\n', '<br>'))
            self.text.append("</p>")
        if self.nb.p.stand is not None:
            self.text.append("<hr>")
            self.text.append("<b>%s</b><p>" % self.nb.tabs[6].split(None,1)[1])
            self.text.append(self.nb.p.stand.replace('\n', '<br>'))
            if len(self.nb.p.events) > 0:
                for x in self.nb.p.events:
                    self.text.append("<br><br><b>%s</b><br>%s</p>" % (x[0].replace('\n', '<br>'),x[1].replace('\n', '<br>')))
            self.text.append("</p>")
        self.afdrukken()

    def MenuExit(self,e=None):
        self.abort = True
        if self.nb.currentTab == 0:
            self.nb.page0.leavep()
        elif self.nb.currentTab == 1:
            self.nb.page1.leavep()
        elif self.nb.currentTab == 2:
            self.nb.page2.leavep()
        elif self.nb.currentTab == 3:
            self.nb.page3.leavep()
        elif self.nb.currentTab == 4:
            self.nb.page4.leavep()
        elif self.nb.currentTab == 5:
            self.nb.page5.leavep()
        elif self.nb.currentTab == 6:
            self.nb.page6.leavep()
        self.Close(True)

    def MenuTabs(self,e):
        d = TabOptions(self,-1,"Wijzigen tab titels", size=(350, 200), style = wx.DEFAULT_DIALOG_STYLE)
        if d.ShowModal() == wx.ID_OK:
            d.leesuit()
            self.saveSettings("tab",d.newtabs)
        d.Destroy()

    def MenuStats(self,e):
        d = StatOptions(self,-1,"Wijzigen statussen", size=(350, 200), style = wx.DEFAULT_DIALOG_STYLE)
        if d.ShowModal() == wx.ID_OK:
            d.leesuit()
            self.saveSettings("stat",d.newstats)
        d.Destroy()

    def MenuCats(self,e):
        d = CatOptions(self,-1,"Wijzigen categorieen", size=(350, 200), style = wx.DEFAULT_DIALOG_STYLE)
        if d.ShowModal() == wx.ID_OK:
            d.leesuit()
            self.saveSettings("cat",d.newcats)
        d.Destroy()

    def MenuTextAttr(self,e):
        d= wx.MessageDialog( self, "Sorry, werkt nog niet", "Oeps", wx.OK)  # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.
        return
        data = wx.FontData()
        data.EnableEffects(True)
        data.SetColour(self.curClr)         # set colour
        data.SetInitialFont(self.curFont)

        dlg = wx.FontDialog(self, data)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            colour = data.GetColour()

            self.log.WriteText('You selected: "%s", %d points, color %s\n' %
                               (font.GetFaceName(), font.GetPointSize(),
                                colour.Get()))

            self.curFont = font
            self.curClr = colour

            #~ self.sampleText.SetFont(self.curFont)
            #~ self.ps.SetLabel(str(self.curFont.GetPointSize()))
            #~ self.family.SetLabel(self.curFont.GetFamilyString())
            #~ self.style.SetLabel(self.curFont.GetStyleString())
            #~ self.weight.SetLabel(self.curFont.GetWeightString())
            #~ self.face.SetLabel(self.curFont.GetFaceName())
            #~ self.nfi.SetLabel(self.curFont.GetNativeFontInfo().ToString())
            #~ self.Layout()

        # Don't destroy the dialog until you get everything you need from the
        # dialog!
        dlg.Destroy()

    def MenuColours(self,e):
        d= wx.MessageDialog( self, "Sorry, werkt nog niet", "Oeps", wx.OK)  # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.

    def MenuKeys(self,e):
        d= wx.MessageDialog( self, "Sorry, werkt nog niet", "Oeps", wx.OK)  # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.

    def MenuHelpOver(self,e):
        wx.MessageBox("wxPython versie van mijn actiebox","Help",wx.ICON_INFORMATION)

    def MenuHelpKeys(self,e):
        wx.MessageBox(self.helptext,"Help")

    def MenuFolly(self,e):
        wx.MessageBox("Yeah you wish...\nHet leven is niet in te stellen helaas","Haha")

    def startfile(self):
        f = os.path.join(self.dirname,self.filename)
        h = checkfile(f,self.newfile)
        if h != '':
            wx.MessageBox(h,"Oeps")
            return
        self.nb.fnaam = f
        self.title = self.filename
        self.nb.rereadlist = True
        self.nb.sorter = None
        self.leesSettings()
        for x in self.nb.tabs.keys():
            self.nb.SetPageText(x,self.nb.tabs[x])
        self.nb.page0.sel = {}
        self.nb.page1.VulCombos()
        if self.nb.currentTab == 0:
            self.nb.page0.vulp()
        else:
            self.nb.SetSelection(0)

    def leesSettings(self):
        h = Settings(self.nb.fnaam)
        self.nb.stats = {}
        self.nb.cats = {}
        self.nb.tabs = {}
        self.nb.pagehelp = ["Overzicht van alle acties",
        "Identificerende gegevens van de actie",
        "Beschrijving van het probleem of wens",
        "Analyse van het probleem of wens",
        "Voorgestelde oplossing",
        "Eventuele vervolgactie(s)",
        "Overzicht stand van zaken"]
        for x in h.stat.keys():
            self.nb.stats[h.stat[x][1]] = (h.stat[x][0],x)
        for x in h.cat.keys():
            self.nb.cats[h.cat[x][1]] = (h.cat[x][0],x)
        for x in h.kop.keys():
            self.nb.tabs[int(x)] = x + " " + h.kop[x]
            #~ self.nb.pagehelp.append(...)
            if 6 not in self.nb.tabs:
                h.kop["6"] = "Voortgang"
                self.nb.tabs[6] = "6 Voortgang"

    def saveSettings(self,srt,d):
        h = Settings(self.nb.fnaam)
        if srt == "tab":
            h.kop = d
            h.write()
            self.nb.tabs = {}
            for x in d.keys():
                #~ if type(x) is str: x = int(x)
                self.nb.tabs[x] = d[x]
                self.nb.SetPageText(int(x)," ".join((x,self.nb.tabs[x])))
        elif srt == "stat":
            h.stat = d
            h.write()
            self.nb.stats = d
            self.nb.page1.cmbStat.Clear()
            for x in self.nb.stats.keys():
                y = self.nb.stats[x]
                self.nb.page1.cmbStat.Append(y[0],y[1])
        elif srt == "cat":
            h.cat = d
            h.write()
            self.nb.cats = d
            self.nb.page1.cmbCat.Clear()
            for x in self.nb.cats.keys():
                y = self.nb.cats[x]
                self.nb.page1.cmbCat.Append(y[0],y[1])
        else:
            pass

    def OnKeyPress(self,evt):
        """
        met behulp van deze methode wordt vanaf globaal (applicatie) niveau dezelfde
        toetsenafhandelingsroutine aangeroepen als vanaf locaal (tab) niveau
        """
        ## print "main.onkeypress"
        keycode = evt.GetKeyCode()
        if self.nb.currentTab == 0:
            self.nb.page0.OnKeyPress(evt)
        elif self.nb.currentTab == 1:
            self.nb.page1.OnKeyPress(evt)
        elif self.nb.currentTab == 2:
            self.nb.page2.OnKeyPress(evt)
        elif self.nb.currentTab == 3:
            self.nb.page3.OnKeyPress(evt)
        elif self.nb.currentTab == 4:
            self.nb.page4.OnKeyPress(evt)
        elif self.nb.currentTab == 5:
            self.nb.page5.OnKeyPress(evt)
        elif self.nb.currentTab == 6:
            self.nb.page6.OnKeyPress(evt)
        evt.Skip()

    def OnPageChanging(self, event):
        """
        deze methode is bedoeld om wanneer er van pagina gewisseld gaat worden
        te controleren of dat wel mogelijk is en zo niet, te melden waarom en de
        paginawissel tegen te houden.
        """
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.nb.GetSelection()
        ## print ('OnPageChanging, old:%d, new:%d, sel:%d' % (old, new, sel))
        ## print "on pagechanging, check self.mag_weg",self.mag_weg
        m = ""
        if old == -1:
            pass
        elif self.nb.fnaam == "":
            m = "Kies eerst een bestand om mee te werken"
            self.mag_weg = False
        elif len(self.nb.data) == 0 and not self.nb.newitem:
            m = "Voer eerst 茅茅n of meer acties op"
            self.mag_weg = False
        elif self.nb.currentItem == -1 and not self.nb.newitem:
            m = "Selecteer eerst een actie"
            self.mag_weg = False
        if not self.mag_weg:
            if m != "":
                d = wx.MessageDialog(self,m,"Navigatie niet toegestaan",wx.ICON_ERROR)
                d.ShowModal()
                d.Destroy()
            self.nb.SetSelection(old)
            event.Veto()
        else:
            event.Skip()

    def OnPageChanged(self, event):
        """
        deze methode is bedoeld om bij het wisselen van pagina het veld / de velden
        van de nieuwe pagina een waarde te geven met behulp van de vulp methode
        """
        old = event.GetOldSelection()
        new = self.nb.currentTab = event.GetSelection()
        sel = self.nb.GetSelection()
        ## print ('OnPageChanged,  old:%d, new:%d, sel:%d' % (old, new, sel))
        ## print len(self.nb.data)
        ## print len(self.nb.data.items())
        if new == 0:
            self.nb.page0.vulp()
        elif new == 1:
            self.nb.page1.vulp()
        elif new == 2:
            self.nb.page2.vulp()
        elif new == 3:
            self.nb.page3.vulp()
        elif new == 4:
            self.nb.page4.vulp()
        elif new == 5:
            self.nb.page5.vulp()
        elif new == 6:
            self.nb.page6.vulp()
        event.Skip()

    def OnLeftDown(self,event):
        """
        deze methode is bedoeld om te bepalen of er op een tab is geklikt en op
        welke, en om de "leave" methode van de betreffende tab aan te roepen.
        """
        self.x = event.GetX()
        self.y = event.GetY()
        item, flags = self.nb.HitTest((self.x, self.y))
        if flags != wx.NOT_FOUND:
            ## print 'LeftDown op',self.nb.currentTab # item,flags
            self.mag_weg = True
            if self.nb.currentTab == 0:
                self.mag_weg = self.nb.page0.leavep()
            elif self.nb.currentTab == 1:
                self.mag_weg = self.nb.page1.leavep()
            elif self.nb.currentTab == 2:
                self.mag_weg = self.nb.page2.leavep()
            elif self.nb.currentTab == 3:
                self.mag_weg = self.nb.page3.leavep()
            elif self.nb.currentTab == 4:
                self.mag_weg = self.nb.page4.leavep()
            elif self.nb.currentTab == 5:
                self.mag_weg = self.nb.page5.leavep()
            elif self.nb.currentTab == 6:
                self.mag_weg = self.nb.page6.leavep()
            ## print self.mag_weg
        ## print "einde OnLeftDown"
        event.Skip()

    def OnLeftUp(self,event):
        if self.mag_weg:
            self.zetfocus(self.nb.currentTab)
        event.Skip()

    def zetfocus(self,n):
        ## print "zetfocus called"
        #~ self.setFocus()
        if n == 0:
            self.nb.page0.p0list.SetFocus()
        elif n == 1:
            self.nb.page1.txtPrc.SetFocus()
        elif n == 2:
            self.nb.page2.text1.SetFocus()
        elif n == 3:
            self.nb.page3.text1.SetFocus()
        elif n == 4:
            self.nb.page4.text1.SetFocus()
        elif n == 5:
            self.nb.page5.text1.SetFocus()
        ## elif n == 6:
            ## self.nb.page6.txtStat.SetFocus()


    def afdrukken(self):
        self.css = ""
        if self.css != "":
            self.css = "".join(("<style>",self.css,"</style>"))
        self.text.insert(0,"".join(("<html><head><title>titel</title>",self.css,"</head><body>")))
        self.text.append("</body></html>")
        self.printer.Print("".join(self.text),self.hdr)
        return
        # de moelijke manier
        data = wx.PrintDialogData()
        data.EnableSelection(False)
        data.EnablePrintToFile(True)
        data.EnablePageNumbers(False)
        data.SetAllPages(True)
        dlg = wx.PrintDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            pdd = dlg.GetPrintDialogData()
            prt = wxPrinter(pdd)
            pda = Prtdata(self.textcanvas)
            if not prt.Print(self,prtdata,False):
                MessageBox("Unable to print the document.")
            prt.Destroy()
        dlg.Destroy()

def main(args):
    app = wx.App(redirect=False)
    frame = MainWindow(None, -1, args[1:])
    app.MainLoop()
if __name__ == '__main__':
    main(sys.argv)
    ## h = raw_input('...')
