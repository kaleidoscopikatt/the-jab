# @name: compadre.py
# @desc: Rigs the Santa game, and uses a hex-encoded file to store information for rigging.
#        Intended to be used as a module to be imported!

import random
import os
import struct
import game.helpers.JSONHelper as JSON
import math

# SETTINGS
COMPADRE_FILE_NAME = ".jab"

# VARIABLES
cwd = os.getcwd()
compadreFile = os.path.join(cwd, COMPADRE_FILE_NAME)

screenWidth = 600

## @name: writeCompadre
## @desc: Writes the current information to Compadre. Use this for rigging.
##        Ben, if you're reading this, UPDATE CURRENTTRY BEFORE running this.
##        Also, clamp currentTry between 1-3, or 1-10 (depending on triesToReset)! :)

def writeCompadre(currentTry, triesToReset, updateNextTry=False):
    if updateNextTry:
        nextTry = random.randint(1, triesToReset)
    else:
        nextTry = readCompadre()["nextTry"]

    with open(compadreFile, 'wb+') as compadre:
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


## @name: __parseDataFile
## @desc: Private function for parsing 👁.👁 into an array of rows.

def __parseDataFile(data):
    left_max, right_min = struct.unpack_from("hh", data)
    return [left_max, right_min]


## @name: __getRandomPosition
## @desc: Private function for getting a random, reachable position

def __getRandomPosition(playerX):
    randomVal = random.randint(1, screenWidth)
    return __getRandomPosition(playerX)


## @name: getCompadre
## @desc: Gets either a random or an unreachable position from 👁.👁

def getCompadre(playerX, floorWidth, data):
    randomVal = __getRandomPosition(playerX, floorWidth, data)
    shouldUnreach = readCompadre()["flag"] == True

    specificData = data[playerX]
    if specificData[0] != 0 and specificData[1] != floorWidth:
        randomIndex = random.randint(0, 1)
        randomOffset = random.randint(50, 100) * (-1 if randomIndex == 0 else 1)

        unreachablePosition = specificData[randomIndex] + randomOffset
    else:
        randomOffset = random.randint(50, 100)
        if specificData[0] == 0:
            unreachablePosition = specificData[1] + randomOffset
        elif specificData[1] == floorWidth:
            unreachablePosition = specificData[0] - randomOffset
    return unreachablePosition if shouldUnreach else randomVal


## @name: boot
## @desc: Initiates everything... please run FIRST.

def boot(triesToReset):
    if not os.path.exists(compadreFile):
        writeCompadre(1, triesToReset, updateNextTry=True)
    ##data = None
    ##with open('👁.👁', 'rb') as f:
    ##    data = __parseDataFile(f.read())
    ##    f.close()
    
    ##return data