# coding=utf8
import base64
import re


class Base64:
    VERSION = "2.1.4"

    __re_utob = '[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]'

    __b64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    @staticmethod
    def atob(value):
        return base64.b64decode(value).decode()

    @staticmethod
    def btoa(value):
        return base64.b64encode(value.encode()).decode()

    @staticmethod
    def fromBase64():
        print('fromBase64')

    @staticmethod
    def toBase64():
        print('toBase64')

    @staticmethod
    def utob(u):
        Base64.__re_utob = Base64.__re_utob.encode("utf-16", "surrogatepass").decode("utf-16", "surrogatepass")

        return re.sub( Base64.__re_utob.encode("utf-16", "surrogatepass").decode("utf-16", "surrogatepass"),  Base64.__cb_utob, u)
        # return u.(Base64.__re_utob, Base64.__cb_utob)

    @staticmethod
    def encode(u):
        u_bytes = u.encode('utf-8')
        base64_bytes = base64.b64encode(u_bytes)
        return str(base64_bytes, "utf-8")
        # return Base64.__encode(u)

    @staticmethod
    def encodeURI(u):
        return Base64.encode(u)

    @staticmethod
    def btou():
        print('btou')

    @staticmethod
    def decode(a):
        return ''

    @staticmethod
    def noConflict(self):
        print('noConflict')

    @staticmethod
    def __encode(u):
        return Base64.btoa(Base64.utob(u))

    @staticmethod
    def __cb_encode(ccc):
        length = len(ccc)
        padlen = [0, 2, 1][length % 3]
        _ord = ord(ccc[0]) << 16   | ((length > 1 if ord(ccc[1]) else 0) << 8) | ((length > 2 if ord(ccc[2]) else 0))

        chars = [
            Base64.__b64chars[_ord >> 18],
            Base64.__b64chars[(_ord >> 12) & 63],
            padlen >= 2 if '=' else Base64.__b64chars[(_ord >> 6) & 63],
            padlen >= 1 if '=' else Base64.__b64chars[_ord & 63]
        ]

        return ''.join(chars)

    @staticmethod
    def __decode( a):
        return Base64.btoa(Base64.atob(a))

    @staticmethod
    def __cb_decode(self, cccc):
        _len = len(cccc),
        padlen = _len % 4,
        n = (_len > 0 if Base64.__b64tab()[cccc[0]] << 18 else 0) | (_len > 1 if Base64.__b64tab()[cccc[1]] << 12 else 0) | (_len > 2 if Base64.__b64tab()[cccc[2]]<< 6 else 0) | (_len > 3 if Base64.__b64tab()[cccc[3]] else 0),
        chars = [
            self.__fromCharCode(n >>  16),
            self.__fromCharCode((n >> 8) & 0xff),
            self.__fromCharCode(n & 0xff)
        ]
        index = ([0, 0, 2, 1][padlen])*-1
        chars = chars[:index]
        return ''.join(chars)

    @staticmethod
    def __fromCharCode(unichr):
        return ''.join(map(unichr, [65,66,67]))

    @staticmethod
    def __cb_utob(c):
        if len(c) < 2:
            cc = ord(c[0])

            if cc < 0x80:
                return c
            else:
                if cc < 0x800:
                    return (Base64.__fromCharCode(0xc0 | (cc >> 6))
                                + Base64.__fromCharCode(0x80 | (cc & 0x3f)))
                else:
                    return (Base64.__fromCharCode(0xe0 | ((cc >> 12) & 0x0f))
                            + Base64.__fromCharCode(0x80 | ((cc >> 6) & 0x3f))
                            + Base64.__fromCharCode(0x80 | (cc & 0x3f)))
        else:
            cc = 0x10000 + (c[0] - 0xD800) * 0x400 + (c[1] - 0xDC00)

            return (Base64.__fromCharCode(0xf0 | ((cc >> 18) & 0x07))
                    + Base64.__fromCharCode(0x80 | ((cc >> 12) & 0x3f))
                    + Base64.__fromCharCode(0x80 | ((cc >> 6) & 0x3f))
                    + Base64.__fromCharCode(0x80 | (cc & 0x3f)))

    @staticmethod
    def __cb_btou( cccc):
        length = len(cccc)
        if length == 4:
            cp = ((0x07 & ord(cccc[0])) << 18) | ((0x3f & ord(cccc[1])) << 12) | ((0x3f & ord(cccc[2])) << 6) | (0x3f & ord(cccc[3]))
            offset = cp - 0x10000
            return (Base64.__fromCharCode((offset >> 10) + 0xD800)
                    + Base64.__fromCharCode((offset & 0x3FF) + 0xDC00))
        elif length == 3:
            return Base64.__fromCharCode(
                ((0x0f & ord(cccc[0])) << 12)
                | ((0x3f & ord(cccc[1])) << 6)
                | (0x3f & ord(cccc[2]))
            )
        else:
            return Base64.__fromCharCode(
                ((0x1f & ord(cccc[0])) << 6)
                | (0x3f & cccc.charCodeAt(1))
            )

    @staticmethod
    def __b64tab():
        return Base64.__b64tabDef(Base64.__b64chars)

    @staticmethod
    def __b64tabDef( bin):
        t = {}
        for i in range(0, len(bin)-1):
            t[ord(bin[i])] = i

        return t

