from datetime import datetime, timezone
from ..extensions import db
now=lambda: datetime.now(timezone.utc)
class Scholarship(db.Model):
    __tablename__ = "scholarships"
    id=db.Column(db.String(36), primary_key=True); institution_id=db.Column(db.String(36), db.ForeignKey('institution_profiles.id'), nullable=False); title=db.Column(db.String(220), nullable=False); slug=db.Column(db.String(240), unique=True, nullable=False); description=db.Column(db.Text, nullable=False); category=db.Column(db.String(100)); funding_type=db.Column(db.String(50)); benefits=db.Column(db.Text); eligibility=db.Column(db.Text); academic_requirements=db.Column(db.Text); country_eligibility=db.Column(db.Text); application_open_date=db.Column(db.Date); application_deadline=db.Column(db.Date); available_positions=db.Column(db.Integer); application_method=db.Column(db.String(30), default='platform'); external_application_url=db.Column(db.String(500)); approval_status=db.Column(db.String(20), default='pending'); publication_status=db.Column(db.String(20), default='draft'); rejection_reason=db.Column(db.Text); approved_by=db.Column(db.String(36), db.ForeignKey('users.id')); approved_at=db.Column(db.DateTime(timezone=True)); created_at=db.Column(db.DateTime(timezone=True), default=now); updated_at=db.Column(db.DateTime(timezone=True), default=now, onupdate=now); institution=db.relationship('InstitutionProfile', backref='scholarships')
class ScholarshipDocument(db.Model):
    __tablename__ = "scholarship_documents"
    id=db.Column(db.String(36), primary_key=True); scholarship_id=db.Column(db.String(36), db.ForeignKey('scholarships.id'), nullable=False); document_name=db.Column(db.String(180)); file_path=db.Column(db.String(500), nullable=False); document_type=db.Column(db.String(80)); created_at=db.Column(db.DateTime(timezone=True), default=now)
class Application(db.Model):
    __tablename__ = "applications"
    __table_args__ = (db.UniqueConstraint('scholarship_id', 'student_id', name='uq_application_student_scholarship'),)
    id=db.Column(db.String(36), primary_key=True); scholarship_id=db.Column(db.String(36), db.ForeignKey('scholarships.id'), nullable=False); student_id=db.Column(db.String(36), db.ForeignKey('student_profiles.id'), nullable=False); application_reference=db.Column(db.String(40), unique=True, nullable=False); cover_letter=db.Column(db.Text); application_status=db.Column(db.String(30), default='submitted'); submitted_at=db.Column(db.DateTime(timezone=True), default=now); reviewed_at=db.Column(db.DateTime(timezone=True)); reviewer_comment=db.Column(db.Text); created_at=db.Column(db.DateTime(timezone=True), default=now); updated_at=db.Column(db.DateTime(timezone=True), default=now, onupdate=now); scholarship=db.relationship('Scholarship', backref='applications'); student=db.relationship('StudentProfile')
class ApplicationDocument(db.Model):
    __tablename__ = "application_documents"
    id=db.Column(db.String(36), primary_key=True); application_id=db.Column(db.String(36), db.ForeignKey('applications.id'), nullable=False); document_type=db.Column(db.String(100)); original_filename=db.Column(db.String(255)); stored_filename=db.Column(db.String(255)); file_path=db.Column(db.String(500), nullable=False); uploaded_at=db.Column(db.DateTime(timezone=True), default=now)
class SavedScholarship(db.Model):
    __tablename__ = "saved_scholarships"
    __table_args__=(db.UniqueConstraint('student_id','scholarship_id',name='uq_saved_scholarship'),)
    id=db.Column(db.String(36), primary_key=True); student_id=db.Column(db.String(36), db.ForeignKey('student_profiles.id'), nullable=False); scholarship_id=db.Column(db.String(36), db.ForeignKey('scholarships.id'), nullable=False); created_at=db.Column(db.DateTime(timezone=True), default=now)
