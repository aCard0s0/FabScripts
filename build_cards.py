import requests
import json
import re
from pathlib import Path

cru_special_case = [
    ("WTR001", "CRU001"),
    ("WTR003", "CRU003"),
    ("WTR038", "CRU022"),
    ("WTR040", "CRU023"),
    ("WTR075", "CRU044"),
    ("WTR076", "CRU045"),
    ("WTR078", "CRU048"),
    ("WTR113", "CRU076"),
    ("WTR115", "CRU078"),
    ("ARC001", "CRU098"),
    ("ARC003", "CRU100"),
    ("ARC038", "CRU119"),
    ("ARC040", "CRU120"),
    ("ARC075", "CRU138"),
    ("ARC077", "CRU139"),
    ("ARC112", "CRU157"),
    ("ARC113", "CRU158"),
    ("ARC115", "CRU159"),
    ("WTR150", "CRU178"),
    ("WTR224", "CRU195"),
    ("WTR225", "CRU196"),
]

def get_flavour(cardCode):
    cardDetails = requests.get("https://fabdb.net/api/cards/" +cardCode).json()
    return cardDetails["flavour"] if cardDetails["flavour"] is not None else ""

def get_card_type(keywords):
    cardType = ""
    for word in keywords:
        word = word.capitalize()
        if "Gem" == word:
            word = "- Gem"
        if "Young" == word:
            word = "- Young"
        if "Attack" == word:
            word = "- Attack"
        if "Weapon" == word:
            word = "Weapon -"
        if "Equipment" == word:
            word = "Equipment -"
        if "1h" == word:
            word = "(1H)"
        if "2h" == word:
            word = "(2H)"
        if "Aura" == word:
            word = "- Aura"
        if "Item" == word:
            word = "- Item"
        if "Reaction" == word:  # remove "-"" previous add by the Attack keyword
            cardType = cardType.replace("- ", "")
        cardType += word +" "
    return cardType

def setCardClass(setCode, number):
    if setCode == "WTR":
        if number >= 1 and number <= 37:
            return "Brute"
        elif number >= 38 and number <= 75:
            return "Guardian"
        elif number >= 76 and number <= 112:
            return "Ninja"
        elif number >= 113 and number < 149:
            return "Warrior"
        return "Generic"
    elif setCode == "ARC":
        if number >= 1 and number <= 37:
            return "Mechanologist"
        elif number >= 38 and number <= 74:
            return "Ranger"
        elif number >= 75 and number <= 112:
            return "Runeblade"
        elif number >= 113 and number < 149:
            return "Wizard"
        return "Generic"
    elif setCode == "MON":
        if number >= 1 and number <= 28:
            return "Illusionist"
        elif number >= 29 and number <= 59:
            return "Warrior"
        if number >= 88 and number <= 104:
            return "Illusionist"
        elif number >= 105 and number <= 118:
            return "Warrior"
        elif number >= 119 and number <= 152:
            return "Brute"
        elif number >= 153 and number <= 186:
            return "Runeblade"
        elif number >= 221 and number <= 228:
            return "Brute"
        elif number >= 229 and number <= 237:
            return "Runeblade"
        return "Generic"
    elif setCode == "CRU":
        if number == 0:
            return "Runeblade"
        elif number >= 1 and number >= 21:
            return "Brute"
        elif number >= 22 and number >= 44:
            return "Guardian"
        elif number >= 45 and number >= 75:
            return "Ninja"
        elif number >= 76 and number >= 96:
            return "Warrior"
        elif number == 97:
            return "Shapeshifter"
        elif number >= 98 and number >= 117:
            return "Mechanologist"
        elif number == 118:
            return "Merchant"
        elif number >= 119 and number >= 137:
            return "Ranger"
        elif number >= 138 and number >= 157:
            return "Runeblade"
        elif number >= 158 and number >= 176:
            return "Wizard"
        return "Generic"

def setTalent(setCode, number):
    if setCode == "MON":
        if number >= 0 and number <= 87:
            return "Light"
        elif number >= 119 and number <= 220:
            return "Shadow"
    return "None"

def request_collection(url, collection, page):
    params = {"set": collection, "page": page}
    resp = requests.get(url, params=params).json()

    lines = []
    for elem in resp["data"]:
        cardCode = elem["printings"][0]["sku"]["number"]
        # special case for cru edition
        if collection == "cru":
            for pair in cru_special_case:
                if pair[0] == cardCode:
                    cardCode = pair[1]
        # special case for arc edition
        if collection == "arc" and cardCode == "WTR224":
            cardCode == "ARC"

        print(cardCode)        
        printings = set([])
        frames = set([]) 

        for p in elem["printings"]:
            pCode = p["sku"]["sku"]
            printings.add(pCode)
            if "-CF" in pCode:
                frames.add("Cold Foil")
            if "-RF" in pCode:
                frames.add("Rainbow")

        if "T" == elem["rarity"]:
            frames.add("Double Slided")

        flavour = get_flavour(cardCode)
        cardType = get_card_type(elem["keywords"])
        
        elem["stats"] = dict(elem["stats"])
        if "attack" in elem["stats"].keys():
            elem["stats"]["power"] = elem["stats"]["attack"]

        setCode = elem["printings"][0]["sku"]["set"]["id"].upper()
        cardClass = setCardClass(setCode, int(re.findall(r'\d+', cardCode)[0]))
        talent = setTalent(setCode, int(re.findall(r'\d+', cardCode)[0]))

        lines.append({
            "cardCode": cardCode,
            "name": elem["name"],
            "text": elem["text"].replace("\n", "\\n") if elem["text"] is not None else "",
            "flavour": flavour.replace("\n", "\\n"),
            "rarity": elem["rarity"],
            "type": cardType.strip(),
            "stats": elem["stats"],
            "setCode": setCode,
            "cardClass": cardClass,
            "talent": talent,
            "imageApiPath": "/images/"+ cardCode,
            "keywords": elem["keywords"],
            "illegalFormats": list(),
            "frames": list(frames),
            "printings": list(printings)
        })
    return lines

def main():
    # The collection name, number of pages and if image is required must correspond
    collections = ["wtr", "arc", "mon", "cru"]
    pages = [8, 8, 11, 7]

    Path("cards/").mkdir(parents=True, exist_ok=True)
    for collection in collections:
        with open("cards/"+collection+".json", 'w+', newline='') as writer:
            data = []
            for page in range(1, pages[collections.index(collection)]+1):
                print(page, collection)
                data.extend(request_collection("https://fabdb.net/api/cards", collection, page))
            json.dump(data, writer)
        if collection == "cru":
            print("ATTENTION: cru collection need to add the 49 card by hand which is equals to 48 except the cardCode and imageApiPath fields.")
            print("ATTENTION: cru collection need to add the 52 card by hand which is equals to 51 except the cardCode and imageApiPath fields.")
            

if __name__ == '__main__':
    main()
