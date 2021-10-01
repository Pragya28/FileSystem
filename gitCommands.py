from git import Repo

def cloneFileRepo():
    try:
        Repo.clone_from("https://github.com/Pragya28/DemoFiles.git", ".\\DemoFiles")
    except Exception as e:
        print(str(e))

# cloneFileRepo()