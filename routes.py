from flask import render_template, redirect, url_for, session, flash
from .forms import LoginForm, TaskForm, RegistrationForm
from .models import db, User, Task
from . import app, cache


@app.route('/')
@app.route('/index')
def index():
    form = TaskForm()
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    tasks = cache.get('tasks')
    if tasks is None:
        task_objs = Task.query.filter_by(user_id=session['user_id']).all()
        tasks = [task.title for task in task_objs]
        cache.set('tasks', tasks)
    return render_template('index.html', tasks=tasks, form=form)


@app.route('/add_task', methods=['POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            user_id=session['user_id']
        )
        db.session.add(task)
        db.session.commit()

        tasks = cache.get('tasks')
        tasks.append(form.title.data)
        cache.set('tasks', tasks)

        return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['username'] = user.username
            session["user_id"] = user.id
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login_register.html', title='Log in', form=form, button_label='Log in')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('login_register.html', title='Register', form=form, button_label='Register')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('logged_in', None)
    return redirect(url_for('login'))
