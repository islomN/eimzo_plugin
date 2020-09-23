import json

from EimzoApplication import EimzoApplication
from EimzoFileInfo import EimzoFileInfo


class EimzoComApp():
    _public_methods_ = ['AppLaunch', 'Sign', 'AttachSign', 'GetCerts',  'GetPkcs', 'HasError']
    _public_attrs_ = ['version']
    _readonly_attr_ = []
    _reg_clsid_ = '{A8E4EE1D-A463-4B44-8640-2FD55112EF79}'
    _reg_progid_ = 'EimzoApp'
    _reg_desc_ = 'Eimzo com application'

    def __init__(self):
        self.version = '0.0.1'

    def AppLaunch(self):
        EimzoApplication().appLaunch()

    def Sign(self, id, jsonData):
        EimzoApplication().sign(id, jsonData)

    def AttachSign(self, id, jsonData):
        EimzoApplication().attachSign(id, jsonData)

    def GetCerts(self):
        return json.dumps(EimzoApplication.getCerts())

    def GetPkcs(self):
        return EimzoApplication.getPkcs()

    def HasError(self):
        return EimzoApplication.hasError()


def main():
    import win32com.server.register
    win32com.server.register.UseCommandLine(EimzoComApp)

if __name__ == '__main__':
    main()
