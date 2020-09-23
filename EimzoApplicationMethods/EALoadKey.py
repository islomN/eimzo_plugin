import json
import os

from EimzoClient import EimzoClient
from EimzoFileInfo import EimzoFileInfo


class EALoadKey:
    @staticmethod
    def Run():
        EALoadKey.__clearStore()
        # print("clear")
        EimzoClient(EALoadKey.__successCallback).listAllUserKeys(EALoadKey.__itemIdGen, EALoadKey.__itemUidGen)

    @staticmethod
    def __successCallback(items, firstId):
        print('items EALoadKey')
        # print("items:" + json.dumps(items))

        f = open(EimzoFileInfo.certsFile(), "w+")
        f.write(json.dumps(items))
        f.close()

    def __errorCallback(r):
        print(json.dumps(r))

    @staticmethod
    def __itemIdGen(o, i):
        # print('__itemIdGen', o, i)
        return "itm-" + str(o["serialNumber"]) + "-" + str(i)

    @staticmethod
    def __itemUidGen(itemId, vo):
        if vo is not None:
            vo["itemId"] = itemId
        return vo

    @staticmethod
    def __clearStore():
        f = open(EimzoFileInfo.certsFile(), "w+")
        f.write("{}")
        f.close()

