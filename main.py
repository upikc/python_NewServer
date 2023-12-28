import sys
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import *
from DataContex import DataContex
from PurchaseWindow import ContentWindow


class ScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 300)
        self.setWidget(mainWindow())
        self.setWidgetResizable(True)
        self.show()


class PurchaseLay(QWidget):
    def __init__(self, DATA):
        super().__init__()
        self.DATA = DATA
        self.setStyleSheet("background-color: rgb(102, 205, 170);")
        self.lay = QGridLayout()
        self.Psum = str(DataContex.GetProdsSum(DATA[0]))
        lab = QLabel("Пользователь: " + DATA[1].login + " Cумма товаров: " + self.Psum + " Время: " + DATA[2])
        lab.setMinimumHeight(30)
        self.lay.addWidget(lab, 0, 0)

        btn = QPushButton()
        btn.setText("Открыть")
        btn.setStyleSheet("background-color: rgb(143, 188, 143);")
        btn.clicked.connect(lambda: ContentWindow(self.DATA, self.Psum))
        self.lay.addWidget(btn, 1, 0)

        self.setLayout(self.lay)


class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.UiLoad()
        self.worker = Worker()
        thread = QThread(self)
        self.worker.moveToThread(thread)
        self.worker.dataChanged.connect(self.ReloadDatalay)
        thread.started.connect(self.worker.task)
        thread.start()

    def UiLoad(self):
        mainLay = QVBoxLayout()
        sortLay = QHBoxLayout()
        self.datalay = QVBoxLayout()
        self.SortingBox = QComboBox()
        self.SearchUser = QTextEdit()
        self.SortingBox.currentTextChanged.connect(self.ReloadDatalay)
        self.SearchUser.textChanged.connect(self.ReloadDatalay)


        self.SortingBox.addItems(["по возрастанию", "По убыванию"])
        mainLay.addLayout(sortLay)
        sortLay.addWidget(self.SortingBox)
        sortLay.addWidget(self.SearchUser)
        mainLay.addLayout(self.datalay)
        self.setLayout(mainLay)

    def ReloadDatalay(self):
        for i in reversed(range(self.datalay.count())):
            self.datalay.itemAt(i).widget().setParent(None)
        sortBool = self.SortingBox.currentText() == "По убыванию"
        listLay = []
        for data in DataContex.loadProdFromFile():
            listLay.append(PurchaseLay(data))
        listLay.sort(key=lambda Purchase: Purchase.Psum, reverse=sortBool)
        for i in listLay:
            if str(i.DATA[1].login).__contains__(self.SearchUser.toPlainText()):
                self.datalay.addWidget(i)


class Worker(QObject):
    dataChanged = pyqtSignal()
    def task(self):
        while True:
            jsonString = DataContex.recvJsonString()
            DataContex.saveTakenString(jsonString)
            self.dataChanged.emit()


app = QApplication(sys.argv)
win = ScrollArea()
win.show()
sys.exit(app.exec_())
