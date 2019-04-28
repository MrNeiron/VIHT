from PyQt5 import QtCore, QtGui, QtWidgets

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