from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy #for database
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db" #configure the database in app, we gonna use sqlite

db = SQLAlchemy(app) #creates a db with the config from app and binds to app

class Data(db.Model): #it's a class to create db rows
    #Define the table columns here
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    dateStamp = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self): # return the task id in string form 
        return '<Data %r>' % self.id
    

@app.route('/', methods=['POST','GET']) # get is by default return, post is when we add stuff
def index():
    if request.method == "POST":
        new_content = request.form['content']#getting value in input fild with name content
        new_Data = Data(content=new_content)
        try:
            db.session.add(new_Data)# add new data to db session
            db.session.commit()# commit the session and make the changes permanent
            return redirect('/') # redirect to home page
        except Exception as e:
            return f"Unexpected error occurred while adding data, please Try again\n error code: {e}"
            
    else:
        datas = Data.query.order_by(Data.dateStamp).all()
        print(datas)
        return render_template('index.html', Datas=datas)

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Data.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Unexpected error while trying to delete data <Data {id}>\n Error Code: {e}"

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    task_to_update = Data.query.get_or_404(id)
    if request.method == "POST":
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Unexpected error while trying to update data <Data {id}>\n Error Code: {e}"
    else:
        return render_template('update.html', row=task_to_update)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()# create database if not already there
    app.run(debug=True)