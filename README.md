## FabScripts

This repository contains Python script to help build the information to be expose by API from project PublicCardAccess PCA.

#### Requiments
Python 3+

#### How to use
The scripts depended on each other so the execution order is important.
1. Run `build_cards.py` to generate a folder with the cards json datasets with all information within a card.
2. Run `build_unlimited.py` to generate a folder with the card json dataset for all unlimited releases.
3. Run `build_releases.py` to generate the releases json datasets.
4. Run `build_imgs.py` to download all cards images from limited and unlimited sets.

#### Note: 
On this repository we already save the limited and unlimited cards dataset and releases dataset.
The images are not within this repository because the size constrains.

####
Upload to the web service PCA.
1. Run `upload_resources.py` will add datasets and images to the databses through the PCA web service.