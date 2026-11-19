import uuid
from flask import Blueprint, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Post, PostReaction, PostComment, InstitutionProfile, StudentProfile, InstitutionFollow
bp=Blueprint('social',__name__,url_prefix='/social')
def uid(): return str(uuid.uuid4())
@bp.post('/posts')
@login_required
def create_post():
    if current_user.role!='institution': abort(403)
    p=InstitutionProfile.query.filter_by(user_id=current_user.id).first()
    if not p: abort(403)
    content=request.form.get('content','').strip()
    if not content: flash('Write something before publishing.','warning'); return redirect(url_for('institution.dashboard'))
    post=Post(id=uid(),institution_id=p.id,content=content,post_type='text',publication_status='published'); db.session.add(post); db.session.commit(); flash('Post published.','success'); return redirect(url_for('institution.public_profile',profile_id=p.id))
@bp.post('/posts/<post_id>/react')
@login_required
def react(post_id):
    post=db.session.get(Post,post_id)
    if not post: abort(404)
    kind=request.form.get('reaction_type','like')
    if kind not in ('like','love','haha','wow','sad','angry'): abort(400)
    reaction=PostReaction.query.filter_by(post_id=post.id,user_id=current_user.id).first()
    if reaction and reaction.reaction_type==kind: db.session.delete(reaction)
    elif reaction: reaction.reaction_type=kind
    else: db.session.add(PostReaction(id=uid(),post_id=post.id,user_id=current_user.id,reaction_type=kind))
    db.session.commit(); return redirect(request.referrer or url_for('home'))
@bp.post('/posts/<post_id>/comments')
@login_required
def comment(post_id):
    post=db.session.get(Post,post_id)
    if not post: abort(404)
    text=request.form.get('comment_text','').strip()
    if not text or len(text)>3000: flash('Comment must contain between 1 and 3000 characters.','warning')
    else: db.session.add(PostComment(id=uid(),post_id=post.id,user_id=current_user.id,comment_text=text)); db.session.commit()
    return redirect(request.referrer or url_for('home'))
@bp.post('/institutions/<institution_id>/follow')
@login_required
def follow(institution_id):
    if current_user.role!='student': abort(403)
    p=StudentProfile.query.filter_by(user_id=current_user.id).first(); inst=db.session.get(InstitutionProfile,institution_id)
    if not p or not inst: abort(404)
    rel=InstitutionFollow.query.filter_by(student_id=p.id,institution_id=inst.id).first()
    if rel: db.session.delete(rel); flash('You unfollowed this institution.','info')
    else: db.session.add(InstitutionFollow(id=uid(),student_id=p.id,institution_id=inst.id)); flash('You are now following this institution.','success')
    db.session.commit(); return redirect(request.referrer or url_for('institution.public_profile',profile_id=inst.id))
