import sys
from PySide6.QtCore import (QDate, QDateTime, QRegularExpression,
                            QSortFilterProxyModel, QTime, Qt)
from PySide6.QtGui import QStandardItemModel, QIcon
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                               QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                               QTreeView, QVBoxLayout, QWidget, QTabWidget, QAbstractItemView)


REGULAR_EXPRESSION = 0
WILDCARD = 1
FIXED_STRING = 2


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
        self.setWindowIcon(QIcon('PSICO_Logo.svg'))
        self.resize(600, 450)

    def tab1UI(self):
        self.tab1.citizen_list_model = QSortFilterProxyModel()
        self.tab1.citizen_list_model.setDynamicSortFilter(True)

        self.tab1.citizen_list_view = QTreeView()
        self.tab1.citizen_list_view.setRootIsDecorated(False)
        self.tab1.citizen_list_view.setAlternatingRowColors(True)
        self.tab1.citizen_list_view.setModel(self.tab1.citizen_list_model)
        self.tab1.citizen_list_view.setSortingEnabled(True)
        self.tab1.citizen_list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tab1.sort_case_sensitivity_check_box = QCheckBox("Case sensitive sorting")
        self.tab1.filter_case_sensitivity_check_box = QCheckBox("Case sensitive filter")

        self.tab1.filter_pattern_line_edit = QLineEdit()
        self.tab1.filter_pattern_line_edit.setClearButtonEnabled(True)
        self.tab1.filter_pattern_label = QLabel("&Filter pattern:")
        self.tab1.filter_pattern_label.setBuddy(self.tab1.filter_pattern_line_edit)

        self.tab1.filter_syntax_combo_box = QComboBox()
        self.tab1.filter_syntax_combo_box.addItem("Regular expression", REGULAR_EXPRESSION)
        self.tab1.filter_syntax_combo_box.addItem("Wildcard", WILDCARD)
        self.tab1.filter_syntax_combo_box.addItem("Fixed string", FIXED_STRING)
        self.tab1.filter_syntax_label = QLabel("Filter &syntax:")
        self.tab1.filter_syntax_label.setBuddy(self.tab1.filter_syntax_combo_box)

        self.tab1.filter_column_combo_box = QComboBox()
        self.tab1.filter_column_combo_box.addItem("ID")
        self.tab1.filter_column_combo_box.addItem("Anzahl Verstöße")
        self.tab1.filter_column_combo_box.addItem("Lieblings Taste")
        self.tab1.filter_column_combo_box.addItem("Durchschn. Tastenanschläge/min")
        self.tab1.filter_column_combo_box.addItem("letzte Aktualisierung")
        self.tab1.filter_column_label = QLabel("Filter &column:")
        self.tab1.filter_column_label.setBuddy(self.tab1.filter_column_combo_box)

        self.tab1.filter_pattern_line_edit.textChanged.connect(self.filter_reg_exp_changed)
        self.tab1.filter_syntax_combo_box.currentIndexChanged.connect(self.filter_reg_exp_changed)
        self.tab1.filter_column_combo_box.currentIndexChanged.connect(self.filter_column_changed)
        self.tab1.filter_case_sensitivity_check_box.toggled.connect(self.filter_reg_exp_changed)
        self.tab1.sort_case_sensitivity_check_box.toggled.connect(self.sort_changed)

        proxy_layout = QGridLayout()
        proxy_layout.addWidget(self.tab1.citizen_list_view, 0, 0, 1, 3)
        proxy_layout.addWidget(self.tab1.filter_pattern_label, 1, 0)
        proxy_layout.addWidget(self.tab1.filter_pattern_line_edit, 1, 1, 1, 2)
        proxy_layout.addWidget(self.tab1.filter_syntax_label, 2, 0)
        proxy_layout.addWidget(self.tab1.filter_syntax_combo_box, 2, 1, 1, 2)
        proxy_layout.addWidget(self.tab1.filter_column_label, 3, 0)
        proxy_layout.addWidget(self.tab1.filter_column_combo_box, 3, 1, 1, 2)
        proxy_layout.addWidget(self.tab1.filter_case_sensitivity_check_box, 4, 0, 1, 2)
        proxy_layout.addWidget(self.tab1.sort_case_sensitivity_check_box, 4, 2)
        self.tab1.setLayout(proxy_layout)

        self.tab1.citizen_list_view.sortByColumn(0, Qt.AscendingOrder)
        self.tab1.filter_column_combo_box.setCurrentIndex(0)
        self.tab1.filter_pattern_line_edit.setText("nfzjf|cbzt")
        self.tab1.filter_case_sensitivity_check_box.setChecked(True)
        self.tab1.sort_case_sensitivity_check_box.setChecked(True)

    #def tab2UI(self):

    #def tab3UI(self):



    def set_source_model(self, model):
        self.tab1.citizen_list_model.setSourceModel(model)
        #self.tab1._source_view.setModel(model)

    def filter_reg_exp_changed(self):
        syntax_nr = self.tab1.filter_syntax_combo_box.currentData()
        pattern = self.tab1.filter_pattern_line_edit.text()
        if syntax_nr == WILDCARD:
            pattern = QRegularExpression.wildcardToRegularExpression(pattern)
        elif syntax_nr == FIXED_STRING:
            pattern = QRegularExpression.escape(pattern)

        reg_exp = QRegularExpression(pattern)
        if not self.tab1.filter_case_sensitivity_check_box.isChecked():
            options = reg_exp.patternOptions()
            options |= QRegularExpression.CaseInsensitiveOption
            reg_exp.setPatternOptions(options)
        self.tab1.citizen_list_model.setFilterRegularExpression(reg_exp)

    def filter_column_changed(self):
        self.tab1.citizen_list_model.setFilterKeyColumn(self.tab1.filter_column_combo_box.currentIndex())

    def sort_changed(self):
        if self.tab1.sort_case_sensitivity_check_box.isChecked():
            case_sensitivity = Qt.CaseSensitive
        else:
            case_sensitivity = Qt.CaseInsensitive

        self.tab1.citizen_list_model.setSortCaseSensitivity(case_sensitivity)


def add_entry(model, id, anzahlVerstöße, lieblingsTaste, durchschnTastenanschläge, letzteAktualisierung):
    model.insertRow(0)
    model.setData(model.index(0, 0), id)
    model.setData(model.index(0, 1), anzahlVerstöße)
    model.setData(model.index(0, 2), lieblingsTaste)
    model.setData(model.index(0, 3), durchschnTastenanschläge)
    model.setData(model.index(0, 4), letzteAktualisierung)


def create_entries_model(parent):
    model = QStandardItemModel(0, 5, parent)

    #ID, Anzahl Verstöße, Lieblings Taste, Durchschn. Tastenanschläge/min, letzte Aktualisierung
    #id, anzahlVerstöße, lieblingsTaste, durchschnTastenanschläge, letzteAktualisierung

    model.setHeaderData(0, Qt.Horizontal, "ID")
    model.setHeaderData(1, Qt.Horizontal, "Anzahl Verstöße")
    model.setHeaderData(2, Qt.Horizontal, "Lieblings Taste")
    model.setHeaderData(3, Qt.Horizontal, "Durchschn. Tastenanschläge/min")
    model.setHeaderData(4, Qt.Horizontal, "letzte Aktualisierung")

    add_entry(model, "nfzjf", 23, "A", 89, QDateTime(QDate(2006, 12, 31), QTime(17, 3)))
    add_entry(model, "fnmu", 53, "A", 78, QDateTime(QDate(2006, 12, 22), QTime(9, 44)))
    add_entry(model, "zjnff", 75, "A", 78, QDateTime(QDate(2006, 12, 31), QTime(12, 50)))
    add_entry(model, "cbzt", 34, "A", 88, QDateTime(QDate(2006, 12, 25), QTime(11, 39)))
    add_entry(model, "dtzj", 27, "A", 67, QDateTime(QDate(2007, 1, 2), QTime(16, 5)))
    add_entry(model, "ezijuh", 35, "A", 56, QDateTime(QDate(2007, 1, 4), QTime(14, 18)))
    add_entry(model, "jtedrg", 24, "A", 62, QDateTime(QDate(2007, 1, 3), QTime(14, 26)))
    add_entry(model, "srfgjk", 63, "A", 67, QDateTime(QDate(2007, 1, 5), QTime(11, 33)))
    add_entry(model, "aerhn", 45, "A", 93, QDateTime(QDate(2007, 1, 5), QTime(12, 0)))
    add_entry(model, "sfgb", 34, "A", 36, QDateTime(QDate(2007, 1, 5), QTime(12, 1)))

    return model


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.set_source_model(create_entries_model(window))
    window.show()
    sys.exit(app.exec())
