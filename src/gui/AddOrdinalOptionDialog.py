import os
import re
from os import path

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from add_ordinal_option_ui import Ui_AddOrdinalOptionDialog

class AddOrdinalOptionDialog(QDialog, Ui_AddOrdinalOptionDialog):
	"""Manages the add alternative dialog
	"""
	def __init__(self, gui_manager, parent):
		QDialog.__init__(self, parent)
		self.setupUi(self)
		self.parent = parent
		self.gui_manager = gui_manager
		self.isError = False	#Error flag for form processing
		self.errorMsg = ""
		
		QObject.connect(self.add_ordinal_option_box,QtCore.SIGNAL("accepted()"), self.process_accept)
		
	def process_accept(self):
		"""Processes clicking of OK button in dialog
		"""
		self.errorMsg = ""
		option_info = None
		
		option_description = self.option_description_edit.text()
		if not option_description:
			self.isError = True
			self.errorMsg += "* Please enter an option description.\n"
		
		option_value = self.option_value_edit.text()
		if not option_value:
			self.isError = True
			self.errorMsg += "* Please enter an option value.\n"
		else:
			try:
				option_value = int(option_value)
			except:
				self.isError = True
				self.errorMsg += "* Option value is not an integer"

		if self.isError:
			self.isError = False
			QMessageBox.critical(self,"Error adding ordinal criteria option",self.errorMsg)
		else:
			option_info = (str(option_description), option_value)
			self.emit(SIGNAL("ordinal_option_info_collected"), option_info)
			self.deleteLater()