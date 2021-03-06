import os
import uuid as uuid
from config import Config
from flask import flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from app import app
from app.forms import *
from app.models import *

## Admin route
@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template('admin.html')
    else:
        flash('Sorry, you must be the Admin to access the Admin Page!')
        return redirect(url_for('dashboard'))

## Index route
@app.route('/')
def index():
    return render_template('index.html')

## User routes
# Dashboard route
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# Delete user route
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

# Login route
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
            else:
                flash('Wrong password... Try again!')
        else:
            flash('That user does not exist... Try again!')
    return render_template('login.html',
        form=form)

# Logout route
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('login'))

# Name route
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

# Update profile user
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    new_data = User.query.get_or_404(id)
    if request.method == 'POST':
        new_data.username = request.form['username']
        new_data.name = request.form['name']
        new_data.email = request.form['email']
        new_data.about = request.form['about']
        # Check for profile image
        if request.files['profile_image']:
            new_data.profile_image = request.files['profile_image']
            # Grab image name
            profile_image_filename = secure_filename(new_data.profile_image.filename)
            # Set UUID
            profile_image_name = str(uuid.uuid1()) + '_' + profile_image_filename
            # Save image
            save = request.files['profile_image']
            new_data.profile_image = profile_image_name
            try:
                db.session.commit()
                save.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_image_name))
                flash('User updated successfully!')
                return render_template('update.html',
                    form=form,
                    new_data=new_data,
                    id=id)
            except:
                flash('Error! Looks like there was a problem... Try again!')
                return render_template('update.html',
                    form=form,
                    new_data=new_data,
                    id=id)
        else:
            db.session.commit()
            flash('User updated successfully!')
            return render_template('update.html',
                form=form,
                new_data=new_data,
                id=id)
    else:
        return render_template('update.html',
            form=form,
            new_data=new_data,
            id=id)

# Add user route
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

# localhost:5000/user/<name>
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

## Post routes
# Add post route
@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Post(
            title=form.title.data,
            slug=form.slug.data,
            poster_id=poster,
            content=form.content.data)
        # Clear the form
        form.title.data = ''
        form.slug.data = ''
        form.content.data = ''
        #form.author.data = ''
        # Add post data to database
        db.session.add(post)
        db.session.commit()
        # Return a message
        flash('Blog post submitted successfully!')
    # Redirect to the webpage
    return render_template('add_post.html',
        form=form)

# Delete post route
@app.route('/post/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Post.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id or id == 1:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            # Return a message
            flash('Blog post was deleted successfully!')
            # Grab all the posts from the database
            posts = Post.query.order_by(Post.date_posted.desc())
            return render_template('posts.html',
                posts=posts)
        except:
            # Return an error message
            flash('Whoops! There was a problem deleting post... Try again!')
            posts = Post.query.order_by(Post.date_posted.desc())
            return render_template('posts.html',
                posts=posts)
    else:
        # Return a message
        flash('You are not authorized to delete that post!')
		# Grab all the posts from the database
        posts = Post.query.order_by(Post.date_posted.desc())
        return render_template('posts.html',
            posts=posts)

# Edit post route
@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        #post.author = form.author.data
        post.content = form.content.data
        # Update database
        db.session.add(post)
        db.session.commit()
        flash('Post has been updated!')
        return redirect(url_for('post', id=post.id))
    if current_user.id == post.poster_id or current_user.id == 1:
        form.title.data = post.title
        form.slug.data = post.slug
        #form.author.data = post.author
        form.content.data = post.content
        return render_template('edit_post.html',
            form=form)
    else:
        flash('You are not authorized to edit that post!')
        posts = Post.query.order_by(Post.date_posted.desc())
        return render_template('posts.html',
            posts=posts)

# Individual post route
@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html',
        post=post)

# Posts route
@app.route('/posts')
def posts():
	# Grab all the posts from the database
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('posts.html',
        posts=posts)

## Search routes
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        # Get data from submitted form
        post.search = form.search.data
        # Query the database
        posts = posts.filter(Post.content.like('%' + post.search + '%'))
        posts = posts.order_by(Post.title.desc()).all()
        return render_template('search.html',
            form=form,
            search=post.search,
            posts=posts)

## Pass stuff to navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)
