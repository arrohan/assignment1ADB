from flask import Flask, render_template, request
import csv
app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/alldata',methods=["POST","GET"])
def search():
	data = list(csv.reader(open('people.csv')))
	return render_template('page.html',dict=data)
	

