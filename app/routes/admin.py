from flask import Blueprint, render_template, abort, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import InstitutionProfile, Scholarship, AdminAction
import uuid
bp=Blueprint('admin',__name__,url_prefix='/admin')
def require_admin():
    if current_user.role!='admin': abort(403)
@bp.get('/')
@login_required
def dashboard():
    require_admin(); return render_template('admin/dashboard.html',pending_institutions=InstitutionProfile.query.filter_by(verification_status='pending').count(),pending_scholarships=Scholarship.query.filter_by(approval_status='pending').count())
@bp.get('/institutions')
@login_required
def institutions():
    require_admin(); return render_template('admin/institutions.html',institutions=InstitutionProfile.query.order_by(InstitutionProfile.created_at.desc()).all())
@bp.post('/institutions/<institution_id>/review')
@login_required
def review_institution(institution_id):
    require_admin(); p=db.session.get(InstitutionProfile,institution_id)
    if not p: abort(404)
    status=request.form.get('status')
    if status not in ('approved','rejected','pending'): abort(400)
    p.verification_status=status; p.verification_reason=request.form.get('reason',''); p.verified_at=db.func.current_timestamp() if status=='approved' else None
    db.session.add(AdminAction(id=str(uuid.uuid4()),admin_id=current_user.id,action_type='institution_'+status,target_entity_type='institution',target_entity_id=p.id,reason=p.verification_reason)); db.session.commit(); flash('Institution review saved.','success'); return redirect(url_for('admin.institutions'))
@bp.get('/scholarships')
@login_required
def scholarships():
    require_admin(); return render_template('admin/scholarships.html',scholarships=Scholarship.query.order_by(Scholarship.created_at.desc()).all())
@bp.post('/scholarships/<scholarship_id>/review')
@login_required
def review_scholarship(scholarship_id):
    require_admin(); s=db.session.get(Scholarship,scholarship_id)
    if not s: abort(404)
    status=request.form.get('status')
    if status not in ('approved','rejected'): abort(400)
    inst=s.institution
    if status=='approved' and inst.verification_status!='approved': flash('Verify the institution before approving its scholarship.','warning'); return redirect(url_for('admin.scholarships'))
    s.approval_status=status; s.publication_status='published' if status=='approved' else 'draft'; s.rejection_reason=request.form.get('reason',''); s.approved_by=current_user.id if status=='approved' else None; db.session.commit(); flash('Scholarship review saved.','success'); return redirect(url_for('admin.scholarships'))
