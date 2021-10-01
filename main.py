from display import homePage, optionsPage

print("#"*100)
status, info = homePage()
print("#"*100)
if status:
    optionsPage(info)
