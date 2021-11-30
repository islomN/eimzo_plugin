import json
from EimzoApplication import EimzoApplication
from EimzoFileInfo import EimzoFileInfo
import win32com.server.register
import os, sys, win32api, win32con, win32com.server.register

class EimzoComApp:
    _public_methods_ = ['AppLaunch', 'Sign', 'AttachSign', 'GetCerts',  'GetPkcs', 'HasError']
    _public_attrs_ = ['version']
    _readonly_attr_ = []
    _reg_clsid_ = '{67C92391-BD99-4090-82F7-09BF3C6EA87A}'
    _reg_progid_ = 'EimzoAppV2'
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

def RegisterClass(cls):
  file = os.path.abspath(sys.modules[cls.__module__].__file__)
  folder = os.path.dirname(file)
  module = os.path.splitext(os.path.basename(file))[0]
  python = win32com.server.register._find_localserver_exe(1)
  python = win32api.GetShortPathName(python)
  server = win32com.server.register._find_localserver_module()
  command = '%s "%s" %s' % (python, server, cls._reg_clsid_)
  typename = module + "." + cls.__name__

  def write(path, value):
    win32api.RegSetValue(win32con.HKEY_CURRENT_USER, path, win32con.REG_SZ, value)

  write("SOFTWARE\\Classes\\" + cls._reg_progid_ + '\\CLSID', cls._reg_clsid_)
  write("SOFTWARE\\Classes\\AppID\\" + cls._reg_clsid_, cls._reg_progid_)
  write("SOFTWARE\\Classes\\CLSID\\" + cls._reg_clsid_, cls._reg_desc_)
  write("SOFTWARE\\Classes\\CLSID\\" + cls._reg_clsid_ + '\\LocalServer32', command)
  write("SOFTWARE\\Classes\\CLSID\\" + cls._reg_clsid_ + '\\ProgID', cls._reg_progid_)
  write("SOFTWARE\\Classes\\CLSID\\" + cls._reg_clsid_ + '\\PythonCOMPath', folder)
  write("SOFTWARE\\Classes\\CLSID\\" + cls._reg_clsid_ + '\\PythonCOM', typename)
  write("SOFTWARE\\Classes\\CLSID\\" + cls._reg_clsid_ + '\\Debugging', "0")

  print("Registered %s" % cls.__name__)

def main():
    RegisterClass(EimzoComApp)
    # win32com.server.register.UseCommandLine(EimzoComApp, debug=1)

if __name__ == '__main__':
    main()

