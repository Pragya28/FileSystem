from os import path, remove, stat, walk
from random import choice
from sys import stdin
from datetime import datetime
import json

from encrypt import encryptFile
from decrypt import decryptFile

def randomLoc():
    pathList = []
    for root, dirs, files in walk(r".\\DemoFiles"):
        for d in dirs:
            pathList.append(path.relpath(path.join(root, d), "."))
    pathList = [p for p in pathList if '.git' not in p]
    # print(pathList)
    loc =  choice(pathList)
    return loc

def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime('%c')
    return formated_date

def createFile(ownerName, receipentName, sharedKey):
    with open("data.json", "r") as f:
        data = json.load(f)
    names = [d['Name'] for d in data]
    filename = input("Enter file name: ")
    while filename in names:
        filename = input("Enter file name: ")
    print("Write your text here: ")
    print("#"*100)
    text = stdin.read()
    print("#"*100)
    filepath = randomLoc() + "\\" + filename
    with open(filepath, "w") as f:
        f.write(text)
    info = stat(filepath)
    d = {
        'Name' : filename,
        'Location' : filepath,
        'Size' : info.st_size,
        'Last Modified' : convert_date(info.st_mtime),
        'Owner' : ownerName,
        'Permitted' : receipentName,
        'Access Key' : encryptFile(filepath, sharedKey)
    }
    data.append(d)
    jsonObj = json.dumps(data, indent=4)
    with open("data.json", "w") as f:
        f.write(jsonObj)

def viewFile(sharedKey):
    with open("data.json", "r") as f:
        data = json.load(f)
    names = [d['Name'] for d in data]
    filename = input("Enter file name: ")
    while filename not in names:
        filename = input("Enter file name: ")
    idx = names.index(filename)
    d = data[idx]
    with open(d['Location']) as f:
        encContents = f.read()
    contents = decryptFile(d['Location'], d['Access Key'], sharedKey)
    print(f'The file {filename} contains:')
    print("#"*100)
    print(contents)
    print("#"*100)
    return idx, contents

def updateFile(ownerName, receipentName, sharedKey):
    with open("data.json", "r") as f:
        data = json.load(f)
    idx, text = viewFile(sharedKey)
    d = data[idx]
    print("What do you want to do with file contents? Select an option")
    print("1. Overwrite the contents")
    print("2. Append at the end")
    op = int(input("Your choice: "))
    print("Write your text here: ")
    print("#"*100)
    if op == 1:
        text = stdin.read()
    elif op == 2:
        text += stdin.read()
    else:
        print("Invalid option. File not updated")
    print("#"*100)
    filename = d['Name']
    filepath = d['Location']
    remove(filepath)
    filepath = randomLoc() + "\\" + filename
    with open(filepath, "w") as f:
        f.write(text)
    info = stat(filepath)
    d = {
        'Name' : filename,
        'Location' : filepath,
        'Size' : info.st_size,
        'Last Modified' : convert_date(info.st_mtime),
        'Access Key' : encryptFile(filepath, sharedKey)
    }
    data[idx] = d
    jobj = json.dumps(data, indent=4)
    with open("data.json", "w") as f:
        f.write(jobj)

# randomLoc()