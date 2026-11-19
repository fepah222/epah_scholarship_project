import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models import InstitutionProfile, Post, InstitutionFollow, StudentProfile
bp=Blueprint('institution',__name__,url_prefix='/institutions')
def own_profile(): return InstitutionProfile.query.filter_by(user_id=current_user.id).first()
@bp.get('/dashboard')
@login_required
def dashboard():
    if current_user.role!='institution': return redirect(url_for('home'))
    p=own_profile(); return render_template('institution/dashboard.html',profile=p)
@bp.route('/edit',methods=['GET','POST'])
@login_required
def edit():
    p=own_profile()
    if not p: return redirect(url_for('home'))
    if request.method=='POST':
        for field in ('institution_name','institution_type','country','region','city','physical_address','phone_number','website','description','history','mission','vision','academic_programmes'): setattr(p,field,request.form.get(field,'').strip())
        db.session.commit(); flash('Institution profile updated.','success'); return redirect(url_for('institution.dashboard'))
    return render_template('institution/edit.html',profile=p)
@bp.get('/<string:profile_id>')
def public_profile(profile_id):
    p=db.session.get(InstitutionProfile,profile_id)
    if not p: return render_template('errors/404.html'),404
    posts=Post.query.filter_by(institution_id=p.id,publication_status='published').order_by(Post.is_pinned.desc(),Post.published_at.desc()).all()
    followers=InstitutionFollow.query.filter_by(institution_id=p.id).count()
    return render_template('institution/public_profile.html',profile=p,posts=posts,followers=followers)
