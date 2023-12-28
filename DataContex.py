from Dataclass_s import RecoveryClass, User, Product
import json
import datetime
import socket


class DataContex:

    @staticmethod
    def GetTime():
        return str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    @staticmethod
    def GetProdsSum(Prods: dict):
        sum = 0
        for i in Prods:
            sum += i[1] * i[0].price
        return sum

    @staticmethod
    def deserialize(takenRecovery_string: str):
        a = json.loads(takenRecovery_string)[0]
        time = json.loads(takenRecovery_string)[1]
        recovery = RecoveryClass(**json.loads(a))
        outputUser = User(**recovery.user)

        dictProdSold: dict = json.loads(json.dumps(recovery.products_with_sold))
        ProdList = list(dictProdSold.keys())

        outputProduct = []  # (user:user , sold : количество)
        for i in ProdList:
            outputProduct.append((Product(**json.loads(i)), dictProdSold[i]))

        return outputProduct, outputUser, time

    @staticmethod
    def saveTakenString(SendString: str):
        with open("takenRecovery.json", "a", encoding="UTF-8") as storage:
            storage.write(json.dumps((SendString, DataContex.GetTime())) + "\r")

    @staticmethod
    def loadProdFromFile() -> list[list[tuple[Product, int]], User, str]:
        # list заказов[tuple[ЭКЗ товара , количество],ЭКЗ юзера , время заказа]
        with open("takenRecovery.json", "r", encoding="UTF-8") as storage:
            returnListOfProdUserTime = []
            for i in storage.readlines():
                Product, User, time = DataContex.deserialize(i)
                returnListOfProdUserTime.append((Product, User, time))
        return returnListOfProdUserTime

    @staticmethod
    def recvJsonString() -> str:
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.bind(("localhost", 8800))
                server.listen(1)
                client_socket, _ = server.accept()
                JsonString = client_socket.recv(1024).decode('utf-8')
                server.close()
            return JsonString  # строка из C#
