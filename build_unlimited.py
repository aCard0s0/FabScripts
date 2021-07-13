import json

def build_releases(collection, dataset, limited=False):
    newDataset = list()
    for card in dataset:
        unCardCode = "U-"+card["cardCode"]
        card["imageApiPath"] = card["imageApiPath"].replace(card["cardCode"], unCardCode)
        card["cardCode"] = unCardCode
        card["setCode"] = collection.upper()
        newDataset.append(card)
    
    with open("cards/"+collection+".json", 'w+', newline='') as writer:
        json.dump(newDataset, writer)

def main():
    datasets = ["cards/wtr.json", "cards/arc.json", "cards/mon.json"]
    for fname in datasets:
        jfile = open(fname, "r")
        collection = "u-"+ fname.split("/")[1].replace(".json", "")
        build_releases(collection, json.loads(jfile.read()))
        jfile.close()

if __name__ == '__main__':
    main()
