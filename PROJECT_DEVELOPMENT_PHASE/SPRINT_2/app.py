from flask import Flask, render_template,request
import sqlite3 as sql

# import ibm_db
# conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=lxt94214;PWD=wqugWwPXISuGdIrs",'','')


app=Flask(__name__)
app.secret_key = 'fasdgfdgdfg'
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashborad():
    return render_template('dashboard.html')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashsub')
def dashsub():
    return render_template('dashsub.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         food = request.form['food']
         calories = request.form['calories']
      
         with sql.connect("users.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (food,calories) VALUES (?,?)",(food,calories))
            msg = "Record successfully added!"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("history.html",msg = msg)
         con.close()


@app.route('/history')
def history():
   con = sql.connect("users.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from users")
   
   users = cur.fetchall();
   return render_template("history.html", users = users)

if __name__ == '__main__':
    app.run(debug=True)