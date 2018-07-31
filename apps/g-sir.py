import os
import sys
import requests

try:
    import subprocess
except:
    import commands

root_path = 'e:\django_projects'
git_token = 'VzqvbcQuzxvdQYbBX6py'


def is_python3():
    return sys.version_info[0] == 3


def pull_gsir_gitlab(path_space, is_python_3=True):
    git_gsir = 'https://gitlab.g-sir.com.cn/api/v4/projects?per_page=100' + '&' + 'private_token=' + git_token
    response = requests.get(git_gsir)
    git_repertories = [item['ssh_url_to_repo'] for item in response.json()]
    for git_path in git_repertories:
        path_split = git_path.split(':')[1].split('/')
        name_space = path_split[0]
        name_repertory = path_split[1][:-4]
        path_repertory = os.path.join(path_space, name_repertory)
        print(path_repertory)
        if not os.path.exists(path_space):
            os.makedirs(path_space)
        if not os.path.exists(path_repertory):
            os.chdir(path_space)
            # os.system('git clone ' + git_path)
            cmd = 'git clone ' + git_path
            if is_python_3:
                return_code, output = subprocess.getstatusoutput(cmd)
            else:
                return_code, output = commands.getstatusoutput(cmd)
            if not return_code:
                os.chdir(path_repertory)
                os.system('git submodule update --init --recursive')
        else:
            os.chdir(path_repertory)
            os.system('git fetch --all')
            os.system('git pull --all')
            os.system('git submodule update --recursive')
    print("finish")


if __name__ == '__main__':
    # git @ gitlab.g - sir.com.cn
    is_python_3 = is_python3()
    pull_gsir_gitlab(root_path, is_python_3)
