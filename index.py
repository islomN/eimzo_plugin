import json
import sys
from EimzoApplication import EimzoApplication

_len = len(sys.argv)
if _len <= 1:
    print("error")
command = sys.argv[1]
if command == "app-launch":
    EimzoApplication().appLaunch()
elif command == "sign":
    if _len < 4:
        print("error")
    else:
        string =""
        for i in range(3, len(sys.argv)):
            string += sys.argv[i]

        EimzoApplication().sign(sys.argv[2], string)
elif command == "attach-sign":
    if _len < 4:
        print("error")
    else:
        EimzoApplication().attachSign(sys.argv[2], sys.argv[3])
elif command == "get-certs":
    print(EimzoApplication.getCerts())
elif command == "get-pkcs":
    print(EimzoApplication.getPkcs())
elif command == "get-error":
    print(EimzoApplication.getError())
elif command == "has-error":
    print(EimzoApplication.hasError())
else:
    print("command not found")
