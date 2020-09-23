from EimzoApplicationMethods.EALoadKey import EALoadKey
from EimzoClient import EimzoClient


class EAAppLunch:
    EimzoMajor = 3
    EimzoMinor = 37

    def __init__(self, errorCallback=None):
        if errorCallback is not None:
            self.__errorCallback = errorCallback


    def Run(self):
        EimzoClient(self.__successCallbackCheckVersion, self.__errorCallback).checkVersion()

    def __successCallbackCheckVersion(self, major, minor, isNewApi):
        print('installApiKeys')

        newVersion = self.EimzoMajor * 100 + self.EimzoMinor
        installedVersion = int(major) * 100 + int(minor)
        EimzoClient.NEW_API = isNewApi
        if installedVersion < newVersion:
            print('')
        else:

            EimzoClient(lambda: EALoadKey.Run()).installApiKeys()

    def __errorCallback(self, message):
        print(message)
