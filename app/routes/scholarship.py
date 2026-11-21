import re
import uuid
from datetime import date
from urllib.parse import urlparse

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..models import (
    Application,
    InstitutionProfile,
    SavedScholarship,
    Scholarship,
    StudentProfile,
)

bp = Blueprint("scholarships", __name__, url_prefix="/scholarships")


def uid():
    return str(uuid.uuid4())


def slugify(value):
    base = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return f"{base or 'scholarship'}-{uuid.uuid4().hex[:6]}"


def parse_optional_date(value, label):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{label} must be a valid date.")


@bp.get("/")
def index():
    search = request.args.get("q", "").strip()
    query = Scholarship.query.filter_by(
        approval_status="approved", publication_status="published"
    )
    if search:
        query = query.filter(Scholarship.title.ilike(f"%{search}%"))
    scholarships = query.order_by(Scholarship.created_at.desc()).all()
    return render_template("scholarships/index.html", scholarships=scholarships, q=search)


@bp.get("/<slug>")
def detail(slug):
    scholarship = Scholarship.query.filter_by(
        slug=slug, approval_status="approved", publication_status="published"
    ).first_or_404()
    already_applied = False
    if current_user.is_authenticated and current_user.role == "student":
        profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
        if profile:
            already_applied = Application.query.filter_by(
                scholarship_id=scholarship.id, student_id=profile.id
            ).first() is not None
    return render_template(
        "scholarships/detail.html",
        scholarship=scholarship,
        already_applied=already_applied,
        today=date.today(),
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if current_user.role != "institution":
        abort(403)
    institution = InstitutionProfile.query.filter_by(user_id=current_user.id).first_or_404()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        external_url = request.form.get("external_application_url", "").strip()
        try:
            opening_date = parse_optional_date(request.form.get("application_open_date"), "Opening date")
            deadline = parse_optional_date(request.form.get("application_deadline"), "Deadline")
            positions_raw = request.form.get("available_positions", "").strip()
            positions = int(positions_raw) if positions_raw else None
            if not title or not description:
                raise ValueError("Title and description are required.")
            if opening_date and deadline and opening_date > deadline:
                raise ValueError("The application opening date cannot be after the deadline.")
            if positions is not None and positions < 1:
                raise ValueError("Available positions must be at least 1.")
            if external_url:
                parsed = urlparse(external_url)
                if parsed.scheme not in ("http", "https") or not parsed.netloc:
                    raise ValueError("The external application link must be a valid http or https URL.")
        except ValueError as error:
            flash(str(error), "danger")
            return render_template("scholarships/create.html"), 400

        scholarship = Scholarship(
            id=uid(),
            institution_id=institution.id,
            title=title,
            slug=slugify(title),
            description=description,
            category=request.form.get("category", "").strip() or None,
            funding_type=request.form.get("funding_type", "").strip() or None,
            benefits=request.form.get("benefits", "").strip() or None,
            eligibility=request.form.get("eligibility", "").strip() or None,
            academic_requirements=request.form.get("academic_requirements", "").strip() or None,
            country_eligibility=request.form.get("country_eligibility", "").strip() or None,
            application_open_date=opening_date,
            application_deadline=deadline,
            available_positions=positions,
            application_method="external" if external_url else "platform",
            external_application_url=external_url or None,
            approval_status="pending",
            publication_status="draft",
        )
        db.session.add(scholarship)
        db.session.commit()
        flash("Scholarship submitted for administrator review.", "success")
        return redirect(url_for("institution.dashboard"))

    return render_template("scholarships/create.html")


@bp.post("/<scholarship_id>/apply")
@login_required
def apply(scholarship_id):
    if current_user.role != "student":
        abort(403)
    scholarship = db.session.get(Scholarship, scholarship_id)
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first_or_404()
    if (
        not scholarship
        or scholarship.approval_status != "approved"
        or scholarship.publication_status != "published"
    ):
        abort(404)

    today = date.today()
    if scholarship.application_open_date and scholarship.application_open_date > today:
        flash("Applications for this scholarship have not opened yet.", "warning")
    elif scholarship.application_deadline and scholarship.application_deadline < today:
        flash("This scholarship deadline has passed.", "warning")
    elif scholarship.application_method == "external":
        flash("This scholarship uses an external application process. Use the institution's application link.", "info")
    elif Application.query.filter_by(
        scholarship_id=scholarship.id, student_id=profile.id
    ).first():
        flash("You have already applied for this scholarship.", "info")
    else:
        application = Application(
            id=uid(),
            scholarship_id=scholarship.id,
            student_id=profile.id,
            application_reference="EN-" + uuid.uuid4().hex[:10].upper(),
            cover_letter=request.form.get("cover_letter", "").strip(),
            application_status="submitted",
        )
        db.session.add(application)
        try:
            db.session.commit()
            flash("Your application has been submitted successfully.", "success")
        except Exception:
            db.session.rollback()
            flash("Your application could not be saved. Please try again.", "danger")

    return redirect(url_for("scholarships.detail", slug=scholarship.slug))


@bp.post("/<scholarship_id>/save")
@login_required
def save(scholarship_id):
    if current_user.role != "student":
        abort(403)
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first_or_404()
    scholarship = db.session.get(Scholarship, scholarship_id)
    if (
        not scholarship
        or scholarship.approval_status != "approved"
        or scholarship.publication_status != "published"
    ):
        abort(404)

    existing = SavedScholarship.query.filter_by(
        student_id=profile.id, scholarship_id=scholarship.id
    ).first()
    if existing:
        db.session.delete(existing)
    else:
        db.session.add(
            SavedScholarship(
                id=uid(), student_id=profile.id, scholarship_id=scholarship.id
            )
        )
    db.session.commit()
    return redirect(url_for("scholarships.index"))
