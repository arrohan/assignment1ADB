from flask import Flask, render_template, request
from azure.storage.blob import BlockBlobService
import pandas as pd
import numpy as np
import csv
app = Flask(__name__)

account_name = "rxa5014storage"
account_key = "Apk1DlIhjJKIlodD/KDtAryxBYORJ48bfuLL05azxOa0J5r0Jesaa7Wt3XRwZdpCDePGrE0WWFk1rDapwI74UA=="
top_level_container_name = "images"

df = pd.read_csv('people.csv')
df1=df.replace(np.nan,"",regex=True)

data = df1.values.tolist()

fileNames = []

@app.route('/', methods=["POST","GET"])
def hello():
	return render_template('index.html')

@app.route('/alldata',methods=["POST","GET"])
def search():	
	blob_service = BlockBlobService(account_name, account_key)
	generator = blob_service.list_blobs(top_level_container_name)
	for blob in generator:
		fileNames.append(blob.name)
	return render_template('alldata.html',dict=data,fileNames=fileNames)

@app.route('/takedata',methods=["POST","GET"])
def searchdata():
	name = request.form.get("SearchBar")
	return render_template('search.html',dict=data, name=name)
	

@app.route('/saldata',methods=["POST","GET"])
def saldata():
	people = []
	sal = request.form.get("salBar")
	sal = float(sal)
	for items in data:
		salary = 0
		if(items[2] != "" and items[2] != " "):
			salary = float(items[2])
		if (salary < sal):
			people.append(items)
	return render_template('salbaseddata.html',dict=people, sal=sal)

@app.route('/update',methods=["POST","GET"])
def updatedata():	
	name = request.form.get("name")
	state = request.form.get("state")
	salary = request.form.get("salary")
	grade = request.form.get("grade")
	room = request.form.get("room")
	telnum = request.form.get("telnum")
	keywords = request.form.get("keywords")
	counter = 0
	for items in data:
		if(items[counter] == name):
			df.loc[counter,'Name']=name
			df.loc[counter,'State']=state
			df.loc[counter,'Salary']=salary
			df.loc[counter,'Grade']=grade
			df.loc[counter,'Room']=room
			df.loc[counter,'Telnum']=telnum
			df.loc[counter,'Keywords']=keywords
			df.to_csv("people.csv",index=False)
			break
		counter+=1
	
	return render_template('index.html',dict=data)