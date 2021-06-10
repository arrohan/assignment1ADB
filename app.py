from flask import Flask, render_template, request
import pandas as pd
import numpy as np
app = Flask(__name__)

path="./static/people.csv"
tempPath="./static/new.csv"
 
fieldnames=['Name','State','Salary','Grade','Room','Telnum','Picture','Keywords']

df = pd.read_csv('people.csv')
df1=df.replace(np.nan,"",regex=True)

data = df1.values.tolist()


@app.route('/', methods=["POST","GET"])
def hello():
	return render_template('index.html')

@app.route('/alldata',methods=["POST","GET"])
def search():	
	return render_template('alldata.html',dict=data)

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
 	with open(tempPath, mode='w') as csv_file:
 		linewriter=csv.writer(csv_file)
 		mywriter=csv.DictWriter(csv_file,fieldnames=fieldnames)
 		mywriter.writeheader()
 		with open(path, mode='r') as csv_file:
 			myreader = csv.DictReader(csv_file)
 			for row in myreader:
 				if row['Name']==name:
 					linewriter.writerow([name,state,salary,grade,room,telnum,row['Picture'],keywords])
 				else: 
 					mywriter.writerow(row)
 	os.remove(path)
 	os.rename(tempPath,path)
 
 	return render_template('index.html')
