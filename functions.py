import mysql.connector
import datetime

mydb = mysql.connector.connect(host="localhost", user="root", passwd="happynewyearmariadb", database="task_record")
mycursor = mydb.cursor()

def getUserAnswer():
	try:
		user_answer = input ("Choice: ")
	except:
		print ("\nInvalid input.")
	return user_answer

def getIntInput(min_range, max_range, needed_input):
	while True:
		try:
			userInput = int (input (needed_input + " [" + str(min_range) + "-" + str(max_range) + "]: "))
			while min_range > userInput or userInput > max_range:
				userInput = int (input (needed_input + " [" + min_range + "-" + max_range + "]: "))
			break
		except:
			print("\nEnter integer within the given range only.")
	return userInput

def getHighestCategoryNo():
	select_maxCategoryNo = "SELECT MAX(categoryNo) FROM category"
	mycursor.execute(select_maxCategoryNo)

	for i in mycursor:
		highest = i
		break

	return (highest[0])

def getHighestTaskNo():
	select_maxTaskNo = "SELECT MAX(taskNo) FROM task"
	mycursor.execute(select_maxTaskNo)

	for i in mycursor:
		highest = i
		break

	return (highest[0])

def getAllCategories():
	get_categories = "SELECT * FROM category"
	mycursor.execute(get_categories)

	categories = []

	for i in mycursor:
		categories.append(i)

	return categories

def getAllTasks():
	get_tasks = "SELECT * FROM task"
	mycursor.execute(get_tasks)

	tasks = []
	for i in mycursor:
		tasks.append(i)
		
	return tasks

def getAllCategoriesAndTasks():
	# join every task with their category and storing it to 'tasks' list
	select_categoriesWithTask = "SELECT * FROM category a NATURAL JOIN task b"
	mycursor.execute(select_categoriesWithTask)
	tasks = []

	for i in mycursor:
		tasks.append(i)

	return tasks

# to print all categories
def showListOfCategories():
	categories = getAllCategories()

	for i in categories:
		print("   [" + str(i[0]) + "] " + i[1])

# to print status choices. can also give status in dictionary form
def showTaskStatus():
	status_dict = {1:"NOT YET STARTED",
	2:"IN-PROGRESS", 3:"MISSED",
	4:"COMPLETED"}

	for x, y in status_dict.items():
		print("   [" + str(x) + "] " + y)

	return status_dict

def showTasks():
	print("\n----------------------------- Viewing tasks -----------------------------")

	# join every task with their category and storing it to 'tasks' list
	categoryAndTask = getAllCategoriesAndTasks()

	# getting category list
	categories = getAllCategories()

	# printing categories together with their tasks
	counter = 1
	status_dict = {1:"NOT YET STARTED",
	2:"IN-PROGRESS", 3:"MISSED",
	4:"COMPLETED"}
	for i in categories:
		print(str(counter) + ") " + i[1])
		for j in categoryAndTask:
			if(i[0] == j[0]):	# using datetime library to convert date to string
				print("\t[" + j[4].strftime("%m/%d/%Y") + "]\t\t" + j[6], end="")
				if (j[6] == status_dict.get(2) or j[6] == status_dict.get(1)): print("\t\t" + j[5])
				else : print("\t\t\t" + j[5])
		# print("\n")
		counter += 1

def addCategory():
	print("\n----------------------------- Adding Category -----------------------------")

	# getting category name
	categoryName = input("Category name: ")

	# getting category type
	print ("""													
   [1] Personal
   [2] Professional
   [3] Others""")

	categoryTypeNo = getIntInput(1,3,"Category type")
	if (categoryTypeNo == 1):
		categoryType = "Personal"
	elif (categoryTypeNo == 2):
		categoryType = "Professional"
	else:
		categoryType = "Others"

	# inserting to database
	insertCategoryStatement = "INSERT INTO category (categoryName, categoryType) VALUES (%s, %s)"
	values = (categoryName, categoryType)

	mycursor.execute(insertCategoryStatement, values)

	mydb.commit()
	print("Category " + categoryName + " successfully added!")



def viewCategory():
	print("\n----------------------------- Viewing Category -----------------------------")
	
	# getting which category to view
	print("Which category you want to view?")
	categories = getAllCategories()
	for i in categories:
		print("\t[" + str(i[0]) + "] " + i[1])
	userChoice = getIntInput(1, getHighestCategoryNo(), "Category")

	print("\n")

	# printing category attributes together with its tasks available
	for i in categories:
		if (i[0] == userChoice):
			print("Category name: " + i[1])
			print("Category type: " + i[2])
		
	print("Task/s:")
	tasks = getAllTasks()
	counter = 0
	for i in tasks:
		if(i[1] == userChoice):
			print("\t[" + i[2].strftime("%m/%d/%Y") + "]\t\t" + i[4] + " \t\t " + i[3])
			counter += 1
	
	if(counter == 0):
		print("\t [no task yet]")

def editTask():
	print("\n----------------------------- Editing Task -----------------------------")

	print("Which task you want to edit?")

	# getting category with its tasks tuple
	categoryAndTask = getAllCategoriesAndTasks()

	# getting taskNo of the task to be edited
	for i in categoryAndTask:
		print("\t[" + str(i[3]) +"] " + i[5] + " (Category: " + i[1] + ")")	
	userChoice = getIntInput(1, getHighestTaskNo(), "Task")

	# continues editing of values until user wishes to end
	while(True):
		categoryAndTask = getAllCategoriesAndTasks()

		# getting which attribute to edit
		print("\nChoose what you want to edit")
		for i in categoryAndTask:
			if(userChoice == i[3]):
				print("\t[1] Details: " + i[5])
				print("\t[2] Category: " + i[1])
				print("\t[3] Deadline: " + i[4].strftime("%m/%d/%Y"))
				print("\t[4] Status: " + i[6])
				print("\t[0] Exit")
		editChoice = getIntInput(0, 3, "Choice")

		# updating the database
		if(editChoice == 1):
			while True:
				value = input ("New task name: ")
				if (value != ""): break

			mycursor.execute("UPDATE task SET details=%s WHERE taskNo=%s", (value, userChoice))
			mydb.commit()
		
		elif(editChoice == 2):
			month = getIntInput(1, 12, "Month")
			day = getIntInput(1, 31, "Day")
			year = getIntInput(2000, 9999, "Year")

			mycursor.execute("UPDATE task SET dueDate='%s/%s/%s' WHERE taskNo=%s", (year, month, day, userChoice))
			mydb.commit()

		elif(editChoice == 3):
			status_dict = showTaskStatus()
			status = getIntInput(1, 4, "Status")

			for x, y in status_dict.items():
				if (x == status):
					mycursor.execute("UPDATE task SET taskStatus=%s WHERE taskNo=%s", (y, userChoice))
					mydb.commit()
					break

		else: break
		print("\n")
		

def createTask():
	# Add task to an existing category
	print("\n----------------------------- Add task -----------------------------")
	categories = getAllCategories()
	found = False
	cName = ""

	# shows all existing categories
	print("Category_no\tCategory_name")
	for i in categories:
		print(str(i[0])+"\t\t"+i[1])
	
	category_num= getIntInput(1,getHighestCategoryNo(), "Add task to category_no")

	# checks if chosen category_num still exist in category
	for i in categories:
		if(category_num==i[0]):
			found= True
			cName = i[1]
	
	if (found):
		task_details = input("Task details: ")

		# limit year to 50 years from now
		task_dueDate_year = getIntInput(2022,2072,"Due date(year)")	
		task_dueDate_month = getIntInput(1,12,"Due date(month)")

		#to specifically limit number of days in the selected month	
		mon31= [1,3,5,7,8,10,12]
		dateNumMax= 0
		if task_dueDate_month==2:
			dateNumMax = 28
			if task_dueDate_year%4==0:
				dateNumMax= 29
		elif task_dueDate_month in mon31:
			dateNumMax=31
		else:
			dateNumMax=30
		task_dueDate_day = getIntInput(1,dateNumMax,"Due date(month)")	

		data= (category_num,task_dueDate_day, task_dueDate_month, task_dueDate_year ,task_details)
		sql = "INSERT INTO task(categoryNo, dueDate, details) VALUES(%s, STR_TO_DATE('%s-%s-%s','%d-%m-%Y'), %s)"

		try:
			mycursor.execute(sql,data)
			mydb.commit()
			autoMissed()
			print("New task was added to ",cName, " successfully!")
		except:
			print("Adding task failed")	
	
	else: 
		print("Category does not exist")

def autoMissed():
	sql = "UPDATE task SET taskStatus='MISSED' WHERE dueDate < CURDATE()"
	mycursor.execute(sql)
	mydb.commit()


def markAsDone():
	print("\n----------------------------- mark as done -----------------------------")
	category_task = getAllCategoriesAndTasks()

	# Keep this straight
	for i in category_task:
		print("\t"+str(i[3])+".\t["+i[1]+"] "+i[5]+"\t........"+i[6]+ " (due: "+i[4].strftime("%m/%d/%Y")+")")

	task_no = getIntInput(1,getHighestTaskNo(),"Mark as done task_no ")
	
	sql="UPDATE task SET taskStatus='DONE' WHERE taskno=" + str(task_no)
	mycursor.execute(sql)
	mydb.commit()
	print("Task status updated!")
	

def deleteTask():
	print("\n----------------------------- delete task -----------------------------")
	category_task = getAllCategoriesAndTasks()

	for i in category_task:
		print("\t"+str(i[3])+".\t["+i[1]+"] "+i[5]+"\t........"+i[6]+ " (due: "+i[4].strftime("%m/%d/%Y")+")")


	task_no = getIntInput(1,getHighestTaskNo(),"Delete task_no ")
	
	print("The deleted data will not be retrieved. Proceed with deletion? \n[Press [y] to delete, press any key to cancel]")
	go = input()

	if go=='y':	
		sql="DELETE FROM task WHERE taskno=" + str(task_no)
		mycursor.execute(sql)
		mydb.commit()
		print("Task_no ",task_no," deleted succesfully!")
		
		# to decrement taskNo of all tasks above the deleted task, 
		# ensures that there are no missing tasks in 1-max(taskNo), all taskNo in options exist
		sql= "UPDATE task SET taskNo = taskNo-1 WHERE taskno>"+str(task_no)
		mycursor.execute(sql)
		mydb.commit()
		print("Tasks task_number updated!")

	else:
		print("Deleting task cancelled")
	


	



	


