from datetime import datetime
from CAPIWS import CAPIWS
from EimzoClientMethods.HelperMethods.EHelper import EHelper


class EFindCertKey2:

    @property
    def items(self):
        return self.__items

    def __init__(self, capiws: CAPIWS, itemIdGen, itemUiGen, items, errors, callback):
        self.__capiws = capiws
        self.__itemIdGen = itemIdGen
        self.__itemUiGen = itemUiGen
        self.__items = items
        self.__errors = errors
        self.__callback = callback

    def Run(self):

        self.__itmkey0 = None
        self.__capiws.callFunction(
            {"plugin": "certkey", "name": "list_all_certificates"},
            self.__callback,
            self.__error
        )

    def __successListCertificates(self, data):

        if data["success"]:
            rec = 0
            for el in  data["certificates"]:
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
                if self.__itmkey0 is None:
                    self.__itmkey0 = itmkey

                itm = self.__itemUiGen(itmkey, vo)
                self.__items.append(itm)
                rec+=1
        else:
            self.__errors.append({"r": data["reason"]})

        self.__callback(self.__itmkey0)

    def __error(self):
        self.__errors.append({"r": "r"})
        self.__callback(self.__itmkey0)
