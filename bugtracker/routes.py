from flask import render_template, url_for, flash, redirect, request, abort
from bugtracker import app, db, bcrypt
from bugtracker.forms import LoginForm, RegistrationForm, ProjectForm, BugForm, AddUserForm, ViewProjectForm, ViewBugForm
from bugtracker.models import User, Project, Bug
from flask_login import login_user, current_user, logout_user, login_required
import dateutil
from dateutil import parser


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = str(date)
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%b %d, %Y'
    return native.strftime(format) 

##############################################################################################################################

@app.route("/")
@app.route("/homepage")
def homepage():
    projects = Project.query.all()
    bugs = Bug.query.all()
    return render_template('homepage.html', projects=projects, bugs=bugs)


'''@app.route("/about")
def about():
    return render_template('about.html', title='About')'''


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, roll=form.roll.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.roll == form.roll.data:
                login_user(user)
                #next_page = request.args.get('next')
                #redirect(next_page) if next_page else redirect(url_for('home'))
                return redirect(url_for('homepage'))
                '''if user.roll == 'admin':
                    return redirect(url_for('homepage_admin'))
                elif user.roll == 'manager':
                    return redirect(url_for('homepage_manager'))
                elif user.roll == 'developer':
                    return redirect(url_for('homepage_developer'))
                elif user.roll == 'tester':
                    return redirect(url_for('homepage_tester'))'''
            else:
                flash('Login Unsuccessful. Please check roll!', 'danger') 
        else:
            flash('Login Unsuccessful. Please check email and password!', 'danger')
        
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


#Projects
@app.route("/new_project", methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, start=form.start.data, email=form.email.data, mngr=form.mngr.data, status=form.status.data, pitch=form.pitch.data)
        db.session.add(project)
        db.session.commit()
        flash('Your project has been created!', 'success')
        return redirect(url_for('homepage'))
    
    return render_template('new_project.html', title='New Project', form=form, legend='New Project')


@app.route("/project/<int:project_id>")
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project.html', title=project.name, project=project)


@app.route("/project/<int:project_id>/update", methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if current_user.roll != "admin":
        abort(403)
    
    form = ViewProjectForm()
    if form.validate_on_submit():
        project.name = form.name.data
        project.status = form.status.data
        project.pitch = form.pitch.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('project', project_id=project.id))
    elif request.method == 'GET':
        form.name.data = project.name
        form.pitch.data = project.pitch
        form.status.data = project.status
    return render_template('update_project.html', title='Update Project', form=form, legend='Update Project')


@app.route("/project/<int:project_id>/delete", methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    if current_user.roll != "admin":
        abort(403)
    
    db.session.delete(project)
    db.session.commit()
    flash('Your project has been deleted!', 'success')
    return redirect(url_for('homepage'))

'''@app.route("/post/<int:post_id>")
def project():
    projects = Project.query.all()
    bugs = Bug.query.all()
    return render_template('homepage.html', projects=projects, bugs=bugs)'''


#Bugs
@app.route("/new_bug", methods=['GET', 'POST'])
@login_required
def new_bug():
    available_projects=db.session.query(Project).all()
    projects_list=[(i.id, i.name) for i in available_projects]
    
    form = BugForm()
    form.pr_name.choices = projects_list
    
    if form.validate_on_submit():
        bug = Bug(name=form.name.data, prid=form.pr_name.data, frmEmail=form.frmEmail.data, toEmail=form.toEmail.data, status=form.status.data, desc=form.desc.data, prio=form.prio.data)
        db.session.add(bug)
        db.session.commit()
        flash('A bug has been created!', 'success')
        return redirect(url_for('homepage'))
    return render_template('new_bug.html', title='New Bug', form=form, legend='New Bug')


@app.route("/bug/<int:bug_id>")
def bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    return render_template('bug.html', title=bug.name, bug=bug)


@app.route("/bug/<int:bug_id>/update", methods=['GET', 'POST'])
@login_required
def update_bug(bug_id):
    if current_user.roll != "admin":
        abort(403)

    available_projects=db.session.query(Project).all()
    projects_list=[(i.id, i.name) for i in available_projects]
    
    form = ViewBugForm()
    form.pr_name.choices = projects_list

    bug = Bug.query.get_or_404(bug_id)
    if form.is_submitted(): #if form.validate_on_submit(): 
        bug.name = form.name.data            
        bug.prid = form.pr_name.data
        bug.status = form.status.data
        bug.prio = form.prio.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('bug', bug_id=bug.id))
    elif request.method == 'GET':
        form.name.data = bug.name
        form.status.data = bug.status
        form.prio.data = bug.prio
        
    return render_template('update_bug.html', title='Update Bug', form=form, legend='Update Bug')


@app.route("/bug/<int:bug_id>/delete", methods=['POST'])
@login_required
def delete_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)

    if current_user.roll != "admin":
        abort(403)
    
    db.session.delete(bug)
    db.session.commit()
    flash('Your bug has been deleted!', 'success')
    return redirect(url_for('homepage'))


#Users
@app.route("/view_users", methods=['GET', 'POST'])
@login_required
def view_users():
    users = User.query.all()
    return render_template('view_users.html', title='Users', users=users, legend='Users')


@app.route("/add_user", methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUserForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data , email=form.email.data, password=hashed_password, roll=form.roll.data)
        db.session.add(user)
        db.session.commit()
        flash('New User added to workforce!', 'success')
        return redirect(url_for('view_users'))

    return render_template('add_user.html', title='Add User', form=form, legend='Add User')


@app.route("/delete_user", methods=['GET', 'POST'])
@login_required
def delete_user():
    users = User.query.all()
    '''form = AddUserForm()
    users = User.query.all()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data , email=form.email.data, password=hashed_password, roll=form.roll.data)
        db.session.add(user)
        db.session.commit()
        flash('User deleted from workforce!', 'success')
        return redirect(url_for('view_users'))'''

    return render_template('delete_user.html', title='Delete User', users=users, legend='Delete User')