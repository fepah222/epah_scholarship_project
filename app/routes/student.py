import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models import StudentProfile, Scholarship, Application, SavedScholarship
bp=Blueprint('student',__name__,url_prefix='/student')
def profile(): return StudentProfile.query.filter_by(user_id=current_user.id).first()
@bp.get('/dashboard')
@login_required
def dashboard():
    if current_user.role!='student': return redirect(url_for('home'))
    p=profile(); saved=SavedScholarship.query.filter_by(student_id=p.id).count() if p else 0; applications=Application.query.filter_by(student_id=p.id).count() if p else 0
    scholarships=Scholarship.query.filter_by(approval_status='approved',publication_status='published').order_by(Scholarship.created_at.desc()).limit(8).all()
    return render_template('student/dashboard.html',profile=p,scholarships=scholarships,saved=saved,applications=applications)
@bp.route('/profile',methods=['GET','POST'])
@login_required
def edit_profile():
    p=profile()
    if not p: flash('Student profile not found.','danger'); return redirect(url_for('home'))
    if request.method=='POST':
        for field in ('country','region','city','biography','current_institution','education_level','field_of_study'): setattr(p,field,request.form.get(field,'').strip())
        db.session.commit(); flash('Profile updated.','success'); return redirect(url_for('student.dashboard'))
    return render_template('student/profile.html',profile=p)
