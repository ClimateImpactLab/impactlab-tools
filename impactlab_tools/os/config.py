import sys
import yaml

def getConfigDictFromFile(filePath):
    with open(filePath, 'r') as f:
        confDict = yaml.load(f)
    return confDict

def getConfigDictFromSysArgv():
    with open(sys.argv[1], 'r') as f:
        confDict = yaml.load(f)

        for key in serverConfig:
            if key not in confDict:
                confDict[key] = serverConfig[key]

        return confDict

## Server config

serverSpecificYML = "../server.yml"

serverConfig = getConfigDictFromFile(serverSpecificYML)

