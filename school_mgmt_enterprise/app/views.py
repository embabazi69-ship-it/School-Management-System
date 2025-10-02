
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, Student, Teacher, Course
from .forms import LoginForm, RegisterForm, StudentForm, TeacherForm, CourseForm
from .payments import create_payment_intent

main_bp = Blueprint('main', __name__)

def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*a, **k):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Admin access required", "danger")
            return redirect(url_for('main.login'))
        return fn(*a, **k)
    return wrapper

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered", "warning")
            return redirect(url_for('main.register'))
        u = User(email=form.email.data, name=form.name.data, role=form.role.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash("Account created. Please login.", "success")
        return redirect(url_for('main.login'))
    return render_template("register.html", form=form)

@main_bp.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u and u.check_password(form.password.data):
            login_user(u)
            flash("Logged in", "success")
            return redirect(url_for('main.dashboard'))
        flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)

@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for('main.index'))

@main_bp.route("/dashboard")
@login_required
def dashboard():
    students_count = Student.query.count()
    teachers_count = Teacher.query.count()
    courses_count = Course.query.count()
    return render_template("dashboard.html", students_count=students_count, teachers_count=teachers_count, courses_count=courses_count)

# Payments example
@main_bp.route("/pay", methods=['POST'])
@login_required
def pay():
    # simple example: expect JSON with amount in cents
    data = request.get_json() or {}
    amount = int(data.get('amount', 0))
    try:
        intent = create_payment_intent(amount)
        return jsonify({'client_secret': intent.client_secret})
    except Exception as e:
        current_app.logger.exception("Payment error")
        return jsonify({'error': str(e)}), 500

# Admin demo: seed demo data
@main_bp.route("/admin/seed", methods=['POST'])
@admin_required
def seed_demo():
    # create demo students/teachers/courses
    for i in range(1,6):
        if not Student.query.filter_by(reg_no=f"REG{i:03}").first():
            s = Student(name=f"Demo Student {i}", reg_no=f"REG{i:03}", klass="JSS1")
            db.session.add(s)
    for i in range(1,4):
        if not Teacher.query.filter_by(name=f"Demo Teacher {i}").first():
            t = Teacher(name=f"Demo Teacher {i}", subject="Math")
            db.session.add(t)
    db.session.commit()
    flash("Demo data seeded", "success")
    return redirect(url_for('main.dashboard'))

# Students/Teachers/Courses routes unchanged...
