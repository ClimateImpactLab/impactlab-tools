import os
import config

def sharedpath(subpath):
    return os.path.join(config.serverConfig['shareddir'], subpath)

def configpath(path):
    if path[0] == '/':
        return path
    return sharedpath(path)

if __name__ == '__main__':
    print datapath('testing')
