import uuid
from datetime import datetime, timezone

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from ..extensions import db
from ..models import User, StudentProfile, InstitutionProfile, UserSettings

bp = Blueprint("auth", __name__, url_prefix="/auth")


def uid():
    return str(uuid.uuid4())


def authenticate(email, password):
    user = User.query.filter_by(email=email.strip().lower()).first()
    if user and user.check_password(password) and user.account_status == "active":
        user.last_login_at = datetime.now(timezone.utc)
        db.session.commit()
        return user
    return None


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        role = request.form.get("role", "student")
        name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if role not in ("student", "institution") or not name or not email or len(password) < 8:
            flash("Complete all required fields. Password must contain at least 8 characters.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "danger")
        else:
            user = User(
                id=uid(), full_name=name, email=email, role=role,
                account_status="active", email_verified=False
            )
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
            if role == "student":
                db.session.add(StudentProfile(id=uid(), user_id=user.id))
            else:
                db.session.add(InstitutionProfile(
                    id=uid(), user_id=user.id, institution_name=name, official_email=email
                ))
            db.session.add(UserSettings(id=uid(), user_id=user.id))
            db.session.commit()
            login_user(user)
            flash("Account created. You can now browse and apply for published scholarships.", "success")
            return redirect(url_for("student.dashboard" if role == "student" else "institution.dashboard"))
    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = authenticate(request.form.get("email", ""), request.form.get("password", ""))
        if user:
            login_user(user, remember=bool(request.form.get("remember")))
            endpoint = {
                "admin": "admin.dashboard",
                "institution": "institution.dashboard",
                "student": "student.dashboard",
            }.get(user.role, "home")
            return redirect(url_for(endpoint))
        flash("Invalid credentials or inactive account.", "danger")
    return render_template("auth/login.html", admin_login=False)


@bp.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated and current_user.role == "admin":
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        user = authenticate(request.form.get("email", ""), request.form.get("password", ""))
        if user and user.role == "admin":
            login_user(user, remember=bool(request.form.get("remember")))
            return redirect(url_for("admin.dashboard"))
        if user:
            logout_user()
        flash("Invalid administrator credentials or inactive administrator account.", "danger")
    return render_template("auth/login.html", admin_login=True)


@bp.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
