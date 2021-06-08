from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def hello():
	return render_template('index.html')

@app.route("/takedata",methods=["POST","GET"])
def search():
	return "Hello"