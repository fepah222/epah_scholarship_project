import uuid
from datetime import date, timedelta

from app.extensions import db
from app.models import User, StudentProfile, InstitutionProfile, Scholarship, Application


def make_user(role, name, email):
    user = User(
        id=str(uuid.uuid4()), full_name=name, email=email,
        password_hash="test-hash", role=role, account_status="active",
        email_verified=True,
    )
    db.session.add(user)
    db.session.flush()
    return user


def login_as(client, user):
    with client.session_transaction() as session:
        session["_user_id"] = user.id
        session["_fresh"] = True


def scholarship_setup():
    institution_user = make_user("institution", "Test Institution", "institution@example.test")
    institution = InstitutionProfile(
        id=str(uuid.uuid4()), user_id=institution_user.id,
        institution_name="Test Institution", official_email=institution_user.email,
        verification_status="approved",
    )
    student_user = make_user("student", "Test Student", "student@example.test")
    student = StudentProfile(id=str(uuid.uuid4()), user_id=student_user.id)
    scholarship = Scholarship(
        id=str(uuid.uuid4()), institution_id=institution.id,
        title="Test Scholarship", slug="test-scholarship",
        description="A scholarship used for workflow tests.",
        approval_status="approved", publication_status="published",
        application_deadline=date.today() + timedelta(days=30),
        application_method="platform",
    )
    db.session.add_all([institution, student, scholarship])
    db.session.commit()
    return institution_user, institution, student_user, student, scholarship


def test_student_can_apply_once(client, app):
    with app.app_context():
        _, _, student_user, student, scholarship = scholarship_setup()
        login_as(client, student_user)

        first = client.post(f"/scholarships/{scholarship.id}/apply", data={"cover_letter": "I am interested."})
        second = client.post(f"/scholarships/{scholarship.id}/apply", data={"cover_letter": "Duplicate."})

        assert first.status_code == 302
        assert second.status_code == 302
        assert Application.query.filter_by(
            scholarship_id=scholarship.id, student_id=student.id
        ).count() == 1


def test_institution_only_sees_its_own_applications(client, app):
    with app.app_context():
        institution_user, _, student_user, student, scholarship = scholarship_setup()
        application = Application(
            id=str(uuid.uuid4()), scholarship_id=scholarship.id,
            student_id=student.id, application_reference="EN-TEST123456",
            application_status="submitted",
        )
        db.session.add(application)
        db.session.commit()
        login_as(client, institution_user)

        response = client.get("/institutions/applications")

        assert response.status_code == 200
        assert b"Test Student" in response.data
        assert b"EN-TEST123456" in response.data


def test_student_cannot_access_institution_application_review(client, app):
    with app.app_context():
        _, _, student_user, _, _ = scholarship_setup()
        login_as(client, student_user)

        response = client.get("/institutions/applications")

        assert response.status_code == 403
