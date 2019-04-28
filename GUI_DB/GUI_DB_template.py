import sys
# Импортируем наш интерфейс из файла
from GUI import * 
from PyQt5 import QtCore, QtGui, QtWidgets

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Здесь прописываем событие нажатия на кнопку
        self.ui.pushButton.clicked.connect(self.MyFunction)
    
    # Пока пустая функция, которая выполняется
    # при нажатии на кнопку
    def MyFunction(self):
        pass
    
    
class CheckableComboBox(QtWidgets.QComboBox):
    def __init__(self, central_widget):
        super(CheckableComboBox, self).__init__(central_widget)
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))
        
    def hidePopup(self):
        if not self.view().underMouse():
            QtWidgets.QComboBox.hidePopup(self)

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())