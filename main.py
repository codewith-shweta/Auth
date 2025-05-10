from flask import Flask , render_template ,request ,redirect, session, url_for
from werkzeug.security import generate_password_hash , check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'nvm'

#config sqlalchemy 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///info.db" 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)           #create db 

#database model  ~single row in our db 
class User(db.Model):
    #details 
    id =db.Column(db.Integer, primary_key =True )
    username =db.Column(db.String(25), unique = True, nullable = False)
    password_hash =db.Column(db.String(15),nullable=False)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_pass(self,password):
        return check_password_hash(self.password_hash,password) 

#Routes
@app.route('/')

def home ():
    if "username" in session:    #session  will check if the user logged in
        return redirect(url_for('dashboard'))
    return render_template("index.html")

#login
@app.route('/login', methods=['POST'])

def login():
    #collect info from the form
    username=request.form['username']
    password =request.form['password']
    #creating a model of the class object and query to our database to check username and password
    user = User.query.filter_by(username=username).first()   #object
    if user and user.check_pass(password):
        session['username']= username
        return redirect(url_for('dashboard'))
    else :
         #otherwise show home page
        return render_template('index.html')
    
#register   
    #check if its in the db
@app.route('/register', methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("index.html", error="user is already here!")
    
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username   #new user 
        return redirect(url_for('dashboard'))   
    
#dashboard
@app.route('/dashboard')
def dashboard():
    if "username" in session:
        return render_template('dashboard.html' , username = session['username'])
    return redirect(url_for('home'))    
    
#logout
# ['bob', 'nvm','josh']    #all we have to do is pop the user out from list 
@app.route('/logout')    
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))


if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    app.run( debug= True)