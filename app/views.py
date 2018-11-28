#CS 361 Group 15
#Lyft but for truck drivers

import mysql.connector
from flask import Flask, render_template, request
#app = Flask(__name__, static_folder='static')
from app import app
@app.route("/")
def main():
    return render_template('index.html');

@app.route("/hello/<name>")
def nameroute(name):
    return "Hello " + name

@app.route("/postJob")
def postJob():
    return render_template('postJob.html');

@app.route("/distributor")
def distributor():
    return render_template('distributorHome.html')

@app.route("/trucker")
def trucker():
    return render_template('truckerHome.html')
    
if __name__ == "__main__":
    #This is set for compabilitity with Cloud9
    app.run(host='0.0.0.0', port=8080, debug=True)

#app = Flask(__name__)
    
@app.route("/create_account", methods=['POST'])
def create_account():
    input_email=request.form['inputEmail']
    input_user=request.form['inputUsername']
    input_password=request.form['inputPassword']
    role=request.form['userType']
    conn = mysql.connector.connect(user='cs340_piccirim', password='1946', host='classmysql.engr.oregonstate.edu', database='cs340_piccirim')
    cur = conn.cursor()
    cur.execute('''INSERT INTO users(email, username, password, role) VALUES(%s,%s, %s, %s)''', (input_email, input_user, input_password, role))
    conn.commit()
    cur.close()
    conn.close()
    if role == '1':
        return render_template('truckerHome.html')
    else:
        return render_template('distributorHome.html')

@app.route("/distributor_post", methods=['POST'])
def distributor_post():
    job_title=request.form['jobTitle']
    job_description=request.form['jobDescription']
    pickup_location=request.form['pickupLocation']
    dropoff_location=request.form['dropoffLocation']
    pickup_date=request.form['pickupDate']
    dropoff_date=request.form['dropoffDate']
    delivery_instructions=request.form['deliveryInstructions']
    conn = mysql.connector.connect(user='cs340_piccirim', password='1946', host='classmysql.engr.oregonstate.edu', database='cs340_piccirim')
    cur = conn.cursor()
    cur.execute('''INSERT INTO jobpost(title, description, pickupDate, dropoffDate, pickupLocation, dropoffLocation, deliveryInstructions) VALUES(%s, %s, %s, %s, %s, %s, %s)''', (job_title, job_description, pickup_date, dropoff_date, pickup_location, dropoff_location, delivery_instructions))
    conn.commit()
    cur.close()
    conn.close()
    return render_template('distributorHome.html');
