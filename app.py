from flask import Flask, render_template, request, redirect, url_for
from azure.storage.blob import BlobServiceClient, PublicAccess, ContentSettings
import pandas as pd
import csv
import numpy as np
import os
import time
app = Flask(__name__)

path="./names.csv"
tempPath="./new.csv"
 
fieldnames=['Name','Room','ID','State','Picture','Caption']

df = pd.read_csv('names.csv')
df1=df.replace(np.nan,"",regex=True)

data = df1.values.tolist()

app.config["image_folder"] = "./static/"



@app.route('/', methods=["POST","GET"])
def hello():
	return render_template('index.html')

@app.route('/homepage', methods=["POST","GET"])
def home():
	return render_template('index.html')

@app.route('/alldata',methods=["POST","GET"])
def search():	
	df = pd.read_csv('people.csv')
	df1=df.replace(np.nan,"",regex=True)
	data = df1.values.tolist()
	return render_template('alldata.html',dict=data)

@app.route('/takedata',methods=["POST","GET"])
def searchdata():
	people = []
	df = pd.read_csv('names.csv')
	print(df.head())
	df1=df.replace(np.nan,"",regex=True)
	data = df1.values.tolist()
	id = request.form.get("SearchBar")
	id = int(id)
	for items in data:
		print("hereeeeeee", items)
		idno = 0
		if(items[2] != "" and items[2] != " "):
			print(items[2])
			idno = int(items[2])
		if(idno == id):
			people.append(items)
	return render_template('search.html',dict=people, id=id)

@app.route('/searchname',methods=["POST","GET"])
def searchname():
	people = []
	df = pd.read_csv('names.csv')
	df1=df.replace(np.nan,"",regex=True)
	data = df1.values.tolist()
	name = request.form.get("SearchName")
	for items in data:
		if(items[0] == name):
			people.append(items)
	return render_template('searchbyname.html',dict=people, id=name)

@app.route('/roomdata',methods=["POST","GET"])
def saldata():
	df = pd.read_csv('names.csv')
	df1=df.replace(np.nan,"",regex=True)
	data = df1.values.tolist()
	people = []
	min = request.form.get("minroom")
	print(min)
	max = request.form.get("maxroom")
	min = int(min)
	print(max)
	max = int(max)
	for items in data:
		room = 0
		if(items[1] != "" and items[1] != " "):
			room = int(items[1])
		if (room >= min and room <= max):
			print(room)
			people.append(items)
	return render_template('salbaseddata.html',dict=people, max=max, min=min)

@app.route('/update',methods=["POST","GET"])
def updatedata():				
	name = request.form.get("name")
	print(name)
	state = request.form.get("state")
	room = request.form.get("room")
	id = request.form.get("id")
	keywords = request.form.get("keywords")
	with open(tempPath, mode='w') as csv_file:
		linewriter=csv.writer(csv_file)
		mywriter=csv.DictWriter(csv_file,fieldnames=fieldnames)
		mywriter.writeheader()
		with open(path, mode='r') as csv_file:
			myreader = csv.DictReader(csv_file)
			for row in myreader:
				if row['Name']==name:
					print(row)
					if(request.form['update'] == 'Update'):
						linewriter.writerow([name,room,id,state,row['Picture'],keywords])
					else:
						continue
				else:
					mywriter.writerow(row)
	os.remove(path)
	os.rename(tempPath,path)

	return render_template('index.html')

@app.route('/updatePicture', methods=["POST","GET"])
def upload():
	return render_template('uploadpic.html')

@app.route('/addPictureToPerson', methods=["POST","GET"])
def addPicToPerson():
	if request.method== "POST":
		result=0
		flag=0
		personName = request.form.get("name")
		with open(path, mode='r') as csv_file:
			myreader = csv.DictReader(csv_file)
			for row in myreader:
				if row['Name']==personName:
					result=1
					break
		if result==1:
			if request.files:
				image = request.files["image"]
				image.save(os.path.join(app.config["image_folder"], image.filename))
				#print("Image saved",image.filename)

				#upload blob onto azure st acc
				MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=rxa5014storage;AccountKey=Apk1DlIhjJKIlodD/KDtAryxBYORJ48bfuLL05azxOa0J5r0Jesaa7Wt3XRwZdpCDePGrE0WWFk1rDapwI74UA==;EndpointSuffix=core.windows.net"
				MY_IMAGE_CONTAINER = "images"
				local_filepath=os.path.join(app.config["image_folder"], image.filename)
				blob_service_client =  BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
				blob_client = blob_service_client.get_blob_client(container=MY_IMAGE_CONTAINER, blob=image.filename)
				image_content_setting = ContentSettings(content_type='image/jpeg')
				with open(local_filepath, "rb") as data:
					blob_client.upload_blob(data,overwrite=True,content_settings=image_content_setting)
				time.sleep(2)

				#update csv with new image filename
				with open(tempPath, mode='w') as csv_file:
					linewriter=csv.writer(csv_file)
					mywriter=csv.DictWriter(csv_file,fieldnames=fieldnames)
					mywriter.writeheader()
					with open(path, mode='r') as csv_file:
						myreader = csv.DictReader(csv_file)
						for row in myreader:
							if row['Name']==personName:
								flag=1
								displayRow=row
								displayRow['Picture']=image.filename
								linewriter.writerow([row['Name'],row['State'],row['Salary'],row['Grade'],row['Room'],row['Telnum'],image.filename,row['Keywords']])
							else:
								mywriter.writerow(row)
			
			os.remove(path)
			os.rename(tempPath,path)
		if flag==1: 
			return render_template('index.html')
		else : 
			return render_template('index.html',result=result)
