#! C:/python26/python
# -*- coding: UTF-8 -*-

import sys, os
if os.name == 'ce':
    import ppygui as gui
    DESKTOP = False
    import pr_globals as pr
else:
    import ppygui.api as gui
    DESKTOP = True
    import pr_globals_ppg as pr
## import images
import dml
import templates as tpl

class SortOptionsDialog(gui.Dialog):
    def __init__(self,_nb):
        gui.Dialog.__init__(self,title="Sorteren",
            action=("Cancel", self.on_cancel))
        self.sippref = gui.SIPPref(self)
        lbl = gui.Label(self,"\n".join((
            "geef hieronder aan op welke kolom(men) er",
            "achtereenvolgens gesorteerd moet worden",
            "en hoe")))
        lijst = ["(geen)"]
        for x in enumerate(_nb.ctitels):
            if x[0] == 1:
                lijst.append("Soort")
            else:
                lijst.append(x[1])
        widgets = []
        self.cmblist = []
        self.rbglist = []
        for tel in range(4):
            t = gui.Label(self, "  %s." % tel)
            cmb = gui.Combo(self, style="list", choices=lijst)
            cmb.selection = 0
            rbg = gui.RadioGroup()
            rba = gui.RadioButton(self, " Asc ", value=True, group=rbg)
            rbb = gui.RadioButton(self, " Desc ", value=False, group=rbg)
            widgets.append((t,cmb,rba,rbb))
            self.cmblist.append(cmb)
            self.rbglist.append(rbg)

        sizer = gui.VBox()
        hsizer = gui.HBox()
        hsizer.add(gui.Spacer(x=10,y=1))
        hsizer.add(lbl)
        sizer.add(hsizer)
        sizer.add(gui.Spacer(y=10,x=1))
        ts = gui.TBox(4, 4, (25,-1,-1,-1), spacing_x=5, spacing_y=5)
        for wdgs in widgets:
            for wdg in wdgs:
                ts.add(wdg)
        sizer.add(ts)
        sizer.add(gui.Spacer(y=10,x=1))
        hsizer = gui.HBox(spacing=5)
        self.bOk = gui.Button(self,title='Ok',action=self.on_ok)
        self.bCancel = gui.Button(self,title='Cancel',action=self.on_cancel)
        hsizer.add(gui.Spacer(x=70))
        hsizer.add(self.bOk)
        hsizer.add(self.bCancel)
        sizer.add(hsizer)
        sizer.add(gui.Spacer())

        self.sizer = sizer

    def on_ok(self,ev=None):
        self._parent.data = []
        for ix,cmb in self.cmblist:
            self._parent.data.append((cmb[cmb.selection],self.rbglist[ix]))
        self.end('ok')

    def on_cancel(self,ev=None):
        self.end('cancel')

class SelectOptionsDialog(gui.Dialog):
    def __init__(self,sel,_nb):
        # sel is de dictionary waarin de filterwaarden zitten, bv:
        # {'status': ['probleem'], 'idlt': '2006-0009', 'titel': 'x', 'soort': ['gemeld'], 'id': 'and', 'idgt': '2005-0019'}
        gui.Dialog.__init__(self, title="Selecteren",
            action=("Cancel", self.on_cancel))
        self.sippref = gui.SIPPref(self)

        self.cb_actie = gui.Button(self, style="check",
            title=_nb.ctitels[0].join((" "," -")))
        lbl_gt = gui.Label(self, "groter dan:")
        self.txt_gt = gui.Edit(self, "")
        self.txt_gt.bind(update=self.OnEvtText)
        ## l1c = gui.Spacer(self, "", size=(70,-1))
        self.rg_enof = gui.RadioGroup()
        self.rb_en = gui.RadioButton(self, "en", group=self.rg_enof)
        self.rb_of = gui.RadioButton(self, "of", group=self.rg_enof)
        lbl_lt = gui.Label(self, "kleiner dan:")
        self.txt_lt = gui.Edit(self, "")
        self.txt_lt.bind(update=self.OnEvtText)
        if "idgt" in sel:
            self.txt_gt.select_all()
            self.txt_gt.selection = sel["idgt"]
        if "id" in sel:
            if sel["id"] == "and":
                self.rg_enof.selection = self.rb_en
            else:
                self.rg_enof.selection = self.rb_of
        if "idlt" in sel:
            self.txt_lt.select_all()
            self.txt_lt.selection = sel["idlt"]

        self.cb_soort = gui.Button(self, " soort -", style="check")
        lbl_soort = gui.Label(self, "selecteer\neen of meer:\n")
        h = _nb.cats.keys()
        h.sort()
        self.lb_soort = gui.List(self,multiple=True)
        ## self.ch_soort = []
        for choice in [x[0] for x in [_nb.cats[y] for y in h]]:
            ## cb = gui.Button(self, title=choice, style="check")
            ## cb.bind(clicked=self.EvtCheckListBox)
            ## self.ch_soort.append(cb)
            self.lb_soort.append(choice)
        self.lb_soort.selection = []
        if "soort" in sel:
            for x in _nb.cats.keys():
                if _nb.cats[x][1] in sel["soort"]:
                    ## # self.ch_soort[int(x)].checked = True
                    self.lb_soort.selection.append(int(x))
            ## # self.cb_soort.checked = True

        self.cb_stat = gui.Button(self, style="check",
            title=_nb.ctitels[2].join((" "," -")))
        lbl_stat = gui.Label(self, "selecteer\neen of meer:\n")
        h = _nb.stats.keys()
        h.sort()
        self.lb_stat = gui.List(self,multiple=True)
        ## self.ch_mut = []
        for choice in [x[0] for x in [_nb.stats[y] for y in h]]:
            ## cb = gui.Button(self, title=choice, style="check")
            ## cb.bind(clicked=self.EvtCheckListBox)
            ## self.ch_mut.append(cb)
            self.lb_stat.append(choice)
        self.lb_stat.selection = []
        if "status" in sel:
            for x in _nb.stats.keys():
                if _nb.stats[x][1] in sel["status"]:
                    ## # self.ch_mut[int(x)].checked = True
                    self.lb_mut.selection.append(int(x))
            ## # self.cb_mut.checked = True

        self.cb_mut = gui.Button(self, style="check",
            title=_nb.ctitels[4].join((" "," -")))
        lbl_mut = gui.Label(self, "zoek naar:")
        self.txt_mut = gui.Edit(self, "")
        self.txt_mut.bind(update=self.OnEvtText)
        if "titel" in sel:
            self.txt_mut.setvalue(sel["titel"])
            self.cb_mut.checked = True

        self.cb_arch = gui.Button(self, title="Archief - ", style="check")
        self.rg_arch = gui.RadioGroup()
        self.rb_arch = gui.RadioButton(self, "Alleen gearchiveerd", group=self.rg_arch)
        self.rb_arch.bind(clicked=self.OnRBClick)
        self.rb_alles = gui.RadioButton(self, "gearchiveerd en lopend", group=self.rg_arch)
        self.rb_alles.bind(clicked=self.OnRBClick)
        if "arch" in sel:
            self.cb_arch.checked = True
            if sel["arch"] == "arch":
                self.rg_arch.selection = rb_arch
            if sel["arch"] == "alles":
                self.rg_arch.selection = rb_alles

        sizer = gui.VBox()
        sizer.add(gui.Spacer(y=5))
        sz0 = gui.HBox()
        sz1 = gui.VBox()
        sz1.add(self.cb_actie,border=(0,-1,-1,-1))
        sz0.add(sz1)
        sz1 = gui.TBox(3,2) # 2,3)
        # sz1.add(gui.Button(self,style="check"))
        sz1.add(lbl_gt)
        sz1.add(self.txt_gt)
        sz2 = gui.HBox()
        sz2.add(self.rb_en)
        sz2.add(self.rb_of)
        sz1.add(sz2)
        sz1.add(gui.Spacer(x=1,y=1))
        # sz1.add(gui.Button(self,style="check"))
        sz1.add(lbl_lt)
        sz1.add(self.txt_lt)
        sz0.add(sz1)
        sizer.add(sz0)
        sizer.add(gui.Spacer(y=10))
        sz0 = gui.HBox()
        sz1 = gui.VBox()
        sz1.add(self.cb_soort,border=(0,-1,-1,-1))
        sz0.add(sz1)
        sz0.add(lbl_soort)
        sz0.add(self.lb_soort)
        sizer.add(sz0)
        sizer.add(gui.Spacer(y=5))
        sz0 = gui.HBox()
        sz1 = gui.VBox()
        sz1.add(self.cb_stat,border=(0,-1,-1,-1))
        sz0.add(sz1)
        sz0.add(lbl_stat)
        sz0.add(self.lb_stat)
        sizer.add(sz0)
        sizer.add(gui.Spacer(y=5))
        sz0 = gui.HBox()
        sz1 = gui.VBox()
        sz1.add(self.cb_mut,border=(0,-1,-1,-1))
        sz0.add(sz1)
        sz0.add(lbl_mut)
        sz0.add(self.txt_mut)
        sizer.add(sz0)
        sizer.add(gui.Spacer(y=10))
        sz0 = gui.HBox()
        sz1 = gui.VBox()
        sz1.add(self.cb_arch,border=(0,-1,-1,-1))
        sz0.add(sz1)
        sz1 = gui.VBox()
        sz1.add(self.rb_arch)
        sz1.add(self.rb_alles)
        sz0.add(sz1)
        sizer.add(sz0)
        sizer.add(gui.Spacer(y=5))

        bsz=gui.HBox(spacing=5)
        bsz.add(gui.Spacer(x=80))
        btn = gui.Button(self, title='OK',action=self.on_ok)
        bsz.add(btn)
        btn = gui.Button(self,title='Cancel',action=self.on_cancel)
        bsz.add(btn)
        sizer.add(bsz)

        self.sizer = sizer

    def on_ok(self,ev=None):
        self._parent.data = []
        self.end('ok')

    def on_cancel(self,ev=None):
        self.end('cancel')

    def OnEvtText(self,evt=None):
        ew = evt.window
        if ew in (self.txt_gt,self.txt_lt):
            it = self.cb_actie
        elif ew == self.txt_stat:
            it = self.cb_stat
        ew.select_all()
        if ew.selection():
            it.checked = True
        else:
            it.checked = False

    def EvtCheckListBox(self,evt=None):
        ew = evt.window
        if ew in self.cl_soort:
            el = self.cl_soort
            it = self.cb_soort
        elif ew == pr.cl_mut:
            el = self.cl_mut
            it = self.cb_mut
        oneormore = False
        for cb in el:
            if cb.checked:
                oneormore = True
                break
        if oneormore:
            it.checked = True
        else:
            it.checked = False

    def OnRBClick(self,evt=None):
        ew = evt.window
        if ew in (self.rb_arch,self.rb_alles):
            self.cb_arch.setvalue(True)

    def SetOptions(self,evt=None):
        sel = {}
        if self.cb_actie.checked: #  checkbox voor "id"
            self.txt_gt.select_all()
            if self.txt_gt.selection: #  Edit voor groter dan
                sel["idgt"] = self.t1a.getvalue()
            if self.txt_lt.selection: #  Edit voor kleiner dan
                sel["idlt"] = self.t1b.getvalue()
            if self.rg_enof.selection == self.rb_en:
                sel["id"] = "and"
            elif self.rg_enof.selection == self.rb_of:
                sel["id"] = "or"
        if self.cb_soort_checked: #  checkbox voor "soort"
            l = [self.parent.parent.cats[str(x)][1]
                for x in range(len(self.parent.parent.cats.keys()))
                    if self.ch_soort[x].checked]
            if l:
                sel["soort"] = l
        if self.cb_mut_checked: #  checkbox voor "laatste mutatie"
            l = [self.parent.parent.stats[str(x)][1]
                for x in range(len(self.parent.parent.stats.keys()))
                    if self.ch_mut[x].checked]
            if l:
                sel["status"] = l
        if self.cb_stat_checked(): # checkbox voor "status"
            self.txt_stat.select_all()
            sel["titel"] = self.stat.selection
        if self.cb_arch_checked: # checkbox voor "gearchiveerd"
            if self.rb_arch_checked:
                sel["arch"] = "arch"
            elif self.rb_alles_checked:
                sel["arch"] = "alles"
        return sel

class OptionsDialog(gui.Dialog):
    """
    listbox
    buttons: move selected up/down, new, edit/delete selected
    big label
    ok/cancel button
    """
    def __init__(self, parent, **kwargs):
        titel = kwargs.get('titel',"")
        ## print titel
        optlist = kwargs.get('keuzes',"")
        ## print optlist
        opttext = kwargs.get('tekst',"")
        ## print opttext
        max = kwargs.get('max',"")
        self.parrent = parent
        gui.Dialog.__init__(self, titel,
            action=("Cancel", self.on_cancel))
        self.sippref = gui.SIPPref(self)

        self.lb_options = gui.List(self)
        h = optlist.keys()
        h.sort()
        for x in h:
            # bij Tabs is dit bv. '1 Titel/Status'
            # bij de andere is dit bv. ('probleem','P')
            try:
                self.lb_options.append(optlist[x].split(" ",1)[1])
            except AttributeError:
                self.lb_options.append(optlist[x][0])
        self.btnlist = (
            gui.Button(self, "Edit"), # "Update in List"),
            gui.Button(self, "Move Up"),
            gui.Button(self, "Move Down"),
            gui.Button(self, "New"),
            gui.Button(self, "Delete"),
            )
        self.btnlist[0].bind(clicked=self.edit)
        self.btnlist[1].bind(clicked=self.moveup)
        self.btnlist[2].bind(clicked=self.movedn)
        self.btnlist[3].bind(clicked=self.new)
        self.btnlist[4].bind(clicked=self.delete)
        self.txt_option = gui.Edit(self)
        self.lbl_options = gui.Label(self,"\n".join([x.decode('latin-1') for x in opttext]))

        sizer = gui.VBox()

        box = gui.HBox()
        box.add(self.lb_options)
        sizer.add(box)

        box = gui.HBox()
        for btn in self.btnlist[:max]:
            box.add(btn)
        sizer.add(box)

        box = gui.HBox()
        box.add(self.txt_option)
        sizer.add(box)

        box = gui.HBox()
        box.add(self.lbl_options)
        sizer.add(box)

        hsizer = gui.HBox()
        self.bOk = gui.Button(self,title='Save',action=self.on_ok)
        self.bCancel = gui.Button(self,title='Cancel',action=self.on_cancel)
        hsizer.add(self.bOk)
        hsizer.add(self.bCancel)
        sizer.add(hsizer)

        self.sizer = sizer

    def on_ok(self,ev=None):
        self._parent.data = []
        self.end('ok')

    def on_cancel(self,ev=None):
        self.end('cancel')

    def edit(self,ev):
        pass

    def moveup(self,ev):
        pass

    def movedn(self,ev):
        pass

    def new(self,ev):
        pass

    def delete(self,ev):
        pass

class Page(gui.Frame):
    def __init__(self,parent):
        self._nb = parent
        gui.Frame.__init__(self,parent)
        self.text1 = gui.Edit(self,multiline=True,
            line_wrap=True)
        self.text1.bind(update=self.OnEvtText)
        #self.bind(gui.EVT_TEXT, self.OnEvtText, self.text1)
        self.btnSave = gui.Button(self, '&Save')
        self.btnSave.bind(clicked=self.savep)
        self.btnSaveGo = gui.Button(self, 'Save + &Go')
        self.btnSaveGo.bind(clicked=self.savepgo)
        self.btnCancel = gui.Button(self, 'Reset (&Z)')
        self.btnCancel.bind(clicked=self.restorep)
        #self.bind(gui.EVT_KEY_DOWN, self.OnKeyPress)

    def doelayout(self):
        sizer0 = gui.VBox()
        sizer1 = gui.VBox()
        sizer1.add(self.text1)
        sizer2 = gui.HBox(spacing=5)
        sizer0.add(sizer1)
        sizer2.add(gui.Spacer(x=20,y=1))
        sizer2.add(self.btnSave)
        sizer2.add(self.btnSaveGo)
        sizer2.add(self.btnCancel)
        sizer0.add(sizer2)
        self.sizer = sizer0

    def vulp(self):
        sel = self.parent.pages.index(self)#  page if page else self.parent.selection
        print "vulp: currentTab is ",sel,self.__class__
        self.init = True
        self.enableButtons(False)
        if sel == 0:
            self.parent.parent.title = " - ".join((self.parent.parent.title,self.seltitel))
        else:
            self.parent.parent.title = " - ".join((self.parent.parent.title,self.parent.p.titel))
            ## self.parent.parent.SetStatusText(self.parent.pagehelp[self.parent.currentTab])
        if sel <= 1 or sel == 6:
            return
        self.oldbuf = ''
        if self.parent.p is not None:
            if sel == 2 and self.parent.p.melding is not None:
                self.oldbuf = self.parent.p.melding
            elif sel == 3 and self.parent.p.oorzaak is not None:
                self.oldbuf = self.parent.p.oorzaak
            elif sel == 4 and self.parent.p.oplossing is not None:
                self.oldbuf = self.parent.p.oplossing
            elif sel == 5 and self.parent.p.vervolg is not None:
                self.oldbuf = self.parent.p.vervolg
            if self.parent.p.arch:
                self.text1.enable(False)
            else:
                self.text1.enable(True)
        self.text1.select_all()
        self.text1.selected_text = self.oldbuf
        self.init = False

    def readp(self,pid):
        self.parent.p = dml.Actie(self.parent.fnaam,pid)
        self.parent.oldId = self.parent.p.id
        self.parent.newitem = False

    def nieuwp(self,evt=None):
        #~ print "nieuwp, eerst kijken of we wel klaar zijn"
        if self.leavep():
            self.parent.p = dml.Actie(self.parent.fnaam,0)
            self.parent.newitem = True
            if self.parent.selection == 1:
                self.vulp() # om de velden leeg te maken
            else:
                self.gotoPage(1)
        else:
            print "nee we waren nog niet klaar"

    def leavep(self):
        ## print "leave page - huidige scherm is",self.parent.currentTab,self.__class__
        if self.parent.currentTab == 1:
            newbuf = (self.txtPrc.getvalue(),self.txtMld.getvalue(),self.cmbStat.GetSelection(),self.cmbCat.GetSelection())
            if self.parent.newitem and newbuf[0] == "" and newbuf [1] == "" and not self.parent.parent.abort:
                self.parent.newitem = False
                self.parent.p = dml.Actie(self.parent.fnaam,self.parent.oldId) # om de gegevens terug te zetten
        elif self.parent.currentTab == 6:
            newbuf = (self.txtStat.getvalue(),self.elijst,self.edata)
            ## print self.oldbuf
            ## print newbuf
        elif self.parent.currentTab > 1:
            newbuf = self.text1.getvalue()
        ok = True
        if self.parent.currentTab > 0 and newbuf != self.oldbuf:
            d = gui.Message.yesnocancel(
                self.parent.parent.title,
                "De gegevens op de pagina zijn gewijzigd, wilt u\nde wijzigingen opslaan voordat u verder gaat?",
                'question', self
                )
            if d == 'yes':
                 ok = self.savep()
            elif d == 'cancel':
                ok = False
        ## print "klaar met controleren, ok is",ok
        return ok

    def savep(self,evt=None):
        print "savep: currentTab is ",self.parent.selection,self.__class__
        self.enableButtons(False)
        if self.parent.selection <= 1 or self.parent.selection == 6:
            return
        self.text1.select_all()
        t = self.text1.selected_text
        if self.parent.selection == 2 and t != self.parent.p.melding:
            self.oldbuf = self.parent.p.melding = t
            self.parent.p.write()
        if self.parent.selection == 3 and t != self.parent.p.oorzaak:
            self.oldbuf = self.parent.p.oorzaak = t
            self.parent.p.write()
        if self.parent.selection == 4 and t != self.parent.p.oplossing:
            self.oldbuf = self.parent.p.oplossing = t
            self.parent.p.write()
        if self.parent.selection == 5 and t != self.parent.p.vervolg:
            self.oldbuf = self.parent.p.vervolg = t
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
        keycode = evt.GetKeyCode()
        togo = keycode - 48
        ## print togo
        if evt.GetModifiers() == gui.MOD_ALT: # evt.AltDown()
            if keycode == gui.WXK_LEFT or keycode == gui.WXK_NUMPAD_LEFT: #  keycode == 314
                self.gotoPrevPage()
            elif keycode == gui.WXK_RIGHT or keycode == gui.WXK_NUMPAD_RIGHT: #  keycode == 316
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
        elif evt.GetModifiers() == gui.MOD_CONTROL: # evt.ControlDown()
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
        elif keycode == gui.WXK_RETURN or keycode == gui.WXK_NUMPAD_ENTER:# 13 or 372: # Enter
            if self.parent.currentTab == 0:
                self.gotoNextPage()
            #~ else:                       # -- waarvoor was dit ook alweer?
                #~ evt.Skip()
        #~ else:
            #~ evt.Skip()
        #evt.Skip()

    def OnEvtText(self,evt):
        #~ print "self.init is", self.init
        if not self.init:
            #~ print "ok, enabling buttons"
            self.enableButtons()

    def OnEvtComboBox(self,evt):
        self.enableButtons()

    def enableButtons(self,state=True):
        self.btnSave.enable(state)
        self.btnSaveGo.enable(state)
        self.btnCancel.enable(state)
        ## print "abled buttons to",state

    def gotoActie(self,evt=None):
        self.gotoPage(1)

    def gotoNextPage(self):
        print "goto next page from", self.parent.currentTab
        if not self.leavep():
            ## print "gotonextpage: mag niet weg"
            return
        old = self.parent.selection
        if old < len(self.parent.pages) - 1:
            self.parent.selection += 1
            print old, self.parent.selection
            self.parent.parent.changepage(old,self.parent.selection)

    def gotoPrevPage(self):
        #~ print "goto prev page from", self.parent.currentTab
        if not self.leavep():
            ## print "gotoprevpage: mag niet weg"
            return
        old = self.parent.selection
        if self.parent.currentTab > 0:
            self.parent.selection -= 1
            self.parent.parent.changepage(old,self.parent.selection)

    def gotoPage(self,new):
        print "goto page",new,"from", self.parent.selection
        if not self.leavep():
            ## print "gotopage: mag niet weg"
            return
        old = self.parent.selection
        if 0 <= new < len(self.parent.pages):
            self.parent.selection = new
            self.parent.parent.changepage(old,self.parent.selection)

    def keyprint(self,evt):
        pass # vraag om printen scherm of actie, bv. met een radioboxdialog - nou die hebben we niet dat wordt een SingleChoiceDialog
        dlg = gui.SingleChoiceDialog(self, 'Wat wil je afdrukken', 'Vraagje',['huidig scherm', 'huidige actie'],gui.CHOICEDLG_STYLE)
        if dlg.ShowModal() == gui.ID_OK:
            if dlg.GetSelection() == 0:
                self.parent.parent.MenuPrintScherm(evt)
            else:
                self.parent.parent.MenuPrintdml.Actie(evt)

class Page0(Page):
    def __init__(self,parent):
        self._nb = parent
        self.seltitel = 'alle meldingen'
        gui.Frame.__init__(self,parent)

        self.p0list = gui.Table(self) # ,columns=['nummer','beschrijving','status'])
        self.PopulateList()

        self.p0list.bind(selchanged=self.OnItemSelected)
        #self.bind(gui.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.p0list)
        self.p0list.bind(itemactivated=self.OnItemActivated)
        #self.p0list.bind(gui.EVT_LEFT_DCLICK, self.OnDoubleClick)
        #self.p0list.bind(gui.EVT_KEY_DOWN, self.OnKeyPress)

        self.btnSort = gui.Button(self, '&Sort')
        self.btnZoek = gui.Button(self,'&Filter')
        self.btnGa = gui.Button(self, '&GaNaar')
        self.btnArch = gui.Button(self, '&Arch.')
        self.btnNieuw = gui.Button(self, '&Nieuw')
        self.btnSort.bind(clicked=self.sort)
        self.btnZoek.bind(clicked=self.select)
        self.btnGa.bind(clicked=self.gotoActie)
        self.btnArch.bind(clicked=self.archiveer)
        self.btnNieuw.bind(clicked=self.nieuwp)

    def doelayout(self):
        sizer0 = gui.VBox()
        sizer1 = gui.VBox()
        sizer2 = gui.HBox(spacing=1)
        sizer1.add(self.p0list)
        sizer0.add(sizer1)
        sizer2.add(self.btnSort)
        sizer2.add(self.btnZoek)
        sizer2.add(self.btnGa)
        sizer2.add(self.btnArch)
        sizer2.add(self.btnNieuw)
        sizer0.add(sizer2)
        self.sizer = sizer0

    def leavep(self):
        return True # niks doen, doorgaan

    def vulp(self):
        Page.vulp(self)
        if not self.parent.rereadlist:
            #self.parent.parent.SetStatusText("%s - %i items" % (self.parent.pagehelp[self.parent.currentTab],len(self.parent.data)))
            return
        self.parent.data = {}
        select = self.sel.copy()
        ## print select
        arch = ""
        if "arch" in select: arch = select.pop("arch")
        ## print arch, select
        try:
            h = dml.Acties(self.parent.fnaam,select,arch)
            ## for x in h.lijst:
                ## print x
        except:
            print "samenstellen lijst mislukt"
        else:
            for y in enumerate(h.lijst):
                x = y[1]
                ## print x
                if len(x) < 5:
                    x.append('')
                # let op: voor correct sorteren moet de volgorde van rubrieken in self.data overeenkomen met die op het scherm
                self.parent.data[y[0]] = (x[0],x[1],".".join((str(x[3][1]),x[3][0])),".".join((str(x[2][1]),x[2][0])),x[5],x[4])
        ## for x,y in self.parent.data.items():
            ## print x,y
        self.PopulateList()
        #self.parent.parent.SetStatusText("%s - %i items" % (self.parent.pagehelp[self.parent.currentTab],len(self.parent.data)))
        #~ print len(self.parent.data),self.parent.currentItem
        if self.parent.sorter is not None:
            print "maar wel opnieuw sorteren"
            self.p0list.SortItems(self.parent.sorter)
        self.parent.rereadlist = False
        self.p0list.rows.select(self.parent.currentItem)

    def PopulateList(self):
        #~ print "populating list..."
        self.p0list.delete_all()
        max = len(self.p0list.columns)
        while max > 0:
            del self.p0list.columns[max-1]
            max = len(self.p0list.columns)
        self.itemDataMap = self.parent.data

        cwidths = (60,24,90,60,120)
        # Adding columns with width and images on the column header
        for ix,col in enumerate(self.parent.ctitels):
            self.p0list.columns.append(col,width=cwidths[ix])

        #info.m_width = 64
        #info.m_width = 24
        #info.m_width = 114
        #info.m_width = 72
        #info.m_width = 292

        self.parent.rereadlist = False
        #if items:
            ## kleur = False
        for ix,it in enumerate(self.parent.data.items()):
            key, data = it
            loc = data[2].index(".")
            self.p0list.rows.append((
                data[0],
                data[2][loc+1:loc+2].upper(),
                data[3][data[3].index(".")+1:],
                data[4],
                data[5]))
            self.p0list.rows.setdata(ix, key)
            ## if kleur:
                ## #~ self.p0list.SetItemBackgroundColour(key,gui.Systemdml.Settings.GetColour(gui.SYS_COLOUR_MENU))
            ## #~ else:
                ## self.p0list.SetItemBackgroundColour(key,gui.Systemdml.Settings.GetColour(gui.SYS_COLOUR_INFOBK))
            ## kleur = not kleur

    def OnItemSelected(self, event):
        print "OnItemSelected"
        if not self.p0list.rows.selection:
            return
        self.parent.currentItem = self.p0list.rows.selection[0]
        ## print self.parent.currentItem
        seli = self.p0list.rows.getdata(self.parent.currentItem)
        ## print "Itemselected",seli,self.parent.data[seli][0]
        self.readp(self.parent.data[seli][0])
        ## print self.parent.p.__dict__
        for pg in self.parent.pages[1:]:
            pg.vulp()

    def OnItemDeselected(self, evt):
        print "OnItemDeSelected"
        item = self.p0list.rows[self.p0list.rows.selection[0]]

    def OnItemActivated(self, event):
        print "OnItemActivated"
        self.currentItem = self.p0list.rows.selection[0]
        self.gotoActie()
        # self.log.WriteText("OnDoubleClick item %s\n" % self.p0list.GetItemText(self.currentItem))

    def select(self,evt=None):
        """niet alleen selecteren op tekst(deel) maar ook op status, soort etc"""
        d = SelectOptionsDialog(self.sel,self._nb)
        if d.popup(self) == 'ok':
            self.sel = self.data
            print self.parent.fnaam,self.sel
            self.parent.rereadlist = True
            self.vulp()
            ## e = gui.MessageDialog( self, "Sorry, werkt nog niet", "Oeps", gui.OK)  # Create a message dialog box
            ## e.ShowModal() # Shows it
            ## e.Destroy() # finally destroy it when finished.
        self._nb.parent.zetfocus(0)

    def sort(self,evt=None):
        """sortering mogelijk op datum/tijd, soort, titel, status via
        #schermpje met 2x4 comboboxjes waarin de volgorde van de rubrieken en de sorteervolgorde per rubriek kunt aangeven"""
        #edt = gui.MessageDialog( self, "Sorry, werkt nog niet", "Oeps", gui.OK)  # Create a message dialog box
        #if edt.popup(self) == 'ok':
        #    data = self.data['attrs']
        d = SortOptionsDialog(self._nb)
        if d.popup(self) == 'ok': # Shows it
            e = gui.Message.ok("Oeps","Sorry, werkt nog niet",)
        self._nb.parent.zetfocus(0)

    def archiveer(self,evt=None):
        seli = self.p0list.getdata(self.parent.currentItem)
        self.readp(self.parent.data[seli][0])
        self.parent.p.setArch(True)
        self.parent.p.write()
        self.parent.rereadlist = True
        self.vulp()
        self.parent.parent.zetfocus(0)

    def enableButtons(self,state=True):
        pass # anders wordt de methode van de Page class geactiveerd

class Page1(Page):
    def __init__(self,parent):
        self._nb = parent
        gui.Frame.__init__(self,parent)
        t1 = gui.Edit(self,readonly=True)
        self.txtId = t1
        #t1.bind(gui.EVT_KEY_DOWN, self.OnKeyPress)

        t2 = gui.Edit(self)
        self.txtDat = t2
        #t2.bind(gui.EVT_KEY_DOWN, self.OnKeyPress)

        t3 = gui.Edit(self)
        #self.bind(gui.EVT_TEXT, self.OnEvtText, t3)
        self.txtPrc = t3
        #t3.bind(gui.EVT_KEY_DOWN, self.OnKeyPress)

        t4 = gui.Edit(self)
        #self.bind(gui.EVT_TEXT, self.OnEvtText, t4)
        self.txtMld = t4
        #t4.bind(gui.EVT_KEY_DOWN, self.OnKeyPress)

        cb1 = gui.Combo(self, style='list')
        #self.bind(gui.EVT_TEXT, self.OnEvtText, cb1)
        self.cmbCat = cb1
        #cb1.bind(gui.EVT_KEY_DOWN, self.OnKeyPress)

        cb2 = gui.Combo(self, style='list')
        #self.bind(gui.EVT_TEXT, self.OnEvtText, cb2)
        self.cmbStat = cb2
        #cb2.bind(gui.EVT_KEY_DOWN, self.OnKeyPress)
        self.VulCombos()

        t5 = gui.Label(self)
        self.lblArch = t5
        #t5.bind(gui.EVT_KEY_DOWN, self.OnKeyPress)
        b5 = gui.Button(self, "Archiveren")
        self.btnArch = b5
        self.btnArch.bind(clicked=self.archiveer)
        #b5.bind(gui.EVT_KEY_DOWN, self.OnKeyPress)

        self.btnSave = gui.Button(self, '&Save')
        self.btnSave.bind(clicked=self.savep)
        self.btnSaveGo = gui.Button(self, 'Save + &Go')
        self.btnSaveGo.bind(clicked=self.savepgo)
        self.btnCancel = gui.Button(self, 'Reset (&Z)')
        self.btnCancel.bind(clicked=self.restorep)
        #self.bind(gui.EVT_KEY_DOWN, self.OnKeyPress)

    def VulCombos(self):
        #~ print "vullen combobox"
        go = True
        while go:
            try:
                del self.cmbStat[1]
            except:
                go = False
        self.catdata = []
        go = True
        while go:
            try:
                del self.cmbCat[1]
            except:
                go = False
        self.statdata = []
        for x in sorted(self.parent.cats.keys()):
            y = self.parent.cats[x]
            self.cmbCat.append(y[0])
            self.catdata.append(y[1])
        for x in sorted(self.parent.stats.keys()):
            y = self.parent.stats[x]
            self.cmbStat.append(y[0])
            self.statdata.append(y[1])

    def doelayout(self):
        sizer0 = gui.VBox()
        sizer1 = gui.TBox(6,2) # rows, cols, hgap, vgap
        sizer1.add(gui.Label(self, "Actie-id:"))
        sizer1.add(self.txtId)
        sizer1.add(gui.Label(self, "Datum/tijd:"))
        sizer1.add(self.txtDat)
        sizer1.add(gui.Label(self, "Onderwerp:"))
        sizer1.add(self.txtPrc)
        sizer1.add(gui.Label(self, "Omschrijving:"))
        sizer1.add(self.txtMld)
        sizer1.add(gui.Label(self, "Categorie:"))
        sizer1.add(self.cmbCat)
        sizer1.add(gui.Label(self, "Status:"))
        sizer1.add(self.cmbStat)
        sizer0.add(sizer1)

        sizer1 = gui.HBox()
        sizer1.add(self.lblArch)
        sizer0.add(sizer1)
        sizer1 = gui.HBox()
        sizer1.add(gui.Spacer(x=80,y=5))
        sizer1.add(self.btnArch)
        sizer0.add(sizer1)
        ## sizer1.add((-1,186), (9,0))
        sizer0.add(sizer1)
        sizer0.add(gui.Spacer())
        sizer2 = gui.HBox(spacing=5)
        sizer2.add(gui.Spacer(x=20,y=1))
        sizer2.add(self.btnSave)
        sizer2.add(self.btnSaveGo)
        sizer2.add(self.btnCancel)
        sizer0.add(sizer2)
        self.sizer = sizer0

    def vulp(self):
        Page.vulp(self)
        self.txtId.text =""
        self.txtDat.text =""
        self.txtPrc.text =""
        self.txtMld.text =""
        self.lblArch.title =""
        self.cmbCat.selection = 0
        self.cmbStat.selection = 0
        if self.parent.p is not None: # and not self.parent.newitem:
            self.txtId.text = self.parent.p.id
            self.txtDat.text = self.parent.p.datum
            self.parch = self.parent.p.arch
            if self.parent.p.titel is not None:
                h = self.parent.p.titel.split(": ")
                self.txtPrc.text = h[0]
                if len(h) > 1:
                    self.txtMld.text = h[1]
            for i,x in enumerate(self.statdata):
                if x == self.parent.p.status:
                    self.cmbStat.selection = i
                    break
            for i,x in enumerate(self.catdata):
                if x == self.parent.p.soort:
                    self.cmbCat.selection = i
                    break
        self.oldbuf = (self.txtPrc.text,self.txtMld.text,self.cmbStat.selection,self.cmbCat.selection)
        self.init = False
        if self.parch:
            aanuit = False
            self.lblArch.title = "Deze actie is gearchiveerd"
            self.btnArch.title = "Herleven"
        else:
            aanuit = True
            self.lblArch.title = ""
            self.btnArch.title = "Archiveren"
        self.txtId.enable(False)
        self.txtDat.enable(False)
        self.txtPrc.enable(aanuit)
        self.txtMld.enable(aanuit)
        self.cmbCat.enable(aanuit)
        self.cmbStat.enable(aanuit)
        if self.parent.newitem:
            self.btnArch.enable(False)
        else:
            self.btnArch.enable(True)
        ## print "klaar met vulp"

    def savep(self,evt=None):
        Page.savep(self)
        self.txtPrc.select_all()
        s1 = self.txtPrc.selection
        self.txtMld.select_all()
        s2 = self.txtMld.selection
        if s1 == "" or s2 == "":
            gui.Message.ok('',"Beide tekstrubrieken moeten worden ingevuld")
            return False
        wijzig = False
        if self.parch != self.parent.p.arch:
            if self.parch:
                self.parent.p.setArch(True)
            else:
                self.parent.p.setArch(False)
            wijzig = True
        t = ": ".join((s1,s2))
        if t != self.parent.p.titel:
            self.parent.p.titel = t
            wijzig = True
        s = self.statdata[self.cmbStat.selection]
        if s != self.parent.p.status:
            self.parent.p.status = s
            wijzig = True
        s = self.catdata[self.cmbCat.selection]
        if s != self.parent.p.soort:
            self.parent.p.soort = s
            wijzig = True
        if wijzig:
            #~ print "savep: schrijven",self.oldbuf
            self.parent.rereadlist = True
            self.parent.p.write()
            if self.parent.newitem:
                #~ print len(self.parent.data)
                self.parent.currentItem = len(self.parent.data) # + 1
                self.parent.data[self.parent.currentItem] = (self.txtDat.text, \
                    ": ".join((self.txtPrc.text,self.txtMld.text)), \
                    self.cmbStat.selection,self.cmbCat.selection, \
                    self.txtId.text)
                self.parent.newitem = False
            self.oldbuf = (self.txtPrc.text,self.txtMld.text, \
                self.cmbStat.selection,self.cmbCat.selection)
        return True

    def archiveer(self,evt=None):
        self.parch = not self.parch
        self.savep()
        self.parent.rereadlist = True
        self.gotoPrevPage()


class Page6(Page):
    def __init__(self,parent):
        self._nb = parent
        gui.Frame.__init__(self,parent)
        self.currentItem = 0
        self.txtStat = gui.Edit(self, multiline=True,
            line_wrap=True)
        self.txtStat.bind(update=self.OnEvtText)
        #self.txtStat.bind(gui.EVT_KEY_DOWN, self.OnKeyPress)
        self.btnVoortg = gui.Button(self,"Nieuw moment")
        self.btnVoortg.bind(clicked=self.addVoortg)
        self.lstVoortg = gui.List(self)
        self.lstVoortg.bind(itemactivated=self.OnItemActivated)
        self.lstVoortg.bind(selchanged=self.OnItemSelected)
        # self.bind(gui.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.lstVoortg)
        self.txtVoortg = gui.Edit(self, multiline=True,
            line_wrap=True)
        self.txtVoortg.bind(update=self.TextIsChanged)

        self.btnSave = gui.Button(self, '&Save')
        self.btnSave.bind(clicked=self.savep)
        self.btnSaveGo = gui.Button(self, 'Save + &Go')
        self.btnSaveGo.bind(clicked=self.savepgo)
        self.btnCancel = gui.Button(self, 'Reset (&Z)')
        self.btnCancel.bind(clicked=self.restorep)

    def doelayout(self):
        sizer0 = gui.VBox()
        sizer1 = gui.VBox()
        sizer1.add(gui.Label(self, "Korte omschrijving stand van zaken:"))
        sizer1.add(self.txtStat)
        sizer2 = gui.HBox()
        sizer2.add(gui.Label(self, "Voortgangsmomenten:"),border=(2,6,-1,-1))
        sizer2.add(gui.Spacer(y=1))
        sizer2.add(self.btnVoortg,border=(-1,-1,2,-1))
        sizer1.add(sizer2)
        sizer1.add(self.lstVoortg)
        ## sizer1.add(gui.Label(self, "Beschrijving moment:"), (4,0), flag = gui.ALL | gui.ALIGN_TOP, border = 4)
        sizer1.add(self.txtVoortg)
        sizer0.add(sizer1)
        sizer2 = gui.HBox(spacing=5)
        sizer2.add(gui.Spacer(x=20,y=1))
        sizer2.add(self.btnSave)
        sizer2.add(self.btnSaveGo)
        sizer2.add(self.btnCancel)
        sizer0.add(sizer2)
        self.sizer = sizer0

    def vulp(self):
        Page.vulp(self)
        self.txtStat.select_all()
        self.txtStat.selected_text = ""
        self.elijst = self.edata = self.olijst = self.odata = []
        self.txtVoortg.select_all()
        self.txtVoortg.selected_text = ""
        self.txtVoortg.enable(False)
        if self.parent.p is not None: # and not self.parent.newitem:
            self.olijst = [x[0] for x in self.parent.p.events]
            self.olijst.reverse()
            self.lstVoortg.choices = [x for x in self.olijst]
            self.odata = [x[1] for x in self.parent.p.events]
            self.odata.reverse()
            self.voortgdata = [x for x in self.odata]
            self.txtStat.select_all()
            self.txtStat.selected_text = self.parent.p.stand
            for x,y in enumerate(self.elijst):
                self.lstVoortg.append(y)
                self.voortgdata.append(x)
        self.txtStat.select_all()
        self.oldbuf = (self.txtStat.selected_text,self.olijst,self.odata)
        self.init = False

    def addVoortg(self):
        # dialoog voor opgeven momenttitel (beginnen met huidige datum/tijd als invul suggestie?)
        # bij ok: item aan listbox toevoegen en "selecteren"
        pass

    def addListItems(self):
        self.lstVoorg.insert(0,"")
        self.voortgdata.insert(0,"")

    def savep(self,evt=None):
        Page.savep(self)
        print "verder met eigen savep()"
        self.txtStat.select_all()
        s1 = self.txtStat.selected_text
        if s1 == "" and self.voortgdata:
            gui.Message.ok("Oeps","Stand van zaken moet worden ingevuld")
            return False
        titelvergeten = False
        for ix,data in enumerate(self.voortgdata):
            if not self.lstVoorg[ix]:
                titelvergeten = True
                break
        if titelvergeten:
            gui.Message.ok("Oeps","Niet alle moment titels zijn ingevuld")
            return False
        wijzig = False
        if s1 != self.parent.p.stand:
            self.parent.p.stand = s1
            wijzig = True
        if self.lstVoorg.choices != self.olijst or self.voortgdata != self.odata:
            wijzig = True
            self.parent.p.events = []
            for ix,data in enumerate(self.voortgdata):
                self.parent.p.events.insert(0,(self.lst.Voortg[ix],data))
        if wijzig:
            #~ print "savep: schrijven"
            self.parent.p.list() # NB element 0 is leeg
            self.parent.p.write()
            self.olijst = [x for x in self.lstVoorg]
            self.odata = [x for x in self.voortgdata]
            self.oldbuf = (self.txtStat.getvalue(),self.olijst,self.odata)
        else:
            print "Leuk hoor, er was niks gewijzigd ! @#%&*Grrr"
        return True

    def OnItemSelected(self, event):
        self.currentItem = self.lstVoorg.selection
        self.txtVoortg.enable(True)
        self.txtVoortg.select_all()
        self.txtVoortg.selected_text = self.voortgdata[self.currentItem]

    def OnItemActivated(self, event):
        # dubbelklikken maakt het mogelijk de momenttitel te veranderen
        # hiervoor moet weer een dialoog voor opgeven momenttitel opkomen
        # ditmaal met de bestaande tekst erin
        pass
        ## ix = event.m_itemIndex
        ## print "activated item",ix
        ## event.Skip()

    def TextIsChanged(self):
        self.txtVoortg.select_all()
        self.voortgdata[self.currentItem] = self.txtVoortg.selected_text

class MainWindow(gui.CeFrame):
    def __init__(self,args):
        gui.CeFrame.__init__(self,
            title="ProbReg",
            action=("About", self.about),
            menu="Menu"
            )
        self.sipp = gui.SIPPref(self)
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
        self.dirname,self.filename = os.path.split(self.fpad)
        #~ print self.dirname,self.filename
        self.title = 'Actieregistratie'
        ## self.printer = EasyPrinter()
        self.p = self.oldbuf = None
        self.newfile = self.newitem = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []

    # --- menu opbouwen -----------------------------------------------------------------------------------------
        self.hoofdmenu = gui.PopupMenu()
    #    hoofdmenu = gui.MenuBar()
        filemenu = gui.Menu()
        filemenu.append(pr.ID_NEW[0],callback=self.MenuNew)
        filemenu.append(pr.ID_OPEN[0],callback=self.MenuOpen)
        filemenu.append_separator()
        submenu = gui.Menu()
        submenu.append(pr.ID_PRINTS[0],callback=self.MenuPrintScherm)
        submenu.append(pr.ID_PRINTA[0],callback=self.MenuPrintActie)
        filemenu.append_menu(pr.ID_PRINT[0], submenu) # )
        filemenu.append_separator()
        filemenu.append(pr.ID_EXIT[0],callback=self.MenuExit)
        setupmenu= gui.Menu()
        submenu = gui.Menu()
        submenu.append(pr.ID_SETFONT[0],callback=self.MenuTextAttr)
        submenu.append(pr.ID_SETCOLR[0],callback=self.MenuColours)
        #~ submenu.append(pr.ID_SETKEYS[0],callback=self.MenuKeys)
        setupmenu.append_menu(pr.ID_SETAPPL[0], submenu)
        submenu = gui.Menu()
        submenu.append(pr.ID_SETTABS[0],callback=self.MenuTabs)
        submenu.append(pr.ID_SETCATS[0],callback=self.MenuCats)
        submenu.append(pr.ID_SETSTATS[0],callback=self.MenuStats)
        setupmenu.append_menu(pr.ID_SETDATA[0], submenu)
        setupmenu.append(pr.ID_SETFOLLY[0],callback=self.MenuFolly)
        helpmenu = gui.Menu()
        helpmenu.append(pr.ID_ABOUT[0],callback=self.MenuHelpOver)
        helpmenu.append(pr.ID_KEYS[0],callback=self.MenuHelpKeys)
        self.helptext = pr.helpinfo
        #self.SetMenuBar(menuBar)

    # --- schermen opbouwen: controls plaatsen -----------------------------------------------------------------------------------------
        ##self.SetTitle(self.title)
        #~ self.SetIcon(gui.Icon("task.ico",gui.BITMAP_TYPE_ICO))
        ##self.SetIcon(images.gettaskIcon())
        #~ self.SetMinSize((476, 560))
        self.nb = gui.NoteBook(self)
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
        self.nb.tabtitels = [
            "&%s" % x for x in self.nb.tabs
            ]
        self.nb.pages = [
            Page0(self.nb),
            Page1(self.nb),
            Page(self.nb),
            Page(self.nb),
            Page(self.nb),
            Page(self.nb),
            Page6(self.nb)
            ]
        for ix,page in enumerate(self.nb.pages):
            self.nb.append(self.nb.tabtitels[ix],
                page)

        if DESKTOP:
            self.cb_menu.append_menu(pr.ID_FILE[0], filemenu)
            self.cb_menu.append_menu(pr.ID_SETTINGS[0], setupmenu)
            self.cb_menu.append_menu(pr.ID_HELP[0], helpmenu)
        else:
            self.hoofdmenu.append_menu(pr.ID_FILE[0], filemenu)
            self.hoofdmenu.append_menu(pr.ID_SETTINGS[0], setupmenu)
            self.hoofdmenu.append_menu(pr.ID_HELP[0], helpmenu)
            #self.nb.bind(lbdown=self.on_bdown)
            self.exitButton = gui.Button(self,"click to Exit")
            self.exitButton.bind(clicked=self.MenuExit)
            self.menuButton = gui.Label(self,"tap for Menu")
            self.menuButton.bind(lbdown=self.on_menu)
        #self.nb.bind(gui.EVT_KEY_DOWN, self.OnKeyPress)
        #self.nb.bind(gui.EVT_LEFT_UP, self.OnLeftUp)
        #self.nb.bind(gui.EVT_LEFT_DOWN, self.OnLeftDown)
        ## self.nb.bind(selchange=self.OnPageChanged)
        ## self.nb.bind(selchanging=self.OnPageChanging)

        # --- schermen opbouwen: layout -----------------------------------------------------------------------------------------
        for pg in self.nb.pages:
            pg.doelayout()
        sizer0 = gui.VBox()
        sizer1 = gui.HBox()
        sizer1.add(self.nb)
        sizer0.add(sizer1)
        if not DESKTOP:
            sizer1 = gui.HBox()
            sizer1.add(self.menuButton)
            sizer1.add(self.exitButton)
            sizer0.add(sizer1)
        self.sizer = sizer0
        self.nb.selection = 0
        if self.filename == "":
            self.MenuOpen(None)
        else:
            self.startfile()

    def MenuNew(self,e):
        """Start a new file"""
        self.newfile = False
        self.dirname = os.getcwd()
        fn = gui.FileDialog.save(wildcards={"XML files": "*.xml"})
        if fn:
            self.filename=fn
            self.dirname=os.path.split(fn)[0]
            self.newfile = True
            self.startfile()
            self.newfile = False

    def MenuOpen(self,e):
        """ Open a file"""
        self.dirname = os.getcwd()
        fn = gui.FileDialog.open(wildcards={"XML files": "*.xml"})
        if fn:
            self.filename=fn
            self.dirname=os.path.split(fn)[0]
            self.startfile()

    def MenuPrintScherm(self,e=None):
        self.text = []
        self.hdr = ("Actie: %s %s" % (self.nb.p.id,self.nb.p.titel))
        if self.nb.currentTab == 0:
            self.text = tpl.print_page0(self.filename, self.nb.data)
        elif self.nb.currentTab == 1:
            self.text = tpl.print_page1(self.nb.data)
        elif 2 <= self.nb.currentTab <= 5:
            data["text1"] = self.nb.pages[self.nb.currentTab].text1.getvalue()
            self.text = tpl.print_pageno(data, self.nb.tabs, self.nb.currentTab)
        elif self.nb.currentTab == 6:
            data["txt"] = self.nb.pages[6].txtStat.getvalue()
            data["elijst"] = self.nb.pages[6].elijst
            self.text = tpl.print_pageno(data, self.nb.tabs, 6)
        self.afdrukken()

    def MenuPrintActie(self,e=None):
        self.text = tpl.print_all(self.nb.data, self.nb.cats, self.nb.stats, self.nb.tabs)
        self.afdrukken()

    def MenuExit(self,e=None):
        self.abort = True
        self.nb.pages[self.nb.currentTab].leavep()
        self.destroy()

    def MenuTabs(self,e):
        d = OptionsDialog(self, titel="Wijzigen tab titels",
            keuzes=self.nb.tabs, tekst=pr.tabhelp, max=3)
        if d.popup(self) == 'ok':
            self.savedml.Settings("tab",self.data)

    def MenuStats(self,e):
        d = OptionsDialog(self, titel="Wijzigen statussen",
            keuzes=self.nb.stats, tekst=pr.stathelp, max=5)
        if d.popup(self) == 'ok':
            self.savedml.Settings("stat",self.data)

    def MenuCats(self,e):
        d = OptionsDialog(self, titel="Wijzigen categorieen",
            keuzes=self.nb.cats, tekst=pr.cathelp, max=5)
        if d.popup(self) == 'ok':
            self.savedml.Settings("cat",self.data)

    def MenuTextAttr(self,e):
        d = gui.Message.ok("Oeps","Sorry, werkt nog niet")

    def MenuColours(self,e):
        d = gui.MessageDialog("Oeps","Sorry, werkt nog niet")

    def MenuKeys(self,e):
        gui.Message.ok("Oeps","Sorry, werkt nog niet")

    def MenuHelpOver(self,e):
        gui.Message.ok("Help","wxPython versie van mijn actiebox")

    def MenuHelpKeys(self,e):
        gui.Message.ok("Help",self.helptext)

    def MenuFolly(self,e):
        gui.Message.ok("Haha","Yeah you wish...\nHet leven is niet in te stellen helaas")

    def about(self,ev=None):
        gui.Message.ok(self.title,"\n".join((
            "Made in 2009 by Albert Visser",
            "Built with PythonCE and PocketPyGui",
            "Originally written using wxPython")))

    def on_menu(self, ev=None):
        if gui.recon_context(self.menuButton, ev):
            gui.context_menu(self, ev, self.hoofdmenu)
        #self.hoofdmenu.popup(self,10,10)

    def on_bdown(self, ev=None):
        if gui.recon_context(self.nb, ev):
            ## self.item = self.tree.selection
            ## if self.item == self.top:
                gui.context_menu(self, ev, self.hoofdmenu)
            ## elif self.item is not None:
                ## gui.context_menu(self, ev, self.editmenu)

    def startfile(self):
        f = os.path.join(self.dirname,self.filename)
        h = dml.checkfile(f,self.newfile)
        if h != '':
            gui.Message.ok("Oeps",h)
            return
        self.nb.fnaam = f
        self.title = self.filename
        self.nb.rereadlist = True
        self.nb.sorter = None
        self.leesSettings()
        self.nb.pages[0].sel = {}
        self.nb.pages[1].VulCombos()
        if self.nb.currentTab == 0:
            self.nb.pages[0].vulp()
        else:
            self.nb.selection = 0

    def leesSettings(self):
        h = dml.Settings(self.nb.fnaam)
        self.nb.stats = {}
        self.nb.cats = {}
        self.nb.tabs = {}
        self.nb.pagehelp = pr.pagehelp
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
            self.nb.pages[1].cmbStat.choices = []
            self.nb.pages[1].statdata = []
            for x in self.nb.stats.keys():
                y = self.nb.stats[x]
                self.nb.pages[1].cmbStat.append(y[0])
                self.nb.pages[1].statdata.append(y[1])
        elif srt == "cat":
            h.cat = d
            h.write()
            self.nb.cats = d
            self.nb.pages[1].cmbCat.choices = []
            self.nb.pages[1].catdata = []
            for x in self.nb.cats.keys():
                y = self.nb.cats[x]
                self.nb.pages[1].cmbCat.append(y[0])
                self.nb.pages[1].catdata.append(y[1])
        else:
            pass

    def OnKeyPress(self,evt):
        """
        met behulp van deze methode wordt vanaf globaal (applicatie) niveau dezelfde
        toetsenafhandelingsroutine aangeroepen als vanaf locaal (tab) niveau
        """
        keycode = evt.GetKeyCode()
        self.nb.pages[self.nb.currentTab].OnKeyPress(evt)

    def OnPageChanging(self, event=None): # _onchanging overloaden?
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
            m = "Voer eerst één of meer acties op"
            self.mag_weg = False
        elif self.nb.currentItem == -1 and not self.nb.newitem:
            m = "Selecteer eerst een actie"
            self.mag_weg = False
        if not self.mag_weg:
            if m != "":
                d = gui.MessageDialog(self,m,"Navigatie niet toegestaan",gui.ICON_ERROR)
                d.ShowModal()
                d.Destroy()
            self.nb.SetSelection(old)
            event.Veto()
        else:
            event.Skip()

    def OnPageChanged(self, event=None): # _onchange overloaden?
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
        self.nb.pages[new].vulp()
        event.Skip()

    def changepage(self,old,new):
        if old == -1:
            pass
        elif self.nb.fnaam == "":
            m = "Kies eerst een bestand om mee te werken"
            self.mag_weg = False
        elif len(self.nb.data) == 0 and not self.nb.newitem:
            m = "Voer eerst één of meer acties op"
            self.mag_weg = False
        elif self.nb.currentItem == -1 and not self.nb.newitem:
            m = "Selecteer eerst een actie"
            self.mag_weg = False
        if not self.mag_weg:
            if m != "":
                d = gui.Message.ok("Navigatie niet toegestaan",m, "error")
            self.nb.selection = old
            return
        self.nb.pages[new].vulp()
        self.zetfocus(new)

    def OnLeftDown(self,event):
        """
        deze methode is bedoeld om te bepalen of er op een tab is geklikt en op
        welke, en om de "leave" methode van de betreffende tab aan te roepen.
        """
        self.x = event.GetX()
        self.y = event.GetY()
        item, flags = self.nb.HitTest((self.x, self.y))
        if flags != gui.NOT_FOUND:
            ## print 'LeftDown op',self.nb.currentTab # item,flags
            self.mag_weg = self.nb.pages[self.nb.currentTab].leavep()
            ## print self.mag_weg
        ## print "einde OnLeftDown"
        event.Skip()

    def OnLeftUp(self,event):
        ## print "OnLeftUp", self.mag_weg
        if self.mag_weg:
            self.zetfocus(self.nb.currentTab)
        event.Skip()

    def zetfocus(self,n):
        ## print "zetfocus called"
        #~ self.setFocus()
        if n == 0:
            self.nb.pages[0].p0list.focus()
        elif n == 1:
            self.nb.pages[1].txtPrc.focus()
        elif 2 <= n <= 5:
            self.nb.pages[n].text1.focus()
        elif n == 6:
            self.nb.pages[6].txtStat.focus()

    def afdrukken(self):
        self.printer.Print("".join(self.text),self.hdr)
        return
        # de moelijke manier
        data = gui.PrintDialogData()
        data.EnableSelection(False)
        data.EnablePrintToFile(True)
        data.EnablePageNumbers(False)
        data.SetAllPages(True)
        dlg = gui.PrintDialog(self, data)
        if dlg.ShowModal() == gui.ID_OK:
            pdd = dlg.GetPrintDialogData()
            prt = wxPrinter(pdd)
            pda = Prtdata(self.textcanvas)
            if not prt.Print(self,prtdata,False):
                self.Message.ok("","Unable to print the document.")
            prt.Destroy()
        dlg.Destroy()

if __name__ == '__main__':
    app = gui.Application(MainWindow(sys.argv[1:]))
    app.run()