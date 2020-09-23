from CAPIWS import CAPIWS
from EimzoClientMethods.EFindCertKey import EFindCertKey
from EimzoClientMethods.EFindCertKey2 import EFindCertKey2
from EimzoClientMethods.EFindCertKeyCertificates import EFindCertKeyCertificates
from EimzoClientMethods.EFindPfx import EFindPfx
from EimzoClientMethods.EFindPfx2 import EFindPfx2
from EimzoClientMethods.EAppendPkcs7Attached import EAppendPkcs7Attached
from EimzoClientMethods.ECheckVersion import ECheckVersion
from EimzoClientMethods.ECreatePkcs7 import ECreatePkcs7
from EimzoClientMethods.EFindPfxCertificate import EFindPfxCertificate
from EimzoClientMethods.EFindToken2 import EFindToken2
from EimzoClientMethods.EInstallApiKey import EInstallApiKey
from EimzoClientMethods.EListAllUserKey import EListAllUserKey
from EimzoClientMethods.ELoadKey import ELoadKey


class EimzoClient:
    NEW_API = False
    API_KEYS =  [
        'localhost', '96D0C1491615C82B9A54D9989779DF825B690748224C2B04F500F370D51827CE2644D8D4A82C18184D73AB8530BB8ED537269603F61DB0D03D2104ABF789970B',
        '127.0.0.1', 'A7BCFA5D490B351BE0754130DF03A068F855DB4333D43921125B9CF2670EF6A40370C646B90401955E1F7BC9CDBF59CE0B2C5467D820BE189C845D0B79CFC96F',
        'edo.uzcardtrade.uz', '2CDFBE9007D8AF296FC18F3C9C382620A053B9E71609F48785B58B62642E7D3D2113BA1B55420863FD0A1C18358C323BC2166936935D97830998A8610F70565F',
        'null', 'E0A205EC4E7B78BBB56AFF83A733A1BB9FD39D562E67978CC5E7D73B0951DB1954595A20672A63332535E13CC6EC1E1FC8857BB09E0855D7E76E411B6FA16E9D',
    ]

    def __init__(self, success = lambda *args: print("default args"), error=lambda message: print(message)):
        self.__capiws = CAPIWS()
        self.__success = success
        self.__error = error

    def checkVersion(self):
        ECheckVersion(self.__capiws, self.__success, self.__error).Run()

    def installApiKeys(self):
        EInstallApiKey(self.__capiws, self.API_KEYS, self.__success,  self.__error).Run()

    def listAllUserKeys(self, itemIdGen, itemUiGen):
        EListAllUserKey(self.NEW_API, self.__capiws, self.__success,  self.__error).Run( itemIdGen, itemUiGen)

    def loadKey(self, itemObject, verifyPassword = False):
        ELoadKey(self.__capiws, itemObject, self.__success,  self.__error, verifyPassword).Run()

    def changeKeyPassword(self, itemObject, success, fail):
        print('changeKeyPassword')

    def createPkcs7(self, id, data, timestamper):
        ECreatePkcs7(self.__capiws, id, data, timestamper, self.__success , self.__error).Run()

    def appendPkcs7Attached(self, id, data, timestamper):
        EAppendPkcs7Attached(self.__capiws, id, data, timestamper, self.__success , self.__error).Run()

    def findCertKeyCertificates(self, itemIdGen, itemUiGen, items, errors, allDisks, diskIndex, params, callback):
        EFindCertKeyCertificates(self.__capiws, itemIdGen, itemUiGen, items, errors, allDisks, diskIndex, params, callback).Run()

    def findCertKeys(self, itemIdGen, itemUiGen, items, errors, callback):
        EFindCertKey(self.__capiws, itemIdGen, itemUiGen, items, errors, callback).Run()

    def findPfxCertificates(self, itemIdGen, itemUiGen, items, errors, allDisks, diskIndex, params, callback):
        EFindPfxCertificate(self.__capiws, itemIdGen, itemUiGen, items, errors, allDisks, diskIndex, params, callback).Run()

    def findPfxs(self, itemIdGen, itemUiGen, items, errors, callback):
        EFindPfx(self.__capiws, itemIdGen, itemUiGen, items, errors, callback).Run()

    def findCertKeys2(self, itemIdGen, itemUiGen, items, errors, callback):
        EFindCertKey2(self.__capiws, itemIdGen, itemUiGen, items, errors, callback).Run()

    def findPfxs2(self, itemIdGen, itemUiGen, items, errors, callback):
        EFindPfx2(self.__capiws, itemIdGen, itemUiGen, items, errors, callback).Run()

    def findTokens2(self, itemIdGen, itemUiGen, items, errors, callback):
        EFindToken2(self.__capiws, itemIdGen, itemUiGen, items, errors, callback).Run()
