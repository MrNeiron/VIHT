import sys
from GUI import *
from DB import DB
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import os
from datetime import datetime



class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Имя файла с расположением баз данных
        self.saveDatabaseFile = self.SetDatabasesFile("AliasDatabases.txt")
        
        # Задание формата отображения времени в отчете
        self.timeFormat = "%H:%M:%S"

        self.Start()
        
        # Инициализация поля отчета
        self.ui.textEdit.setReadOnly(True)
        self.ui.textEdit.setPlainText("\t\t\t****** Добро пожаловать в редактор базы данных  ******\nТекущий файл с расположением баз данных = " + str(self.saveDatabaseFile))
        

        
        # Задание методов на действия
        self.ui.pushButton.clicked.connect(self.OpenFile)
        self.ui.pushButton_2.clicked.connect(self.Refresh)
        self.ui.pushButton_3.clicked.connect(self.Search)
        self.ui.pushButton_4.clicked.connect(self.Save)
        self.ui.pushButton_5.clicked.connect(self.ui.openExtendedSearch)
        self.ui.pushButton_6.clicked.connect(self.Delete)
        self.ui.pushButton_7.clicked.connect(self.Append)
        self.ui.pushButton_8.clicked.connect(self.ClearOutput)
        self.ui.comboBox.activated[str].connect(self.SetDatabase)
        self.ui.comboBox_2.activated[str].connect(self.SetTable)
        self.ui.comboBox_3.activated[str].connect(self.ChoiseCheckMode)
        self.ui.comboBox_4.activated[str].connect(self.SetSearchField)
        self.ui.comboBox_5.activated[str].connect(self.SetEqualItem)
        self.ui.comboBox_6.currentTextChanged[str].connect(self.SetSearchItem)
        self.ui.radioButton.toggled.connect(lambda:self.UnblockSearchExtendButton(self.ui.radioButton))
        self.ui.radioButton_2.toggled.connect(lambda:self.BlockSearchExtendButton(self.ui.radioButton_2))
        
        self.ui.searchWindow.pushButton.clicked.connect(self.ResetComboBoxes)
        self.ui.searchWindow.pushButton_2.clicked.connect(self.AcceptSearchWindow)
        
        self.ui.searchWindow.allSearchFieldComboBoxes[-1].activated[str].connect(self.SetSearchFieldExtend)
        self.ui.searchWindow.allSearchItemComboBoxes[-1].activated[str].connect(self.SetSearchItem)
        self.ui.searchWindow.allExpressionComboBoxes[-1].activated[str].connect(self.ChangeSearchLine)
     
    def Start(self):     

        # Задание текущей базы данных
        self.dbNames = self.LoadDatabases()
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(self.dbNames.keys())
        
        # Выбор таблицы из базы данных
        self.SetDatabase(self.ui.comboBox.currentText())
    
    # Кнопки
    # Открытие диалогового окна для задания базы данных
    def OpenFile(self, emptyList = False):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Выберете базу данных", os.getcwd())[0]
        if fname == '' or fname.split('.')[-1] != 'db': return -1
        alias = os.path.basename(fname).split('.')[0]
         
        yetNames = self.LoadDatabases() if not emptyList else {}
        if alias not in yetNames.keys():
            f = open(self.saveDatabaseFile, 'a')
            f.write(f"{alias} = {fname}\n")
            f.close()
            self.dbNames[alias] = fname
            if not emptyList: self.ui.comboBox.addItem(alias)
        
        self.SetDatabase(alias)
    
    # Откатить значения базы данных до последнего сохранения и сбросить поиск
    def Refresh(self):
        self.searchMode = "simple"
        
        self.appendBuffer.clear()
        self.delBufferId.clear()
        
        self.FillTable()
        
        time = datetime.strftime(datetime.now(), self.timeFormat)
        self.ui.textEdit.append(str(time)+": Обновлено")
    
    # Выполнение поиска
    def Search(self):
        # Определяет будет ли осуществляться обычный поиск или расширенный
        self.searchMode = "condition_extend" if self.ui.radioButton.isChecked() else "condition"
        
        self.appendBuffer.clear()
        self.delBufferId.clear()
        
        message = self.FillTable() if self.curTable != '' else self.myDb.messageNothing
        
        time = datetime.strftime(datetime.now(), self.timeFormat)
        self.ui.textEdit.append(f"{time}: {message}")
    
    # Добавить запись в таблицу(без сохранения)
    def Append(self):
        oldMode=  self.searchMode
        self.searchMode += "_append"
        
        self.FillTable()
        
        self.searchMode = oldMode
        
        time = datetime.strftime(datetime.now(), self.timeFormat)
        self.ui.textEdit.append(str(time) + ": Добавление строки")
    
    # Удалить запись из таблицы(без сохранения)  
    def Delete(self):
        # Получить текущую отмеченную строку таблицы
        delRow = self.ui.tableWidget.currentRow()
        
        if delRow == -1: return -1
        
        oldMode= self.searchMode
        self.searchMode += "_lookId"

        # Получить список с id сохраеннных строк в базе данных
        dataIds,_ = self.GetData()
        delId = 0
        
        # Если количество id не совпадает с количеством строк в таблице, то задействовать буфер с добавленными строками
        if len(dataIds) < delRow+1:
            bufferIds = [buf[self.curColumns[1]] for buf in self.appendBuffer]
            delId = int(bufferIds[delRow - len(dataIds)])
        else:
            delId =  dataIds[delRow][0]
            
        self.delBufferId.append(delId)
        
        self.searchMode = oldMode
        self.searchMode += "_delete"
        
        self.FillTable()
        
        time = datetime.strftime(datetime.now(), self.timeFormat)
        self.ui.textEdit.append(str(time) + ": Удаление строки")
    
    # Сохранить\Обновить данные таблицы в базе данных
    def Save(self):
        if self.ui.tableWidget.rowCount() == 0: return -1
      
        countChanged,messageChanged = self.SaveTable()
  
        for delRow in self.delBufferId:
            self.myDb.Del_row(self.curTable, delRow, print_logs = False)
        
        countAppend, messageAppended = self.SaveBuffer()  
        
        countDel = len(self.delBufferId)
        messageDeleted = f"Удалена {countDel} строка" if (countDel%100 < 11 or countDel % 100 > 19) and countDel % 10 == 1  else f"Удалены {countDel} строки" if (countDel%100 < 11 or countDel % 100 > 19) and 1 < countDel % 10 < 5 else f"Удалено {countDel} строк"
        
        self.appendBuffer.clear()
        self.delBufferId.clear()
        
        # Это для того, чтобы поле поиска при обычном поиске не сбрасывалось при сохранении
        oldComboBoxText = self.ui.comboBox_4.currentText()
        oldComboBoxIndex = self.ui.comboBox_4.findText(oldComboBoxText, QtCore.Qt.MatchFixedString)
        self.ui.comboBox_4.clear()
        self.ui.comboBox_4.addItems(self.curColumns[1:])
        if oldComboBoxText in self.curColumns[1:]:
            self.ui.comboBox_4.setCurrentIndex(oldComboBoxIndex)
        else:
            self.ui.textEdit.append("----------- Неправильно изменено значение ------------------")
        self.searchField = self.ui.comboBox_4.currentText()
        
        # Это для того, чтобы значение поиска при обычном поиске не сбрасывалось при сохранении
        oldComboBoxText = self.ui.comboBox_6.currentText()
        oldComboBoxIndex = self.ui.comboBox_6.findText(oldComboBoxText, QtCore.Qt.MatchFixedString)
        self.ui.comboBox_6.clear()
        items = self.GetItems()
        self.ui.comboBox_6.addItems(items)
        if oldComboBoxIndex == -1:
            self.ui.comboBox_6.setCurrentText(oldComboBoxText)
        elif oldComboBoxText in items:
            self.ui.comboBox_6.setCurrentIndex(oldComboBoxIndex)
        else:
            self.ui.textEdit.append("----------- Неправильно изменено значение ------------------")
        self.SetSearchItem(self.ui.comboBox_6.currentText())
        
        self.checkMode = self.SetCheckMode("All")
        if self.checkMode: self.GetShowList()
            
        self.FillTable()
        
        countAll = self.ui.tableWidget.rowCount()
        messageAll = f"Всего {countAll} строка" if (countAll%100 < 11 or countAll % 100 > 19) and countAll % 10 == 1  else f"Всего {countAll} строки" if (countAll%100 < 11 or countAll % 100 > 19) and 1 < countAll % 10 < 5 else f"Всего {countAll} строк"
        

        time = datetime.strftime(datetime.now(), self.timeFormat)
        self.ui.textEdit.append(f"""{time}: Сохранено
---|{messageChanged}|---
---|{messageAppended}|---
---|{messageDeleted}|---
---|{messageAll}|---""")

    # Очистить поле вывода отчетов    
    def ClearOutput(self):
        self.ui.textEdit.clear()

    # Принять заданные параметры расширенного поиска(просто закрыть окно)
    def AcceptSearchWindow(self):
        self.ui.window.close()
        
    # Разблокировать кнопку расширенного поиска и расширенный поиск
    def UnblockSearchExtendButton(self, b1):
        if b1.isChecked() and self.curTable != '':
            self.ui.pushButton_5.setEnabled(True)
            self.ui.comboBox_4.setEnabled(False)
            self.ui.comboBox_5.setEnabled(False)
            self.ui.comboBox_6.setEnabled(False)
            
            # Если параметры расширенного поиска были сохранены, то задать их заново
            if self.ui.searchWindow.checkBox.isChecked():
                self.ui.searchWindow.allSearchFieldComboBoxes = self.savedSearchFieldComboBoxes
                self.ui.searchWindow.allEqualComboBoxes = self.savedEqualComboBoxes
                self.ui.searchWindow.allSearchItemComboBoxes = self.savedSearchItemComboBoxes
                self.ui.searchWindow.allExpressionComboBoxes = self.savedExpressionComboBoxes
                self.oldAllSearchFieldComboBoxesIndex = [box.currentText() for box in self.ui.searchWindow.allSearchFieldComboBoxes] 
            else:                
                self.ResetComboBoxes()


        elif self.curTable == '': self.ui.pushButton_5.setEnabled(False)           

    # Заблокировать расширенный поиск
    def BlockSearchExtendButton(self, b1):
        if b1.isChecked() and self.curTable != '':
            self.ui.pushButton_5.setEnabled(False)
            self.ui.comboBox_4.setEnabled(True)
            self.ui.comboBox_5.setEnabled(True)
            self.ui.comboBox_6.setEnabled(True)
            
            # Если сохранение отмечено, то сохранить параметры расширенного поиска
            if self.ui.searchWindow.checkBox.isChecked():
                self.savedSearchFieldComboBoxes = self.ui.searchWindow.allSearchFieldComboBoxes
                self.savedEqualComboBoxes = self.ui.searchWindow.allEqualComboBoxes
                self.savedSearchItemComboBoxes = self.ui.searchWindow.allSearchItemComboBoxes
                self.savedExpressionComboBoxes = self.ui.searchWindow.allExpressionComboBoxes
                
            self.SetSearchField(self.ui.comboBox_4.currentText())
            self.SetEqualItem(self.ui.comboBox_5.currentText())
            self.SetSearchItem(self.ui.comboBox_6.currentText())
        
        elif self.curTable == '':
            self.ui.comboBox_4.setEnabled(False)
            self.ui.comboBox_5.setEnabled(False)
            self.ui.comboBox_6.setEnabled(False)

    # Основные методы
    # Задает файл с расположением баз данных
    def SetDatabasesFile(self, file):
        if os.path.exists(file):
            return file
        else:
            file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберете файл с расположениями баз данных", os.getcwd())[0]
            return file
    
    # Загружает базы данных из файла с их расположениями
    def LoadDatabases(self):
        try:
            f = open(self.saveDatabaseFile, 'r')
            lines = [line[:-1] if line[-1] == '\n' else line for line in f]
            if len(lines) == 0 or len(lines) == 1 and lines[0] == '':
                self.dbNames = {}
                self.OpenFile(emptyList = True)
                return self.dbNames
            else:
                dbNames = {line.split(' = ')[0]:line.split(' = ')[1] for line in lines} 
            f.close()        
            return dbNames
        except:
            f.close()
            print("Error database file")
            sys.exit()

    # Задать текущую базу данных    
    def SetDatabase(self, name):
        try:
            self.myDb = DB(self.dbNames[name])
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItems(self.myDb.table_names)
            self.SetTable(self.ui.comboBox_2.currentText())
        except:
            self.ui.textEdit.append(f"Базы данных {name} больше нет!")
            f = open(self.saveDatabaseFile, 'r')
            lines = f.readlines()
            for i,_ in enumerate(lines):
                if lines[i].split(' = ')[0] == name: del lines[i]
            f.close()
            f = open(self.saveDatabaseFile, 'w')
            f.write(''.join(lines))
            f.close()
            self.Start()
            

    # Задать текущую таблицу
    def SetTable(self, name, refresh_buffers = True):
        self.curTable = name
        if refresh_buffers:
            self.appendBuffer = []
            self.delBufferId = []
        self.curColumns = ("All", *self.myDb.Get_columns_names(self.curTable))
        self.SetDefaultCheckState()
        
        self.ui.comboBox_4.clear()
        self.ui.comboBox_4.addItems(self.curColumns[1:])        
        self.searchField = self.ui.comboBox_4.currentText()
        self.searchMode = "simple"
        
        if self.ui.comboBox_5.count() == 0:
            self.ui.comboBox_5.addItems(('=','<>','>','<','>=','<='))
        self.equalItem = self.ui.comboBox_5.currentText()
        
        self.ui.comboBox_6.clear()
        self.ui.comboBox_6.addItems(self.GetItems())
        self.ui.comboBox_6.setEditable(True)
        self.SetSearchItem(self.ui.comboBox_6.currentText())
        
        if self.ui.radioButton.isChecked(): self.ui.pushButton_5.setEnabled(True)
        else:
            self.ui.comboBox_4.setEnabled(True)
            self.ui.comboBox_5.setEnabled(True)
            self.ui.comboBox_6.setEnabled(True)
        self.checkMode = self.SetCheckMode("All")
        if self.checkMode == "pick": self.GetShowList()
        self.hideId = False
            
        self.ResetComboBoxes()
        self.FillTable()
    
    # Задает столбы таблицы
    def ChoiseCheckMode(self, name):
        if self.SetCheckMode(name) == "pick":
            self.checkMode = "pick"
            self.ui.comboBox_3.model().item(0,0).setCheckState(QtCore.Qt.Unchecked)
            self.GetShowList()
        else:
            self.checkMode = "all"
            self.hideId = False
            for i in range(1,len(self.curColumns)):
                #item = self.ui.comboBox_3.model().item(i, 0).setCheckState(QtCore.Qt.Unchecked)
                self.ui.comboBox_3.model().item(i, 0).setCheckState(QtCore.Qt.Unchecked)
        self.FillTable()
        
    # Заполняет таблицу данными
    def FillTable(self):
        
        # Просматривать буффер, если список отображаемых столбцов совпадает со столбцами таблицы
        if self.hideId and len(self.showList)-1 == self.ui.tableWidget.columnCount() or not self.hideId and len(self.showList) == self.ui.tableWidget.columnCount():
            self.ScanBuffer()

        data,message = self.GetData()
        
        # Если нет данных
        if len(data) == 0:
            # Не помню зачем нужно было это делать, но вдруг сломается что-то
            self.searchMode = "simple_delete"
            data,message = self.GetData()
            # Если нет данных даже с удаленными строками
            if len(data) == 0:
                self.curTable = ''
                self.ui.comboBox_2.clear()
                self.ui.comboBox_3.clear()
                self.ui.comboBox_4.clear()
                self.ui.comboBox_4.setEnabled(False)
                self.ui.comboBox_5.setEnabled(False)
                self.ui.comboBox_6.setEnabled(False)
                self.ui.pushButton_5.setEnabled(False)
                self.ui.tableWidget.setRowCount(0)        
                self.ui.tableWidget.setColumnCount(0)
                self.ui.tableWidget
                return message
            else:               
                self.SetTable(self.curTable, False)
                message = message + ".Обновлено"
        
        #self.hideId = False

        # Определение кол-ва строк и столбцов в таблице
        dataRows =  len(data)
        numRows = len(data)
        if len(self.appendBuffer) != 0: numRows += len(self.appendBuffer)
        dataCols = len(data[0])
        numCols = len(data[0])
        if self.hideId: numCols -= 1
 
        self.ui.tableWidget.setRowCount(numRows)        
        self.ui.tableWidget.setColumnCount(numCols)
        self.ui.tableWidget.setHorizontalHeaderLabels(self.curColumns[1:] if self.checkMode == "all" else self.showList[1:] if self.hideId else self.showList)

        # Запись данных из базы данных в таблицу
        for row in range(dataRows):
            for col in range(numCols):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(data[row][col if not self.hideId else col + 1])))
        
        # Запись данных из буфера в таблицу
        if len(self.appendBuffer) != 0:
            for i, row in enumerate(range(dataRows, numRows)):
                for j, col in enumerate(range(numCols)):
                    lookList = self.curColumns[1:] if self.checkMode == "all" else self.showList
                    self.ui.tableWidget.setItem(row, col, QTableWidgetItem(self.appendBuffer[i][lookList[j if not self.hideId else j + 1]]))
        
        self.ui.tableWidget
        
        return message
    
    # Делает выборку данных в зависомости от метода поиска и отображаемых столбцов, взаимодействуя с методами базы данных
    def GetData(self):
        try:
            # Если обычная выборка(без условия)
            if "simple" in self.searchMode: data,message =  self._getDataSimple()

            # Если выборка с условием
            elif "condition" in self.searchMode: data,message = self._getDataCondition()               
                
        except:
            data, message = [],  "Произошла ошибка! Данные не взяты"
        finally:
            return data, message
            
    # Обновляет базу данных данными из таблицы
    def SaveTable(self):
        try:
            changed_rows = self.ScanTable()
            if len(changed_rows.keys()) != 0:
                for row, changed_values in changed_rows.items():
                    for field, value in changed_values:
                        mess = self.myDb.Update_row(self.curTable, field, value, row, print_logs = False)
                        if mess != '': print("message = ", message)
                            
            numRows = len(changed_rows)
            
            message = f"Изменена {numRows} строка" if (numRows%100 < 11 or numRows % 100 > 19) and numRows % 10 == 1  else f"Изменены {numRows} строки" if (numRows%100 < 11 or numRows % 100 > 19) and 1 < numRows % 10 < 5 else f"Изменено {numRows} строк"
        except:
            message = "Произошла ошибка! Таблица не изменена."
            numRows = 0
        finally:
            return numRows, message
    
    # Просматривает таблицу находя измененные данные в таблице
    def ScanTable(self):
        changed_rows = {}
        
        data,_ = self.GetData()
        for row in range(self.ui.tableWidget.rowCount()-len(self.appendBuffer)):
            for col in range(self.ui.tableWidget.columnCount()):
                if self.checkMode == "all":
                    if col == 0: continue
                    if str(data[row][col]) != self.ui.tableWidget.item(row, col).text():
                        
                        # Если в словаре нет ключа с таким id, то добавить по новому ключу список
                        if not changed_rows.get(self.ui.tableWidget.item(row, 0).text()):
                            changed_rows[self.ui.tableWidget.item(row, 0).text()] = []
                            
                        lookList = self.curColumns[1:]
                        changed_rows[self.ui.tableWidget.item(row, 0).text()].append((lookList[col],self.ui.tableWidget.item(row, col).text()))
                else:
                    if str(data[row][col+1 if self.hideId else col]) != self.ui.tableWidget.item(row, col).text():
                        
                        # Если в словаре нет ключа с таким id, то добавить по новому ключу список
                        if not changed_rows.get(data[row][0]):
                            changed_rows[data[row][0]] = []
                            
                        lookList = self.showList[1:] if self.hideId else self.showList                        
                        changed_rows[data[row][0]].append((lookList[col+1 if not self.hideId else col],self.ui.tableWidget.item(row, col).text()))
                     
        return changed_rows

    # Сохраняет новые данные, хранящиеся в буфере, в базу данных        
    def SaveBuffer(self):
        try:
            self.ScanBuffer()
            numRows = len(self.appendBuffer)
            if numRows != 0:
                for buf in self.appendBuffer:
                    value = list(buf.values())
                    
                    mess = self.myDb.Add_values(self.curTable, self.curColumns[1:], value, print_logs = False)
                    if mess != '': print("message = ", mess)
                        
            message = f"Добавлена {numRows} строка" if (numRows%100 < 11 or numRows % 100 > 19) and numRows % 10 == 1  else f"Добавлены {numRows} строки" if (numRows%100 < 11 or numRows % 100 > 19) and 1 < numRows % 10 < 5 else f"Добавлено {numRows} строк"
        except:
            numRows = 0
            message = "Произошла ошибка! Данные не добавлены."
        finally:
            return numRows, message  

    # Просматривает буфер добавленных данных, находя изменения в них
    def ScanBuffer(self):
        if len(self.appendBuffer) != 0:
            for i, row in enumerate(range(self.ui.tableWidget.rowCount() - len(self.appendBuffer), self.ui.tableWidget.rowCount())):
                for j, col in enumerate(range(self.ui.tableWidget.columnCount())):
                    if self.checkMode == "all":
                        self.appendBuffer[i][self.curColumns[1:][col]] = self.ui.tableWidget.item(row, col).text() 
                    else:
                        self.appendBuffer[i][self.showList[col if not self.hideId else col +1]] = self.ui.tableWidget.item(row, col).text() 

    # Сбросить все выпадающие списки в окне расширенного поиска
    def ResetComboBoxes(self):
        for cBox in self.ui.searchWindow.allSearchFieldComboBoxes:
            cBox.clear()
            cBox.addItems(self.curColumns[1:])
        for cBox in self.ui.searchWindow.allEqualComboBoxes:
            cBox.clear()
            cBox.addItems(('=','<>','>','<','>=','<='))
        self.GetItems(self.curColumns[1])
        for cBox in self.ui.searchWindow.allSearchItemComboBoxes:
            cBox.clear()
            cBox.addItems(self.searchFieldItems)
        for cBox in self.ui.searchWindow.allExpressionComboBoxes[:-1]:
            cBox.clear()
            cBox.addItems(("И", "ИЛИ"))

        # Задание отличного набора "И"/"ИЛИ" списка для последнего и предпосленего элемента, чтобы у них была возможность добавления и удаления критериев
        self.ui.searchWindow.allExpressionComboBoxes[-1].clear()
        self.ui.searchWindow.allExpressionComboBoxes[-1].addItems(('+',"И", "ИЛИ"))
        if len(self.ui.searchWindow.allExpressionComboBoxes) > 1:
            self.ui.searchWindow.allExpressionComboBoxes[-2].insertItem(0, '+')
    
        # Задание старый значений полей поиска
        self.oldAllSearchFieldComboBoxesIndex = [self.curColumns[1] for _ in range(len(self.ui.searchWindow.allSearchFieldComboBoxes))]
    
        
    # Изменяет количество критериев поиска
    def ChangeSearchLine(self, value):
        if len(self.ui.searchWindow.allExpressionComboBoxes) < 10 and self.ui.searchWindow.allExpressionComboBoxes[-1].currentText() != '+':
            self.AppendSearhLine()
        elif len(self.ui.searchWindow.allExpressionComboBoxes) != 1 and self.ui.searchWindow.allExpressionComboBoxes[-2].currentText() == '+':
            self.DeleteSearchLine()
        
    # Добавляет еще один критерий поиска в расширенном поиске
    def AppendSearhLine(self):
        # Задает новые значения размеров для новых элементов
        self.ui.searchWindow.windowSize[1] += 60
        self.ui.searchWindow.lastFieldComboBoxSize[1] += 60
        self.ui.searchWindow.lastEqualComboBoxSize[1] += 60
        self.ui.searchWindow.lastItemComboBoxSize[1] += 60
        self.ui.searchWindow.lastExpressionComboBoxSize[1] += 60
        self.ui.searchWindow.checkBoxSize[1] += 60
        
        # Убирает возможность удаления элементов у предыдущего элемента со списоком "И"/"ИЛИ"
        if len(self.ui.searchWindow.allExpressionComboBoxes) > 1:
            if self.ui.searchWindow.allExpressionComboBoxes[-2].itemText(0) == '+':
                self.ui.searchWindow.allExpressionComboBoxes[-2].removeItem(0)
            if self.ui.searchWindow.allExpressionComboBoxes[-2].activated[str].connect(self.ChangeSearchLine):
                self.ui.searchWindow.allExpressionComboBoxes[-2].activated[str].disconnect(self.ChangeSearchLine)
        
        # Изменить размеры окна и чек бокса
        self.ui.window.resize(*self.ui.searchWindow.windowSize)
        self.ui.searchWindow.checkBox.setGeometry(*self.ui.searchWindow.checkBoxSize)
        
        # Добавляет и инициализирует список с полями поиска
        self.ui.searchWindow.allSearchFieldComboBoxes.append(QtWidgets.QComboBox(self.ui.searchWindow.centralwidget))
        self.ui.searchWindow.allSearchFieldComboBoxes[-1].setGeometry(QtCore.QRect(*self.ui.searchWindow.lastFieldComboBoxSize))
        self.ui.searchWindow.allSearchFieldComboBoxes[-1].addItems(self.curColumns[1:])
        self.oldAllSearchFieldComboBoxesIndex.append(self.curColumns[1])
        self.ui.searchWindow.allSearchFieldComboBoxes[-1].activated[str].connect(self.SetSearchFieldExtend)

        # Добавляет и инициализирует список со сравнениями
        self.ui.searchWindow.allEqualComboBoxes.append(QtWidgets.QComboBox(self.ui.searchWindow.centralwidget))
        self.ui.searchWindow.allEqualComboBoxes[-1].setGeometry(QtCore.QRect(*self.ui.searchWindow.lastEqualComboBoxSize))
        self.ui.searchWindow.allEqualComboBoxes[-1].addItems(('=','<>','>','<','>=','<='))
        
        # Добавляет и инициализирует список со значениями поиска
        self.ui.searchWindow.allSearchItemComboBoxes.append(QtWidgets.QComboBox(self.ui.searchWindow.centralwidget))
        self.ui.searchWindow.allSearchItemComboBoxes[-1].setGeometry(QtCore.QRect(*self.ui.searchWindow.lastItemComboBoxSize))
        self.ui.searchWindow.allSearchItemComboBoxes[-1].addItems(self.GetItems())
        self.ui.searchWindow.allSearchItemComboBoxes[-1].setEditable(True)
        self.ui.searchWindow.allSearchItemComboBoxes[-1].activated[str].connect(self.SetSearchItem)
            
        # Добавляет и инициализирует список со значениями "И"/"ИЛИ"  
        self.ui.searchWindow.allExpressionComboBoxes.append(QtWidgets.QComboBox(self.ui.searchWindow.centralwidget))
        self.ui.searchWindow.allExpressionComboBoxes[-1].setGeometry(QtCore.QRect(*self.ui.searchWindow.lastExpressionComboBoxSize))
        self.ui.searchWindow.allExpressionComboBoxes[-1].addItems(('+','И','ИЛИ'))
        
        # Отображает новые списки
        self.ui.searchWindow.allSearchFieldComboBoxes[-1].show()
        self.ui.searchWindow.allEqualComboBoxes[-1].show()
        self.ui.searchWindow.allSearchItemComboBoxes[-1].show()
        self.ui.searchWindow.allExpressionComboBoxes[-1].show()

        # Добавляет метод на действие со списком "И"/"ИЛИ"
        self.ui.searchWindow.allExpressionComboBoxes[-1].activated[str].connect(self.ChangeSearchLine) 
    
    # Удаляет критерий в расширенном поиске
    def DeleteSearchLine(self):
        # Скрывает элементы
        self.ui.searchWindow.allSearchFieldComboBoxes[-1].hide()
        self.ui.searchWindow.allEqualComboBoxes[-1].hide()
        self.ui.searchWindow.allSearchItemComboBoxes[-1].hide()
        self.ui.searchWindow.allExpressionComboBoxes[-1].hide()
        
        # Удаляет элементв
        del self.ui.searchWindow.allSearchFieldComboBoxes[-1]
        del self.oldAllSearchFieldComboBoxesIndex[-1]
        del self.ui.searchWindow.allEqualComboBoxes[-1]
        del self.ui.searchWindow.allSearchItemComboBoxes[-1]
        del self.ui.searchWindow.allExpressionComboBoxes[-1]
        
        # Меняет размеры на предыдующие
        self.ui.searchWindow.windowSize[1] -= 60
        self.ui.searchWindow.lastFieldComboBoxSize[1] -= 60
        self.ui.searchWindow.lastEqualComboBoxSize[1] -= 60
        self.ui.searchWindow.lastItemComboBoxSize[1] -= 60
        self.ui.searchWindow.lastExpressionComboBoxSize[1] -= 60
        self.ui.searchWindow.checkBoxSize[1] -= 60
        
        # Изменить размеры окна и чек бокса
        self.ui.window.resize(*self.ui.searchWindow.windowSize)
        self.ui.searchWindow.checkBox.setGeometry(*self.ui.searchWindow.checkBoxSize)            
        
        # Заново добавляет функцию добавления критериев
        if len(self.ui.searchWindow.allExpressionComboBoxes) > 1:
            self.ui.searchWindow.allExpressionComboBoxes[-2].insertItem(0, '+')        

    
    # Возвращает вариант отображения столбцов
    def SetCheckMode(self, name):
        self.GetShowList()
        if self.ui.comboBox_3.model().item(0,0).checkState() == QtCore.Qt.Checked:
            if name != "All" and len(self.showList) != 0:
                self.ui.comboBox_3.model().item(0,0).setCheckState(QtCore.Qt.Unchecked)
                return "pick"
            else:
                return "all"
        else:
            if len(self.showList) == 0:
                self.ui.comboBox_3.model().item(0,0).setCheckState(QtCore.Qt.Checked)
                return "all"
            else:
                return "pick"        
    
    # Задает список имен текущих столбцов таблицы
    def GetShowList(self):
        self.showList = []
        for i in range(1,len(self.curColumns)):
            item = self.ui.comboBox_3.model().item(i, 0)
            if item.checkState() == QtCore.Qt.Checked:
                self.showList.append(self.curColumns[i])
        if len(self.showList) != 0:
            if "ID" not in self.showList and "Id" not in self.showList and "id" not in self.showList:
                self.showList.insert(0, "ID")
                self.hideId = True
            else:
                self.hideId = False
                
    # Выделят столбцы таблицы, которые должны отображаться, в выпадающем списке    
    def SetDefaultCheckState(self):
        self.ui.comboBox_3.clear()
        for i in range(len(self.curColumns)):
            self.ui.comboBox_3.addItem(self.curColumns[i])
            item = self.ui.comboBox_3.model().item(i, 0)
            item.setCheckState(QtCore.Qt.Unchecked)
            
        self.ui.comboBox_3.model().item(0,0).setCheckState(QtCore.Qt.Checked)
            
    # Задает поле по которому будет осуществляться поиск по одному критерию
    def SetSearchField(self, field):
        self.searchField = field
        self.ui.comboBox_6.clear()
        self.ui.comboBox_6.addItems(self.GetItems())
        self.SetSearchItem(self.ui.comboBox_6.currentText())
    
    # Задает поле по которому будет осуществляться поиск с несколькими критериям
    def SetSearchFieldExtend(self,field):
        index = 0
        for i in range(len(self.oldAllSearchFieldComboBoxesIndex)):
            if self.ui.searchWindow.allSearchFieldComboBoxes[i].currentText() != self.oldAllSearchFieldComboBoxesIndex[i]:
                index = i
                break
        self.oldAllSearchFieldComboBoxesIndex[index] = field
        cBox = self.ui.searchWindow.allSearchItemComboBoxes[index]
        self.searchField = field
        cBox.clear()
        cBox.addItems(self.GetItems())
        
        self.SetSearchItem(cBox.currentText())

    # Возвращает значения, имеющиеся в поле для поиска            
    def GetItems(self, searchField = None):
        self.searchFieldItems = self.myDb.ItemsInColumn(self.curTable, self.searchField if searchField is None else searchField)
        self.searchFieldItems = [item[0] if type(item[0]) is str else str(item[0]) for item in self.searchFieldItems]
        return self.searchFieldItems
                
    # Задает вариант сравнения со значением поиска    
    def SetEqualItem(self, item): # for comboBox_5
        self.equalItem = item
        
    # Задает значение для поиска
    def SetSearchItem(self, name): # for comboBox_6
        self.searchItem = name
            
    # Дополнительные методы
    # Если обычная выборка(без условия) 
    def _getDataSimple(self):       
        # Если нужно просто узнать id строк
        if "lookId" in self.searchMode:
            for optionId in ["ID", "Id", "id"]:
                data,message = self.myDb.Get_values(self.curTable, fields = [optionId], print_logs = False)
                if len(data) != 0: break
                    
        # Если отображаются все столбцы таблицы            
        elif self.checkMode == "all":
            data,message = self.myDb.Get_values(self.curTable, mode = self.checkMode, print_logs = False)
            
        # Если отображаются выборочные столбцы
        else:
            data,message = self.myDb.Get_values(self.curTable, fields = self.showList)
        
        # Если добавляется строка
        if "append" in self.searchMode: self._append()
            
        # Если удаляется строка
        if "delete" in self.searchMode: data,message = self._delete(data)
            
        return data,message
    
    # Если выборка с условием
    def _getDataCondition(self):
                 
        # Если нужно просто узнать id строк
        if "lookId" in self.searchMode: data,message = self._getDataConditionLookId()          
                        
        # Если идет выборка по нескольким критериям поиска
        elif "extend" in self.searchMode: data, message = self._getDataConditionExtend()
        
        # Если идет выборка по одному критерию поиска и отображаются все столбцы таблицы
        elif self.checkMode == "all":
            data,message = self.myDb.Get_values_condition(self.curTable, self.searchField, self.searchItem, equal = self.equalItem)
        
        # Если идет выборка по одному критерию поиска и отображаются выборочные столбцы
        else:
            data,message = self.myDb.Get_values_condition(self.curTable, self.searchField, self.searchItem, table_fields = self.showList, equal = self.equalItem, mode = self.checkMode, print_logs = False)
            
        # Если добавляется строка
        if "append" in self.searchMode: self._append()
            
         # Если удаляется строка
        if "delete" in self.searchMode: data,message = self._delete(data)
    
        return data,message
    
    # Если нужно просто узнать id строк
    def _getDataConditionLookId(self):
        # Если идет выборка по нескольким критериям поиска
        if "extend" in self.searchMode:
            searchFields = (cBox.currentText() for cBox in self.ui.searchWindow.allSearchFieldComboBoxes)
            equalFields = (cBox.currentText() for cBox in self.ui.searchWindow.allEqualComboBoxes)
            searchItems = (cBox.currentText() for cBox in self.ui.searchWindow.allSearchItemComboBoxes)
            expressions = (cBox.currentText() for cBox in self.ui.searchWindow.allExpressionComboBoxes)
            for optionId in ["ID", "Id", "id"]:
                data, message = self.myDb.Get_values_condition_extend(self.curTable, searchFields, equalFields, searchItems, expressions, print_logs = False)
                if len(data) != 0: break
                    
        # Если идет выборка по одному критерию поиска
        else:
            for optionId in ["ID", "Id", "id"]:
                data,message = self.myDb.Get_values_condition(self.curTable, self.searchField, self.searchItem, table_fields = [optionId], equal = self.equalItem, mode = self.checkMode, print_logs = False)
                if len(data) != 0: break
                    
        return data,message
    
    # Если идет выборка по нескольким критериям поиска
    def _getDataConditionExtend(self):
        searchFields = (cBox.currentText() for cBox in self.ui.searchWindow.allSearchFieldComboBoxes)
        equalFields = (cBox.currentText() for cBox in self.ui.searchWindow.allEqualComboBoxes)
        searchItems = (cBox.currentText() for cBox in self.ui.searchWindow.allSearchItemComboBoxes)
        expressions = (cBox.currentText() for cBox in self.ui.searchWindow.allExpressionComboBoxes)
        
        # Если отображаются все столбцы таблицы   
        if self.checkMode == "all":
            data, message = self.myDb.Get_values_condition_extend(self.curTable, searchFields, equalFields, searchItems, expressions, print_logs = False)
            
        # Если отображаются выборочные столбцы
        else:
            data,message = self.myDb.Get_values_condition_extend(self.curTable, searchFields, equalFields, searchItems, expressions, table_fields = self.showList, mode = "pick", print_logs = False)
        return data,message
        
    # Удаляет строку из буффера или таблицы
    def _delete(self, data):
        data,message = [d for d in data if d[0] not in self.delBufferId] if len(data) != 0 else [], self.myDb.messageNothing
        copyAppendBuffer = self.appendBuffer.copy()
        for i, buf in enumerate(copyAppendBuffer):
            item = int(buf[self.curColumns[1]])
            if item in self.delBufferId:
                self.delBufferId.remove(item)
                self.appendBuffer.pop(i)
        
        return data,message
            
    # Добавляет строку в буффер    
    def _append(self):
        self.appendBuffer.append({self.curColumns[1]:str(self._findAppendId())})
        self.appendBuffer[-1].update({name: self._pasteAppendValue(name) for name in self.curColumns[2:]})
    
    # Определяет какой id должен стоять у добавляемой строки
    def _findAppendId(self):
        oldMode = self.searchMode
        self.searchMode = "simple_lookId"
        _id = 1
        data,_ = self.GetData()
        ids = [int(value[0]) for value in data if value[0] not in self.delBufferId]
        if len(self.appendBuffer) != 0:
            ids.extend([int(buf[self.curColumns[1]]) for buf in self.appendBuffer])
        
        while _id in ids:
            _id += 1
        self.searchMode = oldMode
        return _id
    
    # Возвращает значение по-умолчанию в добавляемой строке
    def _pasteAppendValue(self, field):
        if self.myDb.notNulls[self.curTable][field] == 0: return '(Null)'
        if self.myDb.dataTypes[self.curTable][field] == "integer": return '0'
        elif self.myDb.dataTypes[self.curTable][field] == "real": return '0.0'
        elif self.myDb.dataTypes[self.curTable][field] == "date": return '00.00.0000'
        else: return '-'

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())