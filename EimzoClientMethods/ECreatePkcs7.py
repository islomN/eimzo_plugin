import json

from Base64 import Base64
from CAPIWS import CAPIWS

class ECreatePkcs7:
    def __init__(self, capiws:CAPIWS, id, data, timestamper, success, error):
        self.__capiws = capiws
        self.__data = data
        self.__id = id
        self.__timestamper = timestamper
        self.__successCallback = success
        self.__errorCallback = error

    def Run(self):
        self.__capiws.callFunction(
            {"plugin": "pkcs7", "name": "create_pkcs7", "arguments": [Base64.encode(self.__data), self.__id, 'no']},
            self.__successCreatePkcs7,
            self.__error
        )

    def __successCreatePkcs7(self,data):

        try:
            if data["success"]:
                self.__pkcs7 = data["pkcs7_64"]
                # print('signature', data)
                try:
                    if self.__timestamper:
                        try:
                            try:
                                self.__sn = data["signer_serial_number"]
                            except:
                                self.__error("innner signer_serial_number")

                            try:
                                self.__timestamper(data["signature_hex"], self.__successTimestamper, self.__errorCallback)
                            except:
                                self.__error("innner signature_hex __successTimestamper __timestamper : " )
                        except:
                            self.__error("innner __timestamper")
                    else:

                        self.__successCallback(self.__pkcs7)
                except:
                    self.__error('__timestamper' + str(data["signature_hex"] + ': ' + data["signer_serial_number"]))
            else:
                self.__errorCallback(data["reason"])
        except:
            self.__error('__successCreatePkcs7'  + str(data))

    def __successTimestamper(self, tst):
        try:
            self.__capiws.callFunction({"plugin":"pkcs7", "name":"attach_timestamp_token_pkcs7", "arguments":[self.__pkcs7, self.__sn, tst]}, self.__successAttachTimestampTokenPkcs7, self.__error)
        except:
            self.__error('__successTimestamper callFunction')
    def __successAttachTimestampTokenPkcs7(self, data):
        if data["success"]:
            self.__successCallback(data["pkcs7_64"])
        else:
            self.__errorCallback(data["reason"])

    def __error(self, message):
        self.__errorCallback(message)
