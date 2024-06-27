import os

from settings import DEBUG, LANG, TRANS_RELEASE_FOLDER, BASE_FOLDER

script_path = os.path.dirname(os.path.abspath(__file__))
build_scripts_path = script_path + '/build_scripts'
BASE_PATH = f'{BASE_FOLDER}zed-src/'


def build_linux_release():
    # install dependencies
    # os.system(f'cd {BASE_PATH} && ./script/linux')
    # build
    os.system(f'cd {BASE_PATH} && ./build-linux.sh')


if __name__ == '__main__':
    print(f'DEBUG is {DEBUG}')

    a = input(f'Delete folder {TRANS_RELEASE_FOLDER}, continue?(y)')
    if a not in [
        'y',
    ]:
        exit()

    os.system(f'cp -r -f {build_scripts_path}/* {BASE_PATH}')

    build_linux_release()

    os.system(f'rm -rf {TRANS_RELEASE_FOLDER}')
    os.makedirs(f'{TRANS_RELEASE_FOLDER}')
    os.chdir(TRANS_RELEASE_FOLDER)

    os.system(
        f'cp {BASE_FOLDER}zed-src/target/x86_64-unknown-linux-gnu/release/zed {TRANS_RELEASE_FOLDER}/'
    )

    os.system(f'xdg-open {TRANS_RELEASE_FOLDER}')

    print('finished')
