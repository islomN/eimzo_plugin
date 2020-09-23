from CAPIWS import CAPIWS
from EimzoClientMethods.EFindCertKeyCertificates import EFindCertKeyCertificates


class EFindCertKey:
    def __init__(self, capiws:CAPIWS, itemIdGen, itemUiGen, items, errors, callback):
        self.__capiws = capiws
        self.__itemIdGen = itemIdGen
        self.__itemUiGen = itemUiGen
        self.__items = items
        self.__errors = errors
        self.__callback = callback
        self.__allDisks = []

    def Run(self):
        self.__capiws.callFunction(
            {"plugin": "certkey", "name": "list_disks"},
            self.__successListDisks,
            self.__error
        )

    def __error(self):
        self.__errors.append({"r": "error"})
        self.__callback()

    def __successListDisks(self, data):
        if data["success"]:
            _len = len(data["disks"])
            for rec in range(0, _len):
                self.__allDisks.append(data["disks"][rec])
                if int(rec) + 1 >= _len:
                    self.__params = []
                    EFindCertKeyCertificates(
                                             self.__capiws, self.__itemIdGen, self.__itemUiGen, self.__items,
                                             self.__errors, self.__allDisks, 0, self.__params,
                                             lambda params: self.__callback(params[0])
                                             ).Run()
        else:
            self.__errors.append({"r": data["reason"]})
