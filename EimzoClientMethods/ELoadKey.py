from CAPIWS import CAPIWS


class ELoadKey:
    @property
    def itemObject(self):
        return self.__itemObject

    def __init__(self,  capiws:CAPIWS, itemObject, successCallback, errorCallback,verifyPassword):
        self.__capiws = capiws
        self.__successCallback = successCallback
        self.__errorCallback = errorCallback
        self.__itemObject = itemObject
        self.__verifyPassword = verifyPassword

    def Run(self):
        if self.__itemObject:
            vo = self.__itemObject
            if vo["type"] == "certkey":
                self.__capiws.callFunction({"plugin": "certkey", "name": "load_key", "arguments": [vo["disk"], vo["path"], vo["name"], vo["serialNumber"]]}, self.__callbackCertKey, self.__errorCallback)
            elif vo["type"] == "pfx":
                self.__capiws.callFunction({"plugin": "pfx", "name": "load_key", "arguments": [vo["disk"], vo["path"], vo["name"],vo["alias"]]}, self.__callbackPfx, self.__errorCallback)
            elif vo["type"] == "ftjc":
                self.__capiws.callFunction({"plugin": "ftjc", "name": "load_key", "arguments": [vo["cardUID"]]}, self.__callbackFtjc,self.__errorCallback)

    def __success(self, data):
        if data["success"]:
            self.__successCallback()
        else:
            self.__errorCallback(data["reason"])

    def __error(self):
        self.__errorCallback("Error EInstallApiKey")

    def __callbackCertKey(self, data):
        if data["success"]:
            self.__id = data["keyId"]
            self.__successCallback(data["keyId"])
        else:
            self.__errorCallback(data["reason"])

    def __callbackPfx(self, data):
        if data["success"]:
            # print("data= ", data)
            self.__id = data["keyId"]
            if self.__verifyPassword:
                self.__capiws.callFunction({"name": "verify_password", "plugin": "pfx", "arguments": [self.__id]}, self.__callbackVerifyPassword, self.__errorCallback)
            else:
                self.__successCallback(self.__id)

    def __callbackFtjc(self, data):
        if data["success"]:
            self.__id = data["keyId"]
            if self.__verifyPassword:
                self.__capiws.callFunction({"plugin": "ftjc", "name": "verify_pin", "arguments": [self.__id,'1']}, self.__callbackVerifyPassword,  self.__errorCallback)
            else:
                self.__successCallback(self.__id)

    def __callbackVerifyPassword(self, data):
        if data["success"]:
            self.__successCallback(self.__id)
        else:
            self.__errorCallback(data["reason"])



