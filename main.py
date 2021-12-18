from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# making a model
class Todo(db.Model):
    # setting  up columns
    id = db.Column(db.Integer, primary_key=True)
    quant=db.Column(db.Integer())
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        # return a string everytime we create a new element
        return '<Task %r>' % self.id

db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # task_content contains contents of the input
        task_content = request.form['content']
        task_quant = request.form['quant']
        # create Todo_object
        new_task = Todo(content=task_content, quant=task_quant)

        # add to database
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return "There was an issue adding your task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete= Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect ('/')

    except:
        return "There was some issue deleting this item"


@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task= Todo.query.get_or_404(id)

    if request.method=='POST':
        task.content=request.form['content']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return "There was an issue updating the item"

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)