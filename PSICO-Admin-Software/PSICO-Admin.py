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
        self.tab2UI()
        self.tab3UI()
        
        self.setWindowTitle("PSICO Admin-Software")
        self.setWindowIcon(QIcon('./PSICO_Logo.svg'))
        self.resize(600, 450)

    # this is the view definition of the first tab
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

    # this is the view definition of the second tab
    def tab2UI(self):
        self.tab2.totalsView = QTreeView()
        self.tab2.totalsView.setRootIsDecorated(False)
        
        layout = QGridLayout()
        layout.addWidget(self.tab2.totalsView, 0, 0, 0, 0)
        self.tab2.setLayout(layout)

    # this is the view definition of the third tab
    def tab3UI(self):
        self.tab3.heatmapView = QTreeView()
        self.tab3.heatmapView.setRootIsDecorated(False)
        
        layout = QGridLayout()
        layout.addWidget(self.tab3.heatmapView, 0, 0, 0, 0)
        self.tab3.setLayout(layout)

    # the model is beeing connected to the tree views
    def setModels(self, model):
        self.tab1.citizenListModel.setSourceModel(model)
        self.tab2.totalsView.setModel(model)
        self.tab3.heatmapView.setModel(model)

    # reaction on userchanges on the filter pattern 
    def filterPatternChanged(self):
        pattern = self.tab1.filterPatternLineEdit.text()
        reg_exp = QRegularExpression(pattern)
        if not self.tab1.filterCaseSensitivityCheckBox.isChecked():
            options = reg_exp.patternOptions()
            options |= QRegularExpression.CaseInsensitiveOption
            reg_exp.setPatternOptions(options)
        self.tab1.citizenListModel.setFilterRegularExpression(reg_exp)

    # reaction on userchanges on the filter column combo box
    def filterColumnChanged(self):
        self.tab1.citizenListModel.setFilterKeyColumn(self.tab1.filterColumnComboBox.currentIndex())

    # reaction on userchanges on the sort case sensitivity check box
    def sortCaseSensitivityChanged(self):
        if self.tab1.sortCaseSensitivityCheckBox.isChecked():
            caseSensitivity = Qt.CaseSensitive
        else:
            caseSensitivity = Qt.CaseInsensitive
        self.tab1.citizenListModel.setSortCaseSensitivity(caseSensitivity)
    

def addEntry(citizenModel, id, anzahlVerstöße, lieblingsTaste, durchschnTastenanschläge, letzteAktualisierung):
    citizenModel.insertRow(0)
    citizenModel.setData(citizenModel.index(0, 0), id)
    citizenModel.setData(citizenModel.index(0, 1), anzahlVerstöße)
    citizenModel.setData(citizenModel.index(0, 2), lieblingsTaste)
    citizenModel.setData(citizenModel.index(0, 3), durchschnTastenanschläge)
    citizenModel.setData(citizenModel.index(0, 4), letzteAktualisierung)


def createCitizenModel(parent):
    citizenModel = QStandardItemModel(0, 5, parent)

    citizenModel.setHeaderData(0, Qt.Horizontal, "ID")
    citizenModel.setHeaderData(1, Qt.Horizontal, "Anzahl Verstöße")
    citizenModel.setHeaderData(2, Qt.Horizontal, "Lieblingstaste")
    citizenModel.setHeaderData(3, Qt.Horizontal, "Durchschn. Tastenanschläge/min")
    citizenModel.setHeaderData(4, Qt.Horizontal, "letzte Aktualisierung")

    addEntry(citizenModel, "Bürger1", 23, "I", 89, QDateTime(QDate(2006, 12, 31), QTime(17, 3)))
    addEntry(citizenModel, "Bürger2", 53, "D", 78, QDateTime(QDate(2006, 10, 22), QTime(9, 44)))
    addEntry(citizenModel, "Bürger3", 75, "C", 78, QDateTime(QDate(2006, 8, 31), QTime(12, 50)))
    addEntry(citizenModel, "Bürger4", 34, "B", 88, QDateTime(QDate(2006, 11, 25), QTime(11, 39)))
    addEntry(citizenModel, "Bürger5", 27, "A", 67, QDateTime(QDate(2007, 6, 2), QTime(16, 5)))
    addEntry(citizenModel, "Bürger6", 35, "E", 56, QDateTime(QDate(2007, 1, 4), QTime(14, 18)))
    addEntry(citizenModel, "Bürger7", 24, "G", 62, QDateTime(QDate(2007, 3, 3), QTime(14, 26)))
    addEntry(citizenModel, "Bürger8", 63, "F", 67, QDateTime(QDate(2007, 1, 2), QTime(11, 33)))
    addEntry(citizenModel, "Bürger9", 45, "H", 93, QDateTime(QDate(2007, 5, 5), QTime(12, 0)))

    return citizenModel  


if __name__ == '__main__':
    app = QApplication()
    window = Window()
    window.setModels(createCitizenModel(window))
    window.show()
    sys.exit(app.exec())