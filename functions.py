import random
import os
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

def showTasks():
	print("\n----------------------------- Viewing tasks -----------------------------")

	# join every task with their category and storing it to 'tasks' list
	select_categories = "SELECT * FROM category a NATURAL JOIN task b"
	mycursor.execute(select_categories)
	tasks = []

	for i in mycursor:
		tasks.append(i)

	# getting categories and storing it to 'categories' list
	get_categories = "SELECT * FROM category"
	mycursor.execute(get_categories)
	categories = []

	for i in mycursor:
		categories.append(i)

	# printing categories together with their tasks
	for i in categories:
		print(i[1])
		for j in tasks:
			if(i[0] == j[0]):	# using datetime library to convert date to string
				print("\t[" + j[4].strftime("%m/%d/%Y") + "]\t\t" + j[6] + " \t\t " + j[5])

		# print("\n")

