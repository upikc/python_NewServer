from PyQt5.QtWidgets import *

class ContentWindow(QWidget):
    def __init__(self, Purchase : dict, summ):
        super().__init__()
        self.SortCBox = QComboBox()
        self.SortCBox.currentTextChanged.connect(lambda: self.dataWrite(Purchase, self.SortCBox.currentIndex() != 0))
        self.table = QTableWidget(0, 7)
        self.UiLoad(summ)
        self.show()

    def UiLoad(self , summ):
        vbox = QVBoxLayout()
        HToolBox = QHBoxLayout()
        self.table.setHorizontalHeaderLabels(
            ["name", "category", "creator", "price", "description",
             "img", "SOLD"])
        self.SortCBox.addItems(["По возрастанию", "По убыванию"])

        vbox.addWidget(self.table)
        vbox.addLayout(HToolBox)
        HToolBox.addWidget(self.SortCBox)
        HToolBox.addWidget(QLabel("сумма заказа :" + summ))
        self.setLayout(vbox)
        self.setGeometry(300, 300, 920, 450)

    def writeRows(self, Prod : dict, row):
        self.table.removeRow(row)  # стерли строку
        self.table.insertRow(row)  # вставили пустую
        self.table.setItem(row, 0, QTableWidgetItem(str(Prod[0].name)))
        self.table.setItem(row, 1, QTableWidgetItem(str(Prod[0].category)))
        self.table.setItem(row, 2, QTableWidgetItem(str(Prod[0].creator)))
        self.table.setItem(row, 3, QTableWidgetItem(str(Prod[0].price)))
        self.table.setItem(row, 4, QTableWidgetItem(str(Prod[0].description)))
        self.table.setItem(row, 5, QTableWidgetItem(str(Prod[0].img)))
        self.table.setItem(row, 6, QTableWidgetItem(str(Prod[1])))
        self.table.resizeColumnsToContents()

    def dataWrite(self, Purchase, SortRevers: bool):
        sorted_people = sorted(Purchase[0], key=lambda item: item[0].price, reverse=SortRevers)
        for j, i in enumerate(sorted_people):
            self.writeRows(i, j)