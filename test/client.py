# coding=utf8
import json

import win32com.client

o = win32com.client.Dispatch("EimzoApp")
o.Sign("itm-773B0292-0", "test")
