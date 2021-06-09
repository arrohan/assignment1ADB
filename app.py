from flask import Flask, render_template, request
import csv
app = Flask(__name__)

data = list(csv.reader(open('people.csv')))

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/alldata',methods=["POST","GET"])
def search():
	return render_template('page.html',dict=data)
	

