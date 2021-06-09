from flask import Flask, render_template, request
import csv
app = Flask(__name__)

data = list(csv.reader(open('people.csv')))

@app.route('/')
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
	for items in data:
		if(items[0] == name):
			items[1] = state 
			items[2] = salary
			items[3] = grade
			items[4] = room
			items[5] = telnum
			items[7] = keywords
	return render_template('search.html',dict=data)