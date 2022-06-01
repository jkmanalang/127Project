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
	status_dict = {1:"Not yet started",
	2:"In-progress", 3:"Missed",
	4:"Completed"}

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
	for i in categories:
		print(str(counter) + ") " + i[1])
		for j in categoryAndTask:
			if(i[0] == j[0]):	# using datetime library to convert date to string
				print("\t[" + j[4].strftime("%m/%d/%Y") + "]\t\t" + j[6] + " \t\t " + j[5])

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
		editChoice = getIntInput(0, 4, "Choice")

		# updating the database
		if(editChoice == 1):
			value = input ("New task name: ")

			mycursor.execute("UPDATE task SET details=%s WHERE taskNo=%s", (value, userChoice))
			mydb.commit()
		
		elif(editChoice == 2):
			showListOfCategories()
			value = getIntInput(1, getHighestCategoryNo(), "Category")

			mycursor.execute("UPDATE task SET categoryNo=%s WHERE taskNo=%s", (value, userChoice))
			mydb.commit()

		elif(editChoice == 3):
			month = getIntInput(1, 12, "Month")
			day = getIntInput(1, 31, "Day")
			year = getIntInput(2000, 9999, "Day")

			mycursor.execute("UPDATE task SET dueDate='%s/%s/%s' WHERE taskNo=%s", (year, month, day, userChoice))
			mydb.commit()

		elif(editChoice == 4):
			status_dict = showTaskStatus()
			status = getIntInput(1, 4, "Status")

			for x, y in status_dict.items():
				if (x == status):
					mycursor.execute("UPDATE task SET taskStatus=%s WHERE taskNo=%s", (y, userChoice))
					mydb.commit()
					break

		else: break
		print("\n")