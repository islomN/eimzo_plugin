from CAPIWS import CAPIWS


class EInstallApiKey:
    def __init__(self, capiws:CAPIWS, apikeys,  success, error):
        self.__capiws = capiws
        self.__apikeys = apikeys
        self.__success = success
        self.__error = error

    def Run(self):
        return self.__capiws.apikey( self.__apikeys, self.__successCallback, self.__errorCallback)

    def __successCallback(self, data):
        if data["success"]:
            if self.__success is not None:

                self.__success()
        else:
            self.__errorCallback(data["reason"])

    def __errorCallback(self, message):
        if self.__error is not None:
            self.__error(message)
