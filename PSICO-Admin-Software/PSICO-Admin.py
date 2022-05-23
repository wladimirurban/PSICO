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
        self.resize(900, 450)

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
        self.tab1.filterColumnComboBox.addItem("Name")
        self.tab1.filterColumnComboBox.addItem("Anzahl Verstöße")
        self.tab1.filterColumnComboBox.addItem("Eingegebene Buchstaben")
        self.tab1.filterColumnComboBox.addItem("Tastenanschläge / min")
        self.tab1.filterColumnComboBox.addItem("Klicks / min")
        self.tab1.filterColumnComboBox.addItem("Social-Credit-Punkte")
        self.tab1.filterColumnComboBox.addItem("letzte Aktualisierung")
        self.tab1.filterColumnLabel = QLabel("Filter-Spalte:")
        self.tab1.filterColumnLabel.setBuddy(self.tab1.filterColumnComboBox)

        self.tab1.filterPatternLineEdit.textChanged.connect(self.filterPatternChanged)
        self.tab1.filterColumnComboBox.currentIndexChanged.connect(self.filterColumnChanged)
        self.tab1.filterCaseSensitivityCheckBox.toggled.connect(self.filterPatternChanged)
        self.tab1.sortCaseSensitivityCheckBox.toggled.connect(self.sortCaseSensitivityChanged)

        self.tab1.citizenListView.sortByColumn(0, Qt.AscendingOrder)
        self.tab1.filterColumnComboBox.setCurrentIndex(1)
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
    

def addEntry(citizenModel, id, name, anzahlVerstöße, eingegebeneBuchstaben, tastenanschlägeProMin, klicksProMin, socialCredit, letzteAktualisierung):
    citizenModel.insertRow(0)
    citizenModel.setData(citizenModel.index(0, 0), id)
    citizenModel.setData(citizenModel.index(0, 1), name)
    citizenModel.setData(citizenModel.index(0, 2), anzahlVerstöße)
    citizenModel.setData(citizenModel.index(0, 3), eingegebeneBuchstaben)
    citizenModel.setData(citizenModel.index(0, 4), tastenanschlägeProMin)
    citizenModel.setData(citizenModel.index(0, 5), klicksProMin)
    citizenModel.setData(citizenModel.index(0, 6), socialCredit)
    citizenModel.setData(citizenModel.index(0, 7), letzteAktualisierung)


def createCitizenModel(parent):
    citizenModel = QStandardItemModel(0, 8, parent)

    citizenModel.setHeaderData(0, Qt.Horizontal, "ID")
    citizenModel.setHeaderData(1, Qt.Horizontal, "Name")
    citizenModel.setHeaderData(2, Qt.Horizontal, "Anzahl Verstöße")
    citizenModel.setHeaderData(3, Qt.Horizontal, "Eingegebene Buchstaben")
    citizenModel.setHeaderData(4, Qt.Horizontal, "Tastenanschläge / min")
    citizenModel.setHeaderData(5, Qt.Horizontal, "Klicks / min")
    citizenModel.setHeaderData(6, Qt.Horizontal, "Social-Credit-Punkte")
    citizenModel.setHeaderData(7, Qt.Horizontal, "letzte Aktualisierung")

    addEntry(citizenModel, 1, "Bürger9", 23, ''.join(["I","v","E","J","Z"]), 89, 67, 193, QDateTime(QDate(2020, 12, 31), QTime(17, 3)))
    addEntry(citizenModel, 2, "bürger8", 53, ''.join(["D","z","d","e","L"]), 88, 78, 256, QDateTime(QDate(2021, 10, 22), QTime(9, 44)))
    addEntry(citizenModel, 3, "Bürger7", 75, ''.join(["C","f","f","U","ä"]), 78, 56, 178, QDateTime(QDate(2022, 8, 31), QTime(12, 50)))
    addEntry(citizenModel, 4, "Bürger6", 34, ''.join(["B","Ü","k","T","H"]), 88, 67, 256, QDateTime(QDate(2019, 11, 25), QTime(11, 39)))
    addEntry(citizenModel, 5, "bürger5", 27, ''.join(["A","i","G","r","ö"]), 67, 88, 156, QDateTime(QDate(2020, 6, 2), QTime(16, 5)))
    addEntry(citizenModel, 6, "Bürger4", 35, ''.join(["E","P","U","z","p"]), 56, 56, 189, QDateTime(QDate(2020, 1, 4), QTime(14, 18)))
    addEntry(citizenModel, 7, "Bürger3", 24, ''.join(["G","h","K","t","Ö"]), 62, 78, 262, QDateTime(QDate(2019, 3, 3), QTime(14, 26)))
    addEntry(citizenModel, 8, "bürger2", 63, ''.join(["f","U","o","Ü","t"]), 67, 89, 178, QDateTime(QDate(2021, 1, 2), QTime(11, 33)))
    addEntry(citizenModel, 9, "Bürger1", 45, ''.join(["H","k","F","p","A"]), 93, 56, 189, QDateTime(QDate(2022, 5, 5), QTime(12, 0)))
    addEntry(citizenModel, 10, "bürger15", 27, ''.join(["A","i","G","r","ö"]), 67, 88, 156, QDateTime(QDate(2020, 6, 2), QTime(16, 5)))
    addEntry(citizenModel, 11, "Bürger91", 23, ''.join(["I","v","E","J","Z"]), 89, 67, 193, QDateTime(QDate(2020, 12, 31), QTime(17, 3)))
    addEntry(citizenModel, 12, "Bürger81", 53, ''.join(["D","z","d","e","L"]), 88, 78, 256, QDateTime(QDate(2021, 10, 22), QTime(9, 44)))
    addEntry(citizenModel, 13, "bürger71", 75, ''.join(["C","f","f","U","ä"]), 78, 56, 178, QDateTime(QDate(2022, 8, 31), QTime(12, 50)))
    addEntry(citizenModel, 14, "Bürger61", 34, ''.join(["b","Ü","k","T","H"]), 88, 67, 256, QDateTime(QDate(2019, 11, 25), QTime(11, 39)))
    addEntry(citizenModel, 15, "Bürger51", 27, ''.join(["A","i","G","r","ö"]), 67, 88, 156, QDateTime(QDate(2020, 6, 2), QTime(16, 5)))
    addEntry(citizenModel, 16, "Bürger41", 35, ''.join(["E","P","U","z","p"]), 56, 56, 189, QDateTime(QDate(2020, 1, 4), QTime(14, 18)))
    addEntry(citizenModel, 17, "bürger31", 24, ''.join(["g","h","K","t","Ö"]), 62, 78, 262, QDateTime(QDate(2019, 3, 3), QTime(14, 26)))
    addEntry(citizenModel, 18, "Bürger21", 63, ''.join(["F","U","o","Ü","t"]), 67, 89, 178, QDateTime(QDate(2021, 1, 2), QTime(11, 33)))
    addEntry(citizenModel, 19, "Bürger11", 45, ''.join(["H","k","F","p","A"]), 93, 56, 189, QDateTime(QDate(2022, 5, 5), QTime(12, 0)))

    return citizenModel  


if __name__ == '__main__':
    app = QApplication()
    window = Window()
    window.setModels(createCitizenModel(window))
    window.show()
    sys.exit(app.exec())