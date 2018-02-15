import hashlib
import os
import sys


def file_md5(filename):
    myhash = hashlib.md5()
    try:
        os.path.isfile(filename)
        with open(filename, 'rb') as f:
            if os.path.getsize(filename) / (1024 * 1024) <= 1000:
                file = f.read()
                if not file:
                    return
                myhash.update(file)
            else:
                while True:
                    file = f.read(8192)
                    if not file:
                        return
                    myhash.update(file)
    except ValueError:
        myhash.update(filename)
    return myhash.hexdigest()


def myprocess(text):
    sys.stdout.write('\r'+'%.2f' % text + '%')
    sys.stdout.flush()



