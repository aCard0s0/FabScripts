import requests
import json
import shutil
import re
from pathlib import Path

def get_cardCode(cardCode, printings):
    return filter(lambda code: code.startswith(cardCode), printings)

def write_img(collection, cardCode):
    imageResp = requests.get("https://fabdb2.imgix.net/cards/printings/"+ cardCode +".png")
    imageResp.raw.decode_content = True
    if ("-CF" in cardCode):
        cardCode = cardCode.replace("-CF", "")
    elif ("-RF" in cardCode):
        cardCode = cardCode.replace("-RF", "")
    image = open("images/"+ collection +"/"+ cardCode +".png", "wb")
    image.write(imageResp.content)
    image.close()
    print(imageResp.status_code, "Saved", cardCode)

def build_releases(collection, dataset, limited=False):
    Path("images/"+collection).mkdir(parents=True, exist_ok=True)
    if limited:
        Path("images/u-"+collection).mkdir(parents=True, exist_ok=True)

    for card in dataset:
        result = get_cardCode(card["cardCode"], card["printings"])
        write_img(collection, list(result)[0])
        if limited:
            result = get_cardCode("U-"+card["cardCode"], card["printings"])
            write_img("u-"+collection, list(result)[0])

def main():
    datasets = ["cards/wtr.json", "cards/arc.json", "cards/mon.json", "cards/cru.json"]
    limited = [True, True, True, False] # set to true if you want to download 1st edition

    for fname in datasets:
        jfile = open(fname, "r")
        collection = fname.split("/")[1].replace(".json", "")
        data = build_releases(collection, json.loads(jfile.read()), limited[datasets.index(fname)])
        jfile.close()

if __name__ == '__main__':
    main()
