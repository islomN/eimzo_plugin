from CAPIWS import CAPIWS

class ECheckVersion:
    def __init__(self, capiws:CAPIWS, success, error):
        self.__capiws = capiws
        self.__success = success
        self.__error = error

    def Run(self):
        return self.__capiws.version(self.__successCallback, self.__errorCallback)

    def __successCallback(self, data):

        if data["success"]:
            if data["major"] and data["minor"]:
                installedVersion = int(data["major"]) * 100 + int(data["minor"])
                self.__success(data["major"], data["minor"], installedVersion >= 336)
            else:
                self.__error('E-IMZO Version is undefined')
        else:
            self.__error(data["reason"])


    def __errorCallback(self, message):
        self.__error(message)
