class EHelper:
    @staticmethod
    def getX500Val(s, f):
        array = s.split(",")
        for i in range(0, len(array)):
            keys = array[i].split("=")
            if keys[0] == f: return keys[1]
        return ""