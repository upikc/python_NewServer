from DataContex import DataContex

str = open("test.json", "r", encoding="UTF-8").read()
DataContex.saveTakenString(str)  # добавление тестовых данных в хранилище заказов

for i in DataContex.loadProdFromFile():
    print(i[0][0][0].name, i[1].login, i[2])  # подсосик данных с первого продукта
