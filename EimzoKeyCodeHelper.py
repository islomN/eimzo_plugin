import json
import os

from EimzoFileInfo import EimzoFileInfo


class EimzoKeyCodeHelper:

    @staticmethod
    def getKeyCode(itemId):
        if os.path.isfile(EimzoFileInfo.keyCodeFile()) is False:
            return None
        f = open(EimzoFileInfo.keyCodeFile())
        keyCodeFile = f.read()
        f.close()
        if keyCodeFile is None:
            return None
        keyCodeJson = json.loads(keyCodeFile)

        if itemId not in keyCodeJson:
            return None
        return keyCodeJson[itemId]

    @staticmethod
    def saveKeyCode(itemId, keyCode):
        EimzoKeyCodeHelper.removeKeyCodeFile()
        keyCodeOld = EimzoKeyCodeHelper.getKeyCode(itemId)
        if keyCodeOld is None:
            jsonData = {itemId: keyCode}
            f = open(EimzoFileInfo.keyCodeFile(), "w+")
            f.write(json.dumps(jsonData))

    @staticmethod
    def removeKeyCodeFile():
        if os.path.isfile(EimzoFileInfo.keyCodeFile()):
            os.remove(EimzoFileInfo.keyCodeFile())
