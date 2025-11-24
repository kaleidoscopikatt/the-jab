# @name: compadre.py
# @desc: Rigs the Santa game, and uses a hex-encoded file to store information for rigging.
#        Intended to be used as a module to be imported!

import random
import os
import struct
import game.helpers.JSONHelper as JSON

# SETTINGS
COMPADRE_FILE_NAME = ".jab"

# VARIABLES
cwd = os.getcwd()
compadreFile = os.path.join(cwd, COMPADRE_FILE_NAME)

## @name: writeCompadre
## @desc: Writes the current information to Compadre. Use this for rigging.
##        Ben, if you're reading this, UPDATE CURRENTTRY BEFORE running this.
##        Also, clamp currentTry between 1-3, or 1-10 (depending on triesToReset)! :)

def writeCompadre(currentTry, triesToReset):
    with open(compadreFile, 'wb+') as compadre:
        nextTry = random.randint(1, triesToReset)

        ctValue = struct.pack('B', currentTry)
        ntValue = struct.pack('B', nextTry)
        flag = struct.pack('B', int(currentTry==nextTry))

        compadre.write(flag + ctValue + ntValue)
        compadre.close()

## @name: readCompadre
## @desc: Reads the current information stored and relays it back to you!

def readCompadre():
    with open(compadreFile, 'rb+') as compadre:
        ## FCN - Flag, currentTry, nextTry
        data = compadre.read(3)
        if len(data) != 3:
            raise ValueError("Compadre file does not have valid data, cannot run!")
        
        flag, currentTry, nextTry = struct.unpack('BBB', data)
        flagBool = bool(flag)

        return {
            "flag": flagBool,
            "currentTry": currentTry,
            "nextTry": nextTry
        }

## @name: boot
## @desc: Initiates everything... please run FIRST.

def boot(triesToReset):
    if not os.path.exists(compadreFile):
        writeCompadre(1, triesToReset)