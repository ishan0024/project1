from flask import Flask,render_template,request,session,redirect,url_for,flash,jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from flask_mail import Mail, Message
from random import randint


# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='kusumachandashwini'


# Configure Flask-Mail

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'ishank2400@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] =  'syda csrb iyvd oqtl' # Replace with your email password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
otp= randint(0000,9999)


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/university_portal'
db=SQLAlchemy(app)

# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)

class Department(db.Model):
    cid=db.Column(db.Integer,primary_key=True)
    branch=db.Column(db.String(100))

class Attendence(db.Model):
    aid=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(100))
    attendance=db.Column(db.Integer())

class Trig(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))
    usertype=db.Column(db.String(50))

class Tempuser(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))
    usertype=db.Column(db.String(50))


class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(50))
    sname=db.Column(db.String(50))
    sem=db.Column(db.Integer)
    gender=db.Column(db.String(50))
    branch=db.Column(db.String(50))
    email=db.Column(db.String(50))
    number=db.Column(db.String(12))
    address=db.Column(db.String(100))
    
@app.route('/get-data')
def get_user():
    products=[{

            "image":"/static/images/python_logo.jfif",
            "id":1,
            "name":"Python"
        
        },
        {
            "image":"static/images/java_logo.jfif",
            "id":2,
            "name":"Java"
        },
        {
            "image":"static/images/aws_logo.jfif",
            "id":3,
            "name":"AWS"
        },
         {
            "image":"static/images/ai_logo.jfif",
            "id":4,
            "name":"AI"
        },
        {
            "image":"static/images/sql_logo.jfif",
            "id":5,
            "name":"SQL"
        },

        ]
    return jsonify(products)
@app.route('/')
def index(): 
    #result = session.query(Item).all()
    return render_template('index.html')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/verifyemail')
def verifyemail():
    id=session.get(id)    
    return render_template('verifyemail.html',msg="")
'''@app.route('/fetchdata')
def fetchdata():'''


@app.route('/studentdashboard')
def studentdashboard(): 
   return render_template('studentdashboard.html')

@app.route('/teacherdashboard')
def teacherdashboard(): 
 
    return render_template('teacherdashboard.html')

@app.route('/admindashboard')
def admindashboard(): 
 
    return render_template('admindashboard.html')

@app.route('/studentdetails')
@login_required
def studentdetails():
    # query=db.engine.execute(f"SELECT * FROM `student`") 
    query=Student.query.all() 
    return render_template('studentdetails.html',query=query)

@app.route('/triggers')
@login_required
def triggers():
    # query=db.engine.execute(f"SELECT * FROM `trig`") 
    query=Trig.query.all()
    return render_template('triggers.html',query=query)

@app.route('/department',methods=['POST','GET'])
@login_required
def department():
    if request.method=="POST":
        dept=request.form.get('dept')
        query=Department.query.filter_by(branch=dept).first()
        if query:
            flash("Department Already Exist","warning")
            return redirect('/department')
        dep=Department(branch=dept)
        db.session.add(dep)
        db.session.commit()
        flash("Department Added","success")
    return render_template('department.html')

@app.route('/addattendance',methods=['POST','GET'])
@login_required
def addattendance():
    # query=db.engine.execute(f"SELECT * FROM `student`") 
    query=Student.query.all()
    if request.method=="POST":
        rollno=request.form.get('rollno')
        attend=request.form.get('attend')
        print(attend,rollno)
        atte=Attendence(rollno=rollno,attendance=attend)
        db.session.add(atte)
        db.session.commit()
        flash("Attendance added","warning")

        
    return render_template('attendance.html',query=query)

@app.route('/search',methods=['POST','GET'])
@login_required
def search():
    if request.method=="POST":
        rollno=request.form.get('roll')
        bio=Student.query.filter_by(rollno=rollno).first()
        attend=Attendence.query.filter_by(rollno=rollno).first()
        return render_template('search.html',bio=bio,attend=attend)
        
    return render_template('search.html')

@app.route("/delete/<string:id>",methods=['POST','GET'])
@login_required
def delete(id):
    post=Student.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    # db.engine.execute(f"DELETE FROM `student` WHERE `student`.`id`={id}")
    flash("Details Deleted Successfully","danger")
    return redirect('/studentdetails')


@app.route("/edit/<string:id>",methods=['POST','GET'])
@login_required
def edit(id):
    # dept=db.engine.execute("SELECT * FROM `department`")    
    if request.method=="POST":
        rollno=request.form.get('rollno')
        sname=request.form.get('sname')
        sem=request.form.get('sem')
        gender=request.form.get('gender')
        branch=request.form.get('branch')
        email=request.form.get('email')
        num=request.form.get('num')
        address=request.form.get('address')
        # query=db.engine.execute(f"UPDATE `student` SET `rollno`='{rollno}',`sname`='{sname}',`sem`='{sem}',`gender`='{gender}',`branch`='{branch}',`email`='{email}',`number`='{num}',`address`='{address}'")
        post=Student.query.filter_by(id=id).first()
        post.rollno=rollno
        post.sname=sname
        post.sem=sem
        post.gender=gender
        post.branch=branch
        post.email=email
        post.number=num
        post.address=address
        db.session.commit()
        flash("Details Updated Successfully","success")
        return redirect('/studentdetails')
    dept=Department.query.all()
    posts=Student.query.filter_by(id=id).first()
    return render_template('edit.html',posts=posts,dept=dept)



@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        usertype=request.form.get('usertype')
        #user=Tempuser.query.filter_by(email=email).first()
        #if user:
            #flash("Email Already Exists","warning")
            #return render_template('/signup.html')
        #encpassword=generate_password_hash(password)

        # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        temp_user=Tempuser(username=username,email=email,password=password,usertype=usertype)
        db.session.add(temp_user)
        db.session.commit()
        results=Tempuser.query.all()
        lastid=0
        for row in results:
            row=str(row)
            elements=row.split(" ")
            lasttoken=elements[1]
            id=lasttoken[0:len(lasttoken)-1]
            id=int(id)
            lastid=id
        id=lastid
        session['id']=id
        #flash("Signup Succesful. Please Login","success")'''
        return render_template('verifyemail.html')

          

    return render_template('signup.html')

@app.route('/getotp',methods=['POST'])
def getotp():
        email=request.form['email']
        msg=Message('OTP',sender='ishank2400@gmail.com' ,recipients=[email])
        msg.body=str(otp)
        mail.send(msg)
        
        return render_template("getotp.html")

@app.route('/validate',methods=['POST','GET'])
def validate():
        userotp=request.form['otp']
        if otp==int(userotp):
            id=session.get('id')
            temp_user=session.get('id')
        
            user=Tempuser.query.filter_by(id=id).first()
            username=user.username
            email=user.email
            password=user.password
            usertype=user.usertype
            n_user = User(username=username,email=email,password=password,usertype=usertype)
            db.session.add(n_user)
            #db.session.delete(temp_user)
            db.session.commit()
            return render_template('validate.html')
        return render_template('signup.html')
''''    
        @app.route('/fetch-data', methods=['GET'])
        def fetch_data():
    # Connect to the database
   conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True to get column names

    try:
        # Retrieve data from the database
        cursor.execute("SELECT * FROM your_table")
        rows = cursor.fetchall()
        current_id=rows[0][0]
        # Return data as JSON
        return jsonify(rows)

    except mysql.connector.Error as err:
        return f"Error: {err}"

    finally:
        cursor.close()
        conn.close()
    '''

  
'''
  from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

 results=Tempuser.query.all()
        lastid=0
        for row in results:
            row=str(row)
            elements=row.split(" ")
            lasttoken=elements[1]
            id=lasttoken[0:len(lasttoken)-1]
            id=int(id)
            lastid=id
        id=lastid
        db.session.add(id)
        db.session.commit()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://your_username:your_password@your_host/your_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/user/<int:user_id>')
def get_user(user_id):
    # Retrieve a single record using query.get()
    user = User.query.get(user_id)
    if user is None:
        return "User not found", 404
    return render_template('user.html', user=user)

if _name_ == '__main__':
    app.run(host="0.0.0.0",port=5000)
    
    app.run(debug=True)
  
  '''



@app.route('/login',methods=['POST','GET'])
def login(): 
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        # if user and check_password_hash(user.password,password):
        if user and user.password == password:
            login_user(user)
            if user.usertype=='Student':
                flash("Login Successful","primary")
                return redirect(url_for('studentdashboard'))
            if user.usertype=='Teacher':
                flash("Login Successful","primary")
                return redirect(url_for('teacherdashboard'))
            if user.usertype=='Admin':
                flash("Login Successful","primary")
                return redirect(url_for('admindashboard'))
        else:
            flash("Invalid Credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful","warning")
    return redirect(url_for('login'))



@app.route('/addstudent',methods=['POST','GET'])
@login_required
def addstudent():
    # dept=db.engine.execute("SELECT * FROM `department`")
    dept=Department.query.all()
    if request.method=="POST":
        rollno=request.form.get('rollno')
        sname=request.form.get('sname')
        sem=request.form.get('sem')
        gender=request.form.get('gender')
        branch=request.form.get('branch')
        email=request.form.get('email')
        num=request.form.get('num')
        address=request.form.get('address')
        # query=db.engine.execute(f"INSERT INTO `student` (`rollno`,`sname`,`sem`,`gender`,`branch`,`email`,`number`,`address`) VALUES ('{rollno}','{sname}','{sem}','{gender}','{branch}','{email}','{num}','{address}')")
        query=Student(rollno=rollno,sname=sname,sem=sem,gender=gender,branch=branch,email=email,number=num,address=address)
        db.session.add(query)
        db.session.commit()

        flash("Details Updated Successfully","info")


    return render_template('student.html',dept=dept)





@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True) 

