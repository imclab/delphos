#===============================================================================
# Delphos - a decision-making tool for community-based marine conservation.
# 
# @copyright    2007 Ecotrust
# @author        Tim Welch
# @contact        twelch at ecotrust dot org
# @license        GNU GPL 2 
# 
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.  The full license for this distribution
# has been made available in the file LICENSE.txt
#
# $Id$
#
# @summary - 
#===============================================================================

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from main_window_ui import Ui_MainWindow
from core.data.toc_data import *
from copy import deepcopy

import os
import urllib

class DelphosWindow(QMainWindow):
    """Manages the main Delphos window interface (Ui_MainWindow)
    """
    def __init__(self, gui_manager):
        QMainWindow.__init__(self, None)    #Initialize myself as a widget
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)    #Create the components of the window
        
        self.gui_manager = gui_manager
        
        self.dock_full_screen = False
        self.min_doc_dock_width = 200
        
        #Maximize the display to full size
        #self.showMaximized()

        #Add status bar at bottom of window
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        
        #Add progress bar to status bar
        self.pb = QProgressBar(self.statusBar())
        self.pb.setMinimum(0)
        self.pb.setMaximum(0)
        self.statusbar.addPermanentWidget(self.pb)        
        self.pb.hide()
        
        QObject.connect(self.ui.menu_dock_visible, SIGNAL("triggered()"), self.toggle_documentation_window)
        QObject.connect(self.ui.dock_doc, SIGNAL("visibilityChanged(bool)"), self.toggle_dock_visible_menu)

        QObject.connect(self.ui.menu_dock_floating, SIGNAL("triggered()"), self.toggle_dock_float)
        QObject.connect(self.ui.dock_doc, SIGNAL("topLevelChanged(bool)"), self.toggle_dock_floating_menu)

        QObject.connect(self.ui.menu_open_full_doc, SIGNAL("triggered()"), self.load_full_doc)

        #self.ui.dock_doc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def load_full_doc(self, project_type=None, language=None):
        """Load full documentation in external application
        """
        #Find which documentation subdir to look in
        if not project_type:
            project_type = self.gui_manager.project_manager.get_current_project_type()
        if not language:
            language = self.gui_manager.config_manager.get_language()
            
        if project_type == 'fisheries':
            if language == 'english':
                doc_subdir = 'fisheries'+os.sep+'english'+os.sep
            else:
                doc_subdir = 'fisheries'+os.sep+'spanish'+os.sep
        elif project_type == 'sites':
            if language == 'english':
                doc_subdir = 'sites'+os.sep+'english'+os.sep
            else:
                doc_subdir = 'sites'+os.sep+'spanish'+os.sep
        elif project_type == 'communities':
            if language == 'english':
                doc_subdir = 'communities'+os.sep+'english'+os.sep
            else:
                doc_subdir = 'communities'+os.sep+'spanish'+os.sep                
        
        doc_path = os.getcwd()+os.sep+"documentation"+os.sep+doc_subdir+'documentation.html'
        doc_url = "file:"+urllib.pathname2url(unicode(doc_path))

        #file:///U|/dev/delphos/src/documentation/fisheries/english/letter_to_experts.doc
        self.gui_manager.desktop_services.openUrl(QUrl(doc_url))
                                      
    def load_toc(self, project_type=None, language=None):
        """Loads the table of contents within the dock widget
        """
        #Find which toc data to load
        if not project_type:
            project_type = self.gui_manager.project_manager.get_current_project_type()
        if not language:
            language = self.gui_manager.config_manager.get_language()
        
        toc = ""
        if project_type == 'fisheries':
            if language == 'english':
                toc = fisheries_english_toc
            else:
                toc = fisheries_spanish_toc
        elif project_type == 'communities':
            if language == 'english':
                toc = communities_english_toc
            else:
                toc = communities_spanish_toc
        elif project_type == 'sites':        
            if language == 'english':
                toc = sites_english_toc
            else:
                toc = sites_spanish_toc        	        
        self.process_toc(deepcopy(toc))
    
    def process_toc(self, toc):
        self.ui.toc_tree.clear()
        #Make a copy as original will be destroyed
        for heading in toc:
            root_item = self.ui.toc_tree.invisibleRootItem()
            self.process_heading(heading, root_item)
    
    def process_heading(self, heading, parent):
        #print type(heading)
        if type(heading) == str:
            tree_item = QTreeWidgetItem(parent)
            tree_item.setText(0, heading)
        if type(heading) == dict:
            (heading_name, subheadings) = heading.popitem()
            tree_item = QTreeWidgetItem(parent)
            tree_item.setText(0, heading_name)
            for subheading in subheadings:
                self.process_heading(subheading, tree_item)                               

    def process_toc_click(self, item, column):
        """Builds URL from toc heading name and reloads doc editor
        """
        heading = item.text(column)
        #Morph heading name into anchor label name
        label = heading.replace(' ', '_')
        label = heading.replace('/', '_')
        label = heading.replace('.', '')
        label = label.toLower()
        
        #Build URL
        project_type = self.gui_manager.project_manager.get_current_project_type()
        language = self.gui_manager.config_manager.get_language()
        #Load URL and go to anchor within it
        self.ui.doc_browser.load_anchor(label, project_type, language)

    def process_help_click(self, en_name, sp_name):
        """Uses the help type given to load a section of the documentation
        """
        en_label = en_name.replace('help_', '')
        sp_label = sp_name.replace('help_', '')
            
        #Build URL
        project_type = self.gui_manager.project_manager.get_current_project_type()
        language = self.gui_manager.config_manager.get_language()
        #Load URL and go to anchor within it
        if language == 'english':
            self.ui.doc_browser.load_anchor(en_label, project_type, language)
        elif language == 'spanish':
            self.ui.doc_browser.load_anchor(sp_label, project_type, language)
            
        #Show the documentation if its hidden        
        if not self.ui.dock_doc.isVisible():
            self.ui.menu_dock_visible.trigger()
            

    def dock_full_screen(self):
        return self.dock_full_screen

    def toggle_dock(self):
         if self.dock_full_screen:
             
             self.ui.dock_doc.setMinimumSize(self.min_doc_dock_width, 0)
             self.ui.dock_doc.resize(self.min_doc_dock_width, self.ui.dock_doc.height())

             doc_dock_size = self.ui.dock_doc.sizeHint()

             self.ui.toc_box.resize(100, self.ui.toc_box.height())
             self.ui.toc_tree.resize(100, self.ui.toc_box.height())
             self.ui.doc_box.resize(100, self.ui.doc_box.height())
             self.ui.doc_browser.resize(100, self.ui.toc_box.height())
             self.dock_full_screen = False
         else:
             self.ui.dock_doc.setMinimumSize(self.width(), 0)
             self.dock_full_screen = True

    def toggle_documentation_window(self):
        if self.ui.dock_doc.isVisible():
            self.ui.dock_doc.hide()
        else:            
            self.ui.dock_doc.show()

    def toggle_dock_visible_menu(self):
        if self.ui.dock_doc.isVisible():
            self.ui.menu_dock_visible.setChecked(True)
        else:            
            self.ui.menu_dock_visible.setChecked(False)

    def toggle_dock_float(self):
        if self.ui.dock_doc.isFloating():
            self.ui.dock_doc.setFloating(False)
        else:            
            self.ui.dock_doc.setFloating(True)

    def toggle_dock_floating_menu(self, isFloating):
        if isFloating:
            self.ui.menu_dock_floating.setChecked(False)
        else:            
            self.ui.menu_dock_floating.setChecked(True)
