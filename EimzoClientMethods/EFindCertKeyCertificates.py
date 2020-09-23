from datetime import datetime
from CAPIWS import CAPIWS
from EimzoClientMethods.HelperMethods.EHelper import EHelper


class EFindCertKeyCertificates:
    def __init__(self, capiws:CAPIWS, itemIdGen, itemUiGen, items, errors, allDisks, diskIndex, params, callback):
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

        self.__capiws.callFunction(
            {"plugin": "certkey", "name": "list_certificates", "arguments": [self.__allDisks[self.__diskIndex]]},
            self.__success,
            self.__error
        )

    def __success(self, data):
        if data["succes"]:

            for rec in range(0, len(data["certificates"])):
                el = data["certificates"][rec]
                vo = {
                    "disk": el["disk"],
                    "path": el["path"],
                    "name": el["name"],
                    "serialNumber": el["serialNumber"],
                    "subjectName": el["subjectName"],
                    "validFrom": datetime.strptime(el["validFrom"], "yyyymmdd"),
                    "validTo": datetime.strptime(el["validTo"], "yyyymmdd"),
                    "issuerName": el["issuerName"],
                    "publicKeyAlgName": el["publicKeyAlgName"],
                    "CN": EHelper.getX500Val(el["subjectName"], "CN"),
                    "TIN": EHelper.getX500Val(el["subjectName"], "INITIALS"),
                    "O": EHelper.getX500Val(el["subjectName"], "O"),
                    "T": EHelper.getX500Val(el["subjectName"], "T"),
                    "type": 'certkey'
                }

                if vo["TIN"] is None:
                    continue

                itmkey = self.__itemIdGen(vo, rec)
                if len(self.__params) == 0:
                    self.__params.append(itmkey)

                self.__items.append(self.__itemUiGen(itmkey, vo))
            else:
                self.__errors.append({"r": data["reason"]})

            EFindCertKeyCertificates(
                self.__capiws, self.__itemIdGen, self.__itemUiGen, self.__items, self.__errors, self.__allDisks, self.__diskIndex + 1, self.__params, self.__callback
            ).Run()

    def __error(self):
        EFindCertKeyCertificates(
            self.__capiws, self.__itemIdGen, self.__itemUiGen, self.__items, self.__errors, self.__allDisks, self.__diskIndex + 1, self.__params, self.__callback
        ).Run()
