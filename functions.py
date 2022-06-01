import mysql.connector
import datetime

mydb = mysql.connector.connect(host="localhost", user="root", passwd="happynewyearmariadb", database="task_record")
mycursor = mydb.cursor()

def getUserAnswer():
	try:
		user_answer = input ("Choice" + ": ")
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

def showTasks():
	print("\n----------------------------- Viewing tasks -----------------------------")

	# join every task with their category and storing it to 'tasks' list
	select_categories = "SELECT * FROM category a NATURAL JOIN task b"
	mycursor.execute(select_categories)
	tasks = []

	for i in mycursor:
		tasks.append(i)

	# getting category list
	categories = getAllCategories()

	# printing categories together with their tasks
	counter = 1
	for i in categories:
		print(str(counter) + ") " + i[1])
		for j in tasks:
			if(i[0] == j[0]):	# using datetime library to convert date to string
				print("\t[" + j[4].strftime("%m/%d/%Y") + "]\t\t" + j[6] + " \t\t " + j[5])

		# print("\n")
		counter += 1

def addCategory():
	print("\n----------------------------- Adding Category -----------------------------")

	# getting category number
	categoryNo = getHighestCategoryNo()
	categoryNo += 1

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
	insertCategoryStatement = "INSERT INTO category (categoryNo, categoryName, categoryType) VALUES (%s, %s, %s)"
	values = (categoryNo, categoryName, categoryType)

	mycursor.execute(insertCategoryStatement, values)

	mydb.commit()
	print("Category " + categoryName + " successfully added!")



def viewCategory():
	print("\n----------------------------- Viewing Category -----------------------------")
	
	print("Which category you want to view?")

	categories = getAllCategories()

	for i in categories:
		print("\t[" + str(i[0]) + "] " + i[1])

	userChoice = getIntInput(1, getHighestCategoryNo(), "Category")

	print("\n")

	for i in categories:
		if (i[0] == userChoice):
			print("Category name: " + i[1])
			print("Category type: " + i[2])
		
	print("Tasks:")

	tasks = getAllTasks()
	counter = 0
	for i in tasks:
		if(i[1] == userChoice):
			print("\t[" + i[2].strftime("%m/%d/%Y") + "]\t\t" + i[4] + " \t\t " + i[3])
			counter += 1
	
	if(counter == 0):
		print("\t [no task yet]")