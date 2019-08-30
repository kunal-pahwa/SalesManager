import requests
from flask import Flask, render_template, request, json,session, abort
import os
# from flaskext.mysql import MySQL,
# from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

mysql = MySQL()


def create_database():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS `user_load` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(500) DEFAULT NULL,
  `mobile` int(11) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `status` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1
        ''')
    cursor.close()


def insert1(Name,mobile,email,address,area):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("""insert into user_load(Name,mobile,email,address,area,status) values (%s,%s,%s,%s,%s,%s)""",(Name,mobile,email,address,area,'0'))
    conn.commit()
    cursor.close()


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'shopclues'
app.config['MYSQL_DATABASE_DB'] = 'Project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)




@app.route('/insert',methods = ['GET','POST'])
def insertIssue():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == "POST":
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        area = request.form['area']
        print(name)
        insert1(name,mobile,email,address,area)
        cursor.close()
    else:
        return render_template('contact.html')


@app.route('/complaints')
def getComplaints():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''select * from user_load where status=0''')
        rv = cursor.fetchall()
        cursor.close()
        return render_template('load_complaints.html', data=rv)

@app.route('/change_status',methods = ['POST'])
def change_status():
    if request.method == "POST":
        conn = mysql.connect()
        cursor = conn.cursor()
        id = request.form['id']
        result = cursor.execute("""update user_load set status=1 where id = %s""",(id))
        conn.commit()
        cursor.close()
        return "OK"

@app.route('/login',methods = ['GET','POST'])
def user_login():
    if request.method == "POST":
        name = request.form['username']
        password = request.form['password']
        conn = mysql.connect()
        cursor = conn.cursor()
        row_count = cursor.execute('''select * from users where username = %s and password = %s''',(name,password))
        print (row_count)
        if row_count > 0:
            session['logged_in'] = True
            return "Ok"
        else:
            print("home")
            return render_template('/home.html')
    else:
        return render_template('/login.html')


@app.route('/')
def home():
    return render_template('/home.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    create_database()
    app.run(debug=True,use_reloader=False)

