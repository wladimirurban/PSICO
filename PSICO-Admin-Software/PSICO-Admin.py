from ctypes.wintypes import RGB
import sys
from PySide6.QtCore import QDate, QDateTime, QRegularExpression, QSortFilterProxyModel, QTime, Qt
from PySide6.QtGui import QStandardItemModel, QIcon
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout, QLabel,
                                     QLineEdit, QTreeView, QWidget, QTabWidget, QAbstractItemView)

class Window(QTabWidget):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.addTab(self.tab1,"Bürgeranalyse")
        self.addTab(self.tab2,"Gesamtanalyse")
        self.addTab(self.tab3,"Heatmaps")

        self.tab1UI()
        #self.tab2UI()
        #self.tab3UI()
        
        self.setWindowTitle("PSICO Admin-Software")
        self.setWindowIcon(QIcon('./PSICO_Logo.svg'))
        self.resize(600, 450)

    def tab1UI(self):
        self.tab1.citizenListModel = QSortFilterProxyModel()
        self.tab1.citizenListModel.setDynamicSortFilter(True)

        self.tab1.citizenListView = QTreeView()
        self.tab1.citizenListView.setRootIsDecorated(False)
        self.tab1.citizenListView.setAlternatingRowColors(True)
        self.tab1.citizenListView.setModel(self.tab1.citizenListModel)
        self.tab1.citizenListView.setSortingEnabled(True)
        self.tab1.citizenListView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tab1.sortCaseSensitivityCheckBox = QCheckBox("Case-sensitive Sortierung")
        self.tab1.filterCaseSensitivityCheckBox = QCheckBox("Case-sensitiver Filter")

        self.tab1.filterPatternLineEdit = QLineEdit()
        self.tab1.filterPatternLineEdit.setClearButtonEnabled(True)
        self.tab1.filterPatternLabel = QLabel("Filter (RegEx):")
        self.tab1.filterPatternLabel.setBuddy(self.tab1.filterPatternLineEdit)

        self.tab1.filterColumnComboBox = QComboBox()
        self.tab1.filterColumnComboBox.addItem("ID")
        self.tab1.filterColumnComboBox.addItem("Anzahl Verstöße")
        self.tab1.filterColumnComboBox.addItem("Lieblings Taste")
        self.tab1.filterColumnComboBox.addItem("Durchschn. Tastenanschläge/min")
        self.tab1.filterColumnComboBox.addItem("letzte Aktualisierung")
        self.tab1.filterColumnLabel = QLabel("Filter-Spalte:")
        self.tab1.filterColumnLabel.setBuddy(self.tab1.filterColumnComboBox)

        self.tab1.filterPatternLineEdit.textChanged.connect(self.filterPatternChanged)
        self.tab1.filterColumnComboBox.currentIndexChanged.connect(self.filterColumnChanged)
        self.tab1.filterCaseSensitivityCheckBox.toggled.connect(self.filterPatternChanged)
        self.tab1.sortCaseSensitivityCheckBox.toggled.connect(self.sortCaseSensitivityChanged)

        self.tab1.citizenListView.sortByColumn(0, Qt.AscendingOrder)
        self.tab1.filterColumnComboBox.setCurrentIndex(0)
        self.tab1.filterPatternLineEdit.setText("Bürger[345]")
        self.tab1.filterCaseSensitivityCheckBox.setChecked(True)
        self.tab1.sortCaseSensitivityCheckBox.setChecked(True)

        layout = QGridLayout()
        layout.addWidget(self.tab1.citizenListView, 0, 0, 1, 3)
        layout.addWidget(self.tab1.filterPatternLabel, 1, 0)
        layout.addWidget(self.tab1.filterPatternLineEdit, 1, 1, 1, 2)
        layout.addWidget(self.tab1.filterColumnLabel, 2, 0)
        layout.addWidget(self.tab1.filterColumnComboBox, 2, 1, 1, 2)
        layout.addWidget(self.tab1.filterCaseSensitivityCheckBox, 3, 0, 1, 2)
        layout.addWidget(self.tab1.sortCaseSensitivityCheckBox, 3, 1)
        self.tab1.setLayout(layout)

    #def tab2UI(self):

    #def tab3UI(self):

    def setCitizenSourceModel(self, model):
        self.tab1.citizenListModel.setSourceModel(model)

    def filterPatternChanged(self):
        pattern = self.tab1.filterPatternLineEdit.text()
        reg_exp = QRegularExpression(pattern)
        if not self.tab1.filterCaseSensitivityCheckBox.isChecked():
            options = reg_exp.patternOptions()
            options |= QRegularExpression.CaseInsensitiveOption
            reg_exp.setPatternOptions(options)
        self.tab1.citizenListModel.setFilterRegularExpression(reg_exp)

    def filterColumnChanged(self):
        self.tab1.citizenListModel.setFilterKeyColumn(self.tab1.filterColumnComboBox.currentIndex())

    def sortCaseSensitivityChanged(self):
        if self.tab1.sortCaseSensitivityCheckBox.isChecked():
            caseSensitivity = Qt.CaseSensitive
        else:
            caseSensitivity = Qt.CaseInsensitive

        self.tab1.citizenListModel.setSortCaseSensitivity(caseSensitivity)


def updateTotals(anzahlVerstöße, lieblingsTaste, durchschnTastenanschläge):
    global counter
    global totalViolations
    global sumAvgKeystrokes
    global avgKeystrokes
    
    counter += 1
    totalViolations += anzahlVerstöße
    favoriteKey.append(lieblingsTaste)
    sumAvgKeystrokes += durchschnTastenanschläge
    avgKeystrokes = sumAvgKeystrokes/counter
    

def addEntry(model, id, anzahlVerstöße, lieblingsTaste, durchschnTastenanschläge, letzteAktualisierung):
    model.insertRow(0)
    model.setData(model.index(0, 0), id)
    model.setData(model.index(0, 1), anzahlVerstöße)
    model.setData(model.index(0, 2), lieblingsTaste)
    model.setData(model.index(0, 3), durchschnTastenanschläge)
    model.setData(model.index(0, 4), letzteAktualisierung)
    updateTotals(anzahlVerstöße, lieblingsTaste, durchschnTastenanschläge)


def createEntriesModel(parent):
    model = QStandardItemModel(0, 5, parent)

    model.setHeaderData(0, Qt.Horizontal, "ID")
    model.setHeaderData(1, Qt.Horizontal, "Anzahl Verstöße")
    model.setHeaderData(2, Qt.Horizontal, "Lieblings-Taste")
    model.setHeaderData(3, Qt.Horizontal, "Durchschn. Tastenanschläge/min")
    model.setHeaderData(4, Qt.Horizontal, "letzte Aktualisierung")

    addEntry(model, "Bürger1", 23, "I", 89, QDateTime(QDate(2006, 12, 31), QTime(17, 3)))
    addEntry(model, "Bürger2", 53, "D", 78, QDateTime(QDate(2006, 10, 22), QTime(9, 44)))
    addEntry(model, "Bürger3", 75, "C", 78, QDateTime(QDate(2006, 8, 31), QTime(12, 50)))
    addEntry(model, "Bürger4", 34, "B", 88, QDateTime(QDate(2006, 11, 25), QTime(11, 39)))
    addEntry(model, "Bürger5", 27, "A", 67, QDateTime(QDate(2007, 6, 2), QTime(16, 5)))
    addEntry(model, "Bürger6", 35, "E", 56, QDateTime(QDate(2007, 1, 4), QTime(14, 18)))
    addEntry(model, "Bürger7", 24, "G", 62, QDateTime(QDate(2007, 3, 3), QTime(14, 26)))
    addEntry(model, "Bürger8", 63, "F", 67, QDateTime(QDate(2007, 1, 2), QTime(11, 33)))
    addEntry(model, "Bürger9", 45, "H", 93, QDateTime(QDate(2007, 5, 5), QTime(12, 0)))

    return model


if __name__ == '__main__':
    counter = 0
    totalViolations = 0
    favoriteKey = []
    sumAvgKeystrokes = 0
    avgKeystrokes = 0
    app = QApplication()
    window = Window()
    window.setCitizenSourceModel(createEntriesModel(window))
    window.show()
    sys.exit(app.exec())