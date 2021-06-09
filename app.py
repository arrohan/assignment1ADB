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
	people=[]
	sal = request.form.get("salBar")
	sal = int(sal)
	for items in data:
		salary = items[2]
		salary = int(salary)
		if salary > sal:
			people.append(items)
	return render_template('salbaseddata.html',dict=people, sal=sal)