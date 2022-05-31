import random
import os
import mysql.connector


def get_user_answer():
	try:
		user_answer = input ("Choice" + ": ")
	except:
		print ("\nInvalid input.")
	return user_answer

def getAllCategories():
	mydb = mysql.connector.connect(host="localhost", user="root", passwd="happynewyearmariadb", database="task_record")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM category")

	for i in mycursor:
		print(i)

	# print(mydb)