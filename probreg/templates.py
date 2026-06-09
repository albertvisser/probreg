"""Probreg: templates for neatly displaying the text of a registration

currently only used in ppg version
"""
from jinja import Environment, FileSystemLoader
from jinja.filters import stringfilter


@stringfilter
def do_oms(value):
    "return the description of an item"
    return value.split(".")[1]


@stringfilter
def do_wrd(value):
    "return the name of an item"
    return value.split(".")[0]


@stringfilter
def do_crtobr(value):
    "convert carriage return to linebreak indicator"
    return value


@stringfilter
def do_rightpart(value):
    "return the 'rightmost' part of a value"
    return value.split(None, 1)[1]

env = Environment()
env.loader = FileSystemLoader('.')
env.filters['oms'] = do_oms
env.filters['wrd'] = do_wrd
env.filters['crtobr'] = do_crtobr
env.filters['rightpart'] = do_rightpart


def print_page0(filename, data):
    "render the issues list"
    info = {"fname": filename, "data": data}
    tpl = env.get_template("page0.html")
    return tpl.render(info)


def print_page1(data):
    "render the details page"
    info = {}
    for key, val in data.items():
        info[key] = val
    tpl = env.get_template("page1.html")
    return tpl.render(info)


def print_pageno(data, tabs, pageno):
    "render any of the other pages"
    info = {"id": data["id"],
            "titel": data["titel"],
            "ttl": tabs[pageno]}
    if pageno == 6:
        info["txt"] = data["txtStat"]
        info["elijst"] = data["elijst"]
    else:
        info["txt"] = data["text1"]
    tpl = env.get_template("pages.html")
    return tpl.render(info)


def print_all(data, cats, stats, tabs):
    "render the complete summary"
    ttl = data["titel"]
    data["titel"] = data["titel"].replace(":", ".", 1)
    info = {"id": data["id"],
            "titel": ttl,
            "data": data,
            "tabs": tabs}
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
