import uuid, re
from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Scholarship, InstitutionProfile, StudentProfile, Application, SavedScholarship
bp=Blueprint('scholarships',__name__,url_prefix='/scholarships')
def uid(): return str(uuid.uuid4())
def slugify(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')+'-'+uuid.uuid4().hex[:6]
@bp.get('/')
def index():
    q=request.args.get('q','').strip(); query=Scholarship.query.filter_by(approval_status='approved',publication_status='published')
    if q: query=query.filter(Scholarship.title.ilike(f'%{q}%'))
    return render_template('scholarships/index.html',scholarships=query.order_by(Scholarship.created_at.desc()).all(),q=q)
@bp.get('/<slug>')
def detail(slug):
    s=Scholarship.query.filter_by(slug=slug,approval_status='approved',publication_status='published').first_or_404(); return render_template('scholarships/detail.html',scholarship=s)
@bp.route('/create',methods=['GET','POST'])
@login_required
def create():
    if current_user.role!='institution': abort(403)
    inst=InstitutionProfile.query.filter_by(user_id=current_user.id).first_or_404()
    if request.method=='POST':
        title=request.form.get('title','').strip(); desc=request.form.get('description','').strip()
        if not title or not desc: flash('Title and description are required.','danger')
        else:
            s=Scholarship(id=uid(),institution_id=inst.id,title=title,slug=slugify(title),description=desc,category=request.form.get('category'),funding_type=request.form.get('funding_type'),eligibility=request.form.get('eligibility'),approval_status='pending',publication_status='draft')
            db.session.add(s); db.session.commit(); flash('Scholarship submitted for administrator review.','success'); return redirect(url_for('institution.dashboard'))
    return render_template('scholarships/create.html')
@bp.post('/<scholarship_id>/apply')
@login_required
def apply(scholarship_id):
    if current_user.role!='student': abort(403)
    s=db.session.get(Scholarship,scholarship_id); p=StudentProfile.query.filter_by(user_id=current_user.id).first_or_404()
    if not s or s.approval_status!='approved' or s.publication_status!='published': abort(404)
    if s.application_deadline and s.application_deadline<date.today(): flash('This scholarship deadline has passed.','warning')
    elif Application.query.filter_by(scholarship_id=s.id,student_id=p.id).first(): flash('You have already applied.','info')
    else:
        db.session.add(Application(id=uid(),scholarship_id=s.id,student_id=p.id,application_reference='EN-'+uuid.uuid4().hex[:10].upper(),cover_letter=request.form.get('cover_letter',''),application_status='submitted')); db.session.commit(); flash('Application submitted.','success')
    return redirect(url_for('scholarships.detail',slug=s.slug))
@bp.post('/<scholarship_id>/save')
@login_required
def save(scholarship_id):
    if current_user.role!='student': abort(403)
    p=StudentProfile.query.filter_by(user_id=current_user.id).first_or_404(); s=db.session.get(Scholarship,scholarship_id)
    if not s: abort(404)
    existing=SavedScholarship.query.filter_by(student_id=p.id,scholarship_id=s.id).first()
    if existing: db.session.delete(existing)
    else: db.session.add(SavedScholarship(id=uid(),student_id=p.id,scholarship_id=s.id))
    db.session.commit(); return redirect(request.referrer or url_for('scholarships.index'))
