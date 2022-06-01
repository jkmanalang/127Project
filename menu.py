"""
Program: Task Record System (A.Y. 2021-2022 Second Semester - 127 Project) 

<names>

"""

import choices_code
import functions

while True:

	print ("""													
=================== Menu ====================
   [0] View Task (all)
   [1] Add/Create task
   [2] Edit Task
   [3] Delete Task
   [4] Mark task as done
   [5] Add category (i.e., academic, org-related, lovelife, money, to_watch)
   [6] Edit category
   [7] Delete category
   [8] View category
   [9] Add task to a category
   [q] Quit
================================================\n""")

	user_choice = functions.getUserAnswer()

	if user_choice == "0":
		choices_code.viewTask()

	elif user_choice == "1":
		choices_code.addCreateTask()

	elif user_choice == "2":
		choices_code.editTask()

	elif user_choice == "3":
		choices_code.deleteTask()

	elif user_choice == "4":
		choices_code.markAsDone()
 
	elif user_choice == "5":
		choices_code.addCategory()
 
	elif user_choice == "6":
		choices_code.editCategory()
 
	elif user_choice == "7":
		choices_code.deleteCategory()
 
	elif user_choice == "8":
		choices_code.viewCategory()
 
	elif user_choice == "9":
		choices_code.addTaskToCategory()

	elif user_choice == "q":
		print ("\nThank you!\n")
		break

	else:
		print ("\nInvalid choice!\n")