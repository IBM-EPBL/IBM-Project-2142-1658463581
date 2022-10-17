from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'fasdgfdgdfg'


@app.route('/')
def home():
   return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup')
def signup():
   return render_template('signup.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         name = request.form['name']
         email = request.form['email']
         mobile = request.form['mobile']
         city = request.form['city']
         state=request.form['state']
         country=request.form['country']
         password = request.form['Password']
         
         with sql.connect("students.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,email,mobile,city,state,country,password) VALUES (?,?,?,?,?,?,?)",(name,email,mobile,city,state,country,password))
            msg = "Record successfully added!"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("list.html",msg = msg)
         con.close()


@app.route('/list')
def list():
   con = sql.connect("students.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   students = cur.fetchall();
   return render_template("list.html", students = students)


if __name__ == '__main__':
   app.run(debug = True)