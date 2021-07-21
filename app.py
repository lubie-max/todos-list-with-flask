from flask import Flask, render_template, request, redirect
# from flask_sqlalchemy import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///TODOs.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class TODOs(db.Model):
    srno=db.Column(db.Integer, primary_key=True)
    todos=db.Column(db.String(150), nullable=False)
    desc=db.Column(db.String(300), nullable=False)
    created_date=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.srno}-{self.todos}-{self.desc}-{self.created_date}"
 

@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        
        todos=request.form['todos']
        desc=request.form['desc']

        td=TODOs(todos=todos,desc=desc)
        db.session.add(td)
        db.session.commit()
    alltodo=TODOs.query.all()
    print(alltodo)
    return render_template('index.html',alltodo=alltodo)



@app.route('/update/<int:srno>', methods=['POST','GET'])
def update(srno):
    if request.method=='POST':
        title=request.form['todos']
        desc=request.form['desc']
        td=TODOs.query.filter_by(srno=srno).first()
        td.todos=title
        td.desc=desc
        db.session.add(td)
        db.session.commit()
        return redirect('/')
        

    todo=TODOs.query.filter_by(srno=srno).first()
    return render_template('update.html',todo=todo)

        # db.session.update(todo) invalid operation
        # db.session.commit()
       


@app.route('/delete/<int:srno>')
def delete(srno):
    todo=TODOs.query.filter_by(srno=srno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')



if __name__=="__main__":
    app.run(debug=True)