from CAPIWS import CAPIWS
from EimzoClientMethods.EFindPfxCertificate import EFindPfxCertificate


class EFindPfx:
    def __init__(self,capiws:CAPIWS,itemIdGen, itemUiGen, items, errors, callback):
        self.__capiws = capiws
        self.__itemIdGen = itemIdGen
        self.__itemUiGen = itemUiGen
        self.__items = items
        self.__errors = errors
        self.__callback = callback

    def Run(self):
        self.__allDisks = []
        self.__capiws.callFunction({"plugin": "pfx", "name": "list_disks"}, self.__successListDisks, self.__error)

    def __successListDisks(self,data):
        if data["success"]:
            for rec in range(0, len(data["disks"])):
                self.__allDisks.append(data["disks"][rec])

                if int(rec) + 1 >= len(data["disks"]):
                    params = []
                    EFindPfxCertificate(
                        self.__capiws, self.__itemIdGen, self.__itemUiGen, self.__items, self.__errors, self.__allDisks,
                        0, params, self.__callback
                    ).Run()


        else:
            self.__errors.append({"r": data["reason"]})


    def __error(self):
        self.__errors.append({"r": "r"})
        self.__callback()