import requests
import json

from os import listdir
from os.path import isfile, join

def post_img(url, path, fname):
    payload={'code': fname.replace(".png", "")}
    files=[('file',(fname, open(path+"/"+fname,'rb'),'image/png'))]
    rsp = requests.post(url, data=payload, files=files)
    print(fname, rsp.status_code)

def post_cards(url, fname):
    jfile = open(fname, "r")
    arr = json.loads(jfile.read())
    headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
    rsp = requests.post(url, data=json.dumps(arr), headers=headers)
    print(fname, rsp.status_code)

def main():
    ignore = [".DS_Store"]

    # Images directories to updaload to the server
    img_paths = ["images/wtr/", "images/arc/"]
    for path in img_paths:
        files=[]
        [files.append(fname) for fname in listdir(path) if fname not in ignore]
        files.sort()
        for fname in files:
            post_img("http://localhost:8080/images", path, fname)
        print(path, "done")

    # Dataset to updaload to the server
    card_files = ["cards/wtr.json", "cards/arc.json"]
    for fname in card_files:
        post_cards("http://localhost:8080/cards", fname)

if __name__ == '__main__':
    main()