import json

from EimzoApplicationMethods.ESignHelperMethod import ESignHelperMethod
from EimzoClient import EimzoClient
from EimzoFileInfo import EimzoFileInfo
from EimzoKeyCodeHelper import EimzoKeyCodeHelper


class EAAttachSign:
    def __init__(self, itemId, data, timestamper, errorCallback):
        self.__itemId = itemId
        self.__data = data
        self.__timestamper = timestamper

        if errorCallback is not None:
            self.__errroCallback = errorCallback

    def Run(self):
        vo = ESignHelperMethod.getCert(self.__itemId)
        if vo is not None:
            keyCode = EimzoKeyCodeHelper.getKeyCode(self.__itemId)
            if keyCode is not None:
                self.__successAppendPkcs7Attached(keyCode)
            else:
                EimzoClient(self.__successAppendPkcs7Attached, self.__errroCallback).loadKey(vo)
        else:
            self.__errroCallback("сертификат не найден")

    def __successAppendPkcs7Attached(self, id):
        EimzoKeyCodeHelper.saveKeyCode(self.__itemId, id)
        EimzoClient(self.__successCallback, self.__errroCallback).appendPkcs7Attached(id, self.__data, self.__timestamper)

    def __successCallback(self, pkcs7):
        f = open(EimzoFileInfo.pkcsFile(), "w+")
        f.write(pkcs7)
        f.close()

    def __errroCallback(self, message):
        print(message)

