import os

class EimzoFileInfo:
    @staticmethod
    def appsettingFile():
        return os.path.dirname(os.path.abspath(__file__)) + "/appsettings.json"

    @staticmethod
    def certsFile():
        return EimzoFileInfo.__file("certs.json")

    @staticmethod
    def keyFile():
        return EimzoFileInfo.__file("key")

    @staticmethod
    def pkcsFile():
        return EimzoFileInfo.__file("pkcs")

    @staticmethod
    def keyCodeFile():
        return EimzoFileInfo.__file("key_code.json")

    @staticmethod
    def errorFile():
        return EimzoFileInfo.__file("error")

    @staticmethod
    def logFile():
        return EimzoFileInfo.__file("log")

    @staticmethod
    def __file( name):
        return os.path.dirname(os.path.abspath(__file__)) + "/tmpfiles/"+name
