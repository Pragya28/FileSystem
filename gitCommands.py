from git import Repo

def cloneFileRepo():
    try:
        Repo.clone_from("https://github.com/Pragya28/DemoFiles.git", ".\\DemoFiles")
    except Exception as e:
        print(str(e))

def gitPush():
    PATH_OF_GIT_REPO = r'.\\DemoFiles\\.git'  
    COMMIT_MESSAGE = 'committed'
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(all=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Cannot update the changes')    
# cloneFileRepo()