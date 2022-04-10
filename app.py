from flask import Flask, redirect, render_template, request, flash, session
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


@app.route("/")
def homepage():
    """Home Page - Will show list of users"""
    return render_template("home.html")


@app.route("/users")
def all_users():
    """Will Show List of All Users in DB"""
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Display Form to Add User"""
    return render_template('new.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle Form Submission for new User"""
    # create new user from form data
    new_user = User(
        first_name=request.form['fname'],
        last_name=request.form['lname'],
        image_url=request.form['iurl'] or None)
    # add user to db and commit
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>")
def user_profile(user_id):
    """Display User Information"""
    user = User.query.get_or_404(user_id)
    return render_template("userprofile.html", user=user)


@app.route("/users/<int:user_id>/edit")
def user_edit(user_id):
    """Display Form to Edit user"""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_modify(user_id):
    """Handle form submission for modifying user"""
    # get data from user input
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['fname']
    user.last_name = request.form['lname']
    user.image_url = request.form['iurl']
    # update user in DB and commit
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting an existing user"""
    # get userid and delete from DB
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route('/users/<int:user_id>/post-form')
def post_form(user_id):
    """Take to Form to upload post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("post-form.html", user=user, tags=tags)


@app.route('/users/<int:user_id>/post-form', methods=["POST"])
def handle_post(user_id):
    """Handle form submission for adding a post"""
    # get form data and make post
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'], user=user, tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def display_post(post_id):
    """Display Post Information"""
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Display Form to edit"""
    post = Post.query.get_or_404(post_id)
    return render_template("edit-post.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def modify_post(post_id):
    """Handle Form to edit post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' edited.")
    post = Post.query.get_or_404(post_id)

    return redirect(f"/posts/{post.id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle form submission for deleting an existing post"""
    # get post-id and delete from DB
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/users")


@app.route('/tags')
def all_tags():
    """Will Show List of All Tags in DB"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/new', methods=["GET"])
def tags_new_form():
    """Display Form to Add Tag"""
    return render_template('new-tag.html')


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle Form Submission for new Tag"""
    # create new tag from form data
    new_tag = Tag(
        title=request.form['title'])
    # add tag to db and commit
    db.session.add(new_tag)
    db.session.commit()
    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def display_tag(tag_id):
    """Display Tag Information"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    """Display Form to edit tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit-tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def modify_tag(tag_id):
    """Handle Form to edit tag"""
    tag = Tag.query.get_or_404(tag_id)

    tag.title = request.form['title']

    db.session.add(tag)
    db.session.commit()

    flash(f"Post '{tag.title}' edited.")
    tag = tag.query.get_or_404(tag_id)

    return redirect(f"/tags/{tag.id}")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Handle form submission for deleting an existing tag"""
    # get tag-id and delete from DB
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")
