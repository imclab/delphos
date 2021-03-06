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
#===============================================================================

import os
import logging
from delphos_exceptions import *
from sqlalchemy import *
from project import *

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ProjectManager(QObject):
    """Provides access to, handles and maintins delphos projects.
    """
    def __init__(self):
        QObject.__init__(self)
                
        self.current_project_name = ""
        self.current_project_path = ""
        self.current_project_type = ""
        self.current_project = None
        self.default_project_path = "db"
        self.default_file_extension = "del"

    def create_project(self, name, path, type, load_default_altern, load_default_crit, language=None):
        """Create a new delphos Project
    
        name (string) - name of the project
        path (string) - path, relative or absolute, to store project DB
        type (string) - type of project, eg. fisheries or mpa
        """
        
        #If project already open then close it first
        if self.current_project:
            self.__close_current_project()
        
        if not path:
            path = self.default_project_path

        #Check if DB already exists
        db_path = path+'/'+name

        self.current_project_type = type
        
        if os.path.exists(db_path):
            raise DelphosError, "Project named "+name+" already exists at "+path
        elif not self.current_project_type:
            raise DelphosError, "Analysis type not found"        
        
        #Create project
        proj = Project(name, path, type, load_default_altern, load_default_crit, language)
        if not proj:
            raise DelphosError, "Project creation failed"
        
        self.current_project = proj
        self.current_project_name = name
        return True

    def open_project(self, name, path):
        """Open an existing delphos Project
    
        name (string) - name of the project
        path (string) - path, relative or absolute, that DB is stored
        """        
        if self.current_project:
            self.__close_current_project()

        #Verify DB exists
        db_path = path+os.sep+name
        if not os.path.exists(db_path):
            raise DelphosError, "Project named "+name+" doesn't exist at "+path
        
        #Create Project
        proj = Project(name, path)
        if not proj:
            raise DelphosError, "Project open failed"
        
        #Check if project type changed
        project_type = proj.get_project_type()
 
        if not project_type:
            raise DelphosError, "Project type not found"
        elif project_type != self.current_project_type:
            #print "type changed to "+project_type+", notify!"
            self.current_project_type = project_type
            #@todo - Notify to reload the documentation
            #self.emit(SIGNAL("project_type_changed"), project_type)
       
        self.current_project = proj
        self.current_project_name = name
        print "signalling project change"
        self.emit(SIGNAL("project_changed"))
        return True

    def __close_current_project(self):
        """Clear everything out for opening another project
        """
        self.current_project = None
        self.current_project_name = ""
        self.current_project_path = ""
        clear_mappers()

    def get_current_project(self):
        """Returns reference to current Project object
        """
        if self.current_project:
            return self.current_project
        else:
            return False
        
    def has_project_loaded(self):
        if self.current_project:
            return True
        else:
            return False

    #Fisheries, Sites, Communities
    def set_current_project_type(self, type):
        if not type:
            return False
        else:
            self.current_project_type = type
  
    def get_current_project_type(self):
        return self.current_project_type

    def get_current_project_name(self):
        """Returns name of current project
        """
        return self.current_project_name

    def validate_project_name(self, name):
        """Verifies that a given name is suitable for use a a project name
        """
        if name:
            return True

    def get_default_project_path(self):
        """Returns the default path that projects are stored if one is not given
        """
        return self.default_project_path

    def validate_project_path(self, path):
        """Verifies that a given project path is valid
        """
        if os.path.exists(path):
            return True
        else:
            return False
    
    def get_default_file_extension(self):
        return self.default_file_extension
        
#Testing purposes
if __name__ == '__main__':
    os.chdir('..')    #Go to top-level directory
    project_manager = ProjectManager()

#    load_default_criteria = True
#    cur_proj = project_manager.create_project('project2','db', load_default_criteria)

    cur_proj = project_manager.open_project('project2','db')
    cur_proj.add_criteria('Crikey',2,'C')
    cur_proj.remove_criteria(27)
    crit_str = cur_proj.get_criteria_as_string()
    print crit_str