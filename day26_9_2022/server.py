from flask import Flask, render_template , request,flash,redirect,url_for, session
import sqlite3 as sql
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "79ee2819cf0d1c205299496cfa748c3c"  # hello or some word
upload_dir="static/images"
app.config['uploadDir'] = upload_dir
pathpic= "static/pictures"
app.config['uploadPic'] = pathpic
def connectDB():
    conn = sql.connect("users.db")
    conn.row_factory= sql.Row # returns resultset as dictionary
    return conn



@app.route("/")
@app.route("/login", methods=["GET","POST"])
def loginUser():
    if request.method == "GET":
        return render_template("login.html")
    else:
        useremail = request.form['email'] # form data by POSt method
        userpwd = request.form['password'] # form data by POSt method
        with connectDB() as conn:
            cursor = conn.cursor()
            cursor.execute("select password,filename from user where email=?",(useremail,))
            row = cursor.fetchone()
            if row==None: 
                flash("User email does not exist","warning")
                return redirect(url_for("loginUser"))
            else:
                if row['password'] == userpwd:
                    flash("welcome user ","success")
                    session['email']= useremail
                    return render_template("aboutus.html",photo =row['filename'])
                else:
                    flash("wrong password . Try again!","warning")
                    return redirect(url_for("loginUser"))


                




@app.route("/users")
def list_users():
    users = ["Aung Aung","Thiha","Maysi","Mie Mie"]
    return render_template("users.html",usrs = users)

@app.route("/register",methods = ["GET","POST"])
def registerUser():
    if request.method == "GET":
        return render_template("register.html",title="Register User")
    else:
        username = request.form['name'] # accessing data by Post method
        useremail = request.form['email']
        userpwd = request.form['password']
        imgfile = request.files['profile'] # file dictonary
        if username == "" or len(username)<8 :
            flash("Username must not be empty or at least 8 characters","warning")
            return redirect(url_for("registerUser"))
        elif  imgfile.filename == "":
            flash("choose profile picture","info")
            return redirect(url_for("registerUser"))
        else:
            with connectDB() as conn:
                try:
                    filename_form = secure_filename(imgfile.filename)
                    imgfile.save(os.path.join( app.config['uploadDir'],filename_form ))

                    cur = conn.cursor()
                    cur.execute("insert into user (uname, email, password,filename) values (?,?,?,?)",(username, useremail, userpwd,filename_form))
                                       
                    flash("Register Success", "success")
                

                except Exception as e:
                    print(e)
            
        return redirect(url_for("loginUser"))


@app.route("/something")
def aboutus():
    users=[ {"name":" Daw Aye Aye","age":45,"job":"teacher"},
     {"name":"U Tun","age":35,"job":"Manager"},
      {"name":" Daw Seint Seint","age":40,"job":"Director"},
      {"name":"U Ko Ko","age":25,"job":"Programmer"},
       {"name":"Daw Thinzar","age":28,"job":"software engineer"}]
    return render_template("aboutus.html",title="About us",emps=users)

@app.route("/logout")
def logout_user():
    if 'email' in session:
        session.pop("email",None)
    return redirect(url_for("loginUser"))




#Product related codes
@app.route("/products/new",methods=["GET","POST"])
def add_product():
    if request.method == "GET":
        return render_template("product.html")
    else:
        pname = request.form['name']
        price = request.form['price']
        print(type(price))
        
       
        category = request.form['category']
        p_pic =request.files['filename']  # img object
        if pname == "" or len(pname)<6:
            flash("product name should not be empty or at least 6 characters","warning")
            return redirect(url_for("add_product"))
        elif price == "":            
            flash("product price should be filled","warning")
            return redirect(url_for("add_product"))
            
        elif p_pic.filename == "":
            flash("product picture should be choosen","warning")
            return redirect(url_for("add_product"))
        else:
            pic_filename =secure_filename(p_pic.filename)
            p_pic.save(os.path.join(app.config['uploadPic'],pic_filename)) #save imaged into local server

            return "something"



if __name__ == "__main__":
    app.run(debug=True)