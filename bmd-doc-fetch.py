#/usr/bin/python3

import urllib.request
import json
import os
import sys
import html.parser
h = html.parser.HTMLParser()

download_url = "http://www.blackmagicdesign.com/api/support/us/downloads.json"
nav_url = "http://www.blackmagicdesign.com/api/support/us/nav.json"
path = "C:\\Users\\Marcus\\BILDQUADRAT\\BMD_Download"

if len(sys.argv) == 2:
    path = sys.argv[1]

class MyURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0"

urlOpener = MyURLopener()

with urllib.request.urlopen(download_url) as req:
    struc = json.loads(str(req.read(), encoding='UTF-8'))['downloads']
with urllib.request.urlopen(nav_url) as req:
    nav = json.loads(str(req.read(), encoding='UTF-8'))

for obj in struc:
    common_name = h.unescape(nav['families'][obj['relatedFamilies'][0]]['family_name'].replace('<br>', ' '))
    common_dir = path + os.sep + common_name
    dir_name = common_dir + os.sep + obj['name']

    # Ordner finden und ggf. erstellen
    if os.path.isdir(common_dir):
        if os.path.isdir(dir_name):
            continue
    else:
        os.mkdir(common_dir)
    os.mkdir(dir_name)

    downloads = []
    for platform in obj['platforms']:
        if 'readme' in obj['urls'][platform]:
            elem = obj['urls'][platform]['readme']
            if not elem.startswith('http:'):
                elem = 'http:'+elem
            downloads.append(elem)

        # Downloadlink per api holen
        link_url = "http://www.blackmagicdesign.com/api/register/us/download/" + str(obj['urls'][platform]['downloadId'])
        payload = '{"country":"us","platform":"' + platform + '"}'
        if obj['requiresRegistration']:
            payload = '{"country":"de","platform":"Mac OS X","firstname":"Marcus","lastname":"Weiner","email":"melodie124@gmail.com","phone":"+492114435456","city":"Duesseldorf","state":"NRW","terms":true,"product":"' + obj['name'] + '"}'

        req = urllib.request.Request(link_url, bytearray(payload, 'utf-8'), {'Content-type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as resp:
                downloads.append(str(resp.read(), encoding='UTF-8'))
        except:
            print("Error: Could not load '" + obj['name'] + "'")

    for url in downloads:
        print("Downloading " + obj['name'] + "...")
        print(url)
        try:
            urlOpener.retrieve(url, dir_name + os.sep + os.path.basename(url))
        except:
            print("Error: Could not load '" + os.path.basename(url) + "'")

