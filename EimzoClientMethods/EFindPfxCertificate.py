from datetime import datetime

from CAPIWS import CAPIWS
from EimzoClientMethods.HelperMethods.EHelper import EHelper


class EFindPfxCertificate:
    def __init__(self,capiws:CAPIWS, itemIdGen, itemUiGen, items, errors, allDisks, diskIndex, params, callback):
        self.__capiws = capiws
        self.__itemIdGen = itemIdGen
        self.__itemUiGen = itemUiGen
        self.__items = items
        self.__errors = errors
        self.__allDisks = allDisks
        self.__diskIndex = diskIndex
        self.__params = params
        self.__callback = callback

    def Run(self):
        if int(self.__diskIndex) + 1 > len(self.__allDisks):
            self.__callback(self.__params)
            return

        self.__capiws.callFunction({"plugin": "pfx", "name": "list_certificates", "arguments": [self.__allDisks[self.__diskIndex]]},self.__success, self.__error)

    def __successListCertificates(self, data):
        if data["success"]:
            for rec in range(0, data["certificates"]):
                el = data["certificates"][rec]
                x500name_ex = el["alias"].upper()
                x500name_ex = x500name_ex.replace("1.2.860.3.16.1.1=", "INN=")
                x500name_ex = x500name_ex.replace("1.2.860.3.16.1.2=", "PINFL=")
                vo = {
                    "disk": el["disk"],
                    "path": el["path"],
                    "name": el["name"],
                    "alias": el["alias"],
                    "serialNumber": EHelper.getX500Val(x500name_ex, "SERIALNUMBER"),
                    "validFrom": datetime.strptime(EHelper.getX500Val(x500name_ex, "VALIDFROM").replace('/\./g, "-"').replace(" ", "T"), "yyyymmdd"),
                    "validTo": datetime.strptime(EHelper.getX500Val(x500name_ex, "VALIDTO").replace('/\./ g, "-"').replace(" ", "T"), "yyyymmdd"),
                    "CN": EHelper.getX500Val(x500name_ex, "CN"),
                    "TIN": (EHelper.getX500Val(x500name_ex, "INN") if EHelper.getX500Val(x500name_ex, "INN") else EHelper.getX500Val(x500name_ex, "UID")),
                    "UID": EHelper.getX500Val(x500name_ex, "UID"),
                    "O": EHelper.getX500Val(x500name_ex, "O"),
                    "T": EHelper.getX500Val(x500name_ex, "T"),
                    "type": 'pfx'
                }

                if vo["TIN"] is None:
                    continue
                itmkey = self.__itemIdGen(vo, rec)
                if len(self.__params) == 0:
                    self.__params.append(itmkey)

                itm = self.__itemUiGen(itmkey, vo)
                self.__items.append(itm)
            else:
                self.__errors.append({"r" : data["reason"]})

        newModel = EFindPfxCertificate(
            self.__capiws, self.__itemIdGen, self.__itemUiGen, self.__items, self.__errors, self.__allDisks,
            self.__diskIndex + 1, self.__params, self.__callback
        )

        newModel.Run()
        self.__items = newModel.__items

    def __success(self):
        print('')

    def __error(self):
        newModel = EFindPfxCertificate(
            self.__capiws, self.__itemIdGen, self.__itemUiGen, self.__items, self.__errors, self.__allDisks,
            self.__diskIndex + 1, self.__params, self.__callback
        )

        newModel.Run()
        self.__items = newModel.__items

