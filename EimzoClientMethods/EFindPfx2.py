from datetime import datetime

from CAPIWS import CAPIWS
from EimzoClientMethods.HelperMethods.EHelper import EHelper


class EFindPfx2:
    def __init__(self, capiws: CAPIWS, itemIdGen, itemUiGen, items, errors,  callback):
        self.__capiws = capiws
        self.__itemIdGen = itemIdGen
        self.__itemUiGen = itemUiGen
        self.__items = items
        self.__errors = errors
        self.__callback = callback

    def Run(self):
        self.__itmkey0 = None
        self.__capiws.callFunction(
            {"plugin": "pfx", "name": "list_all_certificates"},
            self.__successListCertificates,
            self.__error
        )

    def __successListCertificates(self, data):
        # print('data', data)
        if data["success"]:
            rec = 0
            for el in data["certificates"]:

                x500name_ex = el["alias"].upper()
                x500name_ex = x500name_ex.replace("1.2.860.3.16.1.1=", "INN=")
                x500name_ex = x500name_ex.replace("1.2.860.3.16.1.2=", "PINFL=")
                vo = {
                    "disk": el["disk"],
                    "path": el["path"],
                    "name": el["name"],
                    "alias": el["alias"],
                    "serialNumber": EHelper.getX500Val(x500name_ex, "SERIALNUMBER"),
                    "validFrom": EHelper.getX500Val(x500name_ex, "VALIDFROM"),
                    "validTo": EHelper.getX500Val(x500name_ex, "VALIDTO"),
                    "CN": EHelper.getX500Val(x500name_ex, "CN"),
                    "TIN":  (EHelper.getX500Val(x500name_ex, "INN") if EHelper.getX500Val(x500name_ex,"INN") else EHelper.getX500Val(x500name_ex, "UID")),
                    "UID": EHelper.getX500Val(x500name_ex, "UID"),
                    "O": EHelper.getX500Val(x500name_ex, "O"),
                    "T": EHelper.getX500Val(x500name_ex, "T"),
                    "type": 'pfx'
                }

                if vo["TIN"] is None:
                    continue
                if self.__itemIdGen:
                    itmkey = self.__itemIdGen(vo, rec)
                    if self.__itmkey0 is None:
                        self.__itmkey0 = itmkey

                    if self.__itemUiGen:
                        itm = self.__itemUiGen(itmkey, vo)
                        self.__items.append(itm)
                rec+=1
        else:
            self.__errors.append({"r": data["reason"]})
        self.__callback(self.__itmkey0)

    def __success(self):
        print('')

    def __error(self):
        self.__errors.append({"r":{}})
        self.__callback(self.__itmkey0)

