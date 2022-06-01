import random
import os
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="happynewyearmariadb", database="task_record")
mycursor = mydb.cursor()

def get_user_answer():
	try:
		user_answer = input ("Choice" + ": ")
	except:
		print ("\nInvalid input.")
	return user_answer

def getAllCategories():
	mycursor.execute("SELECT * FROM task")

	for i in mycursor:
		print(i)

	# print(mydb)