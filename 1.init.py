import os
import re
import shutil
from zipfile import ZipFile

import requests
import urllib3

from settings import BASE_FOLDER, USE_PROXY, PROXIES

# disable warning if we use proxy
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


CLIENT_FOLDER = BASE_FOLDER + 'zed-linux-x64'
REPO_NAME = 'zed-industries/zed'
# regex match which file to download if multiple files exists
PREFERRED_RELEASE_NAME_PATTERN = 'zed-linux-x64-.*?.tar.xz'
SOURCE_CODE_NAME_PATTERN = 'v.*.zip'

CMD_STOP_SERVICE = """pkill -9 Zed"""

# 是否从GitHub下载文件
# whether download files from GitHub
DO_DOWNLOAD = True

# 是否删除临时文件
# whether delete template files
# DO_DELETE = False
DO_DELETE = True


def requests_get(url):
    ret = None
    try:
        ret = requests.get(url, proxies=PROXIES, verify=not USE_PROXY)
    except Exception as e:
        print(
            'If github is not available, you can set USE_PROXY to True and set PROXIES to your proxy.'
        )
        print('Exception', e)
    return ret


def get_latest_version():
    """get latest version info"""
    print('get latest version info')
    url = f'https://api.github.com/repos/{REPO_NAME}/releases'
    print(url)

    # get latest official release, not pre-release
    releases = requests_get(url).json()
    official_releases = [release for release in releases if not release['prerelease']]
    res = official_releases[0]

    print(res)
    version_info = {}

    # zipball_url is the source code
    version_info['zipball_url'] = res['zipball_url']

    version_info['name'] = res['name']
    print(f'latest version is {version_info["name"]}')
    return version_info


def backup_old_service():
    backup_suffix = '_old'
    backup_dir = CLIENT_FOLDER + backup_suffix
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    os.mkdir(backup_dir)

    if os.path.exists(CLIENT_FOLDER):
        os.system(f'mv {CLIENT_FOLDER} {CLIENT_FOLDER}{backup_suffix}')
        print(f'old version is moved to {CLIENT_FOLDER}{backup_suffix}')


def download_file(url, file_name=None):
    """download file"""
    print('download file')
    if not file_name:
        file_name = url.split('/')[-1]
    print('downloading ...')
    if DO_DOWNLOAD:
        with requests.get(url, proxies=PROXIES, verify=False, stream=True) as r:
            r.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    print(f'download complete, file saved as {file_name}')
    return file_name


def stop_service():
    if CMD_STOP_SERVICE:
        os.system(CMD_STOP_SERVICE)


def decompress_source_package(file_name):
    if file_name.endswith('.zip'):
        with ZipFile(file_name, 'r') as zip:
            # printing all the contents of the zip file
            extracted_folder = zip.namelist()[0].split('/')[0]
        if extracted_folder:
            os.system(f'unzip -o {file_name}')
            os.system('pwd')
            if DO_DELETE:
                os.system(f'rm -rf zed-src.zip')
            print(extracted_folder)
            os.system(f'mv {extracted_folder} zed-src')


if __name__ == '__main__':
    if os.path.exists(BASE_FOLDER):
        if not (input(f'BASE_FOLDER exists! DELETE {BASE_FOLDER}, continue?(y)')).lower() in [
            'y',
            'yes',
        ]:
            exit()
        os.system(f'rm -rf {BASE_FOLDER}')
    os.makedirs(BASE_FOLDER)
    print('BASE_FOLDER', BASE_FOLDER)
    os.chdir(BASE_FOLDER)

    version_info = get_latest_version()

    print(version_info)
    stop_service()

    # 下载源码
    # get source code
    file_name = download_file(version_info['zipball_url'], 'zed-src.zip')
    file_name = 'zed-src.zip'
    print(f'file_name {file_name}')
    decompress_source_package(file_name)

    print('finished!')
