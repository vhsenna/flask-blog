from flask import render_template, flash, request
from app import app
from app.forms import *
from app.models import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    # Validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form submitted successfully!')
    return render_template('name.html', name=name, form=form)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(
                name=form.name.data,
                email=form.email.data,
                username=form.username.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.username.data = ''
        flash('User added successfully!')
    users_list = User.query.order_by(User.date_added)
    return render_template('add_user.html',
        name=name,
        form=form,
        users_list=users_list)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    new_data = User.query.get_or_404(id)
    if request.method == 'POST':
        new_data.name = request.form['name']
        new_data.email = request.form['email']
        new_data.username = request.form['username']
        try:
            db.session.commit()
            flash('User updated successfully!')
            return render_template('update.html',
                form=form,
                new_data=new_data)
        except:
            flash('Error! Looks like there was a problem... Try again!')
            return render_template('update.html',
                form=form,
                new_data=new_data)
    else:
        return render_template('update.html',
                form=form,
                new_data=new_data)
