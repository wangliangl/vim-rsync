import os
import vim
import time
from subprocess import check_output


IGNORE_FILES = ['vender', '.env', '.git', 'tags']


def without_slash(dirname):
    if dirname.endswith('/'):
        return dirname[:-1]
    return dirname


def with_slash(dirname):
    if not dirname.endswith('/'):
        return dirname+'/'
    return dirname


def path_join(base, path):
    return with_slash(base) + path


def find_sync_dir():
    d = os.path.abspath(os.getcwd())
    syncfile = None
    while d != '/':
        sfile = os.path.join(d, '.vim-sync')
        if os.path.exists(sfile):
            syncfile = sfile
            local_dir = d
            break
        d = os.path.dirname(d)
    if not syncfile:
        return None
    with open(syncfile) as f:
       remote_dir = f.read().strip()
    return remote_dir, local_dir


def find_sync_path(target):
    remote_dir, local_dir = find_sync_dir()
    target = os.path.abspath(target)
    relpath = target[len(with_slash(local_dir)):]
    remote_path = path_join(remote_dir, relpath)
    return remote_path, os.path.abspath(target)


def rsync(src, dst, compress=True):
    print("syncing...")
    cmd = ['rsync', '-azW', '--delete', src, dst]
    start = time.time()
    for ig in IGNORE_FILES:
        cmd.append('--exclude')
        cmd.append(ig)
    check_output(cmd)
    print("finished! in %f s" % (time.time() - start))


def upload():
    remote_dir, local_dir = find_sync_dir()
    rsync(with_slash(local_dir), without_slash(remote_dir))


def download():
    remote_dir, local_dir = find_sync_dir()
    rsync(with_slash(remote_dir), without_slash(local_dir))


def download_file():
    current_file = vim.eval("expand('%:p')")
    remote_path, local_path = find_sync_path(current_file)
    rsync(remote_path, local_path)


def upload_file():
    current_file = vim.eval("expand('%:p')")
    remote_path, local_path = find_sync_path(current_file)
    rsync(local_path, remote_path)


if __name__ == '__main__':
    upload_file('test') 
