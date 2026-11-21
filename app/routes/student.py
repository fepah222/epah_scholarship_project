from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from ..extensions import db
from ..models import StudentProfile, Scholarship, Application, SavedScholarship
from ..uploads import save_public_image, remove_public_image

bp = Blueprint("student", __name__, url_prefix="/student")


def profile():
    return StudentProfile.query.filter_by(user_id=current_user.id).first()


@bp.get("/dashboard")
@login_required
def dashboard():
    if current_user.role != "student":
        return redirect(url_for("home"))
    student = profile()
    saved = SavedScholarship.query.filter_by(student_id=student.id).count() if student else 0
    applications = Application.query.filter_by(student_id=student.id).count() if student else 0
    scholarships = (
        Scholarship.query.filter_by(approval_status="approved", publication_status="published")
        .order_by(Scholarship.created_at.desc()).all()
    )
    return render_template(
        "student/dashboard.html", profile=student, scholarships=scholarships,
        saved=saved, applications=applications
    )


@bp.get("/applications")
@login_required
def applications():
    if current_user.role != "student":
        return redirect(url_for("home"))
    student = profile()
    records = (
        Application.query.filter_by(student_id=student.id)
        .order_by(Application.submitted_at.desc()).all()
        if student else []
    )
    return render_template("student/applications.html", applications=records)


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    student = profile()
    if current_user.role != "student" or not student:
        flash("Student profile not found.", "danger")
        return redirect(url_for("home"))
    if request.method == "POST":
        for field in (
            "country", "region", "city", "biography", "current_institution",
            "education_level", "field_of_study"
        ):
            setattr(student, field, request.form.get(field, "").strip())
        photo = request.files.get("profile_photo")
        if photo and photo.filename:
            try:
                new_path = save_public_image(photo, "students")
            except ValueError as error:
                flash(str(error), "danger")
                return render_template("student/profile.html", profile=student), 400
            remove_public_image(current_user.profile_photo)
            current_user.profile_photo = new_path
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("student.dashboard"))
    return render_template("student/profile.html", profile=student)
