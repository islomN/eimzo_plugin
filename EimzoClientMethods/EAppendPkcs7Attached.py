from CAPIWS import CAPIWS


class EAppendPkcs7Attached:
    def __init__(self, capiws:CAPIWS, id, data, timestamper, success, error):
        self.__capiws = capiws
        self.__id = id
        self.__data = data
        self.__timestamper = timestamper
        self.__successCallback = success
        self.__errorCallback = error

    def Run(self):
        self.__capiws.callFunction(
            {"plugin": "pkcs7", "name": "append_pkcs7_attached", "arguments": [self.__data,  self.__id]},
            self.__successAppendPkcs7Attached,
            self.__error)

    def __successAppendPkcs7Attached(self, data):
        if data["success"]:
            self.__pkcs7 = data["pkcs7_64"]
            if self.__timestamper:
                self.__sn = data["signer_serial_number"]
                self.__timestamper(data["signature_hex"], self.__successTimestamper, self.__error)
            else:
                self.__successCallback(self.__pkcs7)
        else:
            self.__errorCallback(data["reason"])

    def __successTimestamper(self, tst):
        self.__capiws.callFunction(
            {"plugin": "pkcs7", "name": "attach_timestamp_token_pkcs7", "arguments": [self.__pkcs7, self.__sn, tst]},
            self.__successAttachTimestampTokenPkcs7, self.__error)

    def __successAttachTimestampTokenPkcs7(self, data):
        if data["success"]:
            self.__successCallback(data["pkcs7_64"])
        else:
            self.__errorCallback(data["reason"])

    def __error(self):
        self.__errorCallback("errr")