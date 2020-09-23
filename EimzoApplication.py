import json
import os

import requests

from EimzoApplicationMethods.EAAppLunch import EAAppLunch
from EimzoApplicationMethods.EAAttachSign import EAAttachSign
from EimzoApplicationMethods.EASign import EASign
from EimzoFileInfo import EimzoFileInfo
from EimzoKeyCodeHelper import EimzoKeyCodeHelper


class EimzoApplication:
    apiUrl = "https://edotest.uzcardtrade.uz/api/factura/timestamp"

    def __init__(self):
        self.__readSettingFile()

    def timeStamper(self, signatureHex, callback, fail):

        resp = requests.get(self.apiUrl, params={"signatureHex": signatureHex})
        f = open(EimzoFileInfo.logFile(), "w+")
        f.write(str(resp.json()))
        f.close()

        if resp.status_code != 200:
            fail("bad request")
        else:
            callback(resp.json()["data"])

    def appLaunch(self):
        EimzoApplication.__removeHelperFiles()
        EimzoKeyCodeHelper.removeKeyCodeFile()
        if os.path.isfile(EimzoFileInfo.certsFile()): os.remove(EimzoFileInfo.certsFile())

        EAAppLunch(self.__error).Run()

    def wsError(self, e):
        print('wsError')

    def sign(self, id, jsonData):
        EimzoApplication.__removeHelperFiles()
        EASign(id, jsonData, self.timeStamper,self.__error).Run()

    def attachSign(self,id, jsonData):
        EimzoApplication.__removeHelperFiles()
        EAAttachSign(id, jsonData, self.timeStamper,self.__error).Run()

    @staticmethod
    def getPkcs():
        pkcs = ''
        if os.path.isfile(EimzoFileInfo.pkcsFile()):
            f = open(EimzoFileInfo.pkcsFile())
            pkcs = f.read()
            f.close()
        return pkcs

    @staticmethod
    def getCerts():
        certs = ''
        if os.path.isfile(EimzoFileInfo.certsFile()):
            f = open(EimzoFileInfo.certsFile())
            certs =  json.loads(f.read())
            f.close()
        return certs

    @staticmethod
    def getError():
        if os.path.isfile(EimzoFileInfo.errorFile()):
            f = open(EimzoFileInfo.errorFile())
            error = f.read()
            f.close()
            return error
        return ""

    @staticmethod
    def hasError():
        if  os.path.isfile(EimzoFileInfo.errorFile()):
            f = open(EimzoFileInfo.errorFile())
            error = f.read()
            f.close()
            return error is not None if False else True
        return False

    def __error(self, message):
        res = message.find('BadPaddingException')
        if res != -1:
            message = "Пароль неверный."

        res = message.find('Exception')
        if res != -1:
            message = "Произошла неизвестная ошибка"

        f = open(EimzoFileInfo.errorFile(), "w+")
        f.write(message)
        f.close()

    def __readSettingFile(self):
        f = open(EimzoFileInfo.appsettingFile())
        val = json.loads(f.read())["apiUrl"]
        f.close()

        if val is not None:
            self.apiUrl = val

    @staticmethod
    def __removeHelperFiles():
        if os.path.isfile(EimzoFileInfo.errorFile()): os.remove(EimzoFileInfo.errorFile())
        if os.path.isfile(EimzoFileInfo.pkcsFile()): os.remove(EimzoFileInfo.pkcsFile())
