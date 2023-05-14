from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)



class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    asdf = db.Column(db.String(500), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    
    

    
     
    def __repr__(self) -> str:
      return f"{self.sno} - {self.title}"

with app.app_context():
    db.create_all()    


@app.route('/', methods = ["GET" , "POST"])
def hello_world():
    if request.method=="POST":
        title = request.form['title']
        asdf = request.form['asdf']  
        todo = Todo(title=title,asdf=asdf)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)
    

@app.route('/update/<int:sno>', methods = ["GET" , "POST"])
def update(sno):
    if request.method =="POST":
        title = request.form['title']
        asdf = request.form['asdf']  
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.asdf = asdf
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
