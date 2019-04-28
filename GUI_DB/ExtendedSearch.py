# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\users\ivan\githubme\forvivt\utils\ExtendedSearch.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ExtendedSearch(object):
    def setupUi(self, ExtendedSearch):
        ExtendedSearch.setObjectName("ExtendedSearch")
        
        self.windowSize = [248, 184]
        
        ExtendedSearch.resize(*self.windowSize)
        self.centralwidget = QtWidgets.QWidget(ExtendedSearch)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 50, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(100, 50, 51, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(160, 50, 69, 22))
        self.comboBox_3.setEditable(True)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_4 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_4.setGeometry(QtCore.QRect(90, 80, 71, 22))
        self.comboBox_4.setObjectName("comboBox_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 10, 71, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(150, 120, 81, 17))
        self.checkBox.setObjectName("checkBox")
        
        
        ExtendedSearch.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ExtendedSearch)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 248, 21))
        self.menubar.setObjectName("menubar")
        ExtendedSearch.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ExtendedSearch)
        self.statusbar.setObjectName("statusbar")
        ExtendedSearch.setStatusBar(self.statusbar)
        
        self.lastFieldComboBoxSize = [20, 50, 69, 22]
        self.lastEqualComboBoxSize = [100, 50, 51, 22]
        self.lastItemComboBoxSize = [160, 50, 69, 22]
        self.lastExpressionComboBoxSize = [90, 80, 71, 22]
        self.checkBoxSize = [150, 120, 81, 17]
        
        self.allSearchFieldComboBoxes = [self.comboBox]
        self.allEqualComboBoxes = [self.comboBox_2]
        self.allSearchItemComboBoxes = [self.comboBox_3]
        self.allExpressionComboBoxes = [self.comboBox_4]

        self.retranslateUi(ExtendedSearch)
        QtCore.QMetaObject.connectSlotsByName(ExtendedSearch)

    def retranslateUi(self, ExtendedSearch):
        _translate = QtCore.QCoreApplication.translate
        ExtendedSearch.setWindowTitle(_translate("ExtendedSearch", "Расширенный поиск"))
        self.pushButton.setText(_translate("ExtendedSearch", "Сброс"))
        self.pushButton_2.setText(_translate("ExtendedSearch", "Принять"))
        self.checkBox.setText(_translate("ExtendedSearch", "Сохранить"))

