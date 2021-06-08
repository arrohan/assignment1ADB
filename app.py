from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def hello():
	return render_template('index.html')

@app.route("/takedata",methods=["POST","GET"])
def search():
	name = request.form.get("Search Bar")

	return render_template("index.html", value=name)