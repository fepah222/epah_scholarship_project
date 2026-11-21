from datetime import datetime, timezone
from ..extensions import db

now = lambda: datetime.now(timezone.utc)


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date)
    country = db.Column(db.String(100))
    region = db.Column(db.String(100))
    city = db.Column(db.String(100))
    biography = db.Column(db.Text)
    current_institution = db.Column(db.String(180))
    education_level = db.Column(db.String(100))
    field_of_study = db.Column(db.String(150))
    graduation_year = db.Column(db.Integer)
    profile_visibility = db.Column(db.String(20), default="public")
    created_at = db.Column(db.DateTime(timezone=True), default=now)
    updated_at = db.Column(db.DateTime(timezone=True), default=now, onupdate=now)

    user = db.relationship("User", backref=db.backref("student_profile", uselist=False))


class StudentQualification(db.Model):
    __tablename__ = "student_qualifications"

    id = db.Column(db.String(36), primary_key=True)
    student_id = db.Column(db.String(36), db.ForeignKey("student_profiles.id"), nullable=False)
    qualification_name = db.Column(db.String(180), nullable=False)
    awarding_institution = db.Column(db.String(180))
    subject_or_field = db.Column(db.String(180))
    grade_or_result = db.Column(db.String(80))
    year_obtained = db.Column(db.Integer)
    certificate_file = db.Column(db.String(500))
    visibility = db.Column(db.String(20), default="private")
    created_at = db.Column(db.DateTime(timezone=True), default=now)


class InstitutionProfile(db.Model):
    __tablename__ = "institution_profiles"

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), unique=True, nullable=False)
    institution_name = db.Column(db.String(200), nullable=False)
    institution_type = db.Column(db.String(100))
    registration_number = db.Column(db.String(120))
    established_year = db.Column(db.Integer)
    country = db.Column(db.String(100))
    region = db.Column(db.String(100))
    city = db.Column(db.String(100))
    physical_address = db.Column(db.Text)
    official_email = db.Column(db.String(255))
    phone_number = db.Column(db.String(50))
    website = db.Column(db.String(255))
    logo_path = db.Column(db.String(500))
    cover_photo_path = db.Column(db.String(500))
    history = db.Column(db.Text)
    description = db.Column(db.Text)
    mission = db.Column(db.Text)
    vision = db.Column(db.Text)
    academic_programmes = db.Column(db.Text)
    verification_status = db.Column(db.String(20), default="pending", nullable=False)
    verification_reason = db.Column(db.Text)
    verified_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), default=now)
    updated_at = db.Column(db.DateTime(timezone=True), default=now, onupdate=now)

    user = db.relationship("User", backref=db.backref("institution_profile", uselist=False))


class InstitutionDocument(db.Model):
    __tablename__ = "institution_documents"

    id = db.Column(db.String(36), primary_key=True)
    institution_id = db.Column(db.String(36), db.ForeignKey("institution_profiles.id"), nullable=False)
    document_type = db.Column(db.String(100))
    original_filename = db.Column(db.String(255))
    stored_filename = db.Column(db.String(255))
    storage_path = db.Column(db.String(500), nullable=False)
    review_status = db.Column(db.String(20), default="pending")
    admin_comment = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime(timezone=True), default=now)
    reviewed_at = db.Column(db.DateTime(timezone=True))
    reviewed_by = db.Column(db.String(36), db.ForeignKey("users.id"))
