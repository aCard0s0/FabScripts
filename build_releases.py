import requests
import json
import shutil
import re
from pathlib import Path

def get_release_name(setCode):
    info = dict()
    if "WTR" == setCode:
        info["name"] = "Welcome to Rathe (Alpha print)"
        info["date"] = "11/10/2019"
        return info
    elif "U-WTR" == setCode:
        info["name"] = "Welcome to Rathe (Unlimited Edition)"
        info["date"] = "6/11/2020"
        return info
    elif "ARC" == setCode:
        info["name"] = "Arcane Rising (First Edition)"
        info["date"] = "27/05/2020"
        return info
    elif "U-ARC" == setCode:
        info["name"] = "Arcane Rising (Unlimited Edition)"
        info["date"] = "20/11/2020"
        return info
    elif "CRU" == setCode:
        info["name"] = "Crucible of War (First Edition)"
        info["date"] = "28/08/2020"
        return info
    elif "U-CRU" == setCode:
        info["name"] = "Crucible of War (Unlimited Edition"
        info["date"] = "30/07/2021"
        return info
    elif "MON" == setCode:
        info["name"] = "Monarch Booster (First Edition)"
        info["date"] = "07/05/2021"
        return info
    elif "U-MON" == setCode:
        info["name"] = "Monarch Booster (Unlimited Edition"
        info["date"] = "04/06/2021"
        return info

def write_file(fname, data):
    Path("releases/").mkdir(parents=True, exist_ok=True)
    jsonFile = open("releases/"+fname, "w+")
    jsonFile.write(data)
    jsonFile.close()

def build_releases(dataset):
    setCode = dataset[0]["setCode"]
    info = get_release_name(setCode),
    release = {
        "setCode": setCode,
        "name": info[0]["name"],
        "date": info[0]["date"]
    }
    cards = []
    [cards.append(card["cardCode"]) for card in dataset]
    release["cardList"] = cards
    return release

def main():
    datasets = ["cards/wtr.json", "cards/u-wtr.json", "cards/arc.json", "cards/u-arc.json", "cards/mon.json", "cards/u-mon.json", "cards/cru.json",]
    for fname in datasets:
        jfile = open(fname, "r")
        data = build_releases(json.loads(jfile.read()))
        jfile.close()
        write_file(fname.replace("cards/", ""), json.dumps(data))

if __name__ == '__main__':
    main()
