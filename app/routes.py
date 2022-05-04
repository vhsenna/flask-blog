from flask import render_template, flash, request, redirect, url_for
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
    return render_template('name.html',
        name=name,
        form=form)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash password before save
            hashed_password = generate_password_hash(form.password_hash.data, 'sha256')
            user = User(
                username=form.username.data,
                name=form.name.data,
                email=form.email.data,
                password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.username.data = ''
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
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
        new_data.username = request.form['username']
        new_data.name = request.form['name']
        new_data.email = request.form['email']
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
            new_data=new_data,
            id=id)

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User deleted successfully!')
        users_list = User.query.order_by(User.date_added)
        return render_template('add_user.html',
            name=name,
            form=form,
            users_list=users_list)
    except:
        flash('Whoops! There was a problem deleting user... Try again!')
        return render_template('add_user.html',
            name=name,
            form=form,
            users_list=users_list)

@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            slug=form.slug.data,
            content=form.content.data,
            author=form.author.data)
        form.title.data = ''
        form.slug.data = ''
        form.content.data = ''
        form.author.data = ''
        db.session.add(post)
        db.session.commit()
        flash('Blog post submitted successfully!')
    return render_template('add_post.html',
        form=form)

@app.route('/posts')
def posts():
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('posts.html',
        posts=posts)

@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html',
        post=post)

@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.author = form.author.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash('Post has been updated!')
        return redirect(url_for('post', id=post.id))
    form.title.data = post.title
    form.slug.data = post.slug
    form.author.data = post.author
    form.content.data = post.content
    return render_template('edit_post.html',
        form=form)

@app.route('/post/delete/<int:id>')
def delete_post(id):
    post_to_delete = Post.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash('Blog post was deleted successfully!')
        posts = Post.query.order_by(Post.date_posted.desc())
        return render_template('posts.html',
            posts=posts)
    except:
        flash('Whoops! There was a problem deleting post... Try again!')
        posts = Post.query.order_by(Post.date_posted.desc())
        return render_template('posts.html',
            posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login successfull')
                return redirect(url_for('dashboard'))
    return render_template('login.html',
        form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')
