import json
import websocket


class CAPIWS:
    URL = "ws://127.0.0.1:64646/service/cryptapi"

    def callFunction(self, funcDef, callback, error):
        self.__websocketClient(funcDef, callback, error)

    def version(self, callback, error):
        self.__websocketClient({"name": 'version'}, callback, error)

    def apidoc(self, callback, error):
        self.__websocketClient({"name": 'apidoc'}, callback, error)

    def apikey(self, domainAndKey, callback, error):
        self.__websocketClient({"name": 'apikey', "arguments": domainAndKey}, callback, error)

    def __websocketClient(self, data, callback, error):
        self.__callback = callback
        self.__error = error
        self.__data = data
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(
            self.URL,
            on_message=lambda ws, message: (CAPIWS.__on_message(ws, message, callback, error)),
            on_error=lambda ws, message: CAPIWS.__on_error(ws, message, error),
            on_open=lambda ws: CAPIWS.__on_open(ws, data, error),
            header={"host": "localhost"}
        )
        try:
            ws.run_forever()
        except:
            ws.close()

    @staticmethod
    def __on_message(ws, message, successCallback, errorCallback):
        try:
            successCallback(json.loads(message))
        except:
            errorCallback("Не удалось выполнить текущий процесс \"__on_message\" " + message)
        finally:
            ws.close()

    @staticmethod
    def __on_error(ws, message, errorCallback):
        try:
            errorCallback("Ошибка соединения с E-IMZO. Возможно у вас не установлен модуль E-IMZO.")
        except:
            errorCallback("Не удалось выполнить текущий процесс \"__on_error\"")
        finally:
            ws.close()

    @staticmethod
    def __on_open(ws: websocket, data, errorCallback):
        try:
            ws.send(json.dumps(data))
        except:
            errorCallback("Не удалось выполнить текущий процесс \"__on_open\"")
