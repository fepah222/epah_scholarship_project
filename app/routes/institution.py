import uuid

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models import InstitutionProfile, Post, InstitutionFollow, Scholarship, Application
from ..uploads import save_public_image, remove_public_image

bp = Blueprint("institution", __name__, url_prefix="/institutions")


def own_profile():
    return InstitutionProfile.query.filter_by(user_id=current_user.id).first()


@bp.get("/dashboard")
@login_required
def dashboard():
    if current_user.role != "institution":
        return redirect(url_for("home"))
    profile = own_profile()
    if not profile:
        abort(404)
    scholarships = (
        Scholarship.query.filter_by(institution_id=profile.id)
        .order_by(Scholarship.created_at.desc()).all()
    )
    application_count = (
        Application.query.join(Scholarship)
        .filter(Scholarship.institution_id == profile.id).count()
    )
    return render_template(
        "institution/dashboard.html", profile=profile,
        scholarships=scholarships, application_count=application_count
    )


@bp.get("/applications")
@login_required
def applications():
    if current_user.role != "institution":
        abort(403)
    profile = own_profile()
    if not profile:
        abort(404)
    records = (
        Application.query.join(Scholarship)
        .filter(Scholarship.institution_id == profile.id)
        .order_by(Application.submitted_at.desc()).all()
    )
    return render_template("institution/applications.html", applications=records)


@bp.post("/applications/<application_id>/review")
@login_required
def review_application(application_id):
    if current_user.role != "institution":
        abort(403)
    profile = own_profile()
    if not profile:
        abort(404)
    application = db.session.get(Application, application_id)
    if not application or application.scholarship.institution_id != profile.id:
        abort(404)

    new_status = request.form.get("status", "").strip()
    allowed = {"under_review", "accepted", "rejected"}
    if new_status not in allowed:
        abort(400)
    if application.application_status in {"accepted", "rejected"}:
        flash("A final decision has already been recorded for this application.", "warning")
    else:
        application.application_status = new_status
        application.reviewer_comment = request.form.get("reviewer_comment", "").strip() or None
        from datetime import datetime, timezone
        application.reviewed_at = datetime.now(timezone.utc)
        db.session.commit()
        flash("Application review saved.", "success")
    return redirect(url_for("institution.applications"))


@bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    profile = own_profile()
    if current_user.role != "institution" or not profile:
        return redirect(url_for("home"))
    if request.method == "POST":
        for field in (
            "institution_name", "institution_type", "country", "region", "city",
            "physical_address", "phone_number", "website", "description", "history",
            "mission", "vision", "academic_programmes"
        ):
            setattr(profile, field, request.form.get(field, "").strip())
        for field, attribute, folder in (
            ("logo_image", "logo_path", "institution-logos"),
            ("cover_image", "cover_photo_path", "institution-covers"),
        ):
            upload = request.files.get(field)
            if upload and upload.filename:
                try:
                    new_path = save_public_image(upload, folder)
                except ValueError as error:
                    flash(str(error), "danger")
                    return render_template("institution/edit.html", profile=profile), 400
                remove_public_image(getattr(profile, attribute))
                setattr(profile, attribute, new_path)
        db.session.commit()
        flash("Institution profile updated.", "success")
        return redirect(url_for("institution.dashboard"))
    return render_template("institution/edit.html", profile=profile)


@bp.get("/<string:profile_id>")
def public_profile(profile_id):
    profile = db.session.get(InstitutionProfile, profile_id)
    if not profile:
        return render_template("errors/404.html"), 404
    posts = (
        Post.query.filter_by(institution_id=profile.id, publication_status="published")
        .order_by(Post.is_pinned.desc(), Post.published_at.desc()).all()
    )
    followers = InstitutionFollow.query.filter_by(institution_id=profile.id).count()
    return render_template(
        "institution/public_profile.html", profile=profile,
        posts=posts, followers=followers
    )
