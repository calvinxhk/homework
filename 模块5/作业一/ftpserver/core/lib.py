import hashlib
import os


def file_md5(filename):
    if not os.path.isfile(filename):
        return
    with open(filename, 'rb') as f:
        myhash = hashlib.md5()
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
    return myhash.hexdigest()


