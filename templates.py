from jinja import Environment, FileSystemLoader
from jinja.filters import stringfilter

@stringfilter
def do_oms(value):
    return value.split(".")[1]

@stringfilter
def do_wrd(value):
    return value.split(".")[0]

@stringfilter
def do_crtobr(value):
    return value

@stringfilter
def do_rightpart(value):
    return value.split(None,1)[1]

env = Environment()
env.loader = FileSystemLoader('.')
env.filters['oms'] = do_oms
env.filters['wrd'] = do_wrd
env.filters['crtobr'] = do_crtobr
env.filters['rightpart'] = do_rightpart

def print_page0(filename, data):
    info = {
        "fname": filename,
        "data": data
        }
    tpl = env.get_template("page0.html")
    return tpl.render(info)

def print_page1(data):
    info = {}
    for key, val in data.items():
        info[key] = val
    tpl = env.get_template("page1.html")
    return tpl.render(info)

def print_pageno(data,tabs,pageno):
    info = {
        "id": data["id"],
        "titel": data["titel"],
        "ttl": tabs[pageno]
        }
    if pageno == 6:
        info["txt"] = data["txtStat"]
        info["elijst"] = data["elijst"]
    else:
        info["txt"] = data["text1"]
    tpl = env.get_template("pages.html")
    return tpl.render(info)

def print_all(data, cats, stats, tabs):
    ttl = data["titel"]
    data["titel"] = data["titel"].replace(":",".",1)
    info = {
        "id": data["id"],
        "titel": ttl,
        "data": data,
        "tabs": tabs
        }
    try:
        info["soort"] = cats.values()[cats.values().index(data["soort"][1])][0]
    except ValueError:
        info["soort"] = "(onbekende soort)"
    try:
        info["status"] = stats.values()[stats.values().index(data["status"][1])][0]
    except ValueError:
        info["status"] = "(onbekende status)"
    tpl = env.get_template("all.html")
    return tpl.render(info)

def test_print0():
    filename = "argh.xml"
    data = [
        [
            "nummer",
            "datum",
            "1.soort",
            "ahum",
            "1.status",
            "korte: omschrijving",
            "een andere datum"
        ],
        [
            "nummer",
            "datum",
            "1.soort",
            "ahum",
            "0.status",
            "korte: omschrijving",
            "een andere datum"
        ],
        [
            "nummer",
            "datum",
            "1.soort",
            "ahum",
            "1.status",
            "korte: omschrijving",
            "een andere datum"
        ]
    ]
    print print_page0(filename,data)

def test_print1():
    data = {
        'txtId': 'nummer',
        'txtDat': 'datum',
        'txtPrc': 'korte',
        'txtMld': 'omschrijving',
        'cmbCat': 'soort',
        'cmbStat': 'status'
        }
    print print_page1(data)

def test_printno():
    data = {
        "id": "nummer",
        "titel": "korte: omschrijving",
        "text1": "Dit\nis\neen\ntekst",
        "txtStat": "stand van zaken",
        "elijst": [
            ("moment 1","eerst gebeurde er dit"),
            ("moment 2","en later iets anders"),
            ],
        }
    tabs = ["tab 0","tab 1","tab 2","tab 3","tab 4","tab 5","tab 6"]
    pageno = 6
    print print_pageno(data,tabs,pageno)

def test_printall():
    data = {
        "id": "nummer",
        "titel": "korte: omschrijving",
        "soort": ("cat2",2),
        "status": ("stat3",3),
        "melding": "Dit\nis\neen\nmelding",
        "oorzaak": "Dit\nis\neen\noorzaak",
        "oplossing": "Dit\nis\neen\noplossing",
        "vervolg": "Dit\nis\neen\nvervolg",
        "stand": "stand van zaken",
        "events": [
            ("moment 1","eerst gebeurde er dit"),
            ("moment 2","en later iets anders"),
            ],
        }
    tabs = ["tab 0","tab 1","tab 2","tab 3","tab 4","tab 5","tab 6"]
    cats = {0: ("cat0",0),
            1: ("cat1",1),
            2: ("cat2",2),
            3: ("cat3",3),
            4: ("cat4",4),
            5: ("cat5",5),
            6: ("cat6",6)
        }
    stats = {0: ("stat0",0),
             1: ("stat1",1),
             2: ("stat2",2),
             3: ("stat3",3),
             4: ("stat4",4),
             5: ("stat5",5),
             6: ("stat6",6)
        }
    print print_all(data, cats, stats, tabs)

if __name__ == "__main__":
    test_print0()
    ## test_print1()
    ## test_printno()
    ## test_printall()
