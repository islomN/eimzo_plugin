import json
import os

from EimzoFileInfo import EimzoFileInfo


class ESignHelperMethod:
    @staticmethod
    def getCert(itemId):
        if os.path.isfile(EimzoFileInfo.certsFile()):
            f = open(EimzoFileInfo.certsFile())
            certs = json.loads(f.read())

            for cert in certs:
                if cert["itemId"] == itemId:
                    return cert