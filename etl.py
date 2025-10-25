import subprocess
import os
import stat
import shutil

def remove_readonly(func, path, excinfo):
    """
    Error handler for shutil.rmtree to handle read-only files.
    """
    # Change the file permission to writable
    os.chmod(path, stat.S_IWRITE)
    # Retry the removal
    func(path)

def download_repo(repo):
    process = subprocess.Popen(['git', 'clone', "--bare", repo], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        print(f'Repo Downloaded: {repo}')
        print(stdout.decode())
    else:
        print('Error:')
        print(stderr.decode())

def delete_dir_tree(path: str):
    try:
        shutil.rmtree(path, onerror=remove_readonly)
    except OSError as e:
        print(f"Error: {e}")

def create_gitlog_file(project_name: str):
    pn = project_name.replace(".", "")
    log_name = f"repo/{pn}_git_history.txt"
    with open(log_name, "w") as f:
        subprocess.run(["git", "log"], stdout=f, cwd=project_name, stderr=subprocess.PIPE, text=True)
    return log_name

CURRENT_CWD = os.getcwd()
files_dirs = os.listdir(CURRENT_CWD)
repos = []
with open("list.txt", "r") as fp: 
    repos = [line.strip() for line in fp.readlines()]
for repo in repos:
    project_name = repo.split("/")[-1][0:-4]
    if project_name not in files_dirs:
        print(f"Processing {repo}!")
        download_repo(repo)
        log_path = create_gitlog_file(project_name)
        delete_dir_tree(project_name)
    

