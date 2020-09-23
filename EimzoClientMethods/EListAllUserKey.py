from CAPIWS import CAPIWS
from EimzoClientMethods.EFindCertKey import EFindCertKey
from EimzoClientMethods.EFindCertKey2 import EFindCertKey2
from EimzoClientMethods.EFindPfx import EFindPfx
from EimzoClientMethods.EFindPfx2 import EFindPfx2
from EimzoClientMethods.EFindToken2 import EFindToken2


class EListAllUserKey:
    def __init__(self,isNewApi, capiws: CAPIWS, success, error):
        self.__isNewApi = isNewApi
        self.__capiws = capiws
        self.__success = success
        self.__error = error

    def Run(self,  itemIdGen, itemUiGen):

        items = []
        errors = []
        if not self.__isNewApi:
            def callbackCertKeys(firstItmId):
                def callbackPfxs(firstItmId2):
                    if len(items) == 0 and len(errors) > 0:
                        self.__error(errors[0].r)
                    else:
                        firstId = None
                        if len(items) == 1:
                            if firstItmId:
                                firstId = firstItmId
                            elif firstItmId2 :
                                firstId = firstItmId2

                        self.__success(items, firstId)
                EFindPfx(self.__capiws, itemIdGen, itemUiGen, items, errors, callbackPfxs).Run()

            EFindCertKey(self.__capiws, itemIdGen, itemUiGen, items, errors, callbackCertKeys).Run()
        else:
            def callbackCertKeys(firstItmId):
                def callbackPfxs(firstItmId2):
                    def callbackToken(firstItmId3):

                        if len(items) == 0 and len(errors) > 0:
                            self.__error(errors[0].r)
                        else:
                            firstId = None
                            if len(items) == 1:
                                if (firstItmId):
                                    firstId = firstItmId
                                elif firstItmId2:
                                    firstId = firstItmId2
                                elif firstItmId3:
                                    firstId = firstItmId3
                            self.__success(items, firstId)


                    EFindToken2(self.__capiws, itemIdGen, itemUiGen, items, errors, callbackToken).Run()

                EFindPfx2(self.__capiws, itemIdGen, itemUiGen, items, errors, callbackPfxs).Run()

            EFindCertKey2(self.__capiws, itemIdGen, itemUiGen, items, errors, callbackCertKeys).Run()