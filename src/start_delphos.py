import os
import sys
import logging
from core.project_manager import *
from core.project import *
from sqlalchemy import *

if __name__ == '__main__':

	def main_menu(cur_menu):
		#cls()
		print "\nDelphos Menu\n\n1. Create new project\n2. Open project"
		if project_manager.get_current_project():
			print "(B)ack to project menu"
		print "(Q)uit"
		menu_opt = raw_input('\nEnter Option: ')
		
		if menu_opt == '1':
			proj_name = None
			while not project_manager.validate_project_name(proj_name):
				proj_name = raw_input('\nChoose a project name:')
				
			proj_path = None
			proj_path = raw_input('\nChoose a project directory ['+project_manager.get_default_project_path()+']:')	
			if proj_path: #if non-empty validate it
				while not proj_path or not project_manager.validate_project_path(proj_path):
					proj_path = raw_input('\nChoose a project directory ['+project_manager.get_default_project_path()+']:')
			
			default_crit_answer = raw_input('\nLoad default criteria? [Y]:')
			load_default_crit = True
			if default_crit_answer == 'N' or default_crit_answer == 'n':
				load_default_crit = False
	
			isLoaded = project_manager.create_project(proj_name, proj_path, load_default_crit)
			if isLoaded:
				cur_menu[0] = 'project'

		elif menu_opt == '2':
			proj_path = None
			proj_name = None
			
			proj_path = raw_input('\nChoose a project directory ['+project_manager.get_default_project_path()+']:')
			proj_name = raw_input('\nProject Name: ')

			isLoaded = project_manager.open_project(proj_name, proj_path)
			if isLoaded:
				cur_menu[0] = 'project'

		elif menu_opt == 'b' or menu_opt == 'B':
			cur_menu[0] = 'project'
			
		elif menu_opt == 'q' or menu_opt == 'Q':
			sys.exit()
			
	def project_menu(cur_menu):
		#cls()
		print "\nProject Menu\ncurrent project: "+project_manager.get_current_project_name()+"\n\n1. List criteria\n2. Add criteria\n3. Remove criteria\n4. List Alternatives\n5. Add Alternative\n6. Remove Alternative\n(B)ack to main menu\n(Q)uit"
		menu_opt = raw_input('\nEnter Option :')
		
		if menu_opt == '1':
			cur_proj = project_manager.get_current_project()
			if cur_proj:
				crit_str = cur_proj.get_criteria_as_string()		
				cls()
				print crit_str
			else :
				print "Project not loaded!"
		
		elif menu_opt == '2':
			desc = raw_input('\nCriteria description: ')
			type = raw_input('Criteria type [1:bliff, 2:blam, 3:blort]: ')
			cb = raw_input('(C)ost or (B)enefit [C]: ')
			#TODO - verify result
			isAdded = project_manager.get_current_project().add_criteria(desc, type, cb)
		
		elif menu_opt == '3':
			id = raw_input('\nCriteria ID: ')
			#TODO - verify result
			isRemoved = project_manager.get_current_project().remove_criteria(id)

		if menu_opt == '4':
			cur_proj = project_manager.get_current_project()
			if cur_proj:
				altern_str = cur_proj.get_alternatives_as_string()		
				cls()
				print altern_str
			else :
				print "Project not loaded!"
		
		elif menu_opt == '5':
			name = raw_input('\nAlternative name: ')
			#TODO - verify result
			isAdded = project_manager.get_current_project().add_alternative(name)
		
		elif menu_opt == '6':
			id = raw_input('\nAlternative ID:')
			#TODO - verify result
			success = project_manager.get_current_project().remove_alternative(id)
		
		elif menu_opt == 'B' or menu_opt == 'b':
			cur_menu[0] = 'main'
		
		if menu_opt == 'q' or menu_opt == 'Q':
			sys.exit()

	def cls():
		"""Clear screen.
		"""
		for i in range(40):
			print ""

	project_manager = ProjectManager()

	cur_menu = ['main']
	while True:
		#if not project_manager.get_current_project():
		if cur_menu[0] == 'main':
			main_menu(cur_menu)
		elif cur_menu[0] == 'project':
			project_menu(cur_menu)