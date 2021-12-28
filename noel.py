from flask import Flask,render_template,request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__) #debut du programme 

#connection a la base de donnée
app.config['SECRET_KEY'] = 'xxxxxxxxxxxxxx'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:toor_2021_SQL@localhost:3306/personnel'
db=SQLAlchemy(app)

#model de la table dans la bd
class User(db.Model):
    __tablename__='prof'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    username=db.Column(db.String(150))
    telephone=db.Column(db.Integer)

#initialisation des variables
def __init__(self,email,username,telephone):
    self.email=email
    self.username=username
    self.telephone=telephone
    
 
 # Utilisation de la librarie flask_restful  
@app.route('/')##usare flask_restful 
def home():
    userlist=User.query.all()
    return render_template("home.html",userlist=userlist)

#insertion des profs
@app.route('/insert',methods=['GET','POST'])
def insert(): 
    if request.method=='POST':
        email=request.form.get('email')
        username=request.form.get('username')
        telephone=request.form.get('telephone')

        user=User.query.filter_by(email=email).first()
        if user:
            flash('Email already Used ',category='error') 
        elif len(email)<3:
            flash('_> Email > 4 charac',category='error')
        elif len(username)<2:
            flash('_> Username > 4 charac',category='error')
        elif len(telephone)<10:
            flash('_> telephone >= 10 ',category='error')
        else:
            new_user=User(email=email,username=username,telephone=telephone)
            db.session.add(new_user)
            db.session.commit()
            flash('User: "'+username+'" Created',category='success')
            ##login_user(user,remember=True)
            ## userResult=db.session.query(User)
            return redirect(url_for("home"))
    return render_template("insert.html") 

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    uto = User.query.get_or_404(id)
    if request.method=='POST':
        email=request.form.get('email')
        username=request.form.get('username')
        telephone=request.form.get('telephone')
        
        if uto.email==request.form.get('email'):
            flash('Email already Used ',category='error') 
        elif len(email)<3:
            flash('_> Email > 4 charac',category='error')
        elif len(username)<2:
            flash('_> Username > 4 charac',category='error')
        elif len(telephone)!=10:
            flash('_> telephone == 10 ',category='error')
        else:
            uto.email=request.form.get('email')
            uto.username=request.form.get('username')
            uto.telephone=request.form.get('telephone')
            db.session.commit()
            flash('User: "'+uto.username+'" Updated',category='success')
            ##login_user(user,remember=True)
            ## userResult=db.session.query(User)
            return redirect(url_for("home"))
    return render_template("update.html",user=uto)

@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete_user(id):
        utd = User.query.get_or_404(id)
        username = utd.username
        if utd:
            db.session.delete(utd)
            db.session.commit()
            flash('User: "'+username+'" deleted',category='warning')
            return redirect(url_for("home")) 

if __name__ == '__main__':
    app.run(debug=True)


