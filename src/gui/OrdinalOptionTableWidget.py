import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from delphos_exceptions import *

class OrdinalOptionTableWidget(QTableWidget):
    def __init__(self, parent=None):
        QTextBrowser.__init__(self, parent)
        self.resizeRowsToContents()
        self.selected_row = None     #The currently selected row as a list of items

    def load(self, option_recs):
        self.setRowCount(len(option_recs))        
        description_col = 0
        value_col = 1

        for i in range(len(option_recs)):
            description_item = QTableWidgetItem()
            description_item.setText(str(option_recs[i][description_col]))
            self.setItem(i, description_col, description_item)

            value_item = QTableWidgetItem()
            value_item.setText(str(option_recs[i][value_col]))
            self.setItem(i, value_col, value_item)

        self.resizeColumnsToContents()      

    def get_current_row(self):
        selected_row = self.selectedItems()
        if selected_row:
            return selected_row[0].row()
        else:
            raise DelphosError, "You must first select an option"