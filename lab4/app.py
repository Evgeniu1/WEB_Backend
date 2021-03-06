from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import Redis_login

app = Flask(__name__)
app.secret_key = 'iknowyoucanseethis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        if name == Redis_login.USER:
            if passw == Redis_login.PASS:
                session['logged_in'] = True
                return redirect('/')
            else:
                return 'Dont Login'
        else:
            return 'Dont Login'

@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    print(session['logged_in'])
    return redirect('/')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        Redis_login.USER=request.form['username']
        Redis_login.PASS=request.form['password']
        return render_template('login.html')
    return render_template('register.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            task_content = request.form['content']
            new_task = Todo(content=task_content)

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task'

        else:
            tasks = Todo.query.order_by(Todo.date_created).all()
            return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
