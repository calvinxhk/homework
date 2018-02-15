import os
import shutil
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ShellCmd:
    def __init__(self):
        pass

    def cd(self, args):
        try:
            filename = args['filename']
            if filename == '.':
                if os.path.dirname(os.getcwd()) == os.path.join(basedir, 'db'):
                    return os.getcwd()
                os.chdir(os.path.dirname(os.getcwd()))
            else:
                os.chdir(filename)
        except Exception:
            return os.getcwd()
        return os.getcwd()

    def pwd(self, args=0):
        return os.getcwd()

    def ls(self, args=0):
        file = os.getcwd()
        result = '\n'.join(os.listdir(file))
        return result

    def mkdir(self, args):
        file = args['filename']
        os.mkdir(file)
        return os.getcwd()

    def remove(self, args):
        file = args['filename']
        if os.path.isfile(file):
            os.remove(file)
        elif os.path.isdir(file):
            shutil.rmtree(file)
        return os.getcwd()




