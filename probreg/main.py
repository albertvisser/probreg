#! usr/bin/env python
"""Actie (was: problemen) Registratie, GUI toolkit onafhankelijke code
"""
import os
# import sys
import pathlib
import datetime
import functools
# import probreg.gui as gui
from probreg import gui
# import probreg.shared as shared   # import DataError, et_projnames
from probreg import shared   # import DataError, et_projnames
import probreg.dml_django as dmls
import probreg.dml_xml as dmlx
# import probreg.dml_mongo as dmlm
LIN = os.name == 'posix'


class MainWindow:
    """Hoofdscherm met menu, statusbalk, notebook en een "quit" button"""
    def __init__(self, parent, fnaam=""):
        self.parent = parent
        self.dirname, self.filename = '', ''
        self.datatype = None
        self.title = 'Actieregistratie'
        self.initializing = True
        self.exiting = False
        self.helptext = ''
        self.is_newfile = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []
        self.projnames = {x[0].lower(): (x[0], x[1]) for x in dmls.get_projnames()}
        if fnaam:
            self.determine_datatype_from_filename(fnaam)
        self.gui = gui.MainGui(self)
        if not self.datatype:
            self.select_datatype()
        self.work_with_user = self.datatype == shared.DataType.SQL
        if self.work_with_user:
            if not self.projnames:
                raise SystemExit('No projects found; add one ior more in the webapp first')
            self.user = None                        # start without user
            self.is_user = self.is_admin = False
        else:
            self.user = 1                           # pretend user
            self.is_user = self.is_admin = True     # force editability
        self.multiple_files = self.datatype == shared.DataType.XML
        self.multiple_projects = self.datatype == shared.DataType.SQL
        self.use_text_panels = self.datatype == shared.DataType.XML
        self.use_rt = self.datatype == shared.DataType.XML
        self.use_separate_subject = self.datatype in (shared.DataType.SQL, shared.DataType.MNG)
        self.create_book()
        self.gui.create_menu()
        self.enable_settingsmenu()
        self.gui.create_actions([('Ctrl+P', self.print_something), ('Alt+Left', self.goto_prev),
                                 ('Alt+Right', self.goto_next)])
        self.create_book_pages()

        if self.datatype == shared.DataType.XML:
            if self.filename == "":
                self.open_xml()
            else:
                self.startfile()
        elif self.datatype == shared.DataType.SQL:
            self.open_sql(do_sel=not bool(self.filename))
        else:  # if self.datatype == shared.DataType.MNG:
            self.open_mongo()
        self.initializing = False

    def determine_datatype_from_filename(self, fnaam):
        "get datatype from input parameters"
        if fnaam == 'xml':
            self.datatype = shared.DataType.XML
        elif fnaam in ('sql', 'django'):
            self.datatype = shared.DataType.SQL
        elif fnaam in ('mongo', 'mongodb'):
            self.datatype = shared.DataType.MNG
        elif fnaam.lower() in self.projnames:
            self.datatype = shared.DataType.SQL
            self.filename = fnaam  # .lower()
        elif os.path.exists(fnaam) and os.path.isfile(fnaam):
            self.datatype = shared.DataType.XML
            test = pathlib.Path(fnaam)
            self.dirname, self.filename = test.parent, test.name

    def select_datatype(self):
        "get datatype from user if not determinable from filename"
        self.filename = ''
        choice = gui.get_choice_item(None, 'Select Mode', ['XML', 'SQL', 'MNG'])
        if choice == 'XML':
            self.datatype = shared.DataType.XML
        elif choice == 'SQL':
            self.datatype = shared.DataType.SQL
        elif choice == 'MNG':
            self.datatype = shared.DataType.MNG
        else:
            raise SystemExit('No datatype selected')

    def get_menu_data(self):
        """Define application menu
        """
        data = [("&File", [("&Open", self.open_xml, 'Ctrl+O', " Open a new file"),
                           ("&New", self.new_file, 'Ctrl+N', " Create a new file"),
                           ('',),
                           ("&Print", (("Dit &Scherm", self.print_scherm, 'Shift+Ctrl+P',
                                        "Print the contents of the current screen"),
                                       ("Deze &Actie", self.print_actie, 'Alt+Ctrl+P',
                                        "Print the contents of the current issue"))),
                           ('',),
                           ("&Quit", self.exit_app, 'Ctrl+Q', " Terminate the program")]),
                ("&User", [("&Login", self.sign_in, 'Ctrl+L', " Sign in to the database")]),
                ("&Settings", (("&Applicatie", (("&Lettertype", self.font_settings, '',
                                                 " Change the size and font of the text"),
                                                ("&Kleuren", self.colour_settings, '',
                                                 " Change the colours of various items"))),
                               ("&Data", (("&Tabs", self.tab_settings, '',
                                           " Change the titles of the tabs"),
                                          ("&Soorten", self.cat_settings, '',
                                           " Add/change type categories"),
                                          ("St&atussen", self.stat_settings, '',
                                           " Add/change status categories"))),
                               ("&Het leven", self.silly_menu, '',
                                " Change the way you look at life"))),
                ("&View", []),
                ("&Help", (("&About", self.about_help, 'F1', " Information about this program"),
                           ("&Keys", self.hotkey_help, 'Ctrl+H', " List of shortcut keys")))]
        for tabnum, tabtitle in self.book.tabs.items():
            data[3][1].append((f'&{tabtitle}', functools.partial(self.goto_page, int(tabnum)),
                               f'Alt+{tabnum}', "switch to tab"))
        if not self.work_with_user:
            data.pop(1)     # remove login menu
        if self.multiple_projects:
            data[0][1][0] = ("&Other project", self.open_sql, 'Ctrl+O', " Select a project")
            data[0][1][1] = ("&New", self.new_project, 'Ctrl+N', " Create a new project")
        elif not self.multiple_files:
            data[0][1][:3] = []
            # data[0][1].pop(2)  # remove separator
            # data[0][1].pop(1)  # remove file - new
            # data[0][1].pop(0)  # remove file - open
        return data

    def create_book(self):
        """define the tabbed interface and its subclasses
        """
        self.book = self.gui.get_bookwidget()
        self.book.parent = self
        self.book.fnaam = ""
        if self.filename and self.multiple_projects:  # datatype == shared.DataType.SQL:
            self.book.fnaam = self.filename
        self.book.current_item = None
        self.book.data = {}
        self.book.rereadlist = True
        self.lees_settings()
        self.book.ctitels = ["actie", " ", "status", "L.wijz."]
        if self.use_separate_subject:
            self.book.ctitels.extend(("betreft", "omschrijving"))
        else:
            self.book.ctitels.append("titel")
        self.book.current_tab = -1
        self.book.pages = []
        self.book.newitem = False
        self.book.changed_item = False  # waarom True?
        self.book.pagedata = None

    def create_book_pages(self):
        "add the pages to the tabbed widget"
        self.book.pages.append(Page0(self.book))
        self.book.pages.append(Page1(self.book))
        if self.use_text_panels:
            self.book.pages.append(Page(self.book, 2))
            self.book.pages.append(Page(self.book, 3))
            self.book.pages.append(Page(self.book, 4))
            self.book.pages.append(Page(self.book, 5))
        self.book.pages.append(Page6(self.book))

        for i, page in enumerate(self.book.pages):
            self.gui.add_book_tab(self.book, page, "&" + self.book.tabs[i])
        self.enable_all_book_tabs(False)

    def not_implemented_message(self):
        "information"
        gui.show_message(self.gui, "Sorry, werkt nog niet")

    def new_file(self, event=None):
        "Menukeuze: nieuw file"
        self.is_newfile = False
        # self.dirname = str(self.dirname)  # defaults to '.' so no need for `or os.getcwd()`
        fname = gui.get_save_filename(self.gui, start=self.dirname)
        if fname:
            test = pathlib.Path(fname)
            if test.suffix != '.xml':
                gui.show_message(self.gui, 'Naam voor nieuw file moet wel extensie .xml hebben')
                return
            self.dirname, self.filename = test.parent, test.name
            self.is_newfile = True
            self.startfile()
            self.is_newfile = False
            self.enable_all_book_tabs(False)

    def open_xml(self, event=None):
        "Menukeuze: open file"
        self.dirname = self.dirname or os.getcwd()
        fname = gui.get_open_filename(self.gui, start=self.dirname)
        if fname:
            test = pathlib.Path(fname)
            self.dirname, self.filename = test.parent, test.name
            self.startfile()

    def new_project(self, event=None):
        "Menukeuze: nieuw project"
        gui.show_message(self.gui, "Voor deze functie moet u de ActieReg webapplicatie gebruiken")

    def open_sql(self, event=None, do_sel=True):
        "Menukeuze: open project"
        # shared.log('in open_sql: %s', self.filename)
        current = choice = 0
        data = [f'{x}: {y}' for x, y in self.projnames.values()]
        for i, x in enumerate(data):
            if x.lower().startswith(self.filename.lower()):
                current = i
                choice = self.filename
        if do_sel or not choice:
            choice = gui.get_choice_item(self.gui, 'Kies een project om te openen', data, current)
        if choice:
            self.filename = choice.split(': ')[0]
            self.startfile()

    def open_mongo(self, event=None):
        "open database for the MongoDB version"
        self.filename = 'default'
        self.startfile()

    def print_something(self, event=None):
        """callback voor ctrl-P(rint)

        vraag om printen scherm of actie, bv. met een InputDialog
        """
        choices = ['huidig scherm', 'huidige actie']
        choice = gui.get_choice_item(self.gui, 'Wat wil je afdrukken?', choices)
        if choice == choices[0]:
            self.print_scherm()
        else:  # if choice == choices[1]:  geen andere mogelijkheid
            self.print_actie()

    def print_scherm(self, event=None):
        "Menukeuze: print dit scherm"
        self.printdict = {'lijst': [], 'actie': [], 'sections': [], 'events': []}
        if self.book.current_tab == 0:
            self.hdr = "Overzicht acties uit " + self.filename
            lijst = []
            page = self.book.pages[0]
            for item in page.gui.get_items(page.p0list):
                actie = page.gui.get_item_text(page.p0list, item, 0)
                started = self.book.pagedata.datum if self.book.pagedata else 'action start'
                soort = page.gui.get_item_text(page.p0list, item, 1)
                for x in self.book.cats.values():
                    oms, code = x[0], x[1]
                    if code == soort:
                        soort = oms
                        break
                status = page.gui.get_item_text(page.p0list, item, 2)
                l_wijz = page.gui.get_item_text(page.p0list, item, 3)
                titel = page.gui.get_item_text(page.p0list, item, 4)
                if self.use_separate_subject:
                    over = titel
                    titel = page.gui.get_item_text(page.p0list, item, 5)
                    l_wijz = l_wijz[:19]
                    actie = actie + " - " + over
                    started = started[:19]
                if status != self.book.stats[0][0]:
                    if l_wijz:
                        l_wijz = f", laatst behandeld op {l_wijz}"
                    l_wijz = f"status: {status}{l_wijz}"
                else:
                    l_wijz = f"status: {status} op {started}"
                lijst.append((actie, titel, soort, started, l_wijz))
            self.printdict['lijst'] = lijst
        else:
            self.hdr = f"Actie: {self.book.pagedata.id} {self.book.pagedata.titel}"
            if self.book.current_tab == 1:
                page = self.book.pages[1]
                self.printdict['actie'] = page.gui.get_textfield_value(page.id_text)
                self.printdict['datum'] = page.gui.get_textfield_value(page.date_text)
                self.printdict['oms'] = page.gui.get_textfield_value(page.proc_entry)
                self.printdict['tekst'] = page.gui.get_textfield_value(page.desc_entry)
                self.printdict['soort'] = page.gui.get_choice_data(page.cat_choice)
                self.printdict['status'] = page.gui.get_choice_data(page.stat_choice)
                if not self.use_text_panels:
                    self.printdict['melding'] = page.gui.get_textbox_value(page.summary_entry)
                # self.hdr = f"Informatie over actie {data['actie']}: samenvatting"
                self.hdr = f"Informatie over actie {self.printdict['actie']}: samenvatting"
            elif self.book.current_tab == len(self.book.pages) - 1:
                events = []
                for idx, data in enumerate(self.book.pages[-1].event_list):
                    # if self.datatype == shared.DataType.SQL:
                    # if len(data) >= len('eejj-mm-dd hh:mm:ss'):
                    #     data = data[:19]
                    events.append((data, self.book.pages[-1].event_data[idx]))
                self.printdict['events'] = events
            else:   # 2 <= self.book.current_tab <= 5 and self.use_text_panels - enige alternatief
                title = self.book.tabs[self.book.current_tab].split(None, 1)[1]
                text = self.book.pages[self.book.current_tab].gui.get_textarea_contents(
                    self.book.pages[self.book.current_tab].text1)
                self.printdict['sections'] = [(title, text)]
            # else:  # if self.book.current_tab == 6: - geen andere mogelijkheid
        self.gui.preview()

    def print_actie(self, event=None):
        "Menukeuze: print deze actie"
        if self.book.pagedata is None:  # or self.book.newitem:
            gui.show_message(self.gui, "Wel eerst een actie kiezen om te printen")
            return
        self.hdr = f"Actie: {self.book.pagedata.id} {self.book.pagedata.titel}"
        tekst = self.book.pagedata.titel
        try:
            oms, tekst = tekst.split(" - ", 1)
        except ValueError:
            try:
                oms, tekst = tekst.split(": ", 1)
            except ValueError:
                oms = ''
        srt = "(onbekende soort)"
        # for srtoms, srtcode in self.book.cats.values()[:2]:
        for soort in self.book.cats.values():
            # if srtcode == self.book.pagedata.soort:
            if soort[1] == self.book.pagedata.soort:
                # srt = srtoms
                srt = soort[0]
                break
        stat = "(onbekende status)"
        # for statoms, statcode in self.book.stats.values():
        for stat in self.book.stats.values():
            # if statcode == self.book.pagedata.status:
            if stat[1] == self.book.pagedata.status:
                # stat = statoms
                stat = stat[0]
                break
        self.printdict = {'lijst': [],
                          'actie': self.book.pagedata.id,
                          'datum': self.book.pagedata.datum,
                          'oms': oms,
                          'tekst': tekst,
                          'soort': srt,
                          'status': stat}
        empty = "(nog niet beschreven)"
        if self.use_text_panels:
            sections = [[title.split(None, 1)[1], ''] for key, title in
                        sorted(self.book.tabs.items()) if 2 <= key < 6]
            sections[0][1] = self.book.pagedata.melding or empty
            sections[1][1] = self.book.pagedata.oorzaak or empty
            sections[2][1] = self.book.pagedata.oplossing or empty
            sections[3][1] = self.book.pagedata.vervolg or ''
            if not sections[3][1]:
                sections.pop()
            self.printdict['sections'] = sections
        else:
            self.printdict['sections'] = [['Probleem/wens', self.book.pagedata.melding]]
        self.printdict['events'] = list(self.book.pagedata.events)  # [(x, y) for x, y in self.book.pagedata.events] or []
        self.gui.preview()

    def exit_app(self, event=None):
        "Menukeuze: exit applicatie"
        self.exiting = True
        ok_to_leave = True
        if self.book.current_tab >= 0:
            ok_to_leave = self.book.pages[self.book.current_tab].leavep(-1)
        if ok_to_leave:
            self.gui.exit()

    def sign_in(self, *args):
        """aanloggen in SQL/Django mode
        """
        logged_in = False
        dialog = LoginBox(self)
        while not logged_in:
            ok = gui.show_dialog(dialog.gui)
            if not ok:
                break
            test = dmls.validate_user(*self.dialog_data)
            if test[0]:
                text = 'Login accepted'
                logged_in = True
            else:
                text = 'Login failed'
            gui.show_message(self.gui, text)
        if logged_in:
            self.user, self.is_user, self.is_admin = test
            self.book.rereadlist = True
            self.enable_settingsmenu()
            if self.is_user or self.is_admin:
                self.book.pages[0].saved_sortopts = dmls.SortOptions(self.filename)
            else:
                self.book.pages[0].saved_sortopts = None
            self.gui.refresh_page()

    def tab_settings(self, event=None):
        "Menukeuze: settings - data - tab titels"
        gui.show_dialog(SettOptionsDialog(self, TabOptions, "Wijzigen tab titels").gui)

    def stat_settings(self, event=None):
        "Menukeuze: settings - data - statussen"
        gui.show_dialog(SettOptionsDialog(self, StatOptions, "Wijzigen statussen").gui)

    def cat_settings(self, event=None):
        "Menukeuze: settings - data - soorten"
        gui.show_dialog(SettOptionsDialog(self, CatOptions, "Wijzigen categorieën").gui)

    def font_settings(self, event=None):
        "Menukeuze: settings - applicatie - lettertype"
        self.not_implemented_message()

    def colour_settings(self, event=None):
        "Menukeuze: settings - applicatie - kleuren"
        self.not_implemented_message()

    def hotkey_settings(self, event=None):
        "Menukeuze: settings - applicatie- hotkeys (niet geactiveerd)"
        self.not_implemented_message()

    def about_help(self, event=None):
        "Menukeuze: help - about"
        gui.show_message(self.gui, "GUI versie van mijn actiebox")

    def hotkey_help(self, event=None):
        "menukeuze: help - keys"
        if not self.helptext:
            lines = ["=== Albert's actiebox ===\n",
                     "Keyboard shortcuts:",
                     "    Alt left/right:                verder - terug",
                     "    Alt-0 t/m Alt-6:               naar betreffende pagina",
                     "    Alt-O op tab 1:                S_o_rteren",
                     "    Alt-I op tab 1:                F_i_lteren",
                     "    Alt-G of Enter op tab 1:       _G_a naar aangegeven actie",
                     "    Alt-N op elke tab:             _N_ieuwe actie opvoeren",
                     "    Ctrl-P:                        _p_rinten (scherm of actie)",
                     "    Shift-Ctrl-P:                  print scherm",
                     "    Alt-Ctrl-P:                    print actie",
                     "    Ctrl-Q:                        _q_uit actiebox",
                     "    Ctrl-H:                        _h_elp (dit scherm)",
                     "    Ctrl-S:                        gegevens in het scherm op_s_laan",
                     "    Ctrl-G:                        oplaan en _g_a door naar volgende tab",
                     "    Ctrl-Z in een tekstveld:       undo",
                     "    Shift-Ctrl-Z in een tekstveld: redo",
                     "    Alt-Ctrl-Z overal:             wijzigingen ongedaan maken",
                     "    Shift-Ctrl-N op laatste tab:   nieuwe regel opvoeren",
                     "    Ctrl-up/down op laatste tab:   omhoog/omlaag in list"]
            if self.multiple_files:
                lines.insert(8, "    Ctrl-O:                       _o_pen een (ander) actiebestand")
                lines.insert(8, "    Ctrl-N:                       maak een _n_ieuw actiebestand")
            elif self.multiple_projects:
                lines.insert(8, "    Ctrl-O:                       selecteer een (ander) pr_o_ject")
                lines.insert(8, "    Ctrl-N:                       start een _n_ieuw project")
            self.helptext = "\n".join(lines)
        gui.show_message(self.gui, self.helptext)

    def silly_menu(self, event=None):
        "Menukeuze: settings - het leven"
        gui.show_message(self.gui, "Yeah you wish...\nHet leven is niet in te stellen helaas")

    def startfile(self):
        "initialisatie t.b.v. openen bestand / project"
        if self.multiple_files:
            fullname = self.dirname / self.filename
            retval = dmlx.checkfile(fullname, self.is_newfile)
            if retval != '':
                gui.show_message(self.gui, retval)
                return retval
            self.book.fnaam = fullname
            self.title = str(fullname)  # self.filename
        elif self.multiple_projects:
            self.book.fnaam = self.filename
            if not self.projnames:
                raise ValueError('ProgrammingError: self.projnames should never be empty')
            self.title = self.filename
        else:
            self.book.fnaam = self.filename
            self.title = ''
        self.book.rereadlist = True
        self.book.sorter = None
        self.lees_settings()
        for ix, title in self.book.tabs.items():
            self.gui.set_page_title(self.book, ix, title)
        # self.gui.set_tab_titles(self.book.tabs)
        self.book.pages[0].clear_selection()
        self.book.pages[1].vul_combos()
        if self.book.current_tab == -1:
            self.book.current_tab = 0
        if self.book.current_tab == 0:
            self.book.pages[0].vulp()
        else:
            self.gui.set_page(self.book, 0)
        self.book.changed_item = False
        return ''

    def lees_settings(self):
        """instellingen (tabnamen, actiesoorten en actiestatussen) inlezen"""
        # self.book.stats = {0: ('dummy,', 0, 0)}
        # self.book.cats = {0: ('dummy,', ' ', 0)}
        # self.book.tabs = {0: '0 start'}
        data = shared.Settings[self.datatype](self.book.fnaam)
        self.imagecount = data.imagecount
        self.startitem = data.startitem
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
        for item_value, item in data.stat.items():
            self.book.stats[int(item[1])] = db_stat_to_book_stat(item_value, item)
        for item_value, item in data.cat.items():
            self.book.cats[int(item[1])] = db_cat_to_book_cat(item_value, item)
        for tab_num, tab_item in data.kop.items():
            self.book.tabs[int(tab_num)] = db_head_to_book_head(tab_num, tab_item)

    def save_settings(self, srt, data):
        """instellingen (tabnamen, actiesoorten of actiestatussen) terugschrijven

        argumenten: soort, data
        data is een dictionary die in een van de dialogen TabOptions, CatOptions
        of StatOptions wordt opgebouwd"""
        settings = shared.Settings[self.datatype](self.book.fnaam)
        if srt == "tab":
            settings.kop = data
            settings.write()
            self.book.tabs = {}
            for item_value, item in data.items():
                self.book.tabs[int(item_value)] = db_head_to_book_head(item_value, item)
                self.gui.set_page_title(self.book, int(item_value), item[0])
        elif srt == "stat":
            settings.stat = data
            result = settings.write()
            if result:
                gui.show_message(self.gui, f'Kan status {result[1]} niet verwijderen,'
                                 ' wordt nog gebruikt in één of meer acties')
                return
            self.book.stats = {}
            for item_value, item in data.items():
                self.book.stats[int(item[1])] = db_stat_to_book_stat(item_value, item)
        else:  # if srt == "cat":  iets anders niet mogelijk
            settings.cat = data
            result = settings.write()
            if result:
                gui.show_message(self.gui, f'Kan soort {result[1]} niet verwijderen,'
                                 ' wordt nog gebruikt in één of meer acties')
                return
            self.book.cats = {}
            for item_value, item in data.items():
                self.book.cats[int(item[1])] = db_cat_to_book_cat(item_value, item)
        self.book.pages[1].vul_combos()

    def save_startitem_on_exit(self):
        "bijwerken geselecteerde actie om te onthouden voor de volgende keer"
        data = shared.Settings[self.datatype](self.book.fnaam)
        if data.startitem and self.book.pagedata:
            data.startitem = self.book.pagedata.id
            data.write()

    def goto_next(self, *args):
        """redirect to the method of the current page
        """
        # Page.goto_next(self.book.pages[self.book.current_tab])
        self.book.pages[self.book.current_tab].goto_next()

    def goto_prev(self, *args):
        """redirect to the method of the current page
        """
        # Page.goto_prev(self.book.pages[self.book.current_tab])
        self.book.pages[self.book.current_tab].goto_prev()

    def goto_page(self, page):
        """redirect to the method of the current page
        """
        # Page.goto_page(self.book.pages[self.book.current_tab], page)
        self.book.pages[self.book.current_tab].goto_page(page)

    def enable_settingsmenu(self):
        "instellen of gebruik van settingsmenu mogelijk is"
        self.gui.enable_settingsmenu()

    def set_windowtitle(self, text):
        "build title for window"
        self.gui.set_window_title(text)

    def set_statusmessage(self, msg=''):
        """stel tekst in statusbar in
        """
        if not msg:
            msg = self.book.pagehelp[self.book.current_tab]
            if self.book.current_tab == 0:
                msg += f' - {len(self.book.data)} items'
        self.gui.set_statusmessage(msg)
        if self.work_with_user:
            msg = f'Aangemeld als {self.user.username}' if self.user else 'Niet aangemeld'
            self.gui.show_username(msg)

    def get_focus_widget_for_tab(self, tabno):
        "determine field to set focus on"
        widgets = [self.book.pages[0].p0list,
                   self.book.pages[1].proc_entry]
        if self.use_text_panels:
            widgets.extend([self.book.pages[2].text1,
                            self.book.pages[3].text1,
                            self.book.pages[4].text1,
                            self.book.pages[5].text1])
        widgets.append(self.book.pages[-1].progress_list)
        return widgets[tabno]

    def enable_book_navigation(self, state, tabfrom=0, tabto=-1):
        "make specified tabs (in)accessible"
        if tabto == -1:
            tabto = self.gui.get_tab_count(self.book)
        for i in range(tabfrom, tabto):
            self.gui.enable_tab(self.book, i, state)

    def enable_all_book_tabs(self, state):
        "make all tabs (in)accessible"
        self.enable_book_navigation(state, tabfrom=1)

    def enable_all_other_tabs(self, state):
        "make all tabs accessible except the current one"
        for i in range(self.gui.get_tab_count(self.book)):
            if i != self.book.current_tab:
                self.gui.enable_tab(self.book, i, state)


class Page:
    "base class for notebook page"
    def __init__(self, parent, pageno, standard=True):
        self.book = parent
        self.appbase = self.book.parent
        self.pageno = pageno
        self.is_text_page = standard
        if standard:
            self.gui = gui.PageGui(parent, self)
            sizer = self.gui.start_display()
            self.text1 = self.gui.create_text_field(sizer, 490, 330 if LIN else 430, self.on_text)
            if self.appbase.use_rt:
                data = self.get_toolbar_data(self.text1)
                self.toolbar = self.gui.create_toolbar(sizer, self.text1, data)
            self.save_button, self.saveandgo_button, self.cancel_button = self.gui.create_buttons(
                [('Sla wijzigingen op (Ctrl-S)', self.savep),
                 ('Sla op en ga verder (Ctrl-G)', self.savepgo),
                 ('Zet originele tekst terug (Alt-Ctrl-Z)', self.restorep)], sizer)
            self.gui.add_keybind('Alt-N', self.nieuwp, last=True)

    def get_toolbar_data(self, textfield):
        "return texts, shortcuts and picture names for setting op toolbar"
        return (('&Bold', 'Ctrl+B', 'icons/sc_bold', 'Toggle Bold', textfield.text_bold,
                 textfield.update_bold),
                ('&Italic', 'Ctrl+I', 'icons/sc_italic', 'Toggle Italic', textfield.text_italic,
                 textfield.update_italic),
                ('&Underline', 'Ctrl+U', 'icons/sc_underline', 'Toggle Underline',
                 textfield.text_underline, textfield.update_underline),
                ('Strike&through', 'Ctrl+~', 'icons/sc_strikethrough', 'Toggle Strikethrough',
                 textfield.text_strikethrough),
                # ("Toggle &Monospace", 'Shift+Ctrl+M', 'icons/text',
                #     'Switch using proportional font off/on', textfield.toggle_monospace),
                (),
                ("&Enlarge text", 'Ctrl+Up', 'icons/sc_grow', 'Use bigger letters',
                 textfield.enlarge_text),
                ("&Shrink text", 'Ctrl+Down', 'icons/sc_shrink', 'Use smaller letters',
                 textfield.shrink_text),
                (),
                ('To &Lower Case', 'Shift+Ctrl+L', 'icons/sc_changecasetolower',
                 'Use lower case letters', textfield.case_lower),
                ('To &Upper Case', 'Shift+Ctrl+U', 'icons/sc_changecasetoupper',
                 'Use upper case letters', textfield.case_upper),
                (),
                ("Indent &More", 'Ctrl+]', 'icons/sc_incrementindent', 'Increase indentation',
                 textfield.indent_more),
                ("Indent &Less", 'Ctrl+[', 'icons/sc_decrementindent', 'Decrease indentation',
                 textfield.indent_less),
                (),
                # ("Normal Line Spacing", '', 'icons/sc_spacepara1',
                #     'Set line spacing to 1', textfield.linespacing_1),
                # ("1.5 Line Spacing",    '', 'icons/sc_spacepara15',
                #     'Set line spacing to 1.5', textfield.linespacing_15),
                # ("Double Line Spacing", '', 'icons/sc_spacepara2',
                #     'Set line spacing to 2', textfield.linespacing_2),
                # (),
                ("Increase Paragraph &Spacing", '', 'icons/sc_paraspaceincrease',
                 'Increase spacing between paragraphs', textfield.increase_paragraph_spacing),
                ("Decrease &Paragraph Spacing", '', 'icons/sc_paraspacedecrease',
                 'Decrease spacing between paragraphs', textfield.decrease_paragraph_spacing))

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        self.initializing = True
        # if self.appbase.datatype != shared.DataType.MNG:
        if self.book.current_tab == 0:
            text = self.seltitel
        else:
            # state = self.book.current_tab == 1 and self.book.newitem
            # self.enable_buttons(state)
            # if state:
            #     self.book.changed_item = not state  # zorgen dat deze hier altijd uit staat
            text = self.book.tabs[self.book.current_tab].split(None, 1)[1]
            if self.book.pagedata:
                text = self.book.pagedata.titel
                if self.appbase.use_separate_subject:
                    text = f'{self.book.pagedata.over} - {text}'
                text = f'{self.book.pagedata.id} {text}'
        test = self.appbase.title
        if test:
            self.appbase.set_windowtitle(f"{test} | {text}")
        else:
            self.appbase.set_windowtitle(text)
        self.appbase.set_statusmessage()
        if 1 < self.book.current_tab < len(self.book.pages) - 1:
            self.oldbuf = ''
            is_readonly = False
            if self.book.pagedata is not None:
                self.oldbuf = self.get_pagetext()
                is_readonly = self.book.pagedata.arch
            self.gui.set_textarea_contents(self.text1, self.oldbuf)
            if not is_readonly:
                is_readonly = not self.appbase.is_user
            self.gui.set_text_readonly(self.text1, is_readonly)
            if self.appbase.use_rt:
                self.gui.enable_toolbar(self.toolbar, self.appbase.is_user)
            self.oldbuf = self.gui.get_textarea_contents(self.text1)  # make sure it's rich text
            self.gui.move_cursor_to_end(self.text1)
        self.initializing = False
        self.appbase.enable_all_other_tabs(not self.book.newitem)

    def get_pagetext(self):
        "read the textfield on the given page"
        text = ''
        if self.book.current_tab == 2:
            text = self.book.pagedata.melding
        elif self.book.current_tab == 3:
            text = self.book.pagedata.oorzaak
        elif self.book.current_tab == 4:
            text = self.book.pagedata.oplossing
        else:  # if self.book.current_tab == 5: -- momenteel enig andere mogelijkhedi
            text = self.book.pagedata.vervolg
        return text

    def readp(self, pid):
        "lezen van een actie"
        if self.book.pagedata:  # spul van de vorige actie opruimen
            self.book.pagedata.cleanup()
        self.book.pagedata = shared.Actie[self.appbase.datatype](self.book.fnaam, pid,
                                                                 self.appbase.user)
        self.appbase.imagelist = self.book.pagedata.imagelist
        self.book.old_id = self.book.pagedata.id
        self.book.newitem = False

    def nieuwp(self, *args):
        """voorbereiden opvoeren nieuwe actie"""
        shared.log('opvoeren nieuwe actie')
        if not self.appbase.is_user:
            msg = 'Opvoeren niet toegestaan, u bent niet ingelogd'
            gui.show_message(self.book, msg, "Navigatie niet toegestaan")
            return
        if self.leavep(1):
            self.book.oldselection = self.book.current_item
            self.book.newitem = True
            # is dit wel slim? Alle navigatie moet dicht maar dat moeten we in tab 1 regelen
            # if self.book.current_tab == 0:
            #     self.appbase.enable_book_navigation(True, tabfrom=1)
            self.book.pagedata = shared.Actie[self.appbase.datatype](self.book.fnaam, 0,
                                                                     self.appbase.user)
            self.book.pagedata.add_event('Actie opgevoerd')
            self.appbase.imagelist = self.book.pagedata.imagelist
            if self.book.current_tab == 1:
                self.vulp()  # om de velden leeg te maken
                self.gui.set_focus_to_field(self.proc_entry)
            else:
                self.goto_page(1, check=False)
        else:
            shared.log("leavep() geeft False: nog niet klaar met huidige pagina")

    def leavep(self, newtab):
        "afsluitende acties uit te voeren alvorens de pagina te verlaten"
        ok_to_leave = True
        if self.book.current_tab == 0:
            if self.appbase.exiting:
                pass
            elif not self.book.current_item:
                msg = "Selecteer eerst een actie"
                ok_to_leave = False
            elif self.book.fnaam == "":
                wat = ''
                if self.appbase.multiple_files:  # datatype == shared.DataType.XML.name:
                    wat = 'bestand'
                elif self.appbase.multiple_projects:  # datatype == shared.DataType.SQL.name:
                    wat = 'project'
                else:
                    raise ValueError('ProgrammingError: fnaam should only be empty'
                                     ' with multiple files or projects')
                msg = f"Kies eerst een {wat} om mee te werken"
                ok_to_leave = False
            elif not self.book.data and not self.book.newitem:
                # bestand bevat nog geen gegevens en we zijn nog niet bezig met de eerste opvoeren
                msg = "Voer eerst één of meer acties op"
                ok_to_leave = False
            elif self.book.current_item == -1 and not self.book.newitem:
                # geen actie geselecteerd en we zijn niet bezig met een nieuwe
                msg = "Selecteer eerst een actie"
                ok_to_leave = False
            if not ok_to_leave:
                gui.show_message(self.book, msg, "Navigatie niet toegestaan")
        elif self.book.current_tab == 1 and self.book.newitem:
            if newtab > 1:
                gui.show_message(self.book,
                                 "Nieuwe actie: navigatie naar vervolgpagina's niet toegestaan",
                                 self.appbase.title)
                ok_to_leave = False
            elif newtab == 0:
                ok_to_leave = self.abort_add()
        elif self.book.changed_item:
            message = ("De gegevens op de pagina zijn gewijzigd,\n"
                       "wilt u de wijzigingen opslaan voordat u verder gaat?")
            ok, cancel = gui.ask_cancel_question(self.gui, message)
            if ok:
                ok_to_leave = self.savep()
            elif cancel:
                ok_to_leave = False
            if not cancel:
                self.appbase.enable_all_other_tabs(True)
        return ok_to_leave

    def savep(self, *args):
        "gegevens van een actie opslaan afhankelijk van pagina"
        if not self.gui.is_enabled(self.save_button):
            return False
        self.enable_buttons(False)
        if self.book.current_tab <= 1 or self.book.current_tab == 6:
            return False
        if self.book.current_tab == 2 and not self.appbase.use_text_panels:
            return False
        text = self.gui.get_textarea_contents(self.text1)
        event_text = ''
        if self.book.current_tab == 2 and text != self.book.pagedata.melding:
            self.oldbuf = self.book.pagedata.melding = text
            event_text = "Meldingtekst aangepast"
        if self.book.current_tab == 3 and text != self.book.pagedata.oorzaak:
            self.oldbuf = self.book.pagedata.oorzaak = text
            event_text = "Beschrijving oorzaak aangepast"
        if self.book.current_tab == 4 and text != self.book.pagedata.oplossing:
            self.oldbuf = self.book.pagedata.oplossing = text
            event_text = "Beschrijving oplossing aangepast"
        if self.book.current_tab == 5 and text != self.book.pagedata.vervolg:
            self.oldbuf = self.book.pagedata.vervolg = text
            event_text = "Tekst vervolgactie aangepast"
        if event_text:
            self.book.pagedata.add_event(event_text)
            self.update_actie()
        return True

    def savepgo(self, *args):
        "opslaan en naar de volgende pagina"
        if not self.gui.is_enabled(self.saveandgo_button):
            return
        if self.savep():
            self.goto_next()
        else:
            self.enable_buttons()

    def restorep(self, *args):
        "oorspronkelijke (laatst opgeslagen) inhoud van de pagina herstellen"
        # reset font - are these also needed: case? indent? linespacing? paragraphspacing?
        if self.book.current_tab > 1 and self.appbase.use_rt:
            self.gui.reset_font()
        if self.book.current_tab == len(self.book.pages) - 1 and self.status_auto_changed:
            self.book.pagedata.status = '0'
        self.vulp()

    def on_text(self, *args):
        """callback voor EVT_TEXT e.d.

        de initializing flag wordt uitgevraagd omdat deze event ook tijdens vulp()
        en tijdens vul_combos plaatsvindt"""
        if not self.initializing:
            newbuf = self.build_newbuf()
            changed = newbuf != self.oldbuf
            self.enable_buttons(changed)

    # def on_choice(self):
    #     "callback voor combobox (? wordt on_text hier niet gewoon voor gebruikt?)"
    #     self.enable_buttons()

    def build_newbuf(self):
        """read widget contents into the compare buffer
        """
        return self.gui.get_textarea_contents(self.text1)

    def update_actie(self):
        """pass page data from the GUI to the internal storage
        """
        self.book.pagedata.imagecount = self.appbase.imagecount
        self.book.pagedata.imagelist = self.appbase.imagelist
        # aangenomen dat "gemeld" altijd "0" zal blijven en de eerstvolgende status "1"
        # if self.book.current_tab >= 3 and self.book.pagedata.status == '0':
        if (self.book.pagedata.status == '0' and self.appbase.use_text_panels
                and self.book.current_tab >= 3):
            self.book.pagedata.status = '1'
            sel = [y for x, y in self.book.stats.items() if y[1] == '1'][0]
            self.book.pagedata.add_event(f'Status gewijzigd in "{sel[0]}"')

        if self.appbase.work_with_user:
            self.book.pagedata.write(self.appbase.user)
        else:
            self.book.pagedata.write()

        self.book.pagedata.read()
        if self.book.newitem:
            # nieuwe entry maken in de tabel voor panel 0
            # jamaar hier zit toch ook een verschil voor de verschillende datatypes?
            newindex = len(self.book.data)  # + 1
            page = self.book.pages[1]
            itemdata = (page.gui.get_textfield_value(self.date_text),
                        " - ".join((page.gui.get_textfield_value(self.proc_entry),
                                    page.gui.get_textfield_value(self.desc_entry))),
                        page.gui.get_choice_data(self.stat_choice)[0],
                        page.gui.get_choice_data(self.cat_choice)[0],
                        page.gui.get_textfield_value(self.id_text))
            self.book.data[newindex] = itemdata
            # ook nieuwe entry maken in de visuele tree
            page = self.book.pages[0]
            self.book.current_item = page.gui.add_listitem(itemdata[0].split(' ')[0])
            page.gui.set_selection(page.p0list)
            self.book.newitem = False
            self.book.rereadlist = True
        else:
            # actiegegevens bijwerken op panel 0
            page = self.book.pages[0]
            item = page.gui.get_selection(page.p0list)
            page.gui.set_item_text(item, 1, self.book.pagedata.get_soorttext()[0].upper())
            page.gui.set_item_text(item, 2, self.book.pagedata.get_statustext())
            page.gui.set_item_text(item, 3, self.book.pagedata.updated)
            if self.appbase.use_separate_subject:
                page.gui.set_item_text(item, 4, self.book.pagedata.over)
                page.gui.set_item_text(item, 5, self.book.pagedata.titel)
            else:
                page.gui.set_item_text(item, 4, self.book.pagedata.titel)

    def enable_buttons(self, state=True):
        "buttons wel of niet bruikbaar maken"
        self.gui.enable_widget(self.save_button, state)
        if self.book.current_tab < len(self.book.pages) - 1:
            self.gui.enable_widget(self.saveandgo_button, state)
        self.gui.enable_widget(self.cancel_button, state)
        self.book.changed_item = state
        if self.book.current_tab > 0:
            self.appbase.enable_all_other_tabs(not state)

    def goto_actie(self):
        "naar startpagina actie gaan"
        self.goto_page(1)

    def goto_next(self, *args):
        "naar de volgende pagina gaan"
        next = self.book.current_tab + 1
        if self.leavep(next):
            if next >= len(self.book.pages):
                next = 0
            self.appbase.gui.set_page(self.book, next)

    def goto_prev(self, *args):
        "naar de vorige pagina gaan"
        next = self.book.current_tab - 1
        if self.leavep(next):
            if next < 0:
                next = len(self.book.pages) - 1
            self.appbase.gui.set_page(self.book, next)

    def goto_page(self, page_num, check=True):
        "naar de aangegeven pagina gaan"
        if (not check or self.leavep(page_num)) and 0 <= page_num < len(self.book.pages):
            self.appbase.gui.set_page(self.book, page_num)

    def get_textarea_contents(self):
        "get the page text"
        return self.gui.get_textarea_contents(self.text1)

    def abort_add(self):
        "opvoeren nieuw item afbreken"
        message = "Weet u zeker dat u het opvoeren van de actie wilt afbreken?"
        ok = gui.ask_question(self.gui, message)
        if ok:
            self.book.newitem = False
            self.appbase.enable_all_other_tabs(True)
            self.book.current_item = self.book.oldselection  # oude selectie terugzetten
        return ok


class Page0(Page):
    "pagina 0: overzicht acties"
    def __init__(self, parent):
        self.book = parent
        super().__init__(parent, pageno=0, standard=False)
        self.selection = 'excl. gearchiveerde'
        self.sel_args = {}
        self.sorted = (0, "A")

        # widths = [94, 24, 146, 90, 400] if LIN else [64, 24, 114, 72, 292]
        widths = [122, 24, 146, 100, 300] if LIN else [64, 24, 114, 72, 292]
        if self.appbase.use_separate_subject:
            # widths[4] = 90 if LIN else 72
            # extra = 310 if LIN else 220
            # widths.append(extra)
            # widths[4:] = [90, 310] if LIN else [72, 220]
            # widths.append(90 if LIN else 72)
            extra = [140, 140, 210] if LIN else [100, 110, 220]
            widths = widths[:3] + extra

        self.gui = gui.Page0Gui(parent, self)
        self.p0list = self.gui.add_list(self.book.ctitels, widths)
        self.buttons = self.gui.create_buttons([('S&Orteer', self.sort_items),
                                                ('F&Ilter', self.select_items),
                                                ('&Ga naar melding', self.goto_actie),
                                                ('&Archiveer', self.archiveer),
                                                ('Voer &Nieuwe melding op', self.nieuwp)])
        self.gui.finish_display()
        self.p0list.has_selection = False
        self.enable_buttons()

        self.sort_via_options = False
        self.saved_sortopts = None
        # dit werkt hier alleen als ik met een user heb kunnen aanloggen vóór start van de GUI
        # if self.appbase.work_with_user and self.appbase.is_user:
        #     self.saved_sortopts = dmls.SortOptions(self.appbase.filename)
        # self.gui.add_keybind('Alt-N', self.nieuwp, last=True) -- zit al in buttons

    def enable_buttons(self):
        "buttons wel of niet bruikbaar maken"
        sort_button, filter_button, go_button, archive_button, new_button = self.buttons
        self.gui.enable_widget(filter_button, bool(self.appbase.user))
        self.gui.enable_widget(go_button, self.p0list.has_selection)
        self.gui.enable_widget(new_button, self.appbase.is_user and bool(self.appbase.filename))
        if self.p0list.has_selection:
            self.gui.enable_widget(sort_button, bool(self.appbase.user))
            self.gui.enable_widget(archive_button, self.appbase.is_user)
        else:
            self.gui.enable_widget(sort_button, False)
            self.gui.enable_widget(archive_button, False)

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina
        """
        self.selection = ''
        if self.appbase.work_with_user:
            if self.saved_sortopts:
                # laden hier doen garandeert wijzigen van opties bij wijzigen project
                self.saved_sortopts.load_options()
                self.sort_via_options = True
        self.gui.enable_sorting(self.p0list, not self.sort_via_options)
        if self.sort_via_options:
            self.selection = 'volgens user gedefinieerde selectie'

        self.seltitel = 'alle meldingen ' + self.selection
        super().vulp()
        msg = ''
        if self.book.rereadlist:
            msg = self.populate_list()
            self.book.rereadlist = False
            if self.appbase.startitem:
                self.book.current_item = self.gui.get_item_by_id(self.p0list, self.appbase.startitem)
            else:
                self.book.current_item = self.gui.get_first_item(self.p0list)
        self.appbase.enable_all_book_tabs(False)
        self.enable_buttons()
        if self.p0list.has_selection:
            self.appbase.enable_all_book_tabs(True)
            self.gui.set_selection(self.p0list)
            self.gui.ensure_visible(self.p0list, self.book.current_item)
        self.appbase.set_statusmessage(msg)

    def populate_list(self):
        "list control vullen"
        self.book.data = {}
        self.gui.clear_list(self.p0list)

        select = self.sel_args.copy()
        arch = select.pop("arch") if ("arch" in select) else ""  # "alles"
        data = shared.get_acties[self.appbase.datatype](self.book.fnaam, select,
                                                        arch, self.appbase.user)
        for idx, item in enumerate(data):
            if len(item) == 7:  # type == self.appbase.shared.DataType.XML:
                self.book.data[idx] = (item[0],
                                       item[1],
                                       ".".join((item[3][1], item[3][0])),
                                       ".".join((item[2][1], item[2][0])),
                                       item[5],
                                       item[4],
                                       item[6] == 'arch')
            elif len(item) == 8:  # type == self.appbase.shared.DataType.MNG:
                cats = {y: x for x, y in self.book.cats.values()}
                stats = {y: x for x, y in self.book.stats.values()}
                self.book.data[idx] = (item[0],
                                       item[1],
                                       '.'.join((item[2], cats[item[2]])),
                                       '.'.join((item[3], stats[item[3]])),
                                       item[4],
                                       item[5],
                                       item[6],
                                       item[7])
            elif len(item) == 10:  # type == self.appbase.shared.DataType.SQL:
                self.book.data[idx] = (item[0],
                                       item[1],
                                       ".".join((item[5], item[4])),
                                       ".".join((str(item[3]), item[2])),
                                       item[8],
                                       item[6],
                                       item[7],
                                       item[9])
            else:
                raise ValueError('ProgrammingError: Unexpected length of pagedata item')
        # items = self.book.data.items()
        # if items is None:
        #     self.appbase.set_statusmessage('Selection is None?')
        # for _, data in items:
        for data in self.book.data.values():
            new_item = self.gui.add_listitem(self.p0list, data[0])
            self.set_listitem_values(self.p0list, new_item, [data[0]] + list(data[2:]))
        return f'{len(data)} items found'

    def set_listitem_values(self, p0list, item, data):
        "set column values for list entry"
        for col, value in enumerate(data):
            if col == 0 and data[-1]:
                value = value + ' (A)'
            elif col == 1:
                pos = value.index(".") + 1
                value = value[pos:pos + 1].upper()
            elif col == 2:
                pos = value.index(".") + 1
                value = value[pos:]
            if col < len(data) - 1:
                self.gui.set_item_text(p0list, item, col, value)
        p0list.has_selection = bool(data)  # True

    def change_selected(self, item_n):
        """callback voor wijzigen geselecteerd item, o.a. door verplaatsen van de
        cursor of door klikken
        """
        self.book.current_item = item_n
        self.gui.set_selection(self.p0list)
        if not self.book.newitem:
            selindx = self.gui.get_selected_action(self.p0list)
            self.readp(selindx)
        hlp = "&Herleef" if self.book.pagedata.arch else "&Archiveer"
        self.gui.set_button_text(self.buttons[3], hlp)

    def activate_item(self):
        """callback voor activeren van item, door doubleclick of enter
        """
        self.goto_actie()

    def select_items(self, event=None):
        """tonen van de selectie dialoog

        niet alleen selecteren op tekst(deel) maar ook op status, soort etc
        """
        args = self.sel_args, None
        if self.appbase.work_with_user:
            data = dmls.SelectOptions(self.book.fnaam, self.appbase.user)
            args, sel_args = data.load_options(), {}
            for key, value in args.items():
                if key == 'nummer':
                    for item in value:  # splitsen in idgt, id en idlt
                        if len(item) == 1:
                            sel_args['id'] = 'and' if item[0] == 'en' else 'or'
                        elif item[1] == 'GT':
                            sel_args['idgt'] = item[0]
                        elif item[1] == 'LT':
                            sel_args['idlt'] = item[0]
                        else:
                            raise ValueError('ProgrammingError: illegal value in select arguments')
                elif value:
                    sel_args[key] = value
                else:
                    raise ValueError('ProgrammingError: illegal value in select arguments')
            args = sel_args, data
        dialog = SelectOptionsDialog(self.book.parent, *args)
        while True:
            test = gui.show_dialog(dialog.gui)
            if not test:
                break
            self.book.rereadlist = True
            try:
                self.vulp()
            except shared.DataError[self.appbase.datatype] as msg:
                self.book.rereadlist = False
                gui.show_message(self, str(msg))
            else:
                break

    def sort_items(self, *args):
        """tonen van de sorteer-opties dialoog

        sortering mogelijk op datum/tijd, soort, titel, status via schermpje met
        2x4 comboboxjes waarin je de volgorde van de rubrieken en de sorteervolgorde
        per rubriek kunt aangeven"""
        sortopts, sortlist = {}, []
        if self.saved_sortopts:
            sortopts = self.saved_sortopts.load_options()
            # try:
            sortlist = [x[0] for x in dmls.my.SORTFIELDS]
            # except AttributeError:
            #     pass
        else:
            # beter door het vinkje uit te zetten en uit te grijzen en een melding op het scherm
            gui.show_message(self.gui, 'Sorry, multi-column sorteren werkt nog niet')
            return
        if not sortlist:
            sortlist = list(self.book.ctitels)  # [x for x in self.parent.ctitels]
            sortlist[1] = "Soort"
        sortlist.insert(0, "(geen)")
        test = gui.show_dialog(SortOptionsDialog(self.book.parent, sortopts, sortlist).gui)
        if not test:
            return
        if self.sort_via_options:
            self.gui.enable_sorting(False)
            self.book.rereadlist = True
            try:
                self.vulp()
            # moet hier soms nog het daadwerkelijke sorteren tussen (bij XML)?
            except shared.DataError[self.appbase.datatype] as msg:
                self.book.rereadlist = False
                gui.show_message(self, str(msg))
        else:
            self.gui.enable_sorting(True)

    def archiveer(self, *args):
        "archiveren of herleven van het geselecteerde item"
        self.readp(self.gui.get_selected_action(self.p0list))
        self.book.pagedata.arch = not self.book.pagedata.arch
        hlp = "gearchiveerd" if self.book.pagedata.arch else "herleefd"
        self.book.pagedata.add_event(f"Actie {hlp}")
        self.update_actie()  # self.book.pagedata.write()
        self.book.rereadlist = True  # wordt uitgezet in vulp
        self.vulp()
        self.appbase.set_tabfocus(0)
        if self.sel_args.get("arch", "") == "alles":
            self.gui.ensure_visible(self.p0list, self.book.current_item)
            hlp = "&Herleef" if self.book.pagedata.arch else "&Archiveer"
            self.gui.set_archive_button_text(hlp)

    def clear_selection(self):
        "initialize selection criteria"
        self.sel_args = {}


class Page1(Page):
    "pagina 1: startscherm actie"
    def __init__(self, parent):
        self.book = parent
        super().__init__(parent, pageno=1, standard=False)
        self.gui = gui.Page1Gui(parent, self)
        self.id_text = self.gui.add_textentry_line("Actie-id", 120)
        self.date_text = self.gui.add_textentry_line("Datum/tijd:", 150)
        self.proc_entry = self.gui.add_textentry_line("Job/\ntransactie:", 150, self.on_text)
        self.desc_entry = self.gui.add_textentry_line("Melding/code/\nomschrijving:", 360,
                                                      self.on_text)
        self.cat_choice = self.gui.add_combobox_line("Categorie:", 180, self.on_text)
        self.stat_choice = self.gui.add_combobox_line("Status:", 140, self.on_text)
        self.archive_text, self.archive_button = self.gui.add_pushbutton_line("", "Archiveren",
                                                                              self.archiveer)
        if not self.appbase.use_text_panels:
            self.summary_entry = self.gui.add_textbox_line("Samenvatting van het issue:",
                                                           self.on_text)
        self.abort_button = self.gui.create_buttons([('&Breek opvoeren nieuwe actie af (Alt-0)',
                                                      self.breekaf)])[0]
        self.save_button, self.saveandgo_button, self.cancel_button = self.gui.create_buttons(
            [('Sla wijzigingen op (Ctrl-S)', self.savep),
             ('Sla op en ga verder (Ctrl-G)', self.savepgo),
             ('Zet originele tekst terug (Alt-Ctrl-Z)', self.restorep)])
        self.gui.add_keybind('Alt-N', self.nieuwp, last=True)

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        super().vulp()
        self.initializing = True
        self.gui.show_button(self.abort_button, False)
        self.parch = False
        self.gui.set_textfield_value(self.id_text, str(self.book.pagedata.id))
        self.gui.set_textfield_value(self.date_text, self.book.pagedata.datum)
        if self.book.newitem:      # omschrijving(en) invullen niet nodig/mogelijk
            pass                   # deze conditie mag ook weg maar dan moet de else else ook weg
        else:
            self.parch = self.book.pagedata.arch
            if self.appbase.use_separate_subject:
                self.gui.set_textfield_value(self.proc_entry, self.book.pagedata.over)
                self.gui.set_textfield_value(self.desc_entry, self.book.pagedata.titel)
            elif self.book.pagedata.titel:
                if " - " in self.book.pagedata.titel:
                    hlp = self.book.pagedata.titel.split(" - ", 1)
                elif ": " in self.book.pagedata.titel:
                    hlp = self.book.pagedata.titel.split(": ", 1)
                else:
                    hlp = self.book.pagedata.titel
                self.gui.set_textfield_value(self.proc_entry, hlp[0])
                if len(hlp) > 1:
                    self.gui.set_textfield_value(self.desc_entry, hlp[1])
            else:
                raise ValueError('ProgrammmingError: subject should not be empty')
            self.gui.set_choice(self.stat_choice, self.book.stats, self.book.pagedata.status)
            self.gui.set_choice(self.cat_choice, self.book.cats, self.book.pagedata.soort)
            if not self.appbase.use_text_panels:
                self.gui.set_textbox_value(self.summary_entry, self.book.pagedata.melding)

        self.oldbuf = self.get_fieldvalues()
        if self.parch:
            aanuit = False
            self.gui.set_label_value(self.archive_text, "Deze actie is gearchiveerd")
            self.gui.set_button_text(self.archive_button, "Herleven")
        else:
            aanuit = True
            self.gui.set_label_value(self.archive_text, '')
            self.gui.set_button_text(self.archive_button, "Archiveren")

        if not self.appbase.is_user:
            aanuit = False
        self.enable_fields(aanuit)

        self.initializing = False

    def enable_fields(self, state):
        "make fields accessible, depending on user permissions"
        self.gui.enable_widget(self.id_text, False)
        self.gui.enable_widget(self.date_text, False)
        self.gui.enable_widget(self.proc_entry, state)
        self.gui.enable_widget(self.desc_entry, state)
        self.gui.enable_widget(self.cat_choice, state)
        self.gui.enable_widget(self.stat_choice, state)
        if self.book.newitem or not self.appbase.is_user:
            # archiveren niet mogelijk bij nieuw item of als de user niet is ingelogd
            self.gui.enable_widget(self.archive_button, False)
        else:
            self.gui.enable_widget(self.archive_button, True)
        if not self.appbase.use_text_panels:
            self.gui.enable_widget(self.summary_entry, state)
        if self.book.newitem:
            self.gui.show_button(self.abort_button, True)

    def savep(self, *args):
        "opslaan van de paginagegevens"
        if not super().savep():
            return False
        newbuf = self.get_fieldvalues()
        if newbuf == self.oldbuf:
            return False  # niks gewijzigd
        proc, desc = newbuf[:2]
        melding = self.check_proc_desc_gewijzigd(proc, desc)
        if melding:
            gui.show_message(self.gui, melding)
            return False
        self.check_stat_gewijzigd()
        self.check_cat_gewijzigd()
        if self.parch != self.book.pagedata.arch:
            self.book.pagedata.arch = self.parch
            hlp = "gearchiveerd" if self.parch else "herleefd"
            self.book.pagedata.add_event(f"Actie {hlp}")
        if not self.appbase.use_text_panels:
            new_summary = newbuf[-1]  # self.gui.get_textbox_value('summary')
            if new_summary != self.book.pagedata.melding:
                self.book.pagedata.melding = new_summary
                self.book.pagedata.add_event("Meldingtekst aangepast")
        self.update_actie()
        self.oldbuf = self.get_fieldvalues()
        self.enable_buttons(False)  # -- verplaatst vanuit check_proc_desc_gewijzigd
        return True

    def check_proc_desc_gewijzigd(self, proc, desc):
        """kijk of de omschrijving(en) gewijzigd is (zijn)
        en maak indien nodig de bijbehorende event(s) aan
        """
        # proc = self.gui.get_textfield_value('proc')
        # desc = self.gui.get_textfield_value('desc')
        if proc == "" or desc == "":
            melding = "Beide tekstrubrieken moeten worden ingevuld"
            return melding
        # self.enable_buttons(False) -- moet/kan dit al wel hier?
        procdesc = f"{proc} - {desc}"
        if self.appbase.use_separate_subject:
            self.gui.set_textfield_value('proc', proc.capitalize())
            if proc != self.book.pagedata.over:
                self.book.pagedata.over = proc
                self.book.pagedata.add_event(f'Onderwerp gewijzigd in "{proc}"')
            if desc != self.book.pagedata.titel:
                self.book.pagedata.titel = desc
                self.book.pagedata.add_event(f'Titel gewijzigd in "{desc}"')
        elif procdesc != self.book.pagedata.titel:
            self.gui.set_textfield_value('proc', procdesc.capitalize())
            self.book.pagedata.titel = procdesc
            self.book.pagedata.add_event(f'Titel gewijzigd in "{procdesc}"')
        return ''

    def check_stat_gewijzigd(self):
        "kijk of de status gewijzigd is en maak indien nodig de bijbehorende event aan"
        newstat, sel = self.gui.get_choice_data(self.gui.stat_choice)
        verb = ''
        if self.book.newitem:
            verb = 'is'
        elif newstat != self.book.pagedata.status:
            verb = 'gewijzigd in'
        if verb:
            self.book.pagedata.status = newstat
            self.book.pagedata.add_event(f'Status {verb} "{sel}"')

    def check_cat_gewijzigd(self):
        "kijk of de categorie gewijzigd is en maak indien nodig de bijbehorende event aan"
        newcat, sel = self.gui.get_choice_data(self.gui.cat_choice)
        verb = ''
        if self.book.newitem:
            verb = 'is'
        elif newcat != self.book.pagedata.soort:
            verb = 'gewijzigd in'
        if verb:
            self.book.pagedata.soort = newcat
            self.book.pagedata.add_event(f'Categorie {verb} "{sel}"')

    def build_newbuf(self):
        """read widget contents into the compare buffer
        """
        return self.get_fieldvalues()

    def get_fieldvalues(self):
        "collect values of the fields that can be changed"
        fields = [self.gui.get_textfield_value(self.proc_entry),
                  self.gui.get_textfield_value(self.desc_entry),
                  self.gui.get_choice_index(self.stat_choice),
                  self.gui.get_choice_index(self.cat_choice)]
        if not self.appbase.use_text_panels:
            fields.append(self.gui.get_textbox_value(self.summary_entry))
        return fields

    def archiveer(self, *args):
        "archiveren/herleven"
        self.parch = not self.parch
        self.savep()
        self.book.rereadlist = True  # wordt in vulp uitgezet
        self.vulp()

    def vul_combos(self):
        "vullen/verversen comboboxen"
        self.initializing = True
        self.gui.clear_combobox(self.stat_choice)
        for key in sorted(self.book.stats.keys()):
            text, value = self.book.stats[key][:2]
            self.gui.add_combobox_choice(self.stat_choice, text, value)
        self.gui.clear_combobox(self.cat_choice)
        for key in sorted(self.book.cats.keys()):
            text, value = self.book.cats[key][:2]
            self.gui.add_combobox_choice(self.cat_choice, text, value)
        self.initializing = False

    def breekaf(self):
        "opvoeren nieuw item afbreken"
        self.abort_add()
        self.goto_page(0)


class Page6(Page):
    "pagina 6: voortgang"
    def __init__(self, parent):
        super().__init__(parent, pageno=6, standard=False)
        self.current_item = 0
        self.oldtext = ""
        self.event_list, self.event_data, self.old_list, self.old_data = [], [], [], []
        self.gui = gui.Page6Gui(parent, self)
        self.progress_list = self.gui.create_list()
        self.progress_text = self.gui.create_textfield(490, 330 if LIN else 430, self.on_text)
        self.save_button, self.cancel_button = self.gui.create_buttons(
            [('Sla wijzigingen op (Ctrl-S)', self.savep),
             ('Zet originele tekst terug (Alt-Ctrl-Z)', self.restorep)])
        self.gui.finish_display()
        self.status_auto_changed = False   # t.b.v. ongedaan maken automatische statuswijziging 0->1

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        super().vulp()
        self.initializing = True
        # self.gui.init_textfield()

        if not self.book.pagedata:
            raise ValueError('ProgrammingError: page data should not be empty')
        self.event_list = [dbdate2listdate(x[0]) for x in self.book.pagedata.events]
        self.event_list.reverse()
        self.old_list = self.event_list[:]
        self.event_data = [x[1] for x in self.book.pagedata.events]
        self.event_data.reverse()
        self.old_data = self.event_data[:]

        self.gui.clear_list(self.progress_list)
        if self.appbase.is_user:
            text = '-- doubleclick or press Shift-Ctrl-N to add new item --'
        else:
            text = '-- adding new items is disabled --'
        self.gui.add_first_listitem(self.progress_list, text)
        for idx, datum in enumerate(self.event_list):
            self.gui.add_item_to_list(self.progress_list, self.progress_text, idx, datum)
        if self.appbase.work_with_user:
            callback0 = self.gui.on_activate_item
            callback1 = functools.partial(callback0, self.progress_list.item(0))
            self.gui.set_list_callbacks(self.progress_list, callback0, callback1)
        self.gui.clear_textfield(self.progress_text)
        self.gui.set_text_readonly(self.progress_text, True)
        self.oldbuf = (self.old_list, self.old_data)
        self.oldtext = ''
        self.initializing = False

    def savep(self, *args):
        "opslaan van de paginagegevens"
        if not super().savep():
            return False
        # voor het geval er na het aanpassen van een tekst direkt "sla op" gekozen is
        # nog even kijken of de tekst al in self.event_data is aangepast.
        idx = self.current_item
        hlp = self.gui.get_textfield_contents(self.progress_text)
        if idx > 0:
            idx -= 1
        if self.event_data[idx] != hlp:
            self.event_data[idx] = hlp
            self.oldtext = hlp
            short_text = hlp.split("\n", 1)[0]
            maxlen = 80
            if len(short_text) > maxlen:
                short_text = short_text[:maxlen] + "..."
            self.gui.set_listitem_text(idx + 1, f"{self.event_list[idx]} - {short_text}")
            self.gui.set_listitem_data(idx + 1)
        if self.event_list != self.old_list or self.event_data != self.old_data:
            hlp = len(self.event_list) - 1
            for idx, data in enumerate(self.book.pagedata.events):
                datestring = listdate2dbdate(self.event_list[hlp - idx])
                if data != (datestring, self.event_data[hlp - idx]):
                    self.book.pagedata.events[idx] = (datestring, self.event_data[hlp - idx])
            for idx in range(len(self.book.pagedata.events), hlp + 1):
                if self.event_data[hlp - idx]:
                    self.book.pagedata.events.append((listdate2dbdate(self.event_list[hlp - idx]),
                                                      self.event_data[hlp - idx]))
            self.update_actie()
            # waar is deze voor (self.book.current_item.setText) ?
            # self.book.current_item = self.book.page0.p0list.topLevelItem(x)
            # self.book.current_item.setText(4, self.book.pagedata.updated)
            self.book.pages[0].gui.set_item_text(self.book.current_item, 3,
                                                 self.book.pagedata.updated)
            # dit was self.book.page0.p0list.currentItem().setText( -- is dat niet hetzelfde?
            self.old_list = self.event_list[:]
            self.old_data = self.event_data[:]
            self.oldbuf = (self.old_list, self.old_data)
        return True

    def goto_prev(self, *args):
        "set the selection to the previous row, if possible"
        test = self.gui.get_list_row(self.progress_list) - 1
        if test > 0:
            self.gui.set_list_row(self.progress_list, test)

    def goto_next(self, *args):
        "set the selection to the next row, if possible"
        test = self.gui.get_list_row(self.progress_list) + 1
        if test < self.gui.get_list_rowcount(self.progress_list):
            self.gui.set_list_row(self.progress_list, test)

    def on_text(self, *args):
        """callback voor wanneer de tekst gewijzigd is

        de initializing flag wordt uitgevraagd omdat deze event ook tijdens vulp()
        en wijzigen van list positie plaatsvindt
        """
        if self.initializing:
            return
        # lees de inhoud van het tekstveld en vergelijk deze met de buffer
        tekst = self.gui.get_textfield_contents(self.progress_text)
        # str(self.progress_text.get_contents())  # self.progress_list.GetItemText(ix)
        if tekst != self.oldtext:
            # stel de buffer in op de nieuwe tekst
            self.oldtext = tekst
            # maak er platte tekst van om straks in de listbox bij te werken
            tekst_plat = self.gui.convert_text(self.oldtext, to='plain')
            # stel in dat we niet van dit scherm af kunnen zonder te updaten
            if self.appbase.is_user:
                self.enable_buttons()
            self.current_item = self.gui.get_list_row()
            if self.current_item > 0:
                indx = self.current_item - 1
                self.event_data[indx] = tekst
                # item = self.progress_list.currentItem()
                # datum = str(item.text()).split(' - ')[0]
                datum = self.gui.get_listitem_text(self.current_item).split(' - ')[0]
                short_text = ' - '.join((datum, tekst_plat.split("\n")[0]))
                maxlen = 80
                if len(short_text) >= maxlen:
                    short_text = short_text[:maxlen] + "..."
                # item.setText(short_text)
                self.gui.set_listitem_text(self.current_item, short_text)

    def initialize_new_event(self):
        "set up entering new event in GUI"
        if not self.appbase.is_user:
            return
        if (self.book.pagedata.status == '0' and (
                (self.appbase.use_text_panels and self.book.current_tab >= 3)
                or (not self.appbase.use_text_panels and self.book.current_tab == 2))):
            self.book.pagedata.status = '1'
            self.status_auto_changed = True
            sel = [y for x, y in self.book.stats.items() if y[1] == '1'][0]
            datum, oldtext = shared.get_dts(), f'Status gewijzigd in "{sel[0]}"'
            self.event_list.insert(0, datum)
            self.event_data.insert(0, oldtext)
            self.gui.create_new_listitem(self.progress_list, self.progress_text, datum, oldtext)
        datum, oldtext = shared.get_dts(), ''
        self.event_list.insert(0, datum)
        self.event_data.insert(0, oldtext)
        self.gui.create_new_listitem(self.progress_list, self.progress_text, datum, oldtext)
        self.oldtext = oldtext
        self.enable_buttons()

    def build_newbuf(self):
        """read widget contents into the compare buffer
        """
        return (self.event_list, self.event_data)


class TabOptions:
    "hulp klasse bij dialoog voor mogelijke tab headers"
    def initstuff(self, parent):
        "aanvullende initialisatie"
        titel = "Tab titels"
        data = []
        for key in sorted(parent.book.tabs.keys()):
            tab_text = parent.book.tabs[key].split(" ", 1)[1]
            data.append(tab_text)
        tekst = ["De tab titels worden getoond in de volgorde",
                 "zoals ze van links naar rechts staan.",
                 "Er kunnen geen tabs worden verwijderd of toegevoegd."]
        return titel, data, {'can_add_remove': False, 'can_reorder': False}, tekst

    def leesuit(self, parent, optionslist):
        "wijzigingen doorvoeren"
        self.newtabs = {}
        for idx, item in enumerate(optionslist):
            self.newtabs[str(idx)] = str(item)
        parent.save_settings("tab", self.newtabs)


class StatOptions:
    "hulp klasse bij dialoog voor de mogelijke statussen"
    def initstuff(self, parent):
        "aanvullende initialisatie"
        titel = "Status codes en waarden"
        statitems = []
        for row_id in parent.book.stats:
            item_text, item_value = parent.book.stats[row_id]
            statitems.append((row_id, item_value, item_text))
        data = [': '.join((str(y), z)) for x, y, z in sorted(statitems)]
        tekst = ["De waarden voor de status worden getoond in dezelfde volgorde",
                 "als waarin ze in de combobox staan.",
                 "Vóór de dubbele punt staat de code, erachter de waarde.",
                 "Denk erom dat als je codes wijzigt of statussen verwijdert, deze",
                 "ook niet meer getoond en gebruikt kunnen worden in de registratie.",
                 "Omschrijvingen kun je rustig aanpassen"]
        return titel, data, {'can_add_remove': True, 'can_reorder': True}, tekst

    def leesuit(self, parent, optionslist):
        "wijzigingen doorvoeren"
        self.newstats = {}
        for sortkey, item in enumerate(optionslist):
            try:
                value, text = str(item).split(": ")
            except ValueError:
                return 'Foutieve waarde: bevat geen dubbele punt'
            self.newstats[value] = (text, sortkey)
        parent.save_settings("stat", self.newstats)
        return ''


class CatOptions:
    "hulp klasse bij dialoog voor de mogelijke categorieen"
    def initstuff(self, parent):
        "aanvullende initialisatie"
        titel = "Soort codes en waarden"
        catitems = []
        for row_id in parent.book.cats:
            item_text, item_value = parent.book.cats[row_id]
            catitems.append((row_id, item_value, item_text))
        data = [': '.join((str(y), z)) for x, y, z in sorted(catitems)]
        tekst = ["De waarden voor de soorten worden getoond in dezelfde volgorde",
                 "als waarin ze in de combobox staan.",
                 "Vóór de dubbele punt staat de code, erachter de waarde.",
                 "Denk erom dat als je codes wijzigt of soorten verwijdert, deze",
                 "ook niet meer getoond en gebruikt kunnen worden in de registratie.",
                 "Omschrijvingen kun je rustig aanpassen"]
        return titel, data, {'can_add_remove': True, 'can_reorder': True}, tekst

    def leesuit(self, parent, optionslist):
        "wijzigingen doorvoeren"
        self.newcats = {}
        for sortkey, item in enumerate(optionslist):
            try:
                value, text = str(item).split(": ")
            except ValueError:
                return 'Foutieve waarde: bevat geen dubbele punt'
            self.newcats[value] = (text, sortkey)
        parent.save_settings("cat", self.newcats)
        return ''


class SortOptionsDialog:
    """dialoog om de sorteer opties in te stellen
    """
    _asc_id = 1
    _desc_id = 2

    def __init__(self, parent, sortopts, namelist):
        self.parent = parent
        self.gui = gui.SortOptionsDialogGui(self, parent, "Sorteren op meer dan 1 kolom")

        self.sortopts = sortopts
        checked = False if self.parent.master.saved_sortopts else self.parent.sort_via_options
        self.on_off = self.gui.add_checkbox_line('Multi-sorteren mogelijk', checked,
                                                 self.gui.enable_fields)
        self.widgets = []
        for ix, colname in enumerate(namelist):
            lbl = self.gui.add_seqnumtext_to_line(f"  {ix}.")
            cmb = self.gui.add_colnameselector_to_line(namelist, colname)
            for name, orient in self.sortopts:
                if name == colname:
                    break
            else:
                orient = 'asc'
            rbg = self.gui.add_radiobuttons_to_line([(" Asc ", self._asc_id, orient == 'asc'),
                                                     ("Desc", self._desc_id, orient == 'desc')])
            self.widgets.append((lbl, cmb, rbg))
        self.gui.add_okcancel_buttonbox()
        # self.gui.set_defaults()

    def confirm(self):
        """sorteerkolommen en -volgordes teruggeven aan hoofdscherm
        """
        new_sortopts = {}
        for ix, line in enumerate(self.widgets):
            combobox, rbgroup = line[1:]
            fieldname = self.gui.get_combobox_value(line[1])
            checked_id = self.gui.get_rbgroup_value(line[2])
            if fieldname and fieldname != '(geen)':
                orient = 'asc' if checked_id == self._asc_id else 'desc'
                new_sortopts[ix] = (fieldname, orient)
        via_options = self.gui.get_checkbox_value(self.on_off)
        if via_options == self.parent.master.sort_via_options and new_sortopts == self.sortopts:
            gui.show_message(self.gui, 'Probreg', 'U heeft niets gewijzigd')
            return False
        self.parent.master.sort_via_options = via_options
        if via_options and self.parent.saved_sortopts:      # alleen SQL versie
            self.parent.saved_sortopts.save_options(new_sortopts)
        return True


class SelectOptionsDialog:
    """dialoog om de selectie op te geven

    sel_args is de dictionary waarin de filterwaarden zitten, bv:
    {'status': ['probleem'], 'idlt': '2006-0009', 'titel': 'x', 'soort': ['gemeld'],
     'id': 'and', 'idgt': '2005-0019'}
    voor de Django versie is deze overbodig want de selectie ligt vast in de database
    """
    def __init__(self, parent, sel_args, sel_data):
        self.parent = parent
        appbook = parent.book
        # self.datatype = self.parent.parent.parent.datatype
        self._data = sel_data
        self.gui = gui.SelectOptionsDialogGui(self, parent, "Selecteren")

        self.row = 0
        self.cb_actie = self.gui.add_checkbox_to_grid(appbook.ctitels[0] + '   -', self.row, 0)
        block = self.gui.start_optionsblock()
        self.action_gt = self.gui.add_textentry_line_to_block(block, 'groter dan:',
                                                              self.gui.on_text)
        self.action_andor = self.gui.add_radiobuttonrow_to_block(block, ['and', 'or'])
        self.action_lt = self.gui.add_textentry_line_to_block(block, 'kleiner dan:',
                                                              self.gui.on_text)
        self.gui.finish_block(block, self.row, 1)

        self.row += 1
        self.cb_soort = self.gui.add_checkbox_to_grid("soort   -", self.row, 0)
        block = self.gui.start_optionsblock()
        namelist = [x[0] for x in [appbook.cats[y] for y in sorted(appbook.cats.keys())]]
        self.check_cats = self.gui.add_checkboxlist_to_block(block, namelist,
                                                             self.gui.on_cb_checked)
        self.gui.finish_block(block, self.row, 1)

        self.row += 1
        self.cb_status = self.gui.add_checkbox_to_grid(appbook.ctitels[2] + '   -', self.row, 0)
        block = self.gui.start_optionsblock()
        namelist = [x[0] for x in [appbook.stats[y] for y in sorted(appbook.stats.keys())]]
        self.check_stats = self.gui.add_checkboxlist_to_block(block, namelist,
                                                              self.gui.on_cb_checked)
        self.gui.finish_block(block, self.row, 1)

        self.row += 1
        caption = ('zoek in   -' if parent.use_separate_subject else appbook.ctitels[4] + '   -')
        self.cb_zoek = self.gui.add_checkbox_to_grid(caption, self.row, 0)
        block = self.gui.start_optionsblock()
        caption = (appbook.ctitels[4] if parent.use_separate_subject else 'zoek naar:')
        self.text_zoek = self.gui.add_textentry_line_to_block(block, caption, self.gui.on_text)
        if parent.use_separate_subject:
            self.zoek_andor = self.gui.add_radiobuttonrow_to_block(block, ['and', 'or'])
            self.text_zoek2 = self.gui.add_textentry_line_to_block(block, appbook.ctitels[5],
                                                                   self.gui.on_text)
        self.gui.finish_block(block, self.row, 1)

        self.row += 1
        self.cb_arch = self.gui.add_checkbox_to_grid("Archief    -", self.row, 0)
        block = self.gui.start_optionsblock()
        self.radio_arch = self.gui.add_radiobuttonrow_to_block(
            block, ["Alleen gearchiveerd", "gearchiveerd en lopend"], self.gui.on_rb_checked,
            alignleft=False)
        self.gui.finish_block(block, self.row, 1)

        self.gui.add_okcancel_buttonbar()
        self.gui.finalize_display()

        self.set_default_values(sel_args)

    def set_default_values(self, sel_args):
        """get search settings and present them in the dialog
        """
        set_checkbox = False
        if "idgt" in sel_args:
            self.gui.set_textentry_value(self.text_gt, sel_args["idgt"])
            set_checkbox = True
        if "id" in sel_args:
            idx = 0 if sel_args["id"] == "and" else 1
            self.gui.set_radiobutton_value(self.action_andor[idx], True)
        if "idlt" in sel_args:
            self.gui.set_textentry_value(self.text_lt, sel_args["idlt"])
            set_checkbox = True
        self.gui.set_checkbox_value(self.cb_actie, set_checkbox)

        set_checkbox = False
        if "soort" in sel_args:
            for x in self.parent.parent.cats:
                if self.parent.parent.cats[x][-1] in sel_args["soort"]:
                    self.gui.set_checkbox_value(self.check_cats[int(x)], True)
                    set_checkbox = True
        self.gui.set_checkbox_value(self.cb_soort, set_checkbox)

        set_checkbox = False
        if "status" in sel_args:
            for x in self.parent.parent.stats:
                if self.parent.parent.stats[x][-1] in sel_args["status"]:
                    self.gui.set_checkbox_value(self.check_stats[int(x)], True)
                    set_checkbox = True
        self.gui.set_checkbox_value(self.cb_status, set_checkbox)

        set_checkbox = False
        if "titel" in sel_args:
            if self.parent.parent.use_separate_subject:
                for item in sel_args["titel"]:
                    if item[0] == 'about':
                        self.gui.set_textentry_value(self.text_zoek, item[1])
                        set_checkbox = True
                    elif item[0] == 'title':
                        self.gui.set_textentry_value(self.text_zoek2, item[1])
                        set_checkbox = True
                    elif item[0] == 'of':
                        self.gui.set_radiobutton_value(self.zoek_andor[0], True)
                    else:
                        self.gui.set_radiobutton_value(self.zoek_andor[1], True)
            else:
                self.gui.set_textentry_value(self.text_zoek, sel_args["titel"])
                set_checkbox = True
        self.gui.set_checkbox_value(self.cb_zoek, set_checkbox)

        set_checkbox = False
        if "arch" in sel_args:
            if sel_args["arch"] == "arch":
                self.gui.set_radiobutton_value(self.radio_arch[0], True)
                set_checkbox = True
            if sel_args["arch"] == "alles":
                self.gui.set_radiobutton_value(self.radio_arch[1], True)
                set_checkbox = True
        self.gui.set_checkbox_value(self.cb_arch, set_checkbox)

    def confirm(self):
        "export dialog values to sender"
        selection = 'excl. gearchiveerde'
        sel_args = {}
        if self.gui.get_checkbox_value(self.cb_actie):
            ok, selargs = self.get_actie_selargs()
            if not ok:
                gui.show_error(self.gui, 'Kies een verbindende conditie voor actie selecties')
                self.gui.set_focus_to(self.action_andor[0])
                return False
            selection = '(gefilterd)'
            sel_args.update(selargs)
        if self.gui.get_checkbox_value(self.cb_soort):
            lst = self.get_cat_selargs()
            if lst:
                selection = '(gefilterd)'
                sel_args["soort"] = lst
        if self.gui.get_checkbox_value(self.cb_status):
            lst = self.get_stat_selargs()
            if lst:
                selection = '(gefilterd)'
                sel_args["status"] = lst
        if self.gui.get_checkbox_value(self.cb_zoek):
            ok, selargs = self.get_search_selargs()
            if not ok:
                gui.show_error(self.gui, 'Kies een verbindende conditie voor zoekargumenten')
                self.gui.set_focus_to(self.zoek_andor[0])
                return False
            selection = '(gefilterd)'
            sel_args.update(selargs)
        if self.gui.get_checkbox_value(self.cb_arch):
            selection, arch = self.get_arch_selargs(selection)
            if arch:
                sel_args['arch'] = arch
        self.parent.selection = selection
        self.parent.sel_args = sel_args
        if self._data:
            self._data.save_options(sel_args)
        return True

    def get_actie_selargs(self):
        "check conditions for filtering on action ids"
        sel_args = {}
        if id_gt := self.gui.get_textentry_value(self.text_gt):
            sel_args["idgt"] = id_gt
        if id_lt := self.gui.get_textentry_value(self.text_lt):
            sel_args["idlt"] = id_lt
        if all([id_gt, id_lt]):
            if self.gui.get_radiobutton_value(self.text_andor[0]):
                sel_args["id"] = "and"
            elif self.gui.get_radiobutton_value(self.text_andor[1]):
                sel_args["id"] = "or"
            else:
                return False, {}
        return True, sel_args

    def get_cat_selargs(self):
        "check conditions for filtering on category"
        return [self.parent.parent.cats[x][-1]
                for x in range(len(self.parent.parent.cats.keys()))
                if self.gui.get_checkbox_value(self.check_cats[x])]

    def get_stat_selargs(self):
        "check conditions for filtering on status"
        return [self.parent.parent.stats[x][-1]
                for x in range(len(self.parent.parent.stats.keys()))
                if self.gui.get_checkbox_value(self.check_stats[x])]

    def get_search_selargs(self):
        "check conditions for filtering on subject/description"
        sel_args = {}
        if self.parent.parent.use_separate_subject:
            if any([about := self.gui.get_textentry_value(self.text_zoek),
                    desc := self.gui.get_textentry_value(self.text_zoek2)]):
                sel_args['titel'] = []
            if about:
                sel_args["titel"].append(('about', about))
            if desc:
                sel_args["titel"].append(('title', desc))
            if all([about, desc]):
                if self.gui.get_radiobutton_value(self.zoek_andor[0]):
                    sel_args["titel"].append(("and",))
                elif self.gui.get_radiobutton_value(self.zoek_andor[1]):
                    sel_args["titel"].append(("or",))
                else:
                    return False, {}
        else:
            if sel := self.gui.get_textentry_value(self.text_zoek):
                sel_args['titel'] = sel
        return True, sel_args

    def get_arch_selargs(self, selection):
        "check conditions for filtering on archive status"
        arch = ''
        if self.gui.get_radiobutton_value(self.radio_arch[0]):
            arch = "arch"
            if selection != '(gefilterd)':
                selection = '(gearchiveerd)'
        elif self.gui.get_radiobutton_value(self.radio_arch[1]):
            arch = "alles"
            if selection != '(gefilterd)':
                selection = ''
        return selection, arch


class SettOptionsDialog:
    """generic dialog to maintain options
    """
    def __init__(self, parent, settingtype, title):
        self.parent = parent
        self.settingtype = settingtype()
        self.gui = gui.SettOptionsDialogGui(self, parent, title)
        titel, data, actions, infotext = self.settingtype.initstuff(parent)
        self.elb = self.gui.add_listbox_with_buttons(titel, data, actions)
        self.gui.add_label(infotext)
        self.gui.add_okcancel_buttonbox()
        self.gui.finish_display()

    def confirm(self):
        "exchange dialog data with sender"
        # or in this case: update the settings type
        # qt version
        new_items = self.gui.read_listbox_data(self.elb)
        self.settingtype.leesuit(self.parent, new_items)


class LoginBox:
    """Sign in with userid & password
    """
    def __init__(self, parent):
        self.parent = parent
        self.parent.dialog_data = ()
        self.gui = gui.LoginBoxGui(self, parent)
        self.t_username = self.gui.add_textinput_line('Userid')
        self.t_password = self.gui.add_textinput_line('Password', hide=True)
        self.gui.add_okcancel_buttonbox()
        self.gui.finish_display()

    def confirm(self):
        "exchange dialog data with sender"
        self.parent.dialog_data = (self.gui.get_textinput_value(self.t_username),
                                   self.gui.get_textinput_value(self.t_password),
                                   self.parent.filename)


def db_stat_to_book_stat(item_value, item):
    """zet een in Settings ingelezen status instelling om naar zoals de applicatie deze gebruikt

    subroutine van gemaakt omdat dit op meerdere plekken gebruikt wordt"""
    retval = [item[0], item_value]
    return retval


def db_cat_to_book_cat(item_value, item):
    """zet een in Settings ingelezen categorie instelling om naar zoals de applicatie deze gebruikt

    subroutine van gemaakt omdat dit op meerdere plekken gebruikt wordt"""
    retval = [item[0], item_value]
    return retval


def db_head_to_book_head(tab_num, tab_item):
    """zet een in Settings ingelezen tabheading instelling om naar zoals de applicatie deze gebruikt

    subroutine van gemaakt omdat dit op meerdere plekken gebruikt wordt"""
    return " ".join((tab_num, tab_item[0].title()))


def dbdate2listdate(datestring):
    "opslagdatum EEJJMMDD etc laten zien als dd-mm-EEJJ etc"
    try:
        date = datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
        return date.strftime('%d-%m-%Y %H:%M:%S')
    except ValueError:
        return datestring  # assume other format


def listdate2dbdate(datestring):
    "weergavedatum dd-mm-EEJJ etc omzetten naar opslagdatum EEJJMMDD etc"
    try:  # try old format
        date = datetime.datetime.strptime(datestring, '%d-%m-%Y %H:%M:%S')
        return date.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return datestring  # assume already converted


def main(arg=None):
    "opstart routine"
    frame = MainWindow(None, arg)
    frame.gui.go()
