from display import homePage, optionsPage
from os import path
from gitCommands import cloneFileRepo

print("#"*100)
status, info = homePage()
print("#"*100)
if status:
    if not path.exists(".\\Demofiles"):
        cloneFileRepo()
    optionsPage(info)
